



from minizinc import Instance, Model, Solver


# model = Model("2fix1free.mzn")
model = Model("Theorem1.mzn")

solver = Solver.lookup("cp-sat")

for dz in range(16):
    # bdz = [int(b) for b in f"{dz:04b}"]
    
    instance = Instance(solver, model)
    instance["alldz"] = dz

    result = instance.solve()
    print(dz, result.status)
