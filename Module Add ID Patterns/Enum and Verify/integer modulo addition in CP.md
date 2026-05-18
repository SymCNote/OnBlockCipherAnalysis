

# Model Modulo Addition with CP (short string)

Take the **4-bit string** as an example, $x = [x3,x2,x1,x0]$.

Using CP (minizinc), we can use **bit-wise and int-wise constraints simultaneously.**

Therefore, XOR and modulo addition can be modeled simultaneously.



## When enumerating all differentials

In this note, we only consider which pattern is possible to be propagated, without consideration of probability.

### PART I. Verifying the possible differential propagation.

Given an example


$$
\begin{cases}
\Delta x = 0x2 = [0,0,1,0]\\
\Delta y = 0xd = [1,0,1,1]
\end{cases}
$$

Method 1 (Python)

```python
dx = 0b0010
dy = 0b1011

print(f"dx={dx:04b}")
print(f"dy={dy:04b}")


seen = set()

for x0 in range(16):
    x1 = x0 ^ dx
    for y0 in range(16):
        y1 = y0 ^ dy
        z0 = (x0 + y0) & 0xF
        z1 = (x1 + y1) & 0xF
        dz = z0 ^ z1
        if dz not in seen:
            seen.add(dz)
            print(f"dz={dz:04b} ({dz})")
```

```
dx=0010
dy=1011
dz=1101 (13)
dz=1001 (9)
dz=0101 (5)
dz=1111 (15)
dz=0111 (7)
```



To transform this logic to CP:

`2fix1free.mzn`

```cypher
% the difference
array[0..3] of var 0..1: dx;
array[0..3] of var 0..1: dy;
constraint dx = array1d(0..3,[0, 0, 1, 0]);
constraint dy = array1d(0..3,[1, 0, 1, 1]);
var 0..15: DX;
var 0..15: DY;
constraint DX = sum(i in 0..3)(dx[i] * pow(2,3-i));
constraint DY = sum(i in 0..3)(dy[i] * pow(2,3-i));


% the value
array[0..3] of var 0..1: x0;
array[0..3] of var 0..1: x1;
array[0..3] of var 0..1: y0;
array[0..3] of var 0..1: y1;
var 0..15: X0;
var 0..15: X1;
var 0..15: Y0;
var 0..15: Y1;
constraint X0 = sum(i in 0..3)(x0[i] * pow(2,3-i));
constraint X1 = sum(i in 0..3)(x1[i] * pow(2,3-i));
constraint Y0 = sum(i in 0..3)(y0[i] * pow(2,3-i));
constraint Y1 = sum(i in 0..3)(y1[i] * pow(2,3-i));

% difference <--> value
constraint forall(i in 0..3)(dx[i] = (x0[i] + x1[i]) mod 2);
constraint forall(i in 0..3)(dy[i] = (y0[i] + y1[i]) mod 2);


% ---===---

% x + y = z, z here
array[0..3] of var 0..1: dz;
var 0..15: DZ;
constraint DZ = sum(i in 0..3)(dz[i] * pow(2,3-i));
array[0..3] of var 0..1: z0;
array[0..3] of var 0..1: z1;
var 0..15: Z0;
var 0..15: Z1;
constraint Z0 = sum(i in 0..3)(z0[i] * pow(2,3-i));
constraint Z1 = sum(i in 0..3)(z1[i] * pow(2,3-i));

constraint Z0 = (X0 + Y0) mod 16;
constraint Z1 = (X1 + Y1) mod 16;
constraint forall(i in 0..3)(dz[i] = (z0[i] + z1[i]) mod 2);


% ----- ===== -----
% some test
int: alldz;
constraint DZ = alldz;

output["X: " ++ show(dx) ++ show(x0) ++ show(x1) ++ "\n"];
output["Y: " ++ show(dy) ++ show(y0) ++ show(y1) ++ "\n"];
output["Z: " ++ show(dz) ++ show(z0) ++ show(z1)];
```





### $\star$ PART II. Model the theorem.

**Theorem 1 (see [13]).** The differential $(\alpha, \beta \to \gamma)$ is possible if and only if  

$$
\alpha[0] \oplus \beta[0] \oplus \gamma[0] = 0
$$

and for all $i \in [1, n-1]$, if $\alpha[i-1] = \beta[i-1] = \gamma[i-1] = t$, then

$$
\begin{cases}
\alpha[i] \oplus \beta[i] \oplus \gamma[i] = t & \text{if } \alpha[i-1] = \beta[i-1] = \gamma[i-1] = t\\
\text{No constraint} & \text{if } \alpha[i-1] = \beta[i-1] = \gamma[i-1] \text{ unsat }
\end{cases}
$$

* No carries here are necessary to model.
* Only care the bits where $dx[i-1]=dy[i-1]=dz[i-1]$.

```cypher
array[0..3] of var 0..1: dx;
array[0..3] of var 0..1: dy;
constraint dx = array1d(0..3,[0, 0, 1, 0]);
constraint dy = array1d(0..3,[1, 0, 1, 1]);
var 0..15: DX;
var 0..15: DY;
constraint DX = sum(i in 0..3)(dx[i] * pow(2,3-i));
constraint DY = sum(i in 0..3)(dy[i] * pow(2,3-i));

array[0..3] of var 0..1: dz;
var 0..15: DZ;
constraint DZ = sum(i in 0..3)(dz[i] * pow(2,3-i));


constraint dz[3] = (dx[3] + dy[3]) mod 2; % the lowest bit
constraint forall(i in 0..2)(
  if ((dx[i+1] = dy[i+1]) /\ (dx[i+1] = dz[i+1])) then ((dx[i] + dy[i] + dz[i]) mod 2 = dx[i+1]) endif
);

int: alldz;
constraint DZ = alldz;
```





### Assistant. The calling model

Call this model in Python, `all possible ADD trail.py`

```python
from minizinc import Instance, Model, Solver

# --- Choose testing model ---
# model = Model("2fix1free.mzn")
model = Model("Theorem1.mzn")

solver = Solver.lookup("cp-sat")

for dz in range(16):
    # bdz = [int(b) for b in f"{dz:04b}"]
    
    instance = Instance(solver, model)
    instance["alldz"] = dz

    result = instance.solve()
    print(dz, result.status)
```

The result for both CP models.

```
0 UNSATISFIABLE
1 UNSATISFIABLE
2 UNSATISFIABLE
3 UNSATISFIABLE
4 UNSATISFIABLE
5 SATISFIED
6 UNSATISFIABLE
7 SATISFIED
8 UNSATISFIABLE
9 SATISFIED
10 UNSATISFIABLE
11 UNSATISFIABLE
12 UNSATISFIABLE
13 SATISFIED
14 UNSATISFIABLE
15 SATISFIED
```



After trying more instances of dx, dy, and dz to test whether Theorem 1 is satisfied.





## When considering the probability.

