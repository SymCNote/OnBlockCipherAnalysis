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

<img width="1025" height="295" alt="image" src="https://github.com/user-attachments/assets/f3924da7-757d-4fe7-b4d3-130f9fb587fe" />

**将该 Boomerang 连接起来的关键是让 上图右侧的输入差分= $\beta^L \parallel \beta^R$**

现在分别考虑 $\beta^L$ 和 $\beta^R$:

* 对 $\beta^L$:

  
