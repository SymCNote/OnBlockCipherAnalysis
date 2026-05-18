# import warnings
# from minizinc import Instance, Model, Solver
# from itertools import product
# from tqdm import tqdm

# warnings.filterwarnings("ignore", module="minizinc")

# model = Model("2add.mzn")
# solver = Solver.lookup("cp-sat")

# binary_values = [[int(bit) for bit in format(i, '04b')] for i in range(16)]

# total = 0
# unsat_count = 0
# unsat_solutions = []

# for dx_bits, dy_bits, dg_bits, dh_bits in tqdm(product(binary_values, repeat=4)):
#     total += 1

#     instance = Instance(solver, model)
    
#     instance["dx14"] = dx_bits
#     instance["dy14"] = dy_bits
#     instance["dg14"] = dg_bits
#     instance["dh14"] = dh_bits
    
#     result = instance.solve()
    
#     if result.status == "UNSATISFIABLE":
#         unsat_count += 1
#         unsat_solutions.append({
#             'dx': dx_bits.copy(),
#             'dy': dy_bits.copy(),
#             'dg': dg_bits.copy(),
#             'dh': dh_bits.copy()
#         })

# print(f"\n===== 完成 =====")
# print(f"总共测试: {total} 个组合")
# print(f"UNSAT 解的数量: {unsat_count}")
# print(unsat_solutions)



import warnings
from minizinc import Instance, Model, Solver
from itertools import product
from tqdm import tqdm

warnings.filterwarnings("ignore", module="minizinc")

model = Model("2add.mzn")
solver = Solver.lookup("cp-sat")

binary_values = [[int(bit) for bit in format(i, '04b')] for i in range(16)]

# 固定 dx, dy, dg 为特定值
fixed_dx = [0,0,0,0]  # 可以改成你想要的任何值
fixed_dy = [0,0,0,0]  # 可以改成你想要的任何值
fixed_dg = [0,0,0,0]  # 可以改成你想要的任何值

total = 0
unsat_count = 0
unsat_solutions = []

print(f"固定 dx={fixed_dx}, dy={fixed_dy}, dg={fixed_dg}")
print("遍历 dh (16种可能)...")

for dh_bits in tqdm(binary_values, total=16):
    total += 1
    print(fixed_dx,fixed_dy,fixed_dg,dh_bits[::-1], end = '')
    instance = Instance(solver, model)
    
    instance["dx14"] = fixed_dx
    instance["dy14"] = fixed_dy
    instance["dg14"] = fixed_dg
    instance["dh14"] = dh_bits[::-1]
    
    result = instance.solve()
    
    print(result.status, end = '')

    if result.status == "UNSATISFIABLE":
        unsat_count += 1
        unsat_solutions.append({
            'dx': fixed_dx.copy(),
            'dy': fixed_dy.copy(),
            'dg': fixed_dg.copy(),
            'dh': dh_bits.copy()
        })

# print(f"\n===== 完成 =====")
# print(f"总共测试: {total} 个组合")
# print(f"UNSAT 解的数量: {unsat_count}")

# 保存结果
if unsat_solutions:
    with open("unsat_fixed_xyz.txt", "w", encoding="utf-8") as f:
        f.write(f"固定 dx={fixed_dx}, dy={fixed_dy}, dg={fixed_dg}\n")
        f.write(f"UNSAT 解的数量: {unsat_count}\n")
        f.write("=" * 60 + "\n\n")
        
        for idx, sol in enumerate(unsat_solutions, 1):
            f.write(f"UNSAT #{idx}:\n")
            f.write(f"  dh = {sol['dh']}\n")
            dh_int = int(''.join(map(str, sol['dh'])), 2)
            f.write(f"  dh_int = {dh_int}\n")
            f.write("-" * 40 + "\n")
    
    print(f"结果已保存到 unsat_fixed_xyz.txt")
else:
    print("没有找到 UNSAT 解")