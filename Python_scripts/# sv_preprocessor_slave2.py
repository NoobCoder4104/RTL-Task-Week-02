# sv_preprocessor.py - Script 2 of 6 (UPDATED for multiple slaves)

import os
import re

# ---- CONFIGURATION ----
RTL_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\APB_RTL"
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs"

TOP_MODULE_FILE = "slave2.v"  # ← CHANGE to "slave1.v" or "slave2.v" based on choice

# TOP_MODULE_FILES = "slave1.v"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def preprocess_file(file_path, base_path, processed_files=None):
    """Read file and expand `include directives"""
    if processed_files is None:
        processed_files = set()
    
    file_path = os.path.normpath(file_path)
    if file_path in processed_files:
        return ""
    
    processed_files.add(file_path)
    
    if not os.path.exists(file_path):
        return f"// ERROR: File not found - {file_path}\n"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find and replace `include "filename.v"
    include_pattern = r'`include\s+["<]([^">]+)[">]'
    
    def replace_include(match):
        include_file = match.group(1)
        possible_paths = [
            os.path.join(base_path, include_file),
            os.path.join(base_path, os.path.basename(include_file)),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return preprocess_file(path, base_path, processed_files)
        return f"// WARNING: Include file not found - {include_file}\n"
    
    content = re.sub(include_pattern, replace_include, content)
    return content

# OPTION A: Process single file (USE THIS)
top_file_path = os.path.join(RTL_FOLDER, TOP_MODULE_FILE)
preprocessed_content = preprocess_file(top_file_path, RTL_FOLDER)

output_file = os.path.join(OUTPUT_FOLDER, f'apb_{TOP_MODULE_FILE.replace(".v", "")}_preprocessed.sv')
with open(output_file, 'w') as f:
    f.write(preprocessed_content)

print(f"✅ Preprocessed: {TOP_MODULE_FILE}")
print(f"📄 Output: {output_file}")
print(f"📝 Lines: {len(preprocessed_content.splitlines())}")
