



from minizinc import Instance, Model, Solver

model = Model("2add.mzn")

solver = Solver.lookup("cp-sat")

with open("2addrecode.txt", "w") as f:
    line = f" dx  |  dy  |  dg  --ID-->  dh\n"
    f.write(line)
    for dx in range(16):    
        for dy in range(16):
            for dg in range(16):
                for dh in range(16):
                    instance = Instance(solver, model)
                    instance["dx41"] = [int(b) for b in f"{dx:04b}"]
                    instance["dy41"] = [int(b) for b in f"{dy:04b}"]
                    instance["dg41"] = [int(b) for b in f"{dg:04b}"]
                    instance["dh41"] = [int(b) for b in f"{dh:04b}"]

                    # if instance.solve().status.name == "UNSATISFIABLE":
                    #     print(f"dx={dx:04b},dy={dy:04b},dg={dg:04b} -x-> dh={dh:04b}")

                    if instance.solve().status.name == "UNSATISFIABLE":
                        line = f"{dx:04b} | {dy:04b} | {dg:04b} --ID--> {dh:04b}\n"
                        f.write(line)
                        print(line.strip())