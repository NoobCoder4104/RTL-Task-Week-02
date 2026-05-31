# parser_v0_I2C.py
import os
import json
from datetime import datetime

TOKEN_FILE = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\I2C outputs\i2c_i2c_token_stream.json"
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\I2C outputs"
PROTOCOL = "I2C"
MODULE_NAME = "i2c"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def parse_module(tokens):
    ast = {
        'protocol': PROTOCOL,
        'module_name': None,
        'ports': [],
        'parameters': [],
        'fsm_states': [],
        'always_blocks': []
    }
    
    # Find module name
    for i, t in enumerate(tokens):
        if t['type'] == 'KEYWORD' and t['value'] == 'module':
            if i + 1 < len(tokens):
                ast['module_name'] = tokens[i+1]['value']
            break
    
    # Find ports
    i = 0
    in_port_list = False
    while i < len(tokens):
        t = tokens[i]
        
        if t['type'] == 'KEYWORD' and t['value'] in ['input', 'output', 'inout']:
            direction = t['value']
            i += 1
            if i < len(tokens) and tokens[i]['type'] == 'KEYWORD' and tokens[i]['value'] in ['wire', 'reg']:
                i += 1
            if i < len(tokens) and tokens[i]['type'] == 'IDENTIFIER':
                ast['ports'].append({
                    'name': tokens[i]['value'],
                    'direction': direction
                })
        i += 1
    
    # Find FSM states
    fsm_keywords = ['IDLE', 'START', 'STOP', 'DATA', 'ACK', 'ADDRESS', 'REPEATED_START']
    for t in tokens:
        if t['type'] == 'IDENTIFIER':
            for state in fsm_keywords:
                if state in t['value'].upper():
                    if t['value'] not in ast['fsm_states']:
                        ast['fsm_states'].append(t['value'])
    
    return ast

# Main
print(f"Parser - {PROTOCOL} {MODULE_NAME}")
print("=" * 40)

with open(TOKEN_FILE, 'r') as f:
    tokens = json.load(f)

ast = parse_module(tokens)
print(f"Module: {ast['module_name']}")
print(f"Ports: {len(ast['ports'])}")
print(f"FSM States: {ast['fsm_states']}")

# Save outputs
json_output = os.path.join(OUTPUT_FOLDER, f"{PROTOCOL.lower()}_{MODULE_NAME}_ast.json")
with open(json_output, 'w') as f:
    json.dump(ast, f, indent=2)

sample_output = os.path.join(OUTPUT_FOLDER, "sample_ast.json")
with open(sample_output, 'w') as f:
    json.dump({
        'module_name': ast['module_name'],
        'ports_count': len(ast['ports']),
        'fsm_states': ast['fsm_states']
    }, f, indent=2)

print(f"Outputs saved to {OUTPUT_FOLDER}")