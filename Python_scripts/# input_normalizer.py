# input_normalizer.py - Script 1 of 6
import os
import csv

# ---- CONFIGURATION
RTL_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\APB_RTL"  # actual folder path
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs"
# ------------------------------------------

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Possible top module indicators (look for these in file content)
TOP_INDICATORS = ['PSEL', 'PENABLE', 'PADDR', 'PWDATA', 'PRDATA', 'PCLK', 'PRESETn']

def analyze_file(file_path):
    """Quickly check if file looks like a top module"""
    try:
        with open(file_path, 'r') as f:
            content = f.read().upper()
            score = sum(1 for indicator in TOP_INDICATORS if indicator in content)
            return 'likely_top' if score >= 4 else 'submodule'
    except:
        return 'unknown'

rtl_files = []
for file in os.listdir(RTL_FOLDER):
    if file.endswith(('.v', '.sv', '.vh')):
        full_path = os.path.join(RTL_FOLDER, file)
        analysis = analyze_file(full_path)
        rtl_files.append({
            'file_name': file,
            'file_path': full_path,
            'file_type': 'rtl_source',
            'is_top_module': analysis
        })

csv_output = os.path.join(OUTPUT_FOLDER, 'apb_file_manifest.csv')
with open(csv_output, 'w', newline='') as csvfile:
    fieldnames = ['file_name', 'file_path', 'file_type', 'is_top_module']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rtl_files)

print(f"✅ Found {len(rtl_files)} RTL files")
print(f"\n📋 Files identified:")
for f in rtl_files:
    print(f"   {f['file_name']:20} → {f['is_top_module']}")