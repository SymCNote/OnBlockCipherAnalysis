

### Addition Modulo $2^n$

#### ~ Definition 1 Add Modulo $2^n$

Let $x \boxplus y \rightarrow z$,


$$
\begin{cases} z[0] = x[0] \oplus y[0], \\ z[i] = x[i] \oplus y[i] \oplus c[i-1], \quad 1 \leq i \leq n-1. \end{cases}
$$


where $c=(c[n-1],...,c[1],c[0])$ is carry, and is defined recursively as:



$$
\begin{cases} c[0] = x[0] \land y[0], \\ c[i] = (x[i] \land y[i]) \oplus (x[i] \land c[i-1]) \oplus (y[i] \land c[i-1]), & 1 \leq i \leq n-1. \end{cases}
$$


**To check “non-linearity" operation "Add":**

```python
dx, dy = 2, 8
n = 4
mod = 1 << n

results = {}

for x in range(mod):
    for y in range(mod):
        x_prime = x ^ dx
        y_prime = y ^ dy
        z = (x + y) % mod
        z_prime = (x_prime + y_prime) % mod
        dz = z_prime ^ z
        
        if dz not in results:
            results[dz] = []
        results[dz].append((x, y))

for dz in sorted(results.keys()):
    print(f"dz={dz:04b}({dz:2d}), count={len(results[dz])}:")

# output:
# dz=0110( 6), count=64:
# dz=1010(10), count=128:
# dz=1110(14), count=64:
```



#### ~ Property 1. Sat AddRX Prop on Word

Let $\Delta x$, $\Delta y$, and $\Delta z$ be fixed **n-bit XOR differences**. The differential ($\Delta x \boxplus \Delta y \rightarrow \Delta z$) passing modular addition <u>is possible</u> if and only if: 
$$
(\Delta x \ll 1, \Delta y \ll 1, \Delta z \ll 1) \land (\Delta x \oplus \Delta y \oplus \Delta z \oplus (\Delta y \ll 1)) = 0,\\
\text{where } eq(x,y,z)=(\neg x \oplus y) \land (\neg x \oplus z))\ \text{is equal to 1 iff. } (x=y=z)
$$

* $eq(x,y,z)$ means $x=y=z$, and $(\Delta y \ll 1)$ in $\Delta x \oplus \Delta y \oplus \Delta z \oplus (\Delta y \ll 1)$ can be replaced by $\Delta x(or\ z)$

* All the operations in the above equation are **bit-wise** operations.

* **Non-linearity**: For the fixed input difference, **many** output differences will satisfy.

To model property 1:

```cypher
int: n = 4;
int: nMod = pow(2,n);

% bin to int
var 0..2^4-1: dXint = sum(i in 0..n-1)(dXbin[3-i]*(2^i));
var 0..2^4-1: dYint = sum(i in 0..n-1)(dYbin[3-i]*(2^i));
var 0..2^4-1: dZint = sum(i in 0..n-1)(dZbin[3-i]*(2^i));

array[0..n-1] of var 0..1: dXbin;
array[0..n-1] of var 0..1: dYbin;
array[0..n-1] of var 0..1: dZbin;

% shift on bit
array[0..n-1] of var 0..1: dXbin1 = array1d(0..n-1, [dXbin[i] | i in 1..n-1] ++ [0]);
array[0..n-1] of var 0..1: dYbin1 = array1d(0..n-1, [dYbin[i] | i in 1..n-1] ++ [0]);
array[0..n-1] of var 0..1: dZbin1 = array1d(0..n-1, [dZbin[i] | i in 1..n-1] ++ [0]);

% eq
array[0..n-1] of var 0..1: eqXYZ;
constraint forall(i in 0..n-1)(eqXYZ[i] = eq3(dXbin1[i],dYbin1[i],dZbin1[i]));

% add
array[0..n-1] of var 0..1: addXYZ;
constraint forall(i in 0..n-1)(addXYZ[i] = xor4(dXbin[i], dYbin[i], dZbin[i], dYbin1[i]));

% and 2 constraints
constraint forall(i in 0..n-1)(eqXYZ[i] + addXYZ[i] < 2);


% ------------
constraint dXint = 2;
constraint dYint = 8;
constraint dZint = 10; 


% ============
predicate eq3(var int: xb, var int: yb, var int: zb) = 
  (xb=yb) /\ (xb=zb)
;

predicate xor4(var int: a, var int: b, var int: c, var int: d) = 
  (a+b+c+d) mod 2 = 1
;
```



#### ~ Property 2. Sat AddRX Prop on Bit

Let $\Delta x$, $\Delta y$, and $\Delta z$ be fixed $n$-bit XOR differences. The differential $\Delta x \boxplus \Delta y \rightarrow \Delta z$ passing modular addition is possible if and only if 
$$
\Delta x[0] \oplus \Delta y[0] \oplus \Delta z[0] = 0
$$

and, if $(\Delta x[i-1] = \Delta y[i-1] = \Delta z[i-1])$, then this bit must satisfy:

$$
\Delta x[i-1] = \Delta y[i-1] = \Delta z[i-1] = \Delta x[i] \oplus \Delta y[i] \oplus \Delta z[i], \quad \text{for } 1 \leq i \leq n-1.
$$

* The last position must satisfies $\Delta x[0]\oplus \Delta y[0] = \Delta z[0]$.

* This property shows explicitly **where the carry impacts the previous bits** $z[i]$ **when the current-position bits satisfy** $\Delta x[i-1]=\Delta y[i-1]=\Delta z[i-1]$.

  * $\Delta x[i-1]=\Delta y[i-1]=\Delta z[i-1]=0$, then $\Delta x[i-1]\oplus \Delta y[i-1]\oplus \Delta z[i-1]=0$, where follows this table:

    | $x[i]$ | $y[i]$ | $z[i]$ | carry |
    | :----: | :----: | :----: | :---: |
    |   0    |   0    |   0    |   0   |
    |   0    |   1    |   1    |   0   |
    |   1    |   0    |   1    |   0   |
    |   1    |   1    |   0    |   0   |

    That means **there is no carry** form position $[i−1]$ that impacts the modulo addition on position $[i]$.

  * $\Delta x[i-1]=\Delta y[i-1]=\Delta z[i-1]=1$, then $\Delta x[i-1]\oplus \Delta y[i-1]\oplus \Delta z[i-1]=1$, where follows this table:

    | $x[i]$ | $y[i]$ | $z[i]$ | carry |
    | :----: | :----: | :----: | :---: |
    |   0    |   0    |   1    |   1   |
    |   0    |   1    |   0    |   1   |
    |   1    |   0    |   1    |   1   |
    |   1    |   1    |   1    |   1   |

    That means **there is a carry** form position $[i−1]$ that impacts the modulo addition on position $[i]$.

* There is no constraint on the position where $\Delta x[i-1]=\Delta y[i-1]=\Delta z[i-1]$ is not satisfied.

```cypher
int: n = 4;
int: nMod = pow(2,n);

% bin to int
var 0..2^4-1: dXint = sum(i in 0..n-1)(dXbin[i]*(2^i));
var 0..2^4-1: dYint = sum(i in 0..n-1)(dYbin[i]*(2^i));
var 0..2^4-1: dZint = sum(i in 0..n-1)(dZbin[i]*(2^i));

array[0..n-1] of var 0..1: dXbin;
array[0..n-1] of var 0..1: dYbin;
array[0..n-1] of var 0..1: dZbin;

constraint (dXbin[0] + dYbin[0] + dZbin[0]) mod 2 = 0;

array[1..n-1] of var -1..1: eqXYZ; % no need the lowest position
constraint forall(i in 1..n-1)(
  eqXYZ[i] = if (dXbin[i-1] = dYbin[i-1]) /\ (dXbin[i-1] = dZbin[i-1]) then dXbin[i-1] else -1 endif
);
constraint forall(i in 1..n-1)(
  if eqXYZ[i] >= 0 then (dXbin[i] + dYbin[i] + dZbin[i]) mod 2 = 0 endif
);

constraint dXint = 2 /\ dYint = 8;
constraint dZint = 6;
```



#### ! Connect Property 1 and 2 (explanation of Property 1)

To understand property 1 in relation to property 2.

$$
\begin{aligned}
eq(\Delta x \ll 1, \Delta y \ll 1, \Delta z \ll 1) \land (\Delta x \oplus \Delta y \oplus \Delta z \oplus (\Delta y \ll 1)) = 0,\qquad & (property. 1)\\
\Delta x[i-1] = \Delta y[i-1] = \Delta z[i-1] = \Delta x[i] \oplus \Delta y[i] \oplus \Delta z[i].\quad \text{for } 1 \leq i \leq n-1. \qquad & (property. 2)
\end{aligned}
$$


For a string $x$, $x \ll 1$ means picking up positions $x[0..(n-1)]$. 

$$
eq(\Delta x \ll 1, \Delta y \ll 1, \Delta z \ll 1) \Leftrightarrow x[i-1]=y[i-1]=z[i-1],\quad 1<i<n-1
$$

Then the tables of property 2 can be followed.

Let $EQ = eq(\Delta x \ll 1, \Delta y \ll 1, \Delta z \ll 1)$, so $EQ\in\lbrace0,1\rbrace$.

If $EQ=0$, no carry impacts the previous one bit. To satisfy $0$-result, $(\Delta x \oplus \Delta y \oplus \Delta z \oplus (\Delta y \ll 1))$ is free. 

If $EQ=1$, one carry impacts the previous one bit. To satisfy $0$-result, $(\Delta x \oplus \Delta y \oplus \Delta z \oplus (\Delta y \ll 1))$ must be 0. $(\Delta x \oplus \Delta y \oplus \Delta z)$ is the same as property 2, and $(\Delta y \ll 1)$, accurately, $(\Delta x/y/z \ll 1))$ denotes the same as $EQ$.

Therefore, properties 1 and 2 are equal.



#### ~ Property 3. Sat AddRX Prop on A Lower Set.

Let $\Delta x$, $\Delta y$, and $\Delta z$ be fixed $n$-bit XOR differences. Suppose that the differential $(\Delta x \boxplus \Delta y \to \Delta z)$ passing modular addition is possible. If $l_1 = \min\lbrace i \mid \Delta x[i] = 1,\ 0 \leq i \leq n\rbrace$, $l_2 = \min\lbrace i \mid \Delta y[i] = 1,\ 0 \leq i \leq n\rbrace$ and $l = \min\lbrace l_1, l_2\rbrace$, we have:

1. If $l_1 = l_2 = l$, then $\Delta z[i] = 0$ for $0 \leq i \leq l$.

2. If $l_1 \neq l_2$, then $\Delta z[l] = 1$, $\Delta z[i] = 0$ for $0 \leq i \leq l-1$.



* Focus on the lower $l$ bits of the difference on $x,y,z$.
  * For 1. the carry is propagated from the lower position to the higher one, so *the impact of carry will not appear until the first common 1-differential position*.
  * For 2. ($\Delta z[i] = 0$ for $0 \leq i \leq l-1$) is the same as 1. And for the first $(1,0)/(0,1)$ pair of $(\Delta x[l],\Delta y[l])$, there is no carry impact on $\Delta z[l]$, so $\Delta z[l]=\Delta x[l] \oplus \Delta y[l] = 1$.

#### ~ Property 4. Condition for $(0,0) \rightarrow 0$

Let $\Delta x$, $\Delta y$, and $\Delta z$ be fixed $n$-bit XOR differences, where $\Delta x = x \oplus x'$, $\Delta y = y \oplus y'$ and $\Delta z = z \oplus z'$. Suppose the differential $(\Delta x \boxplus \Delta y \to \Delta z)$ passing modular addition is possible. If $\Delta x = \Delta y = (0 \cdots 0 ({1}_{pos=l}) 0 \cdots 0)$, then $\Delta z = (0 \cdots 0)$ if and only if $x[l] \neq y[l]$ or $x'[l] \neq y'[l]$.

* The point is considering when the carry appears in the **value** (instead of the difference).

  * Let $x[l]$ be the bit position of value $x$, so we have the following table:

    | $(x[l],x'[l])$ | $(y[l],y'[l])$ | $(z[l],z'[l])$ | $\Delta z[l]$ | $(z[l+1],z'[l+1])$ | $\Delta z[l+1]$ |
    | :------------: | :------------: | :------------: | :-----------: | :----------------: | :-------------: |
    |     (0,1)      |     (0,1)      |     (0,0)      |       0       |       (0,1)        |        1        |
    |     (0,1)      |     (1,0)      |     (1,1)      |       0       |       (0,0)        |        0        |
    |     (1,0)      |     (0,1)      |     (1,1)      |       0       |       (0,0)        |        0        |
    |     (1,0)      |     (1,0)      |     (0,0)      |       0       |       (1,0)        |        1        |

    That is, when $x[l] = y[l]$ or $x'[l] = y'[l]$, there is a carry on the higher one bit of $z[l]$ or $z'[l]$, thereby bringing $1$ to $\Delta z[l+1]$.



