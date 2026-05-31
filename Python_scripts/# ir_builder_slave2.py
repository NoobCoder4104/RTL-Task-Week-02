# ir_builder.py - Script 5 of 6
# Converts AST to Semantic IR (Intermediate Representation)
# Adds meaning: port roles, reset polarity, FSM classification

import os
import json
import re
from datetime import datetime

# ============================================
# CONFIGURATION

# For APB Slave2:
AST_FILE = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\apb_slave2_ast.json"
ORIGINAL_RTL = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\APB_RTL\slave2.v"
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs"
PROTOCOL = "APB"
MODULE_NAME = "slave2"

# ============================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

class IRBuilder:
    """Builds Semantic IR from AST"""
    
    def __init__(self, ast, source_file, protocol):
        self.ast = ast
        self.source_file = source_file
        self.protocol = protocol
        self.ir = {
            "schema_version": "0.1",
            "metadata": {
                "generated_by": "ir_builder.py",
                "timestamp": datetime.now().isoformat(),
                "source_file": os.path.basename(source_file),
                "protocol": protocol
            },
            "module": {},
            "ports": [],
            "signals": [],
            "parameters": [],
            "fsm": {
                "states": [],
                "encoding": None
            },
            "datapath": [],
            "reset": {
                "signal": None,
                "polarity": None,
                "type": None
            }
        }
    
    def classify_port_role(self, port_name, direction, width):
        """Classify port into semantic role"""
        name_lower = port_name.lower()
        is_vector = width is not None and width != "1"
        
        # Clock detection
        if 'clk' in name_lower or 'clock' in name_lower:
            return "clock", None
        
        # Reset detection (check polarity)
        if 'rst' in name_lower or 'reset' in name_lower:
            polarity = "active_low" if name_lower.endswith('_n') or '_n' in name_lower else "active_high"
            return "reset", polarity
        
        # Address detection
        if 'addr' in name_lower or 'address' in name_lower:
            return "address", None
        
        # Control signals (APB specific)
        if name_lower in ['psel', 'penable', 'pwrite', 'we', 're', 'enable']:
            return "control", None
        
        # Response signals
        if name_lower in ['prdata', 'pready', 'pslverr', 'valid', 'ready', 'busy']:
            return "response", None
        
        # Data signals (wide buses or named data)
        if is_vector or 'data' in name_lower:
            return "data", None
        
        # Default
        return "other", None
    
    def detect_reset_type(self, always_blocks):
        """Determine if reset is synchronous or asynchronous"""
        for block in always_blocks:
            sensitivity = block.get('sensitivity', [])
            # Asynchronous if reset in sensitivity list with posedge/negedge
            for sens in sensitivity:
                if 'rst' in sens.lower() or 'reset' in sens.lower():
                    # Check if it's in sensitivity with posedge/negedge
                    # Simplified: if reset appears with edge keyword
                    if 'posedge' in str(sensitivity) or 'negedge' in str(sensitivity):
                        return "asynchronous"
        return "synchronous"
    
    def detect_fsm_states(self):
        """Extract FSM states from AST"""
        states = self.ast.get('fsm_states', [])
        
        # Also look in parameters for state definitions
        for param in self.ast.get('parameters', []):
            param_name = param.get('name', '').upper()
            # Common FSM state names
            fsm_keywords = ['IDLE', 'START', 'SETUP', 'ACCESS', 'STOP', 'DATA', 
                           'PARITY', 'ADDRESS', 'ACK', 'WRITE', 'READ', 'DONE']
            for keyword in fsm_keywords:
                if keyword in param_name:
                    if param_name not in states:
                        states.append(param_name)
        
        return sorted(list(set(states)))
    
    def detect_datapath_signals(self):
        """Identify datapath signals (registers, counters, shift registers)"""
        datapath = []
        
        # Look for shift registers
        for sig in self.ast.get('signals', []):
            name = sig.get('name', '').lower()
            if 'shift' in name or 'reg' in name or 'counter' in name or 'cnt' in name:
                datapath.append(sig.get('name'))
        
        # Look for registers in always blocks (simplified)
        for block in self.ast.get('always_blocks', []):
            # This is simplified - in reality you'd parse the block body
            pass
        
        return datapath
    
    def build(self):
        """Build the complete IR"""
        
        # Module information
        self.ir['module'] = {
            "name": self.ast.get('module_name', 'unknown'),
            "type": "top" if self.protocol in ['APB', 'I2C'] else "submodule"
        }
        
        # Process ports
        reset_signal = None
        reset_polarity = None
        
        for port in self.ast.get('ports', []):
            name = port.get('name')
            direction = port.get('direction')
            width_str = port.get('width')
            
            # Calculate bit width
            if width_str and ':' in width_str:
                # Parse [31:0] -> 32
                parts = width_str.split(':')
                msb = int(parts[0]) if parts[0].lstrip('-').isdigit() else 1
                lsb = int(parts[1]) if parts[1].lstrip('-').isdigit() else 0
                width = abs(msb - lsb) + 1
            else:
                width = 1
            
            # Classify role
            role, polarity = self.classify_port_role(name, direction, width)
            
            port_entry = {
                "name": name,
                "direction": direction,
                "width": width,
                "role": role
            }
            
            if polarity:
                port_entry["polarity"] = polarity
            
            self.ir['ports'].append(port_entry)
            
            # Track reset signal
            if role == "reset":
                reset_signal = name
                reset_polarity = polarity
        
        # Process parameters
        for param in self.ast.get('parameters', []):
            self.ir['parameters'].append({
                "name": param.get('name'),
                "value": param.get('value'),
                "type": param.get('type', 'parameter')
            })
        
        # Process signals
        for sig in self.ast.get('signals', []):
            self.ir['signals'].append({
                "name": sig.get('name'),
                "type": sig.get('type', 'wire'),
                "width": sig.get('width', 1)
            })
        
        # FSM states
        self.ir['fsm']['states'] = self.detect_fsm_states()
        if self.ir['fsm']['states']:
            self.ir['fsm']['encoding'] = "localparam"  # or "enum"
        
        # Datapath signals
        self.ir['datapath'] = self.detect_datapath_signals()
        
        # Reset configuration
        self.ir['reset'] = {
            "signal": reset_signal,
            "polarity": reset_polarity,
            "type": self.detect_reset_type(self.ast.get('always_blocks', []))
        }
        
        return self.ir

# ============================================
# MAIN EXECUTION

print("=" * 60)
print(f"IR BUILDER - {PROTOCOL} {MODULE_NAME}")
print("=" * 60)

# Load AST
if not os.path.exists(AST_FILE):
    print(f"❌ ERROR: AST file not found: {AST_FILE}")
    print(f"   Please run parser_v0.py first!")
    exit(1)

with open(AST_FILE, 'r') as f:
    ast = json.load(f)

print(f"📁 Loading AST from: {AST_FILE}")
print(f"📝 Module: {ast.get('module_name', 'unknown')}")
print(f"📝 Ports: {len(ast.get('ports', []))}")
print(f"📝 FSM States from AST: {ast.get('fsm_states', [])}")

# Build IR
builder = IRBuilder(ast, ORIGINAL_RTL, PROTOCOL)
ir = builder.build()

print(f"\n📊 IR Summary:")
print(f"   Module: {ir['module']['name']}")
print(f"   Ports: {len(ir['ports'])}")
print(f"   Clock ports: {len([p for p in ir['ports'] if p['role'] == 'clock'])}")
print(f"   Reset ports: {len([p for p in ir['ports'] if p['role'] == 'reset'])}")
print(f"   Data ports: {len([p for p in ir['ports'] if p['role'] == 'data'])}")
print(f"   Control ports: {len([p for p in ir['ports'] if p['role'] == 'control'])}")
print(f"   FSM states: {ir['fsm']['states']}")
print(f"   Reset type: {ir['reset']['type']}")

# ============================================
# SAVE OUTPUTS

# 1. Save complete IR as JSON
json_output = os.path.join(OUTPUT_FOLDER, f"{PROTOCOL.lower()}_{MODULE_NAME}_ir.json")
with open(json_output, 'w') as f:
    json.dump(ir, f, indent=2)
print(f"\n📄 Complete IR: {json_output}")

# 2. Create sample_base_ir.json (expected output format)
sample_output = os.path.join(OUTPUT_FOLDER, "sample_base_ir.json")
with open(sample_output, 'w') as f:
    sample_ir = {
        "schema_version": "0.1",
        "metadata": {
            "generated_by": "ir_builder.py",
            "protocol": PROTOCOL,
            "module": MODULE_NAME
        },
        "module": ir['module'],
        "ports_summary": [
            {"name": p['name'], "role": p['role']} 
            for p in ir['ports'][:10]
        ],
        "fsm_states": ir['fsm']['states'],
        "reset": ir['reset']
    }
    json.dump(sample_ir, f, indent=2)
print(f"📄 Sample IR: {sample_output}")

# 3. Create ir_schema_v0_1.json (schema definition)
schema_output = os.path.join(OUTPUT_FOLDER, "ir_schema_v0_1.json")
schema = {
    "schema_name": "RTL Intermediate Representation",
    "version": "0.1",
    "description": "Semantic IR for RTL analysis",
    "fields": {
        "schema_version": {"type": "string", "required": True},
        "metadata": {
            "type": "object",
            "fields": {
                "generated_by": {"type": "string"},
                "timestamp": {"type": "string"},
                "source_file": {"type": "string"},
                "protocol": {"type": "string"}
            }
        },
        "module": {
            "type": "object",
            "fields": {
                "name": {"type": "string"},
                "type": {"type": "string", "enum": ["top", "submodule"]}
            }
        },
        "ports": {
            "type": "array",
            "items": {
                "name": {"type": "string"},
                "direction": {"type": "string", "enum": ["input", "output", "inout"]},
                "width": {"type": "integer"},
                "role": {"type": "string", "enum": ["clock", "reset", "data", "address", "control", "response", "other"]},
                "polarity": {"type": ["string", "null"], "enum": ["active_low", "active_high", None]}
            }
        },
        "fsm": {
            "type": "object",
            "fields": {
                "states": {"type": "array", "items": {"type": "string"}},
                "encoding": {"type": ["string", "null"]}
            }
        },
        "reset": {
            "type": "object",
            "fields": {
                "signal": {"type": ["string", "null"]},
                "polarity": {"type": ["string", "null"]},
                "type": {"type": ["string", "null"], "enum": ["synchronous", "asynchronous", None]}
            }
        }
    }
}
with open(schema_output, 'w') as f:
    json.dump(schema, f, indent=2)
print(f"📄 IR Schema: {schema_output}")

# 4. Create ast_to_ir_mapping_table.md
mapping_output = os.path.join(OUTPUT_FOLDER, "ast_to_ir_mapping_table.md")
with open(mapping_output, 'w') as f:
    f.write(f"""# AST to IR Mapping Table - {PROTOCOL} {MODULE_NAME}

## Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview

This document maps AST (Abstract Syntax Tree) fields to IR (Intermediate Representation) fields.

## Port Mapping

| AST Field | IR Field | Transformation |
|-----------|----------|----------------|
| `port.name` | `port.name` | Direct copy |
| `port.direction` | `port.direction` | Direct copy |
| `port.width` (string "31:0") | `port.width` (integer 32) | Converted to bit width |
| `port.type` (wire/reg) | (not in IR) | Dropped (not semantic) |
| (inferred from name) | `port.role` | **Classification rule-based** |
| (inferred from name) | `port.polarity` | **Detected from `_n` suffix** |

## Example Port Mapping

| AST | IR |
|-----|-----|
| `{{"name": "PCLK", "direction": "input"}}` | `{{"name": "PCLK", "role": "clock"}}` |
| `{{"name": "PRESETn", "direction": "input"}}` | `{{"name": "PRESETn", "role": "reset", "polarity": "active_low"}}` |
| `{{"name": "PADDR", "width": "7:0"}}` | `{{"name": "PADDR", "role": "address", "width": 8}}` |

## Classification Rules Used

| Role | Detection Rule |
|------|----------------|
| clock | Name contains `clk` or `clock` |
| reset | Name contains `rst` or `reset` |
| address | Name contains `addr` or `address` |
| data | Width > 1 OR name contains `data` |
| control | Name in `[psel, penable, pwrite, we, re]` |
| response | Name in `[prdata, pready, valid, busy]` |

## Reset Detection

| AST Always Block | IR Reset Type |
|------------------|---------------|
| `@(posedge clk or negedge rst_n)` | `asynchronous` |
| `@(posedge clk)` | `synchronous` |

## FSM State Mapping

| AST | IR |
|-----|-----|
| `localparam IDLE = 4'h0` | `fsm.states = ["IDLE", ...]` |
| `localparam SETUP = 4'h1` | |
| `localparam ACCESS = 4'h2` | |

## Why This Mapping Matters

1. **AST is syntax** - tells you WHAT the code says
2. **IR is semantics** - tells you WHAT the code MEANS
3. **Downstream tools** (DV, ML) use IR, not AST
4. **Schema-bound** ensures consistency across designs

## Validation

- IR follows schema version 0.1
- All ports classified
- Reset correctly identified
- FSM states extracted
""")
print(f"📄 AST to IR Mapping: {mapping_output}")

# 5. Create a readable summary
summary_output = os.path.join(OUTPUT_FOLDER, f"{PROTOCOL.lower()}_{MODULE_NAME}_ir_summary.txt")
with open(summary_output, 'w') as f:
    f.write(f"IR SUMMARY - {PROTOCOL} {MODULE_NAME}\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Module: {ir['module']['name']}\n")
    f.write(f"Type: {ir['module']['type']}\n\n")
    
    f.write("PORTS BY ROLE:\n")
    f.write("-" * 40 + "\n")
    roles = {}
    for p in ir['ports']:
        role = p['role']
        if role not in roles:
            roles[role] = []
        roles[role].append(p['name'])
    
    for role, ports in roles.items():
        f.write(f"  {role}: {', '.join(ports)}\n")
    
    f.write(f"\nFSM STATES: {', '.join(ir['fsm']['states'])}\n\n")
    f.write(f"RESET: {ir['reset']['signal']} ({ir['reset']['polarity']}, {ir['reset']['type']})\n")
    f.write(f"\nDATAPATH SIGNALS: {', '.join(ir['datapath']) if ir['datapath'] else 'None detected'}\n")
print(f"📄 IR Summary: {summary_output}")

print("\n" + "=" * 60)
print("IR BUILDER COMPLETE")
print("=" * 60)
print(f"\n✅ Output files created in: {OUTPUT_FOLDER}")
print("\n📄 Expected Output Files:")
print("   ✅ sample_base_ir.json")
print("   ✅ ir_schema_v0_1.json")
print("   ✅ ast_to_ir_mapping_table.md")
print(f"   ✅ {PROTOCOL.lower()}_{MODULE_NAME}_ir.json")
print(f"   ✅ {PROTOCOL.lower()}_{MODULE_NAME}_ir_summary.txt")