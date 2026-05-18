




import subprocess
from concurrent.futures import ThreadPoolExecutor

# 生成文件名：0-9 用数字，10-15 用 a-f
files = []
for i in range(16):
    if i < 10:
        suffix = str(i)
    else:
        suffix = chr(ord('a') + i - 10)  # 10→a, 11→b, ..., 15→f
    files.append(f"5id2add(CP)4inew{suffix}.py")


def run(py):
    subprocess.run(["python", py])

with ThreadPoolExecutor(max_workers=16) as exe:
    exe.map(run, files)