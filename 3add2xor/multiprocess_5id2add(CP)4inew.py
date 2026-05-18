



from joblib import Parallel, delayed
from minizinc import Instance, Model, Solver
import heapq

def check_combination(dx, dy, dg, du):
    model = Model("2add5inew.mzn")
    solver = Solver.lookup("cp-sat")
    
    results = []
    for dh in range(16):
        instance = Instance(solver, model)
        instance["dx41"] = [int(b) for b in f"{dx:04b}"]
        instance["dy41"] = [int(b) for b in f"{dy:04b}"]
        instance["dg41"] = [int(b) for b in f"{dg:04b}"]
        instance["du41"] = [int(b) for b in f"{du:04b}"]
        instance["dh41"] = [int(b) for b in f"{dh:04b}"]
        
        if instance.solve().status.name == "UNSATISFIABLE":
            key = (dx, dy, dg, du, dh)
            line = f"{dx:04b}* | {dy:04b}* --ID--> {dg:04b}* | {du:04b}* | {dh:04b}*\n"
            results.append((key, line))
    return results

if __name__ == "__main__":
    combinations = [
        (dx, dy, dg, du)
        for dx in range(16)
        for dy in range(16)
        for dg in range(16)
        for du in range(16)
    ]
    
    print(f"All comb: {len(combinations)}")
    
    all_results = Parallel(n_jobs=16)(
        delayed(check_combination)(dx, dy, dg, du)
        for dx, dy, dg, du in combinations
    )
    
    merged = []
    for sublist in all_results:
        merged.extend(sublist)
    
    merged.sort(key=lambda x: x[0])
    
    with open("multiprocess_2add5inew_sorted.txt", "w") as f:
        header = f"  dx  |   dy  --ID-->   dg  |   dg  |   dh\n"
        f.write(header)
        for _, line in merged:
            f.write(line)
    
    print(f"# {len(merged)}")