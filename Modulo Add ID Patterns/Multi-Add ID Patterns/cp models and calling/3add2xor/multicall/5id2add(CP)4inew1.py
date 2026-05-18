



from minizinc import Instance, Model, Solver

model = Model("2add5inew1.mzn")

solver = Solver.lookup("cp-sat")

with open("2add5inew1.txt", "w") as f:
    line = f"  dx  |   dy  --ID-->   dg  |   dg  |   dh\n"
    f.write(line)
    dx = 1
    for dy in range(16):
        for dg in range(16):
            for du in range(16):
                for dh in range(16):
                    instance = Instance(solver, model)
                    instance["dx41"] = [int(b) for b in f"{dx:04b}"]
                    instance["dy41"] = [int(b) for b in f"{dy:04b}"]
                    instance["dg41"] = [int(b) for b in f"{dg:04b}"]
                    instance["du41"] = [int(b) for b in f"{du:04b}"]
                    instance["dh41"] = [int(b) for b in f"{dh:04b}"]

                    # if instance.solve().status.name == "UNSATISFIABLE":
                    #     print(f"dx={dx:04b},dy={dy:04b},dg={dg:04b} -x-> dh={dh:04b}")

                    if instance.solve().status.name == "UNSATISFIABLE":
                        line = f"{dx:04b}* | {dy:04b}* --ID--> {dg:04b}* | {du:04b}* | {dh:04b}*\n"
                        f.write(line)
                        print(line.strip())