# clock_reset_analyzer_Slave1.py - Script 6 of 6
# Analyzes clock and reset behavior from IR and original RTL

import os
import json
import re
from datetime import datetime

# ============================================
# CONFIGURATION - FOR APB Slave1
# ============================================

IR_FILE = r"E:/Asmicore_Mentorship Programme/Tasks (RTL+ML+DV)/Projects of weeks/RTL Task 02/Outputs/apb_slave1_ir.json"
RTL_FILE = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\APB_RTL\slave1.v"
OUTPUT_FOLDER = r"E:/Asmicore_Mentorship Programme/Tasks (RTL+ML+DV)/Projects of weeks/RTL Task 02/Outputs"
PROTOCOL = "APB"
MODULE_NAME = "slave1"

# ============================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def analyze_clocks(ir, rtl_content):
    """Identify all clock signals"""
    clocks = []
    
    # From IR ports with role 'clock'
    for port in ir.get('ports', []):
        if port.get('role') == 'clock':
            clocks.append({
                'name': port.get('name'),
                'source': 'port',
                'direction': port.get('direction')
            })
    
    # Search RTL for clock patterns
    patterns = [
        r'always\s+@\s*\(\s*posedge\s+(\w+)',
        r'always\s+@\s*\(\s*negedge\s+(\w+)',
        r'input\s+wire\s+(\w*clk\w*)',
        r'input\s+(\w*clk\w*)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, rtl_content, re.IGNORECASE)
        for match in matches:
            if not any(c['name'] == match for c in clocks):
                clocks.append({
                    'name': match,
                    'source': 'detected_in_rtl',
                    'direction': 'input'
                })
    
    # Remove duplicates
    unique = {}
    for c in clocks:
        if c['name'] not in unique:
            unique[c['name']] = c
    
    return list(unique.values())

def analyze_resets(ir, rtl_content):
    """Identify all reset signals"""
    resets = []
    
    # From IR ports with role 'reset'
    for port in ir.get('ports', []):
        if port.get('role') == 'reset':
            polarity = port.get('polarity', 'unknown')
            resets.append({
                'name': port.get('name'),
                'source': 'port',
                'polarity': polarity,
                'type': 'unknown',
                'affects_registers': []
            })
    
    # Search RTL for reset patterns
    patterns = [
        r'always\s+@\s*\(\s*[^)]*?(?:posedge|negedge)\s+(\w*rst\w*)',
        r'input\s+wire\s+(\w*rst\w*)',
        r'input\s+(\w*rst\w*)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, rtl_content, re.IGNORECASE)
        for match in matches:
            if not any(r['name'] == match for r in resets):
                polarity = 'active_low' if '_n' in match.lower() else 'active_high'
                resets.append({
                    'name': match,
                    'source': 'detected_in_rtl',
                    'polarity': polarity,
                    'type': 'unknown',
                    'affects_registers': []
                })
    
    # Determine async vs sync
    for reset in resets:
        reset_name = reset['name']
        
        # Check for async reset (in sensitivity list)
        async_pattern = r'always\s+@\s*\(\s*[^)]*?(?:posedge|negedge)\s+' + reset_name
        if re.search(async_pattern, rtl_content, re.IGNORECASE):
            reset['type'] = 'asynchronous'
        else:
            # Check for sync reset (inside always block)
            sync_pattern = r'always\s+@\s*\(\s*posedge\s+\w+\s*\)[\s\S]*?if\s*\(\s*' + reset_name
            if re.search(sync_pattern, rtl_content, re.IGNORECASE):
                reset['type'] = 'synchronous'
            else:
                reset['type'] = 'unknown'
        
        # Find registers affected by this reset
        pattern = r'if\s*\(\s*' + reset_name + r'\s*\)\s*begin(.*?)end'
        matches = re.findall(pattern, rtl_content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            reg_pattern = r'(\w+)\s*<='
            registers = re.findall(reg_pattern, match)
            for reg in registers:
                if reg not in reset['affects_registers']:
                    reset['affects_registers'].append(reg)
    
    return resets

def analyze_always_blocks(rtl_content, resets):
    """Analyze always blocks"""
    blocks = []
    pattern = r'always\s+@\s*\(([^)]+)\)\s*(?:begin)?\s*([\s\S]*?)(?:end|always)'
    matches = re.findall(pattern, rtl_content, re.DOTALL | re.IGNORECASE)
    
    for i, (sensitivity, body) in enumerate(matches):
        block = {
            'id': i + 1,
            'sensitivity_list': sensitivity.strip(),
            'clock': None,
            'reset': None,
            'reset_type': None
        }
        
        # Find clock
        if 'posedge' in sensitivity or 'negedge' in sensitivity:
            edge_pattern = r'(?:posedge|negedge)\s+(\w+)'
            edge_matches = re.findall(edge_pattern, sensitivity)
            for sig in edge_matches:
                if 'clk' in sig.lower():
                    block['clock'] = sig
                elif 'rst' in sig.lower() or 'reset' in sig.lower():
                    block['reset'] = sig
                    block['reset_type'] = 'asynchronous'
        
        # If no reset in sensitivity, check body for sync reset
        if block['reset'] is None:
            for reset in resets:
                if re.search(r'if\s*\(\s*' + reset['name'] + r'\s*\)', body, re.IGNORECASE):
                    block['reset'] = reset['name']
                    block['reset_type'] = 'synchronous'
                    break
        
        blocks.append(block)
    
    return blocks

# ============================================
# MAIN EXECUTION
# ============================================

print("=" * 60)
print(f"CLOCK/RESET ANALYZER - {PROTOCOL} {MODULE_NAME}")
print("=" * 60)

# Load IR
if not os.path.exists(IR_FILE):
    print(f"ERROR: IR file not found: {IR_FILE}")
    exit(1)

with open(IR_FILE, 'r') as f:
    ir = json.load(f)
print(f"Loading IR from: {IR_FILE}")

# Load RTL
if not os.path.exists(RTL_FILE):
    print(f"WARNING: RTL file not found: {RTL_FILE}")
    rtl_content = ""
else:
    with open(RTL_FILE, 'r') as f:
        rtl_content = f.read()
    print(f"Loading RTL from: {RTL_FILE}")

# Run analyses
print("\nAnalyzing...")
clocks = analyze_clocks(ir, rtl_content)
resets = analyze_resets(ir, rtl_content)
always_blocks = analyze_always_blocks(rtl_content, resets)

# Build reset dependencies
reset_deps = []
for r in resets:
    if r['affects_registers']:
        reset_deps.append({
            'reset_signal': r['name'],
            'polarity': r['polarity'],
            'type': r['type'],
            'registers_affected': r['affects_registers'],
            'count': len(r['affects_registers'])
        })

# Generate summary
summary = {
    'total_clocks': len(clocks),
    'total_resets': len(resets),
    'total_always_blocks': len(always_blocks),
    'async_resets': sum(1 for r in resets if r['type'] == 'asynchronous'),
    'sync_resets': sum(1 for r in resets if r['type'] == 'synchronous'),
    'active_low_resets': sum(1 for r in resets if r['polarity'] == 'active_low'),
    'active_high_resets': sum(1 for r in resets if r['polarity'] == 'active_high'),
    'registers_under_reset': sum(d['count'] for d in reset_deps)
}

# Add IR reset info
summary['ir_reset_signal'] = ir.get('reset', {}).get('signal')
summary['ir_reset_polarity'] = ir.get('reset', {}).get('polarity')
summary['ir_reset_type'] = ir.get('reset', {}).get('type')

# ============================================
# SAVE OUTPUTS
# ============================================

# 1. Complete analysis JSON
analysis_data = {
    'metadata': {
        'generated_by': 'clock_reset_analyzer.py',
        'timestamp': datetime.now().isoformat(),
        'protocol': PROTOCOL,
        'module': MODULE_NAME
    },
    'clocks': clocks,
    'resets': resets,
    'always_blocks_analysis': always_blocks,
    'reset_dependencies': reset_deps,
    'summary': summary
}

json_output = os.path.join(OUTPUT_FOLDER, f"{PROTOCOL.lower()}_{MODULE_NAME}_clock_reset_analysis.json")
with open(json_output, 'w') as f:
    json.dump(analysis_data, f, indent=2)
print(f"\nComplete analysis: {json_output}")

# 2. clock_reset_report.json
report_output = os.path.join(OUTPUT_FOLDER, "clock_reset_report.json")
report = {
    'protocol': PROTOCOL,
    'module': MODULE_NAME,
    'timestamp': datetime.now().isoformat(),
    'clocks': [{'name': c['name']} for c in clocks],
    'resets': [
        {
            'name': r['name'],
            'polarity': r['polarity'],
            'type': r['type'],
            'registers_affected_count': len(r['affects_registers'])
        } for r in resets
    ],
    'summary': summary
}
with open(report_output, 'w') as f:
    json.dump(report, f, indent=2)
print(f"Clock/Reset Report: {report_output}")

# 3. clock_reset_rules_v0.md
rules_output = os.path.join(OUTPUT_FOLDER, "clock_reset_rules_v0.md")
with open(rules_output, 'w') as f:
    f.write("# Clock/Reset Detection Rules v0\n\n")
    f.write(f"**Protocol:** {PROTOCOL}\n")
    f.write(f"**Module:** {MODULE_NAME}\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("## Clocks Found\n\n")
    for c in clocks:
        f.write(f"- `{c['name']}` (source: {c['source']})\n")
    
    f.write("\n## Resets Found\n\n")
    for r in resets:
        f.write(f"- `{r['name']}` (polarity: {r['polarity']}, type: {r['type']})\n")
    
    f.write("\n## Detection Rules\n\n")
    f.write("| Rule | Pattern |\n")
    f.write("|------|---------|\n")
    f.write("| Clock | Name contains 'clk' or 'clock' |\n")
    f.write("| Reset (active low) | Name ends with '_n' |\n")
    f.write("| Reset (active high) | Name contains 'rst' without '_n' |\n")
    f.write("| Async Reset | In sensitivity list: `@(posedge clk or negedge rst_n)` |\n")
    f.write("| Sync Reset | Inside always block: `if (rst) ...` |\n")
print(f"Detection rules: {rules_output}")

# 4. reset_graph_v0.md
graph_output = os.path.join(OUTPUT_FOLDER, "reset_graph_v0.md")
with open(graph_output, 'w') as f:
    f.write(f"# Reset Dependency Graph - {PROTOCOL} {MODULE_NAME}\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("```\n")
    for dep in reset_deps:
        f.write(f"{dep['reset_signal']} ({dep['polarity']}, {dep['type']})\n")
        f.write(f"    └── Affects {dep['count']} registers\n")
    if not reset_deps:
        f.write("No reset dependencies detected.\n")
    f.write("```\n\n")
    
    f.write("## Always Block Summary\n\n")
    f.write("| Block | Sensitivity | Clock | Reset | Reset Type |\n")
    f.write("|-------|-------------|-------|-------|------------|\n")
    for b in always_blocks:
        f.write(f"| {b['id']} | `{b['sensitivity_list']}` | {b.get('clock', '-')} | {b.get('reset', '-')} | {b.get('reset_type', '-')} |\n")
print(f"Reset graph: {graph_output}")

# 5. Print summary
print("\n" + "=" * 60)
print("ANALYSIS SUMMARY")
print("=" * 60)
print(f"""
Clocks: {', '.join([c['name'] for c in clocks])}
Resets: {', '.join([r['name'] for r in resets])}
Async Resets: {summary['async_resets']}
Sync Resets: {summary['sync_resets']}
Active Low Resets: {summary['active_low_resets']}
Active High Resets: {summary['active_high_resets']}
Always Blocks: {summary['total_always_blocks']}
Registers Under Reset: {summary['registers_under_reset']}

IR Reset Signal: {summary['ir_reset_signal']}
IR Reset Polarity: {summary['ir_reset_polarity']}
IR Reset Type: {summary['ir_reset_type']}
""")

print("=" * 60)
print("CLOCK/RESET ANALYZER COMPLETE")
print("=" * 60)
print(f"\nOutput folder: {OUTPUT_FOLDER}")