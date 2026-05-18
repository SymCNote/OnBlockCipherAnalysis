# Model 2,3 Modulo Additions

> ref: Finding Impossible Differentials in ARX Ciphers  under Weak Keys

We refined the results reported in this paper and identified additional ID patterns by considering the "right branch."



The basic idea is to detect contradictions that appear not only at the output but also in the middle (which is automatically detected by the given model). The model provided can only be applied to *short* patterns, say no larger than 6 bits (The efficiency requires a more accurate evaluation).



## PART I. for all 2 continuous modulo additions

### Verification ref (recode)

verified specific patterns with Python: `2add_alldh.py`

```python
dx4 = 0b0000
dy4 = 0b0000
dg4 = 0b0001

seen_dh = set()

for dx_bit in (0, 1):   
    dx = (dx4 << 1) | dx_bit
    for dy_bit in (0, 1):
        dy = (dy4 << 1) | dy_bit
        for dg_bit in (0, 1):    
            dg = (dg4 << 1) | dg_bit
            
            for x0 in range(32):
                x1 = x0 ^ dx
                for y0 in range(32):
                    y1 = y0 ^ dy
                    for g0 in range(32):
                        g1 = g0 ^ dg

                        z0 = (x0 + y0) & 0x1F 
                        z1 = (x1 + y1) & 0x1F
                        
                        h0 = (z0 + g0) & 0x1F
                        h1 = (z1 + g1) & 0x1F

                        dz = z0 ^ z1
                        dh = h0 ^ h1
                        
                        seen_dh.add(dh)

for dh in sorted(seen_dh):
    print(f"{dh:02d}: {dh:05b}", end = "| ")
print("\n#h:", len(seen_dh))
```



For the special pattern $dx = [0,0,0,0], dy = [0,0,0,0], dz = [0,0,0,1]$

For all $dh$, the ID results given in ref:

```
current IDC-pattern (Δx, Δy, Δg → Δh): (0000*, 0000*, 0001* → 0100*)
current IDC-pattern (Δx, Δy, Δg → Δh): (0000*, 0000*, 0001* → 0101*)
current IDC-pattern (Δx, Δy, Δg → Δh): (0000*, 0000*, 0001* → 1000*)
current IDC-pattern (Δx, Δy, Δg → Δh): (0000*, 0000*, 0001* → 1001*)
current IDC-pattern (Δx, Δy, Δg → Δh): (0000*, 0000*, 0001* → 1010*)
current IDC-pattern (Δx, Δy, Δg → Δh): (0000*, 0000*, 0001* → 1100*)
current IDC-pattern (Δx, Δy, Δg → Δh): (0000*, 0000*, 0001* → 1101*)
```

All the possible $dh$ we found:

```
00: 00000
01: 00001
02: 00010
03: 00011
04: 00100
05: 00101
06: 00110
07: 00111
12: 01100
13: 01101
14: 01110
15: 01111
28: 11100
29: 11101
30: 11110
31: 11111

#dh: 16
```

So we found 8 ID patterns without constraint on the last bit.

That shows `(24,25) = 1011*` is missed in the ref.



### Our method for finding ID

#### CASE 1. 2 Modulo Additions

<img width="250" height="400" alt="2addnew (1)" src="https://github.com/user-attachments/assets/048dd73f-c5ff-4685-9847-10c2f61d65d2" />



**Free variables: $\Delta x$, $\Delta y$, $\Delta g$, $\Delta h$**. ($\Delta y$ is independent of $\Delta g$)



##### The called CP model: `2add3inew.mzn`

```cypher
% differential x
array[0..3] of 0..1: dx41;  % <-- give value X[4,3,2,1]
var 0..1: dx0;
array[0..4] of var 0..1: dx;
constraint dx[4] = dx0 /\ forall(i in 0..3)(dx[i] = dx41[i]);
% value x
array[0..4] of var 0..1: x0;
array[0..4] of var 0..1: x1;
constraint forall(i in 0..4)(dx[i] = (x0[i] + x1[i]) mod 2);
% to int x
var 0..31: ix0 = sum(i in 0..4)(x0[i] * pow(2,4-i));
var 0..31: ix1 = sum(i in 0..4)(x1[i] * pow(2,4-i));

% differential y
array[0..3] of 0..1: dy41;  % <-- give value Y[4,3,2,1]
var 0..1: dy0;
array[0..4] of var 0..1: dy;
constraint dy[4] = dy0 /\ forall(i in 0..3)(dy[i] = dy41[i]);
% value y
array[0..4] of var 0..1: y0;
array[0..4] of var 0..1: y1;
constraint forall(i in 0..4)(dy[i] = (y0[i] + y1[i]) mod 2);
var 0..31: iy0 = sum(i in 0..4)(y0[i] * pow(2,4-i));
var 0..31: iy1 = sum(i in 0..4)(y1[i] * pow(2,4-i));

% --- differential z ---
array[0..4] of var 0..1: dz;
array[0..4] of var 0..1: z0;
array[0..4] of var 0..1: z1;
constraint forall(i in 0..4)(dz[i] = (z0[i] + z1[i]) mod 2);
var 0..31: iz0 = sum(i in 0..4)(z0[i] * pow(2,4-i));
var 0..31: iz1 = sum(i in 0..4)(z1[i] * pow(2,4-i));

% differential g
array[0..3] of 0..1: dg41;  % <-- give value G[4,3,2,1]
var 0..1: dg0;
array[0..4] of var 0..1: dg;
constraint dg[4] = dg0 /\ forall(i in 0..3)(dg[i] = dg41[i]);
% value g
array[0..4] of var 0..1: g0;
array[0..4] of var 0..1: g1;
constraint forall(i in 0..4)(dg[i] = (g0[i] + g1[i]) mod 2);
var 0..31: ig0 = sum(i in 0..4)(g0[i] * pow(2,4-i));
var 0..31: ig1 = sum(i in 0..4)(g1[i] * pow(2,4-i));

% differential h
array[0..3] of 0..1: dh41;  % <-- give value H[4,3,2,1]
var 0..1: dh0;
array[0..4] of var 0..1: dh;
constraint dh[4] = dh0 /\ forall(i in 0..3)(dh[i] = dh41[i]);
% value h
array[0..4] of var 0..1: h0;
array[0..4] of var 0..1: h1;
constraint forall(i in 0..4)(dh[i] = (h0[i] + h1[i]) mod 2);
var 0..31: ih0 = sum(i in 0..4)(h0[i] * pow(2,4-i));
var 0..31: ih1 = sum(i in 0..4)(h1[i] * pow(2,4-i));


% propagation x add y = z
constraint iz0 = (ix0 + iy0) mod 32;
constraint iz1 = (ix1 + iy1) mod 32;

% propagation z add g = h
constraint ih0 = (iz0 + ig0) mod 32;
constraint ih1 = (iz1 + ig1) mod 32;



% output["dx: " ++ show(dx) ++ " | x0: " ++ show(x0) ++ " (" ++ show(ix0) ++ ")" ++ " | x0: " ++ show(x1) ++ " (" ++ show(ix1) ++ ")" ++ "\n"];
% output["dy: " ++ show(dy) ++ " | y0: " ++ show(y0) ++ " (" ++ show(iy0) ++ ")" ++ " | y0: " ++ show(y1) ++ " (" ++ show(iy1) ++ ")" ++ "\n"];
% output["dz: " ++ show(dz) ++ " | z0: " ++ show(z0) ++ " (" ++ show(iz0) ++ ")" ++ " | z0: " ++ show(z1) ++ " (" ++ show(iz1) ++ ")" ++ "\n"];
% output["dg: " ++ show(dg) ++ " | g0: " ++ show(g0) ++ " (" ++ show(ig0) ++ ")" ++ " | g0: " ++ show(g1) ++ " (" ++ show(ig1) ++ ")" ++ "\n"];
% output["dh: " ++ show(dh) ++ " | h0: " ++ show(h0) ++ " (" ++ show(ih0) ++ ")" ++ " | h0: " ++ show(h1) ++ " (" ++ show(ih1) ++ ")" ++ "\n"];
```



##### The calling Python: `5id2add (CP)3inew.py`

```python
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
```



##### Results

* All IDs we found:

  * Ours **6080** 5-bit patterns `2add3inew.txt`

  * ref's **6016** 5-bit patterns `5idpatterns.txt`


* Time for all solving:

  * Ours 4.28 hours
  
  * ref's 6 hours
  




#### CASE 2. 2 Modulo Additions and 1 XOR



<img width="250" height="400" alt="2addnew (2)" src="https://github.com/user-attachments/assets/01a43f2a-994d-44aa-9fda-ab37ec62bc2f" />

**Free variables: $\Delta x$, $\Delta y$, $\Delta h$**. ($\Delta g$ is based on $\Delta y$)
**Rotation is omitted.**



##### The called CP model `2add4inew.mzn`.

```cypher
% differential x
array[0..3] of 0..1: dx41;  % <-- give value X[4,3,2,1]
var 0..1: dx0;
array[0..4] of var 0..1: dx;
constraint dx[4] = dx0 /\ forall(i in 0..3)(dx[i] = dx41[i]);
% value x
array[0..4] of var 0..1: x0;
array[0..4] of var 0..1: x1;
constraint forall(i in 0..4)(dx[i] = (x0[i] + x1[i]) mod 2);
% to int x
var 0..31: ix0 = sum(i in 0..4)(x0[i] * pow(2,4-i));
var 0..31: ix1 = sum(i in 0..4)(x1[i] * pow(2,4-i));

% differential y
array[0..3] of 0..1: dy41;  % <-- give value Y[4,3,2,1]
var 0..1: dy0;
array[0..4] of var 0..1: dy;
constraint dy[4] = dy0 /\ forall(i in 0..3)(dy[i] = dy41[i]);
% value y
array[0..4] of var 0..1: y0;
array[0..4] of var 0..1: y1;
constraint forall(i in 0..4)(dy[i] = (y0[i] + y1[i]) mod 2);
var 0..31: iy0 = sum(i in 0..4)(y0[i] * pow(2,4-i));
var 0..31: iy1 = sum(i in 0..4)(y1[i] * pow(2,4-i));

% --- value z ---
array[0..4] of var 0..1: z0;
array[0..4] of var 0..1: z1;
var 0..31: iz0 = sum(i in 0..4)(z0[i] * pow(2,4-i));
var 0..31: iz1 = sum(i in 0..4)(z1[i] * pow(2,4-i));

% differential g
array[0..3] of 0..1: dg41;  % <-- give value Y[4,3,2,1]
var 0..1: dg0;
array[0..4] of var 0..1: dg;
constraint dg[4] = dg0 /\ forall(i in 0..3)(dg[i] = dg41[i]);
% value g
array[0..4] of var 0..1: g0;
array[0..4] of var 0..1: g1;
constraint forall(i in 0..4)(dg[i] = (g0[i] + g1[i]) mod 2);
var 0..31: ig0 = sum(i in 0..4)(g0[i] * pow(2,4-i));
var 0..31: ig1 = sum(i in 0..4)(g1[i] * pow(2,4-i));

% differential h
array[0..3] of 0..1: dh41;  % <-- give value H[4,3,2,1]
var 0..1: dh0;
array[0..4] of var 0..1: dh;
constraint dh[4] = dh0 /\ forall(i in 0..3)(dh[i] = dh41[i]);
% value h
array[0..4] of var 0..1: h0;
array[0..4] of var 0..1: h1;
constraint forall(i in 0..4)(dh[i] = (h0[i] + h1[i]) mod 2);
var 0..31: ih0 = sum(i in 0..4)(h0[i] * pow(2,4-i));
var 0..31: ih1 = sum(i in 0..4)(h1[i] * pow(2,4-i));


% propagation x add y = z
constraint iz0 = (ix0 + iy0) mod 32;
constraint iz1 = (ix1 + iy1) mod 32;

% g = z xor y
constraint forall(i in 0..4)(g0[i] = (z0[i] + y0[i]) mod 2);
constraint forall(i in 0..4)(g1[i] = (z1[i] + y1[i]) mod 2);

% propagation z add g = h
constraint ih0 = (iz0 + ig0) mod 32;
constraint ih1 = (iz1 + ig1) mod 32;



% output["dx: " ++ show(dx) ++ " | x0: " ++ show(x0) ++ " | x1: " ++ show(x1) ++ "\n"];
% output["dy: " ++ show(dy) ++ " | y0: " ++ show(y0) ++ " | y1: " ++ show(y1) ++ "\n"];
% % output["dz: " ++ show(dz) ++ " | z0: " ++ show(z0) ++ " | z1: " ++ show(z1) ++ "\n"];
% output["dg: " ++ show(dg) ++ " | g0: " ++ show(g0) ++ " | g1: " ++ show(g1) ++ "\n"];
% output["dh: " ++ show(dh) ++ " | h0: " ++ show(h0) ++ " | h1: " ++ show(h1) ++ "\n"];
```



##### The calling Python: `5id2add (CP)4inew.py`

```
from minizinc import Instance, Model, Solver

model = Model("2add4inew.mzn")

solver = Solver.lookup("cp-sat")

with open("2add4inew.txt", "w") as f:
    line = f"  dx  |   dy  --ID-->   dg  |   dh\n"
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
                        line = f"{dx:04b}* | {dy:04b}* --ID--> {dg:04b}* | {dh:04b}*\n"
                        f.write(line)
                        print(line.strip())
```



##### Results

We found **40940/65536 ~ 62%** ID trails `2add4inew.txt`.





## PART II. for all 3 continuous modulo additions



<img width="200" height="500" alt="2addnew (5)" src="https://github.com/user-attachments/assets/6480bdae-8771-439f-b253-494da15ae024" />

**Free variables: $\Delta x$, $\Delta y$, $\Delta h$**. ($\Delta g$ is based on $\Delta y$, and $\Delta u$ is based on $\Delta g$)
**Rotation is omitted.**

##### The called CP model: `2add3inew.mzn`

##### The calling Python: `5id2add (CP)4inew.py`

##### Results

We found **977415/1048576 ~ 93%**  ID patterns in `3add5inNEW.txt`

