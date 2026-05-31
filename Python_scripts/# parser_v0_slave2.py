# parser_v0.py - Script 4 of 6
# Extracts module structure from token stream (AST Generation)

import os
import json
import re
from datetime import datetime

# ============================================
# CONFIGURATION - CHANGE FOR YOUR FILE
# ============================================

# For APB Slave2:
TOKEN_FILE = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\apb_slave2_token_stream.json"
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs"
PROTOCOL = "APB"
MODULE_NAME = "slave2"


# ============================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.ast = {
            'protocol': PROTOCOL,
            'module_name': None,
            'ports': [],
            'signals': [],
            'parameters': [],
            'fsm_states': [],
            'always_blocks': [],
            'assignments': []
        }
    
    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    def peek_next_token(self, offset=1):
        if self.position + offset < len(self.tokens):
            return self.tokens[self.position + offset]
        return None
    
    def consume(self):
        token = self.current_token()
        self.position += 1
        return token
    
    def match(self, expected_type, expected_value=None):
        token = self.current_token()
        if token and token['type'] == expected_type:
            if expected_value is None or token['value'] == expected_value:
                self.consume()
                return token
        return None
    
    def parse_module(self):
        """Parse module declaration"""
        # Find 'module' keyword
        while self.position < len(self.tokens):
            token = self.current_token()
            if token['type'] == 'KEYWORD' and token['value'] == 'module':
                self.consume()
                break
            self.position += 1
        
        # Get module name
        module_token = self.current_token()
        if module_token and module_token['type'] == 'IDENTIFIER':
            self.ast['module_name'] = module_token['value']
            self.consume()
            print(f"  📦 Module found: {self.ast['module_name']}")
        
        # Parse ports
        self.parse_ports()
        
        # Parse rest of module content
        self.parse_module_body()
        
        return self.ast
    
    def parse_ports(self):
        """Parse module ports (inputs, outputs, inouts)"""
        # Look for port declarations
        while self.position < len(self.tokens):
            token = self.current_token()
            
            # Check for port direction keywords
            if token['type'] == 'KEYWORD' and token['value'] in ['input', 'output', 'inout']:
                direction = token['value']
                self.consume()
                
                # Check for wire/reg after direction
                signal_type = 'wire'
                next_token = self.current_token()
                if next_token and next_token['type'] == 'KEYWORD' and next_token['value'] in ['wire', 'reg', 'logic']:
                    signal_type = next_token['value']
                    self.consume()
                
                # Get port name
                port_token = self.current_token()
                if port_token and port_token['type'] == 'IDENTIFIER':
                    port_name = port_token['value']
                    self.consume()
                    
                    self.ast['ports'].append({
                        'name': port_name,
                        'direction': direction,
                        'type': signal_type,
                        'width': None  # Will parse width later
                    })
                    
                    # Check for width [X:Y]
                    if self.current_token() and self.current_token()['value'] == '[':
                        self.consume()  # Skip '['
                        msb = self.current_token()['value'] if self.current_token() else None
                        self.consume()  # Skip msb
                        self.consume()  # Skip ':'
                        lsb = self.current_token()['value'] if self.current_token() else None
                        self.consume()  # Skip lsb
                        self.consume()  # Skip ']'
                        
                        if self.ast['ports']:
                            self.ast['ports'][-1]['width'] = f"{msb}:{lsb}"
            
            # Check for 'endmodule' - stop parsing ports
            elif token['type'] == 'KEYWORD' and token['value'] == 'endmodule':
                break
            
            # Check for semicolon - move on
            elif token['value'] == ';':
                self.consume()
            
            else:
                self.position += 1
            
            # Safety: don't go too far
            if self.position > len(self.tokens) - 1:
                break
    
    def parse_module_body(self):
        """Parse parameters, signals, always blocks inside module"""
        
        while self.position < len(self.tokens):
            token = self.current_token()
            
            if not token:
                break
            
            # End of module
            if token['type'] == 'KEYWORD' and token['value'] == 'endmodule':
                print(f"  ✅ Found endmodule")
                break
            
            # Parse parameters and localparams
            if token['type'] == 'KEYWORD' and token['value'] in ['parameter', 'localparam']:
                param_type = token['value']
                self.consume()
                
                # Get parameter name
                name_token = self.current_token()
                if name_token and name_token['type'] == 'IDENTIFIER':
                    param_name = name_token['value']
                    self.consume()
                    
                    # Get '='
                    if self.current_token() and self.current_token()['value'] == '=':
                        self.consume()
                        
                        # Get value
                        value_token = self.current_token()
                        param_value = value_token['value'] if value_token else None
                        
                        if param_value:
                            self.ast['parameters'].append({
                                'name': param_name,
                                'value': param_value,
                                'type': param_type
                            })
                            self.consume()
                    
                    # Skip to semicolon
                    while self.current_token() and self.current_token()['value'] != ';':
                        self.consume()
                    if self.current_token() and self.current_token()['value'] == ';':
                        self.consume()
            
            # Parse FSM states from localparam
            if token['type'] == 'IDENTIFIER':
                # Look for FSM state names (IDLE, START, DATA, STOP, etc.)
                fsm_keywords = ['IDLE', 'START', 'SETUP', 'ACCESS', 'STOP', 'DATA', 
                               'PARITY', 'ADDRESS', 'ACK', 'WRITE', 'READ']
                for fsm_state in fsm_keywords:
                    if fsm_state in token['value'].upper():
                        if token['value'] not in self.ast['fsm_states']:
                            self.ast['fsm_states'].append(token['value'])
            
            # Parse always blocks
            if token['type'] == 'KEYWORD' and 'always' in token['value']:
                block_type = token['value']
                self.consume()
                
                # Parse sensitivity list
                sensitivity = []
                if self.current_token() and self.current_token()['value'] == '@':
                    self.consume()
                    if self.current_token() and self.current_token()['value'] == '(':
                        self.consume()
                        while self.current_token() and self.current_token()['value'] != ')':
                            if self.current_token()['type'] == 'KEYWORD':
                                sensitivity.append(self.current_token()['value'])
                            elif self.current_token()['type'] == 'IDENTIFIER':
                                sensitivity.append(self.current_token()['value'])
                            self.consume()
                        self.consume()  # Skip ')'
                
                self.ast['always_blocks'].append({
                    'type': block_type,
                    'sensitivity': sensitivity,
                    'line': token.get('line', 0)
                })
            
            # Parse assign statements
            if token['type'] == 'KEYWORD' and token['value'] == 'assign':
                self.consume()
                left = None
                right = None
                
                # Get left side
                if self.current_token() and self.current_token()['type'] == 'IDENTIFIER':
                    left = self.current_token()['value']
                    self.consume()
                
                # Get '='
                if self.current_token() and self.current_token()['value'] == '=':
                    self.consume()
                    
                    # Get right side (simplified)
                    right_parts = []
                    while self.current_token() and self.current_token()['value'] != ';':
                        right_parts.append(self.current_token()['value'])
                        self.consume()
                    
                    right = ' '.join(right_parts)
                    self.consume()  # Skip ';'
                    
                    self.ast['assignments'].append({
                        'left': left,
                        'right': right,
                        'line': token.get('line', 0)
                    })
            
            self.position += 1
    
    def parse(self):
        return self.parse_module()

# ============================================
# MAIN EXECUTION
# ============================================

print("=" * 60)
print(f"PARSER v0 - {PROTOCOL} {MODULE_NAME}")
print("=" * 60)

# Load tokens
if not os.path.exists(TOKEN_FILE):
    print(f"❌ ERROR: Token file not found: {TOKEN_FILE}")
    print(f"   Please run lexer_tokenizer.py first!")
    exit(1)

with open(TOKEN_FILE, 'r') as f:
    tokens = json.load(f)

print(f"📁 Loading tokens from: {TOKEN_FILE}")
print(f"📝 Total tokens: {len(tokens)}")

# Parse
parser = Parser(tokens)
ast = parser.parse()

# ============================================
# SAVE OUTPUTS
# ============================================

# 1. Save AST as JSON
json_output = os.path.join(OUTPUT_FOLDER, f"{PROTOCOL.lower()}_{MODULE_NAME}_ast.json")
with open(json_output, 'w') as f:
    json.dump(ast, f, indent=2)
print(f"📄 AST JSON: {json_output}")

# 2. Create sample_ast.json (expected output format)
sample_output = os.path.join(OUTPUT_FOLDER, "sample_ast.json")
with open(sample_output, 'w') as f:
    sample_ast = {
        'protocol': PROTOCOL,
        'module_name': ast['module_name'],
        'ports_count': len(ast['ports']),
        'fsm_states': ast['fsm_states'],
        'parameters_count': len(ast['parameters']),
        'always_blocks_count': len(ast['always_blocks']),
        'first_5_ports': ast['ports'][:5] if ast['ports'] else []
    }
    json.dump(sample_ast, f, indent=2)
print(f"📄 Sample AST: {sample_output}")

# 3. Create parser_scope_v0.md (documentation)
md_output = os.path.join(OUTPUT_FOLDER, "parser_scope_v0.md")
with open(md_output, 'w') as f:
    f.write(f"""# Parser Scope v0 - {PROTOCOL} {MODULE_NAME}

## Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Parser Summary

| Item | Value |
|------|-------|
| Module Name | {ast['module_name']} |
| Number of Ports | {len(ast['ports'])} |
| Number of Signals | {len(ast['signals'])} |
| Number of Parameters | {len(ast['parameters'])} |
| FSM States Found | {len(ast['fsm_states'])} |
| Always Blocks | {len(ast['always_blocks'])} |
| Assign Statements | {len(ast['assignments'])} |

## Ports List

| Name | Direction | Type | Width |
|------|-----------|------|-------|
""")
    for port in ast['ports']:
        f.write(f"| {port['name']} | {port['direction']} | {port['type']} | {port['width'] or '1'} |\n")
    
    f.write(f"""
## Parameters/Localparams

| Name | Value | Type |
|------|-------|------|
""")
    for param in ast['parameters']:
        f.write(f"| {param['name']} | {param['value']} | {param['type']} |\n")
    
    f.write(f"""
## FSM States Found

{', '.join(ast['fsm_states']) if ast['fsm_states'] else 'No FSM states detected'}

## Always Blocks

| Type | Sensitivity | Line |
|------|-------------|------|
""")
    for block in ast['always_blocks']:
        f.write(f"| {block['type']} | {', '.join(block['sensitivity'])} | {block['line']} |\n")
    
    f.write(f"""
## Observations

- Module parsed successfully
- {len(ast['ports'])} ports extracted
- {len(ast['fsm_states'])} potential FSM states identified
- {len(ast['always_blocks'])} always blocks found

## Limitations (v0)

- Width parsing simplified
- Multi-dimensional arrays not supported
- Complex expressions not fully parsed
- Package imports not handled

## Next Steps

- Pass AST to ir_builder.py
- Classify ports by role (clock, reset, data, control)
- Build semantic IR
""")
print(f"📄 Parser scope: {md_output}")

# 4. Create unsupported_sv_patterns.md
unsupported = os.path.join(OUTPUT_FOLDER, "unsupported_sv_patterns.md")
with open(unsupported, 'w') as f:
    f.write(f"""# Unsupported SystemVerilog Patterns - {PROTOCOL} {MODULE_NAME}

## Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Patterns Not Supported in v0 Parser

| Pattern | Description | Found? |
|---------|-------------|--------|
| `typedef` | User-defined types | {'Yes' if any(t['value'] == 'typedef' for t in tokens) else 'No'} |
| `enum` | Enumerated types | {'Yes' if any(t['value'] == 'enum' for t in tokens) else 'No'} |
| `struct` | Structures | No |
| `union` | Unions | No |
| `interface` | Interfaces | No |
| `modport` | Module ports | No |
| `generate` | Generate blocks | {'Yes' if any(t['value'] == 'generate' for t in tokens) else 'No'} |
| `package` | Packages | No |
| `import` | Package imports | {'Yes' if any(t['value'] == 'import' for t in tokens) else 'No'} |

## Notes

- The parser successfully extracted basic module structure
- Complex SV features will be added in future versions
- For this project, v0 parser is sufficient
""")
print(f"📄 Unsupported patterns: {unsupported}")

print("\n" + "=" * 60)
print("PARSER v0 COMPLETE")
print("=" * 60)
print(f"\n✅ Output files created in: {OUTPUT_FOLDER}")
print("\n📄 Expected Output Files:")
print("   ✅ sample_ast.json")
print("   ✅ parser_scope_v0.md")
print("   ✅ unsupported_sv_patterns.md")
print(f"   ✅ {PROTOCOL.lower()}_{MODULE_NAME}_ast.json")