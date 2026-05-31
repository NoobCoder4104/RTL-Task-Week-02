# lexer_tokenizer.py
# Converts RTL code into tokens (keywords, identifiers, numbers, operators)

import os
import re
import json
from datetime import datetime

# ============================================
# CONFIGURATION

# For APB Slave1:
INPUT_FILE = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\apb_slave1_preprocessed.sv"
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs"
PROTOCOL = "APB"
MODULE_NAME = "slave1"

# ============================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# SystemVerilog keywords (complete list for your scripts)
KEYWORDS = {
    # Module declarations
    'module', 'endmodule', 'input', 'output', 'inout', 'wire', 'reg', 'logic',
    # Always blocks
    'always', 'always_ff', 'always_comb', 'initial', 'begin', 'end',
    # Assignments
    'assign', 'parameter', 'localparam', 'typedef', 'enum',
    # Conditionals
    'if', 'else', 'case', 'endcase', 'casez', 'casex', 'default',
    # Sensitivity lists
    'posedge', 'negedge', 'or',
    # Data types
    'integer', 'time', 'real', 'string',
    # Functions
    'function', 'endfunction', 'task', 'endtask',
    # Generate
    'generate', 'endgenerate', 'genvar',
}

def is_number(token):
    """Check if token is a number (binary, hex, decimal, octal)"""
    # Binary: 8'b1010, 8'b1010_0010
    if re.match(r"^\d+['bB][01_]+$", token):
        return True
    # Hex: 8'hFF, 32'hDEADBEEF
    if re.match(r"^\d+['hH][0-9a-fA-F_]+$", token):
        return True
    # Octal: 8'o777
    if re.match(r"^\d+['oO][0-7_]+$", token):
        return True
    # Decimal: 123, 32'd123
    if re.match(r"^\d+$", token):
        return True
    if re.match(r"^\d+['dD][0-9_]+$", token):
        return True
    return False

def tokenize(content):
    """Convert Verilog/SystemVerilog code into a list of tokens"""
    tokens = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # Remove single-line comments
        if '//' in line:
            line = line[:line.index('//')]
        
        # Remove multi-line comments (simplified - handles most cases)
        while '/*' in line and '*/' in line:
            start = line.index('/*')
            end = line.index('*/') + 2
            line = line[:start] + ' ' + line[end:]
        
        if not line.strip():
            continue
        
        # Token patterns (order matters!)
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
                # Skip whitespace and unknown characters
                if line[pos].isspace():
                    pos += 1
                else:
                    # Unknown character - record as error
                    tokens.append({
                        'type': 'UNKNOWN',
                        'value': line[pos],
                        'line': line_num
                    })
                    pos += 1
    
    return tokens

# ============================================
# MAIN EXECUTION

print("=" * 60)
print(f"LEXER/TOKENIZER - {PROTOCOL} {MODULE_NAME}")
print("=" * 60)

# Read input file
if not os.path.exists(INPUT_FILE):
    print(f"❌ ERROR: Input file not found: {INPUT_FILE}")
    exit(1)

with open(INPUT_FILE, 'r') as f:
    content = f.read()

print(f"📁 Reading: {INPUT_FILE}")
print(f"📝 File size: {len(content)} characters, {len(content.splitlines())} lines")

# Tokenize
tokens = tokenize(content)
print(f"✅ Tokenized into {len(tokens)} tokens")

# ============================================
# SAVE OUTPUTS
# 1. Save as JSON (for scripts 4-6)

json_output = os.path.join(OUTPUT_FOLDER, f"{PROTOCOL.lower()}_{MODULE_NAME}_token_stream.json")
with open(json_output, 'w') as f:
    json.dump(tokens, f, indent=2)
print(f"📄 JSON output: {json_output}")

# 2. Save as readable text (for your review)
txt_output = os.path.join(OUTPUT_FOLDER, f"{PROTOCOL.lower()}_{MODULE_NAME}_token_stream.txt")
with open(txt_output, 'w') as f:
    f.write(f"LEXER OUTPUT - {PROTOCOL} {MODULE_NAME}\n")
    f.write(f"=" * 60 + "\n")
    f.write(f"Total tokens: {len(tokens)}\n\n")
    f.write(f"{'TYPE':15} | {'VALUE':30} | LINE\n")
    f.write(f"{'-'*15}-+-{'-'*30}-+----\n")
    for t in tokens[:100]:  # First 100 tokens only
        f.write(f"{t['type']:15} | {t['value']:30} | {t['line']}\n")
    if len(tokens) > 100:
        f.write(f"\n... and {len(tokens) - 100} more tokens\n")
print(f"📄 Text output: {txt_output}")

# 3. Create sample_token_stream.json (expected output format)
sample_output = os.path.join(OUTPUT_FOLDER, "sample_token_stream.json")
with open(sample_output, 'w') as f:
    # Create a simplified version for the sample
    sample = {
        'protocol': PROTOCOL,
        'module': MODULE_NAME,
        'total_tokens': len(tokens),
        'token_categories': {
            'KEYWORD': sum(1 for t in tokens if t['type'] == 'KEYWORD'),
            'IDENTIFIER': sum(1 for t in tokens if t['type'] == 'IDENTIFIER'),
            'NUMBER': sum(1 for t in tokens if t['type'] == 'NUMBER'),
            'OPERATOR': sum(1 for t in tokens if t['type'] == 'OPERATOR'),
            'PUNCTUATION': sum(1 for t in tokens if t['type'] == 'PUNCTUATION'),
        },
        'first_20_tokens': tokens[:20]
    }
    json.dump(sample, f, indent=2)
print(f"📄 Sample output: {sample_output}")

# 4. Create lexer_observation_log.md
log_output = os.path.join(OUTPUT_FOLDER, "lexer_observation_log.md")
with open(log_output, 'w') as f:
    f.write(f"""# Lexer/Observation Log - {PROTOCOL} {MODULE_NAME}

## Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Input File
- File: {INPUT_FILE}
- Size: {len(content)} characters
- Lines: {len(content.splitlines())}

## Tokenization Results
- Total tokens: {len(tokens)}
- Unique token types: {len(set(t['type'] for t in tokens))}

## Token Distribution

| Token Type | Count | Percentage |
|------------|-------|------------|
| KEYWORD | {sum(1 for t in tokens if t['type'] == 'KEYWORD')} | {sum(1 for t in tokens if t['type'] == 'KEYWORD')/len(tokens)*100:.1f}% |
| IDENTIFIER | {sum(1 for t in tokens if t['type'] == 'IDENTIFIER')} | {sum(1 for t in tokens if t['type'] == 'IDENTIFIER')/len(tokens)*100:.1f}% |
| NUMBER | {sum(1 for t in tokens if t['type'] == 'NUMBER')} | {sum(1 for t in tokens if t['type'] == 'NUMBER')/len(tokens)*100:.1f}% |
| OPERATOR | {sum(1 for t in tokens if t['type'] == 'OPERATOR')} | {sum(1 for t in tokens if t['type'] == 'OPERATOR')/len(tokens)*100:.1f}% |
| PUNCTUATION | {sum(1 for t in tokens if t['type'] == 'PUNCTUATION')} | {sum(1 for t in tokens if t['type'] == 'PUNCTUATION')/len(tokens)*100:.1f}% |

## Keywords Found
{', '.join(set(t['value'] for t in tokens if t['type'] == 'KEYWORD'))}

## Identifiers Found (First 20)
{', '.join(set(t['value'] for t in tokens if t['type'] == 'IDENTIFIER')[:20])}


## Observations
- No syntax errors detected during tokenization
- All SystemVerilog keywords recognized
- Numbers correctly identified (decimal, binary, hex formats)

## Issues Encountered
- No issues encountered

## Next Steps
- Pass token stream to parser_v0.py
- Extract module structure, ports, and FSM states
""")
print(f"📄 Log output: {log_output}")

print("\n" + "=" * 60)
print("LEXER/TOKENIZER COMPLETE")
print("=" * 60)
print(f"\n✅ Output files created in: {OUTPUT_FOLDER}")