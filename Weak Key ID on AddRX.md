

### Addition Modulo $2^n$

#### ! Definition 1. Add Modulo $2^n$

Let $x \boxplus y \rightarrow z$,


$$
\begin{cases} z[0] = x[0] \oplus y[0], \\ 
z[i] = x[i] \oplus y[i] \oplus c[i-1], \quad 1 \leq i \leq n-1. \end{cases}
$$


where $c=(c[n-1],...,c[1],c[0])$ is carry, and is defined recursively as:



$$
\begin{cases} c[0] = x[0] \land y[0], \\ 
c[i] = (x[i] \land y[i]) \oplus (x[i] \land c[i-1]) \oplus (y[i] \land c[i-1]), & 1 \leq i \leq n-1. \end{cases}
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

* $eq(x,y,z)$ is a 4-bit vector, and $(\Delta y \ll 1)$ in $\Delta x \oplus \Delta y \oplus \Delta z \oplus (\Delta y \ll 1)$ can be replaced by $\Delta x(or\ z)$

* All the operations in the above equation are **bit-wise** operations.

* Let $A=(\Delta x \ll 1, \Delta y \ll 1, \Delta z \ll 1)$, $B=(\Delta x \oplus \Delta y \oplus \Delta z \oplus (\Delta y \ll 1)) = 0$, then $A[i] \land B[i] = 0$ for all $i$.

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

#### ~ Property 4. Condition for $(x\boxplus y) \rightarrow 0$

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



---

New in this paper

---



#### ~ Property 5. Modulo Subtraction $0 \leftarrow (z\boxminus y)$ 

Let $x = z \oplus y$ and $x' = z' \oplus y'$, where $x, y, z, x', y', z' \in \mathbb{F}_2^n$. Suppose that $\Delta x = x \oplus x'$, $\Delta y = y \oplus y'$ and $\Delta z = z \oplus z'$. If $\Delta z = \Delta y = (0 \cdots 0\ (1_{pos=l})\ 0 \cdots 0)$, $0\le l\le n-1$, then $\Delta x = (0 \cdots 0)$ if and only if $z[l] = y[l]$ or $z'[l] = y'[l]$.



* There is a simple way to prove this property:

  consider the bits around position $l$, ($l$ and $l-1$) from $\Delta x = 0$, $\Delta y[l] = \Delta z[l] = 1$, we enumerate the possible values at position $l$ of $z,y$ , and $x$ as follows:

  | $(z[l],z'[l])$ | $(y[l],y'[l])$ | $(x[l],x'[l])$ | $borrow[l+1],borrow'[l+1]$ | $\Delta X[l]=0$ |
  | :------------: | :------------: | :------------: | :------------------------: | :-------------: |
  |     (0,1)      |     (0,1)      |     (0,0)      |           (0,0)            |        Y        |
  |     (0,1)      |     (1,0)      |     (0,1)      |           (1,0)            |        N        |
  |     (1,0)      |     (0,1)      |     (1,0)      |           (0,1)            |        N        |
  |     (1,0)      |     (1,0)      |     (0,0)      |           (0,0)            |        Y        |

	That is when $y[l] \neq z[l]$ nor $y'[l] \neq z'[l]$, on one hand, $\Delta x[l]\neq 0$; on the other hand, it must borrow 1 from the previous position, which means the previous bit has at least one non-zero difference.



### ~ Property 6. 5-bit ID

Let $z = x \oplus y$, $z' = x' \oplus y'$, $h = z \oplus g$ and $h' = z' \oplus g'$, where $x, y, z, g, h, x', y', z', g', h' \in \mathbb{F}_2^5$. Suppose that $\Delta x = x \oplus x'$, $\Delta y = y \oplus y'$, $\Delta z = z \oplus z'$, $\Delta g = g \oplus g'$ and $\Delta h = h \oplus h'$. If $\Delta z[2:1] \neq 00$, then we have  


$$
(\Delta x = 1000*, \ \Delta y = 00***, \ \Delta g = 0000* \ \to \ \Delta h = 00***).
$$


Proof (Reductio ad absurdum): $\Delta z=[z[4],z[3],z[2],z[1],z[0]]$

1. By (property 2), not property 1.

   From property 2., we have "if $\Delta x[i-1] = \Delta y[i-1] = \Delta z[i-1]$, then the differential propagation satisfies $\Delta x[i-1] = \Delta y[i-1] = \Delta z[i-1] = \Delta x[i] \oplus \Delta y[i] \oplus \Delta z[i], \quad \text{for } 1 \leq i \leq n-1.$"

   * Suppose $\Delta z[3] = 0$, then the condition $\Delta x[i-1] = \Delta y[i-1] = \Delta z[i-1]$ is satisfied for $i=4$, so there are two equations:

     * $\Delta h = \Delta z \boxplus \Delta g$

       $(\Delta z[3] = \Delta g[3] = \Delta h[3] = 0) =  (\Delta z[4] \oplus \Delta g[4] \oplus \Delta h[4]=0\oplus \Delta z[4])$, i.e., $\Delta z[4] = 0$.

     * $\Delta z = \Delta x \boxplus \Delta y$

       $(\Delta x[3] = \Delta y[3] = \Delta z[3] = 0) =  (\Delta x[4] \oplus \Delta y[4] \oplus \Delta z[4]=1\oplus \Delta z[4])$, i.e., $\Delta z[4] = 1$.

     Here we meet a contradiction. **Therefore, $\Delta z[3] = 1$.**
     
     

2. From definition 1. ($\Delta z[i] = \Delta x \oplus \Delta y \oplus \Delta carry[i]$), there are two equations for $carry_1[2]$ and $carry_2[2]$:

   * $\Delta z[i] = \Delta x[i] \oplus \Delta y[i] \oplus \Delta c_1[i - 1].$ That is $\Delta z[3] = \Delta x[3] \oplus \Delta y[3] \oplus \Delta c_1[2]$, **therefore, $\Delta c_1[2]=1$.**
   * $\Delta h[i] = \Delta z[i] \oplus \Delta g[i] \oplus \Delta c_2[i - 1].$ That is $\Delta h[3] = \Delta z[3] \oplus \Delta g[3] \oplus \Delta c_2[2]$, **therefore, $\Delta c_2[2] = 1$.**

   

3. For $\Delta z[2]$:

#### **CASE-1. $\Delta z[2] = 1$**. 

##### **CASE-1.1, for $\Delta x \boxplus \Delta y = \Delta z$.**

we have $\Delta x[2]=1$, $\Delta z[2] = \Delta x[2] \oplus \Delta y[2] \oplus \Delta c_1[ 1]\Rightarrow \Delta y[2] \oplus \Delta c_1[ 1] = 1$.

That is we have 3 conditions $\Delta z[2] = 1, \Delta x[2]=0$, $\Delta c[2] = 1$, and $\Delta y[2] \oplus \Delta c[1] = 1$.

From Definition 1. $c[i] = (x[i] \land y[i]) \oplus (x[i] \land c[i-1]) \oplus (y[i] \land c[i-1])$, we have:


$$
\Delta c_1[2] = \Delta(x[2] \land y[2]) \oplus \Delta (x[2] \land c_1[1]) \oplus \Delta (y[2] \land c_1[1])
$$

   * for $\Delta (x[2] \land y[2])$,

$$
\begin{aligned}
& \Delta (x[2] \land y[2]) \\
& =(x[2] \land y[2]) \oplus (x'[2] \land y'[2])\\
& =x[2] \land \Delta y[2],\ where\ x[2] = x'[2]\ since\ \Delta x[2] = 0\\
& = \cases{
0,\ \ \ \ \ \,if\ \Delta y[2] = 0\ (\Delta c_1[1] = 1)\\
x[2],\ if\ \Delta y[2] = 1\ (\Delta c_1[1] = 0)
}
\end{aligned}
$$

   * for $\Delta (x[2] \land c[1])$,

$$
\begin{aligned}
& \Delta (x[2] \land c_1[1])\\
& = (x[2] \land c_1[1]) \oplus (x'[2] \land c'_1[1])\\
& = x[2] \land \Delta c_1[1]\\
& = \cases{
x[2],\ \ if\ \Delta y[2] = 0\ (\Delta c_1[1] = 1)\\
0,\ \ \ \ \ \ \,if\ \Delta y[2] = 1\ (\Delta c_1[1] = 0)
}
\end{aligned}
$$

   * for $\Delta (y[2] \land c[1])$.
     
$$
\begin{aligned}
& \Delta (y[2] \land c_1[1])\\
& = (y[2] \land c_1[1]) \oplus (y'[2] \land c_1'[1])\\
& = \cases{
y[2]\land \Delta c[1] = y[2],\ \ \ \ if\ \Delta y[2] = 0\ (\Delta c_1[1] = 1)\\
c_1[1]\land \Delta y[2] = c_1[1],\ if\ \Delta y[2] = 1\ (\Delta c_1[1] = 0)
}
\end{aligned}
$$


   Finally,


$$
\begin{aligned}
& \Delta c[2] =1\\
& = \Delta(x[2] \land y[2]) \oplus \Delta (x[2] \land c_1[1]) \oplus \Delta (y[2] \land c_1[1])\\
& = \cases{
0\oplus x[2] \oplus y[2] = x[2] \oplus y[2], \ \ \,if\ \Delta y[2] = 0\ (\Delta c_1[1] = 1)\\
x[2] \oplus 0 \oplus c_1[1] = x[2] \oplus c_1[1], if\ \Delta y[2] = 1\ (\Delta c_1[1] = 0)\\
}
\end{aligned}
$$

   And from $c[i] = (x[i] \land y[i]) \oplus (x[i] \land c[i-1]) \oplus (y[i] \land c[i-1])$, we have:

$$
\begin{aligned}
& c_1[2] = (x[2] \land y[2]) \oplus (x[2] \land c_1[1]) \oplus (y[2] \land c_1[1])\\
& c_1[2] = \cases{
1\oplus c_1[1] \land (x[2] \oplus y[2]) = c_1[1],\ if\ \Delta y[2] = 0\ (\Delta c_1[1] = 1)\\
y[2] \land (x[2] \oplus c_1[1]) \oplus 1 = y[2],\ \ \,if\ \Delta y[2] = 1\ (\Delta c_1[1] = 0)\\
}
\end{aligned}
$$

   And consider $z[2]=x[2] \oplus y[2] \oplus c_1[1]$.

$$
z[2] =\cases{
c_1[1]+1 = c_1[2]+1,\ where\ x[2]\oplus y[2] = 1\ for\ \Delta y[2] = 0\ (\Delta c_1[1] = 1)\\
y[2]+1 = c_1[2]+1,\ \ \,where\ x[2]\oplus c_1[1] = 1\ for\ \Delta y[2] = 1\ (\Delta c_1[1] = 0)
}
$$

   Finally, we obtain **the combined result $z[2] = c_1[2]+1$.**



##### **CASE 1.2, for $\Delta z \boxplus \Delta g = \Delta h$.**

we have $\Delta z[2]=1$, $\Delta g[2]=0$, $\Delta c_2[2] = 1$, $\Delta h[2] = \Delta z[2] \oplus \Delta g[2] \oplus \Delta c_2[1]\Rightarrow \Delta h[2] = \Delta c_1[ 1] + 1$.

That is we have 4 conditions $\Delta z[2] = 1, \Delta g[2]=0, \Delta c_2[2]=1$, and $\Delta h[2] = \Delta c_1[ 1] + 1$.

From Definition 1. $c[i] = (x[i] \land y[i]) \oplus (x[i] \land c[i-1]) \oplus (y[i] \land c[i-1])$, we have:


$$
\Delta c_1[2] = \Delta(z[2] \land g[2]) \oplus \Delta (z[2] \land c_2[1]) \oplus \Delta (g[2] \land c_2[1])
$$

   * for $\Delta(z[2] \land g[2])$,


$$
\begin{aligned}
& \Delta(z[2] \land g[2])\\
& = (z[2] \land g[2]) \oplus (z'[2] \land g'[2]) \\
& = g[2] \land \Delta z[2],\ where\ g[2]=g'[2]\ since\ \Delta g[2] = 0\\
& = g[2],\ where\ \Delta z[2] = 1
\end{aligned}
$$


* for $\Delta (z[2] \land c_2[1])$,


$$
\begin{aligned}
& \Delta (z[2] \land c_2[1])\\
& = (z[2] \land c_2[1]) \oplus (z'[2] \land c'_2[1])\\
& = \cases{
(z[2] \land c_2[1]) \oplus (z'[2] \land c'_2[1]),\ where\ \Delta c_2[1] = 1 \\
c_2[1] \land \Delta z[2],\qquad\qquad\qquad\quad where\ \Delta c_2[1] = 0
}
\end{aligned}
$$


* for $\Delta (g[2] \land c_2[1])$,


$$
\begin{aligned}
& \Delta (g[2] \land c_2[1])\\
& = (g[2] \land c_2[1]) \oplus (g'[2] \land c'_2[1])\\
& = \cases{
g[2],\ where\ \Delta c_2[1] = 1\\
0, \ \quad where\ \Delta c_2[1] = 0
}
\end{aligned}
$$


Finally, 


$$
\begin{aligned}
& \Delta c_2[2]\\ 
& = \Delta(z[2] \land g[2]) \oplus \Delta (z[2] \land c_2[1]) \oplus \Delta (g[2] \land c_2[1])\\
& = \cases{
g[2] \oplus (z[2] \land c_2[1]) \oplus (z'[2] \land c'_2[1]) \oplus g[2] = \Delta  (z[2] \land c_2[1]),\ where\ \Delta c_2[1] = 1\\
g[2] \oplus (c_2[1]) \land \Delta z[2]) \oplus 0 = g[2] \oplus c_2[1],\qquad\qquad\qquad\qquad \ \ where\ \Delta c_2[1] = 0\\
}
\end{aligned}
$$


And from $c[i] = (z[i] \land g[i]) \oplus (z[i] \land c[i-1]) \oplus (g[i] \land c[i-1])$, we have:


$$
c_2[2] = (z[2] \land g[2]) \oplus (z[2] \land c_2[1]) \oplus (g[2] \land c_2[1])\\
$$


From the deduction above, we have:

1. for $\Delta c_2[1] = 1$, we have $\Delta c_2[2] = 1$, $c_2[1] \neq c'_2[1]$ and $z[2] \neq z'[2]$, so only $z[2] = c_2[1]=1$ will satisfy.
2. for $\Delta c_2[1] = 0$, $\Delta c_2[1] = 1 = g[2] \oplus c_2[1]$, so $g[2] \land c_2[1] = 0$.


$$
c_2[2] = \cases{
(z[2] \land g[2]) \oplus (z[2] \land c_2[1]) \oplus (g[2] \land z[2]) = z[2] \land c_2[1] \rightarrow c_2[2] = z[2] = c_2[1],\ where\ \Delta c_2[1] = 1 \\
z[2] \land (g[2] \oplus c_2[1]=1) \oplus (g[2] \land c_2[1]=0) \rightarrow c_2[2] = z[2],\qquad\qquad\qquad\quad where\ \Delta c_2[1] = 0\
}
$$


**So the combination results $c_2[2] = z[2]$.**

**For CASE 1.1 and CASE 1.2, we have $c_2[2] = z[2] = c_1[2] \oplus 1$.**



Furthermore, find contradiction using $\Delta z[4]$


$$
(\Delta x = 1000*, \ \Delta y = 00***, \ \Delta g = 0000* \ \to \ \Delta h = 00***).
$$


###### **CASE-1.1.1 $\Delta z[4] = 1$.**



$\Delta z[4] = \Delta x[4] \oplus \Delta y[4] \oplus \Delta c_1[3] \rightarrow \Delta c_1[3] = 0$

$\Delta h[4] = \Delta z[4] \oplus \Delta g[4] \oplus \Delta c_2[3] \rightarrow \Delta c_2[3] = 1$



By $x \boxplus y = z$:

$\Delta c_1[3] = \Delta (x[3] \land y[3]) \oplus \Delta (x[3] \land c_1[2]) \oplus \Delta (y[3] \land c_1[2])=0$

* $\Delta x[3] = \Delta y[3] = 0 \rightarrow \Delta (x[3] \land y[3])=0$
* $\Delta (x[3] \land c_1[2]) = x[3] \land \Delta c_1[2]$
* $\Delta (y[3] \land c_1[2]) = y[3] \land \Delta c_1[2]$

$\Delta c_1[3] = \Delta c_1[2] \land (x[3] \oplus y[3])=0$, and $\Delta c_1[2] = 1$ from above, so $x[3] \oplus y[3] = 0$.

$z[3] = x[3] \oplus y[3] \oplus c_1[2] = c_1[2]$.



By $z \boxplus g = h$:

$\Delta c_2[3] = \Delta (z[3] \land g[3]) \oplus \Delta (z[3] \land c_2[2]) \oplus \Delta (g[3] \land c_2[2])=1$

* $\Delta (z[3] \land g[3]) = g[3] \land \Delta z[3]$, where $\Delta z[3] = 1$ from above, so $ \rightarrow g[3]$
* $\Delta (z[3] \land c_2[2])$ can not be simplified
* $\Delta (g[3] \land c_2[2]) = g[3] \land \Delta c_2[2] = g[3]$

$\Delta c_2[3] = \Delta (z[3] \land c_2[2]) = 1$, so only $z[3] = c_2[2] = 1$ will satisfy.



Finally, $z[3] = c_1[2] = c_2[2]$, and we have $c_2[2] = z[2] = c_1[2] \oplus 1$ from above, **that is $c_1[2] = c_1[2] \oplus 1$, which meets a contradiction.**



###### **CASE-1.1.2 $\Delta z[4] = 0$.**



$\Delta z[4] = \Delta x[4] \oplus \Delta y[4] \oplus \Delta c_1[3] \rightarrow \Delta c_1[3] = 1$

$\Delta h[4] = \Delta z[4] \oplus \Delta g[4] \oplus \Delta c_2[3] \rightarrow \Delta c_2[3] = 0$



By $x \boxplus y = z$:

$\Delta c_1[3] = \Delta c_1[2] \land (x[3] \oplus y[3])=1$, $x[3] \oplus y[3] = 1$.

$z[3] = x[3] \oplus y[3] \oplus c_1[2] = c_1[2] \oplus 1$, and equal to $z[2]$ from above.



By $z \boxplus g = h$:

$\Delta c_2[3] = \Delta (z[3] \land g[3]) \oplus \Delta (z[3] \land c_2[2]) \oplus \Delta (g[3] \land c_2[2])=0$

$\Delta c_2[3] = \Delta (z[3] \land c_2[2]) = 0$, so only $z[3] = c_2[2] \oplus 1$ will satisfy, and equal to $z[2] \oplus 1$.



Finally, **$z[3] = z[2] = z[2] \oplus 1$, also meets a contradiction.**



Conclude, when $\Delta z[2] = 1$, here is an impossible.
