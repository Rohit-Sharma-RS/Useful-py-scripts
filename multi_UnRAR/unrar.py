import rarfile
import os

rar_files = [r"part1.rar", r"part2.rar", r"part3.rar"]
output_folder = "combined_folder"
os.makedirs(output_folder, exist_ok=True)

for rar_file in rar_files:
    with rarfile.RarFile(rar_file) as rf:
        rf.extractall(output_folder)

print(f"All files extracted to '{output_folder}' successfully!")
