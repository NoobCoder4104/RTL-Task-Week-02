# ir_builder_I2C.py
import os
import json
from datetime import datetime

AST_FILE = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\I2C outputs\i2c_i2c_ast.json"
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\I2C outputs"
PROTOCOL = "I2C"
MODULE_NAME = "i2c"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def classify_port(name):
    name_lower = name.lower()
    if 'clk' in name_lower:
        return 'clock', None
    elif 'rst' in name_lower:
        polarity = 'active_low' if '_n' in name_lower else 'active_high'
        return 'reset', polarity
    elif 'addr' in name_lower:
        return 'address', None
    elif 'data' in name_lower:
        return 'data', None
    elif name_lower in ['we', 're', 'en', 'enable']:
        return 'control', None
    else:
        return 'other', None

# Main
print(f"IR Builder - {PROTOCOL} {MODULE_NAME}")
print("=" * 40)

with open(AST_FILE, 'r') as f:
    ast = json.load(f)

# Build IR
ir = {
    'schema_version': '0.1',
    'metadata': {
        'generated_by': 'ir_builder.py',
        'timestamp': datetime.now().isoformat(),
        'protocol': PROTOCOL
    },
    'module': {
        'name': ast.get('module_name'),
        'type': 'top'
    },
    'ports': [],
    'fsm': {
        'states': ast.get('fsm_states', []),
        'encoding': 'localparam'
    },
    'reset': {}
}

# Classify ports
for port in ast.get('ports', []):
    role, polarity = classify_port(port['name'])
    port_entry = {
        'name': port['name'],
        'direction': port['direction'],
        'role': role
    }
    if polarity:
        port_entry['polarity'] = polarity
        if role == 'reset':
            ir['reset'] = {
                'signal': port['name'],
                'polarity': polarity,
                'type': 'asynchronous'  # I2C uses async reset
            }
    ir['ports'].append(port_entry)

print(f"Module: {ir['module']['name']}")
print(f"Ports: {len(ir['ports'])}")
print(f"FSM States: {ir['fsm']['states']}")

# Save outputs
json_output = os.path.join(OUTPUT_FOLDER, f"{PROTOCOL.lower()}_{MODULE_NAME}_ir.json")
with open(json_output, 'w') as f:
    json.dump(ir, f, indent=2)

sample_output = os.path.join(OUTPUT_FOLDER, "sample_base_ir.json")
with open(sample_output, 'w') as f:
    json.dump({
        'module': ir['module'],
        'ports_summary': [{'name': p['name'], 'role': p['role']} for p in ir['ports'][:10]],
        'fsm_states': ir['fsm']['states']
    }, f, indent=2)

print(f"Outputs saved to {OUTPUT_FOLDER}")