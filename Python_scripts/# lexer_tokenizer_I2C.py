# lexer_tokenizer_I2C.py
import os
import re
import json
from datetime import datetime

INPUT_FILE = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\I2C outputs\i2c_preprocessed.sv"
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\I2C outputs"
PROTOCOL = "I2C"
MODULE_NAME = "i2c"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

KEYWORDS = {
    'module', 'endmodule', 'input', 'output', 'inout', 'wire', 'reg', 'logic',
    'always', 'always_ff', 'always_comb', 'initial', 'begin', 'end',
    'assign', 'parameter', 'localparam', 'typedef', 'enum',
    'if', 'else', 'case', 'endcase', 'posedge', 'negedge', 'or'
}

def tokenize(content):
    tokens = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        if '//' in line:
            line = line[:line.index('//')]
        
        if not line.strip():
            continue
        
        patterns = [
            ('KEYWORD', r'\b(?:' + '|'.join(re.escape(kw) for kw in KEYWORDS) + r')\b'),
            ('NUMBER', r"\d+['bBhHdDoO][01a-fA-FxXzZ?_]+|\d+"),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('OPERATOR', r'[=!<>]=|[=!<>]|&&|\|\||[+\-*/%&|^~?:]'),
            ('PUNCTUATION', r'[;:,\(\)\[\]{}]'),
        ]
        
        pos = 0
        while pos < len(line):
            match = None
            for token_type, pattern in patterns:
                regex = re.compile(pattern)
                match = regex.match(line, pos)
                if match:
                    value = match.group(0)
                    tokens.append({
                        'type': token_type,
                        'value': value,
                        'line': line_num
                    })
                    pos = match.end()
                    break
            if not match:
                if line[pos].isspace():
                    pos += 1
                else:
                    tokens.append({
                        'type': 'UNKNOWN',
                        'value': line[pos],
                        'line': line_num
                    })
                    pos += 1
    
    return tokens

# Main
print(f"Lexer/Tokenizer - {PROTOCOL} {MODULE_NAME}")
print("=" * 40)

with open(INPUT_FILE, 'r') as f:
    content = f.read()

tokens = tokenize(content)
print(f"Tokenized {len(tokens)} tokens")

# Save outputs
json_output = os.path.join(OUTPUT_FOLDER, f"{PROTOCOL.lower()}_{MODULE_NAME}_token_stream.json")
with open(json_output, 'w') as f:
    json.dump(tokens, f, indent=2)

sample_output = os.path.join(OUTPUT_FOLDER, "sample_token_stream.json")
sample = {
    'protocol': PROTOCOL,
    'module': MODULE_NAME,
    'total_tokens': len(tokens),
    'first_20_tokens': tokens[:20]
}
with open(sample_output, 'w') as f:
    json.dump(sample, f, indent=2)

log_output = os.path.join(OUTPUT_FOLDER, "lexer_observation_log.md")
with open(log_output, 'w') as f:
    f.write(f"# Lexer Observation Log - I2C\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"**Total Tokens:** {len(tokens)}\n\n")
    f.write(f"**Keyword Count:** {sum(1 for t in tokens if t['type'] == 'KEYWORD')}\n")
    f.write(f"**Identifier Count:** {sum(1 for t in tokens if t['type'] == 'IDENTIFIER')}\n")
    f.write(f"**Number Count:** {sum(1 for t in tokens if t['type'] == 'NUMBER')}\n")

print(f"Outputs saved to {OUTPUT_FOLDER}")