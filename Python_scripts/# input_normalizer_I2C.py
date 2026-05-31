# input_normalizer_I2C.py
import os
import csv

RTL_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\I2C_RTL"
OUTPUT_FOLDER = r"E:\Asmicore_Mentorship Programme\Tasks (RTL+ML+DV)\Projects of weeks\RTL Task 02\Outputs\I2C outputs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

rtl_files = []
def new_func(RTL_FOLDER):
    return os.listdir(RTL_FOLDER)
for file in new_func(RTL_FOLDER):
    if file.endswith(('.v', '.sv')):
        full_path = os.path.join(RTL_FOLDER, file)
        
        # Identify role
        if file == "i2c.v":
            role = "top_module"
        elif "master" in file.lower():
            role = "submodule_master"
        elif "slave" in file.lower():
            role = "submodule_slave"
        else:
            role = "unknown"
        
        rtl_files.append({
            'file_name': file,
            'file_path': full_path,
            'file_type': 'rtl_source',
            'is_top_module': role
        })

csv_output = os.path.join(OUTPUT_FOLDER, 'i2c_file_manifest.csv')
with open(csv_output, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['file_name', 'file_path', 'file_type', 'is_top_module'])
    writer.writeheader()
    writer.writerows(rtl_files)

print(f"✅ I2C File Manifest Created")
print(f"📄 {csv_output}")
print(f"\nFiles found:")
for f in rtl_files:
    print(f"   {f['file_name']:20} → {f['is_top_module']}")