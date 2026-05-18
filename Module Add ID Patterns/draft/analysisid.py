import re
from minizinc import Instance, Model, Solver

model = Model("2add.mzn")
solver = Solver.lookup("cp-sat")

pattern = re.compile(
    r"\((\d{4})\*,\s*(\d{4})\*,\s*(\d{4})\*\s*→\s*(\d{4})\*"
)

with open("5idpatterns.txt", "r", encoding="utf-8") as f:
    for line in f:
        match = pattern.search(line)
        if not match:
            continue

        dx, dy, dg, dh = match.groups()
        dx = dx.replace("*", "")
        dy = dy.replace("*", "")
        dg = dg.replace("*", "")
        dh = dh.replace("*", "")
        print(dx)
        input()

        instance = Instance(solver, model)

        instance["dx14"] = [int(b) for b in dx]
        instance["dy14"] = [int(b) for b in dy]
        instance["dg14"] = [int(b) for b in dg]
        instance["dh14"] = [int(b) for b in dh]

        result = instance.solve()
        print("Status:", result.status)