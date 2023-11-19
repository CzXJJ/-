import numpy as np
import os
import json
from pymatgen.core import Structure
from pymatgen.io.cif import CifWriter

def create_structure(matrix, coords, elements):
    lattice = np.array(matrix, dtype=np.float64, ndmin=2).reshape((3, 3))
    structure = Structure(lattice, elements, coords)
    return structure

# 读取.data文件
with open('db_2.data', 'r') as file:
    data = json.load(file)

# 创建文件夹
original_dir = "结构/原始结构"
relaxed_dir = "结构/弛豫后结构"
os.makedirs(original_dir, exist_ok=True)
os.makedirs(relaxed_dir, exist_ok=True)

# 针对每个结构执行操作
for entry_key, entry_value in data.items():
    if "rstruc" in entry_value:
        # 处理rstruc
        original_structure = create_structure(entry_value["rstruc"][0], entry_value["rstruc"][1], entry_value["rstruc"][2])
        original_cif_path = os.path.join(original_dir, f"{entry_key}_原始结构.cif")
        original_cif_writer = CifWriter(original_structure, write_magmoms=False)
        original_cif_writer.write_file(original_cif_path)

    if "ustruc" in entry_value:
        # 处理ustruc
        relaxed_structure = create_structure(entry_value["ustruc"][0], entry_value["ustruc"][1], entry_value["ustruc"][2])
        relaxed_cif_path = os.path.join(relaxed_dir, f"{entry_key}_弛豫后结构.cif")
		# 将gaps和energy信息写入文件
        relaxed_cif_writer = CifWriter(relaxed_structure, write_magmoms=False)
        comment = f"Energy: {entry_value.get('energy', 'N/A')}, Gap: {entry_value.get('gaps', {}).get('direct_gap', 'N/A')}"
        cif_content = str(relaxed_cif_writer)
        cif_content = f"#{comment}\n{cif_content}"
        with open(relaxed_cif_path, 'w', encoding='ascii') as f:
            f.write(cif_content)
 
