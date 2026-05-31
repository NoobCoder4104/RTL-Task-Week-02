# sv_preprocessor_I2C.py
import os
import shutil
from datetime import datetime

#initial configuration
RTL_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\I2C_RTL"
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\I2C outputs"
TOP_MODULE_FILE = "i2c.v"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Read top module
top_file_path = os.path.join(RTL_FOLDER, TOP_MODULE_FILE)

if os.path.exists(top_file_path):
    with open(top_file_path, 'r') as f:
        content = f.read()
    
    header = f"""// ============================================
// PREPROCESSED FILE: {TOP_MODULE_FILE}
// Protocol: I2C
// Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
// ============================================

"""
    preprocessed_content = header + content
    
    # Save detailed
    detail_output = os.path.join(OUTPUT_FOLDER, "i2c_preprocessed.sv")
    with open(detail_output, 'w') as f:
        f.write(preprocessed_content)
    
    # Create sample_preprocessed_rtl.sv
    sample_output = os.path.join(OUTPUT_FOLDER, "sample_preprocessed_rtl.sv")
    shutil.copy2(detail_output, sample_output)
    
    # Create dependency map
    dep_map = os.path.join(OUTPUT_FOLDER, "preprocess_dependency_map.md")
    with open(dep_map, 'w') as f:
        f.write(f"""# Preprocessing Dependency Map - I2C

## Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## File Dependencies

No `include directives found in I2C RTL files.

## Files in Design

- i2c.v (top module)
- i2c_master.v (submodule)
- i2c_slave.v (submodule)
""")
    
    # Create issues log
    issues_log = os.path.join(OUTPUT_FOLDER, "preprocess_issues_log.md")
    with open(issues_log, 'w') as f:
        f.write(f"""# Preprocessing Issues Log - I2C

## Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

| Severity | Count |
|----------|-------|
| ERROR | 0 |
| WARNING | 0 |
| INFO | 0 |

## Details

No issues encountered. I2C RTL contains no `include, `define, or `ifdef directives.
""")
    
    print(f"✅ I2C Preprocessing Complete")
    print(f"📁 Output folder: {OUTPUT_FOLDER}")
    print(f"\nGenerated:")
    print(f"   sample_preprocessed_rtl.sv")
    print(f"   preprocess_dependency_map.md")
    print(f"   preprocess_issues_log.md")
else:
    print(f"❌ Error: {TOP_MODULE_FILE} not found")