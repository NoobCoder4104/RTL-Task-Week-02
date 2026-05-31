# clock_reset_analyzer_I2C.py
import os
import json
import re
from datetime import datetime

IR_FILE = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\I2C outputs\i2c_i2c_ir.json"
RTL_FILE = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\I2C_RTL\I2C.v"
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\I2C outputs"
PROTOCOL = "I2C"
MODULE_NAME = "i2c"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("=" * 60)
print(f"CLOCK/RESET ANALYZER - {PROTOCOL} {MODULE_NAME}")
print("=" * 60)

# Load IR
with open(IR_FILE, 'r') as f:
    ir = json.load(f)
print(f"Loading IR from: {IR_FILE}")

# Load RTL
with open(RTL_FILE, 'r') as f:
    rtl_content = f.read()
print(f"Loading RTL from: {RTL_FILE}")

# Extract clocks from IR
clocks = [p for p in ir.get('ports', []) if p.get('role') == 'clock']
resets = [p for p in ir.get('ports', []) if p.get('role') == 'reset']

# Find FSM states from IR
fsm_states = ir.get('fsm', {}).get('states', [])

# Find always blocks
always_pattern = r'always\s+@\s*\(([^)]+)\)'
always_blocks = re.findall(always_pattern, rtl_content)

# Summary
summary = {
    'total_clocks': len(clocks),
    'total_resets': len(resets),
    'fsm_states': fsm_states,
    'total_always_blocks': len(always_blocks)
}

# Add IR reset info
summary['ir_reset_signal'] = ir.get('reset', {}).get('signal')
summary['ir_reset_polarity'] = ir.get('reset', {}).get('polarity')
summary['ir_reset_type'] = ir.get('reset', {}).get('type')

# Save report
report = {
    'protocol': PROTOCOL,
    'module': MODULE_NAME,
    'timestamp': datetime.now().isoformat(),
    'clocks': clocks,
    'resets': resets,
    'fsm_states': fsm_states,
    'summary': summary
}

report_output = os.path.join(OUTPUT_FOLDER, "clock_reset_report.json")
with open(report_output, 'w') as f:
    json.dump(report, f, indent=2)

print(f"\nClock/Reset Report: {report_output}")

# Print summary
print("\n" + "=" * 60)
print("ANALYSIS SUMMARY")
print("=" * 60)
print(f"""
Clocks: {', '.join([c['name'] for c in clocks])}
Resets: {', '.join([r['name'] for r in resets])}
FSM States: {fsm_states}
Always Blocks: {len(always_blocks)}

IR Reset Signal: {summary['ir_reset_signal']}
IR Reset Polarity: {summary['ir_reset_polarity']}
IR Reset Type: {summary['ir_reset_type']}
""")

print("=" * 60)
print("CLOCK/RESET ANALYZER COMPLETE")