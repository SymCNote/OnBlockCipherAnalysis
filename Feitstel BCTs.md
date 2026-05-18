Some information and knowledge about Feistel BCTs



# Feistel Connectivity Table

> From [2020-ToSC-On the Feistel Counterpart of the Boomerang Connectivity Table](https://tosc.iacr.org/index.php/ToSC/article/view/8568)

这篇文章中给出了 Feistel 连接表 FBCT, 及其扩展的 FBDT, FBET. 基础的 Boomerang Connectivity Table 在多篇文章中提出, 待补充......

## FBCT

> From [2020-ToSC-On the Feistel Counterpart of the Boomerang Connectivity Table](https://tosc.iacr.org/index.php/ToSC/article/view/8568)

下图为 Feistel 结构 (classical) 用于解释相关 Connectivity Tables 的图. 其中:

* $L^i,R^i$ 分别表示 (① ② ③ ④) 4 条路径上输入的 left, right 分支. 以 $L^1,R^1$ 为例, 其加密一轮的结果为 $F(L^1)\oplus R^1 \parallel L^1$. 
* 轮函数 $F$ 是包括 Key Addition, multiple independent Sbox, Linear Layer (但 Linear Layer 对 FBCT 没什么影响, 重要的是 the concatenation of multiple independent Sbox).
* 该层的输入差分为 $\beta^L \parallel \beta^R$, 输出差分为 $\gamma^L\parallel \gamma^R$ .

需要注意: **Feistel 结构的加解密具有一致性** (仅使用的密钥顺序不同)

<img width="1025" height="295" alt="image" src="https://github.com/user-attachments/assets/f3924da7-757d-4fe7-b4d3-130f9fb587fe" />

**将该 Boomerang 连接起来的关键是让 上图右侧的输入差分= $\beta^L \parallel \beta^R$**

现在分别考虑在 ③ ④ 上分别**满足**差分 $\beta^L$ 和 $\beta^R$:

* 对 $\beta^L$, 需要满足 $L_3\oplus L_4=\beta^L$, 这个推导是直接的, 不需要额外的条件:

$$
L^3 \oplus L^4 = (L^3 \oplus L^1) \oplus (L^1 \oplus L^2) \oplus (L^2 \oplus L^4)
= \gamma^R \oplus \beta^L \oplus \gamma^R = \beta^L.
$$

* 对 $\color{red}{\beta^R}$, 需要满足 $R_3\oplus R_4=\beta^R$:

  用 $G_3,G_4$ 分别表示右侧两条路径的左侧输入, 因为右侧的路径是由反向 (自下而上) 传播过来的. 由: 
  
$$
\begin{aligned}
&R^3=F(L^1 \oplus \gamma^R) \oplus G^3\\
&R^4=F(L^1 \oplus \gamma^R \oplus \beta^L) \oplus G^4\\
&G^3=F(L^1) \oplus R^1 \oplus \gamma^L\\
&G^4=F(L^1 \oplus \beta^L) \oplus (R^1 \oplus \beta^R) \oplus \gamma^L
\end{aligned} 
$$


  可进行如下推导: 

$$
\begin{aligned}
R^3 \oplus R^4 &= F(L^1 \oplus \gamma^R) \oplus G^3 \oplus F(L^1 \oplus \gamma^R \oplus \beta^L) \oplus G^4 \\
&= F(L^1 \oplus \gamma^R) \oplus F(L^1) \oplus R^1 \oplus \gamma^L \oplus F(L^1 \oplus \gamma^R \oplus \beta^L) \oplus F(L^1 \oplus \beta^L) \oplus (R^1 \oplus \beta^R) \oplus \gamma^L \\
&= \left[F(L^1 \oplus \gamma^R) \oplus F(L^1) \oplus F(L^1 \oplus \gamma^R \oplus \beta^L) \oplus F(L^1 \oplus \beta^L)\right] \oplus \beta^R.
\end{aligned}
$$

  所以为了让 $R^3\oplus R^4=\beta^R$, 上式最后一行需要满足以下关系:

$$
F(L^1) \oplus F(L^1 \oplus \gamma^R) \oplus F(L^1 \oplus \beta^L) \oplus F(L^1 \oplus \gamma^R \oplus \beta^L) = 0.
$$

所以，可以令 $L^1=x, \beta^L=\Delta_{i}, \gamma^R=\nabla_{o}$, 上式就可以写成:

$$
S(x) \oplus S(x \oplus \Delta_i) \oplus S(x \oplus \nabla_o) \oplus S(x \oplus \Delta_i \oplus \nabla_o) = 0.
$$

**注意:** 这里 $\beta^L$ 和 $\gamma^R$ 都是 Sbox 输入端的差分, 即 $\beta^L$ 是第 r 轮的左侧输入差分, $\gamma^R$ 是第 r+1 轮的右侧输入差分.

而这里连接的概率为:

$$
2^{-n} \times \text{No.}\lbrace x \in \mathbb{F}_2^n \mid S(x) \oplus S(x \oplus \Delta_i) \oplus S(x \oplus \nabla_o) \oplus S(x \oplus \Delta_i \oplus \nabla_o) = 0 \rbrace.
$$

最终 FBCT 的定义为:

<img width="1200" height="120" alt="image" src="https://github.com/user-attachments/assets/a0a3db91-e39b-4ab0-9144-7d4bb7462e62" />

