# Quasidifferential cryptanalysis

> From [Differential Cryptanalysis in the Fixed-Key Model](https://eprint.iacr.org/2022/837)



# Traditional

## 差分分析的 强假设

对于一个差分转移: $F:\mathbb{F}_2^n \rightarrow \mathbb{F_2^m}$, 有输入, 输出差分 $(a,b)$, 则:


$$
F(x)+F(x+a)=b
$$

固定 $a,b$, 对满足上式的 $x$, 将 $(a,b)$ 记作正确的差分对. 差分分布表定义:


$$
DDT_{a,b}^F = \left|\left\{x \in \mathbb{F}_2^n \mid F(x) + F(x+a) = b\right\}\right| = 2^n \Pr[F(x) + F(x+a) = b]
$$

这里的假设是 **$x$ 是均匀随机**的, 差分概率 $p\gg 2^{-n}$, 对应数据复杂度 $\O(1/p)$.

正是因为上面说的这种均匀随机假设, 多轮差分特征可以认为**轮间独立**, 记作:


$$
\begin{aligned}
& \Pr[F(x) + F(x + a_1) = a_{r+1}] \\
& = \sum_{a_2, \dots, a_r} \Pr[\Lambda_{i=1}^r F_i(x_i) + F_i(x_i + a_i) = a_{i+1}] \\
& = \prod_{i=1}^T \Pr \left[ F_i(z_i) + F_i(z_i + a_i) = a_{i+1} \right]
\end{aligned}
$$

也就是可以启发式独立, 用 DDT 算: (记为 *强假设差分概率公式*)


$$
\text{DDT}_{a_1, a_{r+1}}^{F} / 2^n = \sum_{a_2, \dots, a_r} \prod_{i=1}^r \text{DDT}_{a_i, a_{i+1}}^{F_i} / 2^n
$$

该公式计算的结果是近似的, 有一个极端反例, $F=F_2\circ F_1$, 其中 $F_2=F_1^{-1}$, 解释如下:

* 设差分转移 $a\stackrel{F_1}{\rightarrow} b$ 概率为 $p$, 则 $b\stackrel{F_1^{-1}}{\rightarrow} a$ 概率为 $p$, 依照独立性假设, 计算得 $a\stackrel{F}{\rightarrow} a$ 概率为 $p^2$. $p<1$.

* 但实际情况是 $a\stackrel{F_1^{-1}\circ F_1}{\longrightarrow} a$ 概率为 1.



## 线性分析

something





有对函数的向量空间 $\mathbb{R[F}_2^n]$, 其中函数都是在 $\mathbb{F}_2^n$ 上的. 有函数 $\delta_x(y)$, 满足


$$
\delta_x(y) = \cases{1\qquad x=y\\0\qquad x\neq y}
$$


对内积 $<f,g> = \sum_{x\in \mathbb{F}_2^n}f(x)g(x)$, $\delta_x$ 构成了其**标准正交基** ($<\delta_x,\delta_y>$是 $2^n$ 长的单位向量)



==由 $\mathbb{F}_2^n$ 的<u>群特征</u>组成 $\mathbb{R[F}_2^n]$ 的一组基, 使*二元域加法与非零乘法群同态*, 任何这样的同态都具有 $\chi_u(x) = (−1)^{u^Tx}$ 的形式，其中 $u\in F_2^n$. 特征 $\chi_u$ 构成 $\mathbb{R[F}_2^n]$ 的正交基, 特别的 $<\chi_u,\chi_v>=2^n\delta_u(v)$, (仅当 $u=v$ 时,值为 $2^n$ 个 1 相加.)==

这种同态的作用, 意义:

* 有限交换群的特征标理论：$\mathbb{F}_2^n$ 是初等阿贝尔 2- 群，其不可约特征标恰好形如 $\chi_u(x) = (−1)^{u^Tx}$.
* 正交性：$\langle \chi_u,\chi_v \rangle =2^n\delta_u(v)$, 构成正交基.

* **群同态：$\chi_u(x+y)=\chi_u(x)\chi_u(y)$.** (剥离密钥)



***Definition. Fourier Transformation***

有函数 $f:\mathbb{F}_2^n\rightarrow \mathbb{R}$. 对其的傅里叶变换为 


$$
(\mathcal{F}_n f)(u) = \langle \chi_u, f \rangle = \sum_{x\in\mathbb{F}_2^n}(-1)^{u^Tx}f(x)
$$
(**对掩码 $u$, 可算出对应 $x$ 转换后的相关度, 相当于对掩码 $u$ 做投影**)

由于其中引入了 $\chi_u$, 其又有*群同态的性质*, 所以 假设有函数 $g(x) = f(x+t)$, 对 $g(x)$ 做傅里叶变换可以得到:


$$
\begin{aligned}
&(\mathcal{F}_ng)(u) \\ 
& = \langle \chi_u,g \rangle \\
& = \langle \chi_u(x+t),f(x+t) \rangle.\ \ let\ (y = x+t),\ since\ x\in\mathbb{F}_2^n,\ then\ y\in\mathbb{F}_2^n\ \text{(shift\ only).} \\
& = \langle \chi_u(y+t),f(y) \rangle = \sum_{y\in\mathbb{F}_2^n}\chi_u(y+t),f(y) \\
& = \chi_u(t)\sum_{y\in\mathbb{F}_2^n}\chi_u(y)f(y).\ \ because\ homomorphism\ of\ \chi_u.\\
& = \chi_u(t)\langle \chi_u(y),f(y) \rangle \\
& = \chi_u(t)(\mathcal{F}_ng)(u)
\end{aligned}
$$
***Definition. Transition Matrix***

$F: \mathbb{F}_2^n\rightarrow \mathbb{F}_2^m$. $T^F: \mathbb{R[F}_2^n]\rightarrow \mathbb{R[F}_2^m]$ 定义$\delta_x\rightarrow \delta_{F(x)}$ 为对于所有$x\in\mathbb{F}_2^n$ 定义的唯一线性算子. $F$的转移矩阵是$T^F$相对于$\mathbb{R[F}_2^n]$和$\mathbb{R[F}_2^m]$的标准基的坐标表示.

转移矩阵的作用是将 **输入 $x$ 映射到 输出 $f(x)$,** 例子:

设 $n=2, \mathbb{F}_{2^2} = \{00,01,10,11\}, G(00)=01, G(01) = 00, G(10) = 11, G(11) = 10$, 映射出的转移矩阵为:

$$
T^F =
\begin{pmatrix}
 & x = 00 & x = 01 & x = 10 & x = 11 \\
y = F(x) = 00 & 0 & 0 & 1 & 0 \\
y = F(x) = 01 & 1 & 0 & 0 & 0 \\
y = F(x) = 10 & 0 & 0 & 0 & 1 \\
y = F(x) = 11 & 0 & 1 & 0 & 0
\end{pmatrix}
$$
其计算形式为: $\vec{y} = T^F \vec{x}$

***Definition. Correlation Matrix***

$F: \mathbb{F}_2^n\rightarrow \mathbb{F}_2^m$. 定义 $C^F: \mathbb{R[F}_2^n]\rightarrow \mathbb{R[F}_2^m]$ 为转移矩阵 $T^F$ 的傅里叶变换. 即 $C^F=\mathcal{F}_m T^F \mathcal{F}_n^{-1}$. $F$ 的相关矩阵是$C^F$相对于$\mathbb{R[F}_2^n]$和$\mathbb{R[F}_2^m]$的标准基的坐标表示.

**傅里叶矩阵的构造:**

* **傅里叶矩阵是 Walsh Hadamard Matrix, 一种对称的正交矩阵.** (恰好满足递归构造条件) **满足 $F^{-1}=1/nF$.**

傅里叶矩阵是把所有特征 $\chi_u(x)$ 按行排成矩阵, 行为输入掩码 $u$, 列为输入变量 $x$.

$\mathcal{F}[u,x] = \chi_u(x) = (-1)^{u^Tx}$, 每行对不同输入掩码 $u$, 遍历输入 $x$ 求得特征.

例子:

$n=2，x,u\in\{00,01,10,11\}$

对 $u=00$, 计算 $\chi_{00}(x)\rightarrow[(-1)^0,(-1)^0,(-1)^0,(-1)^0] = [1,1,1,1]$.

对 $u=01$, 计算 $\chi_{01}(x)\rightarrow[(-1)^{0\cdot 0\oplus 1\cdot 0},(-1)^{0\cdot 0\oplus 1\cdot 1},(-1)^{0\cdot 1\oplus 1\cdot 0},(-1)^{0\cdot 1\oplus 1\cdot 1}]=[1,-1,1,-1]$.

......

得到 Fourier Matrix $\mathcal{F}_M$ (其中行标 $v$ 为输出掩码, 列标可为 $x$ 或 $F(x)$, 因为 其均遍历空间:


$$
\begin{array}{c|cccc}
 & F(x)=00 & F(x)=01 & F(x)=10 & F(x)=11 \\
\hline
v=00 & 1 & 1 & 1 & 1 \\
v=01 & 1 & -1 & 1 & -1 \\
v=10 & 1 & 1 & -1 & -1 \\
v=11 & 1 & -1 & -1 & 1 \\
\end{array}
$$
且 $\mathcal{F}_M^{-1} = 1/4 \mathcal{F}$. (注意行列的表示交换了, 同理 $u$, $v$ 也可互换)


$$
1/4 \times \left(\begin{array}{c|cccc}
 & v=00 & v=01 & v=10 & v=11 \\
\hline
x=00 & 1 & 1 & 1 & 1 \\
x=01 & 1 & -1 & 1 & -1 \\
x=10 & 1 & 1 & -1 & -1 \\
x=11 & 1 & -1 & -1 & 1 \\
\end{array}
\right)
$$
对变换 $C^F=\mathcal{F}_m T^F \mathcal{F}_n^{-1}$ 之后的矩阵, 其 entry 满足:


$$
C_{v,u}^F=2P_r[v^TF(x)+u^Tx=0]-1
$$
**为什么? **

$\mathcal{F}_m T^F \mathcal{F}_n^{-1}$:

* 先算 $T^F\mathcal{F}_n^{-1}=\sum_{x\in \mathbb{F}_2^n}T^F[y,x]\mathcal{F}_n^{-1}[x,v]=T^F\mathcal{F}_n^{-1}[y,v]$

* 再算 $\mathcal{F}_m (T^F \mathcal{F}_n^{-1})=\sum_{y\in \mathbb{F}_2^m}\mathcal{F}[u,y](T^F\mathcal{F}_n^{-1}[y,v])=\mathcal{F}_m T^F \mathcal{F}_n^{-1}[u,v]$ 

Means, **map the value space of ($x$ and $y$) to the mask space ($u$ and $v$)**

Finally, the entries of the result matrix represent: $\sum_{x\in\mathbb{F}_2^n}(-1)^{ux+vy}$.





# Quasi



## Quasidifferential Basis

对于差分攻击, 每个函数的输入是一对, 如$(x,y)$，满足$x+y=a$. 直接将傅里叶变换转化为差分攻击是不可行的. 相比之下, 我们要注意$(x,y)$的分布. 因此给出一个函数 $p: \mathbb{F}_2^n \times\mathbb{F}_2^n \rightarrow [0,1]$. 如果能把 $(x,y)$ 同时映射到 如 掩码 上, 即可方便用傅里叶变换.

***Definition. Correlation Matrix***

对 $a,u \in \mathbb{F}_2^n$, 有函数==$\beta_{u,a}(x+y) = \chi_u(x)\delta_a(x+y)$==. 所有$\beta_{u,a}$的集合将被称为$\mathbb{R[F}_2^n \times \mathbb{F}_2^n]$的**准微分基**，其中 $u$ 是"掩码"，$a$ 是**固定**差分 $y=x+a$ .

注意: 

* $\chi$ 只对 $x$, 一方面不破坏 pair=$(x,y)$ 的结构, 另一方面, 因为差分固定为 $a$, 所以求 $x$ 的特征就求得 $(x+y)$ 的特征.

* $\delta_a(x+y)$ 表示只留下 满足 $x+y=a$ 的 pair.

$\beta_{u,a}$ 在其集合里是线性无关的, 且相互正交

***Theorem. properties of $\beta_{u,a}$***

* $\beta_{u,a}$ 的移位不变性: 

  对于所有 $(u, a)\in \mathbb{F}_2^n \times \mathbb{F}_2^n$ 且 $t\in\mathbb{F}_2^n$，有 $\beta_{u,a}(x + t, y + t) = \chi_u(t) \beta_{u,a}(x, y)$

$$
\begin{aligned}
& \beta_{u,a}(x + t, y + t) \\
& = \chi_u(x+t)\delta_a(x+y+t+t) \\
& = \chi_u(t)\cdot \chi_u(x)\delta_a(x+y), since\ \chi_u\ homomorphism  \\
& = \chi_u(t) \beta_{u,a}(x, y)

\end{aligned}
$$

* $\beta_{u,a}$ 的正交性:

  对所有 $$(u, a), (v, b) \in \mathbb{F}_2^n \times \mathbb{F}_2^n$$，有 $\langle \beta_{v,b}, \beta_{u,a} \rangle = 2^n \delta_v(u) \delta_b(a).$

  当 $a\neq b$, $x+y=a=b$ 不可能成立, $\langle \beta_{v,b}, \beta_{u,a} \rangle=0$;

  当 $a=b$, 
  $$
  \begin{aligned}
  & \langle \beta_{v,b}, \beta_{u,a} \rangle \\
  & = \sum_{(x,y) \in \mathbb{F}_2^n \times \mathbb{F}_2^n} \chi_v(x) \, \delta_a(x+y) \, \chi_u(x) \, \delta_a(x+y) \\
  & = \sum_{(x,y) \in \mathbb{F}_2^n \times \mathbb{F}_2^n} \chi_v(x) \, \chi_u(x) \, \delta_a(x+y),\ where\ (u=x=v)\ and\ (x+y=a=b) \\
  & = \sum_{(x,y) \in \mathbb{F}_2^n \times \mathbb{F}_2^n} \chi_v(u) \delta_a(b)\\
  & = 2^n \delta_v(u) \delta_b(a).
  \end{aligned}
  $$
  

类比傅里叶变换 (将函数由 $\chi_u$ 更换为 $\beta_{u,a}$), 得到 **准差分变换算子**:


$$
\mathcal{Q}_n: \mathbb{R}[\mathbb{F}_2^n\times \mathbb{F}_2^n] \rightarrow [\mathbb{F}_2^n\times \mathbb{F}_2^n]\quad using\quad (\mathcal{Q}_nf)(u,a)=\langle \beta_{u,a}, f\rangle
$$
$(\mathcal{Q}_nf)(u,a)$ 表示: 差分固定为 $a$ 时，线性掩码 $u$ 的系数, $(\mathcal{Q}_nf)(u,a)/2^n$ 是坐标.



## Quasidifferential Transition Matrix

对线性分析，对值 $(x,y=F(x))$ 的转移矩阵为 $T^F$. 但迁移到差分分析, 需要对考虑 pair, 即 $(x_1,y_1),(x_2,y_2)$. 这只需要对其分别的 $T^F$ 做张量积 (tensor product):


$$
\left( T^F \otimes T^F \right)_{(y_1, y_2), (x_1, x_2)} = T^F_{y_1, x_1} T^F_{y_2, x_2} = \delta_{y_1}(F(x_1)) \delta_{y_2}(F(x_2)).
$$
假设 $x,y \in \mathbb{F}_2^n$, 其中, $\left( T^F \otimes T^F \right)_{(y_1, y_2), (x_1, x_2)}$ 矩阵大小为 $n^2\times n^2$, 其中元素当且仅当 $y_1=F(x_1)$ 和 $y_2=F(x_2)$ 同时满足时, 为1.


$$
X = \begin{pmatrix} x_{11} & x_{12} \\ x_{21} & x_{22} \end{pmatrix}, \quad
Y = \begin{pmatrix} y_{11} & y_{12} \\ y_{21} & y_{22} \end{pmatrix}.

X \otimes Y =
\begin{pmatrix}
x_{11}Y & x_{12}Y \\
x_{21}Y & x_{22}Y
\end{pmatrix}
=
\begin{pmatrix}
x_{11}y_{11} & x_{11}y_{12} & x_{12}y_{11} & x_{12}y_{12} \\
x_{11}y_{21} & x_{11}y_{22} & x_{12}y_{21} & x_{12}y_{22} \\
x_{21}y_{11} & x_{21}y_{12} & x_{22}y_{11} & x_{22}y_{12} \\
x_{21}y_{21} & x_{21}y_{22} & x_{22}y_{21} & x_{22}y_{22}
\end{pmatrix}.
$$
***Definition. Quasidifferential Transition Matrix*** (其实应该对应线性的相关矩阵)

设 $n, m$ 为正整数，$F : \mathbb{F}_2^n \to \mathbb{F}_2^m$.**准差分转移矩阵** $D^F$ 定义为 $T^F \otimes T^F$ 在定义 3.1 的**准差分基**下的矩阵表示，即：


$$
D^F = \mathcal{Q}_m (T^F \otimes T^F) \mathcal{Q}_n^{-1}
$$
其意义是将 输入, 输出差分 映射到掩码上 $(a,b)\rightarrow (u,v)$, 与线性部分类似. 且 $\mathcal{Q}_n^{-1}=1/n\, \mathcal{Q}_n^T$.


$$
D_{(v,b),(u,a)}^{\text{F}} = \langle \delta_{(v,b)}, \mathcal{Q}_n(T^{\text{F}} \otimes T^{\text{F}}) \mathcal{Q}_n^{\text{T}} \delta_{(u,a)} \rangle / 2^n = \langle \beta_{v,b}, (T^{\text{F}} \otimes T^{\text{F}}) \beta_{u,a} \rangle / 2^n.
$$
其结果为 转移矩阵 (二维) $D^F$ 的第 $(v,b)$ 行, 第 $(u,a)$ 列,

方法:

* 对于一个矩阵 $M$, 其位置 $(i,j)$ 的 entry 为 $M_{i,j} = \langle \delta_{i}, M\delta_{j}\rangle$, 其中 $\delta_i,\delta_j$ 都是单位列向量, 且仅在位置 $i,j$ 为 1.

  $D^F_{(v,b),(u,a)}=\langle \delta_{(v,b)}, D^F_{(v,b),(u,a)} \delta_{(u,a)}\rangle$

  用 $\delta_{v,b},\delta_{u,a}$ 的目的是找到矩阵 $D^F_{(v,b),(u,a)}$ 中对应的点.

* 共轭转置搬运 (对实数域=转置搬运): $\langle u, Av\rangle = \langle A^Tu,v \rangle$.

* $D^F_{(v,b),(u,a)} = \begin{pmatrix} D_{(0,0),(0,0)} & D_{(0,0),(0,1)} & D_{(0,0),(1,0)} & D_{(0,0),(1,1)} \\ D_{(0,1),(0,0)} & D_{(0,1),(0,1)} & D_{(0,1),(1,0)} & D_{(0,1),(1,1)} \\ D_{(1,0),(0,0)} & D_{(1,0),(0,1)} & D_{(1,0),(1,0)} & D_{(1,0),(1,1)} \\ D_{(1,1),(0,0)} & D_{(1,1),(0,1)} & D_{(1,1),(1,0)} & D_{(1,1),(1,1)} \end{pmatrix}.$

* Recall $\beta_{u,a}(x,y)=\chi_u(x)\delta_a(x+y)$, $\mathcal{Q}_n$ 由 $\chi_u(x)$ 生成 (行标为 $u$, 列标为 $x$), 所以当映射到某一个点时 ($\delta=1$), $\mathcal{Q}_n\cdot \delta = \beta$.

将上面式子展开:

几个关键点:

* 张量积 $(T^{\text{F}} \otimes T^{\text{F}})$ 的意义是 将输入pair $(x_1,x_2)$ 映射到 输出pair $y_1,y_2, y=F(x)$. 所以 $(T^{\text{F}} \otimes T^{\text{F}}) \beta_{u,a}(x_1,x_2)=\beta_{u,a}(y_1,y_2)$.
* $x$ 和 $y$ 是对偶的, 可以互换.

$$
\begin{aligned}
& D_{(v,b),(u,a)}^{\text{F}}  \\
& = \langle \beta_{v,b}, (T^{\text{F}} \otimes T^{\text{F}}) \beta_{u,a} \rangle / 2^n \\
& = 1/2^n \cdot \langle \beta_{v,b}(x_1,x_2), \beta_{u,a}(y_1,y_2) \rangle,\ (swap\ x\ and\ y)\\
& = 1/2^n \cdot \langle \beta_{v,b}(y_1,y_2), \beta_{u,a}(x_1,x_2) \rangle\\
& = 1/2^n \cdot \sum_{x_1,x_2\in \mathbb{F}_2^n\times \mathbb{F}_2^n} \beta_{v,b}(y_1,y_2)\cdot \beta_{u,a}(x_1,x_2) \\
& = 1/2^n \cdot \sum_{x_1,x_2\in \mathbb{F}_2^n\times \mathbb{F}_2^n} \chi_u(x_1)\delta_a(x_1+x_2)\cdot \chi_v(y_1)\delta_a(y_1+y_2) \\
& = 1/2^n \cdot \sum_{x\in \mathbb{F}_2^n} (-1)^{u^Tx+v^Ty},\ where\ y=F(x)\ and\ x+a = F(x)+b
\end{aligned}
$$

最终, 通过遍历值 $x$ 可以求得其 差分 $(a\rightarrow b)$, 掩码 $(u \rightarrow v)$ 下的相关性.



对等式 $D_{(v,b),(u,a)}^{\text{F}}=\frac{1}{2^n}\cdot\sum_{x_1\in \mathbb{F}_2^n, F(x+a)=F(x)+b} (-1)^{u^Tx+v^Ty}$.

* 当 $u=v=\vec{0}, D^F_{(0,b),(0,a)}=\frac{\sum_{x\in \mathbb{F}_2^n, x+a=F(x)+b}1}{2^n}$. 这就是 $P_r(a\rightarrow b) = \frac{DDT_{a,b}^F}{2^{-n}}$.
* 当 $a=b=\vec{0}, D^F_{(0,b),(0,a)} = \frac{\sum_{x\in \mathbb{F}_2^n}(-1)^{u^Tx+v^Ty}}{2^n}=C^F_{u,v}$. 这就是线性相关度.

对 $D^F_{(v,b),(u,a)}$ 有如下性质：

1. 若 $F$ 是双射，则
