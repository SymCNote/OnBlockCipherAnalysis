# List Merging

## Rebound Attack





对一个很大的 list, 长度为 $k$ bits, 可将其分为 若干个 $s$ bits 的小块, 而**需要 merge 的块数量为 $z$.** (**$zs \le k$**)

**问题1:** 假设需要 merge $N$ 个 list $L_1,...,L_N$.

$L_1,\dots, L_N$ 是 $N$ 个 list, 大小为 $2^{\ell_1},\dots, 2^{\ell_N}$, 每个 list 的元素都是从 $\lbrace 0,1\rbrace$ 中均匀随机独立采样的. 有 布尔 函数 $t: (\lbrace 0,1\rbrace^k)^N\rightarrow \lbrace0,1\rbrace$.

将 $N$ 拆为两半 $1,\dots,N',N',\dots,N$, 则 $t$ 可以拆解为 3 个函数:


$$
\begin{aligned}
& t_j: \lbrace 0,1\rbrace^{2s} & \rightarrow & \lbrace0,1\rbrace\\
& f_j: (\lbrace 0,1\rbrace^k)^{N'} & \rightarrow & \lbrace0,1\rbrace^{s}\\
& f’_j: (\lbrace 0,1\rbrace^k)^{N-N'} & \rightarrow & \lbrace0,1\rbrace^{s}\\
\end{aligned}
$$


注: $(\overrightarrow{x_1},...\overrightarrow{x_N})\in{(\lbrace 0,1\rbrace^k)^{N}}=L_1\times ...\times L_N$.

对 **有效 (merging required)** 的分块数量 $z$, 取 $j=1,...,z$.


$$
t(\overrightarrow{x_1}, \ldots, \overrightarrow{x_N}) = 1 \quad \Leftrightarrow \quad \forall j = 1, \ldots, z,
\begin{cases} 
t_j(v_j, v'_j) = 1 \\ 
\text{with }\begin{cases} v_j = f_j(x_1, \ldots, x_{N'})\\ 
 v'_j = f'_j(x_{N'+1}, \ldots, x_N) \end{cases}
\end{cases}
$$


*将 函数 $f_j,f'_j$ 理解为对 list 元素是 $\overrightarrow{x_1}, \ldots, \overrightarrow{x_N}$ 的**特征提取.*** 

假设成功 merge 上的概率为 $P_t \Leftarrow t(\overrightarrow{x_1},...,\overrightarrow{x_N})=1$, 记 $\mathcal{L}_{sol}$ 为 merged $N$ 个 list 之后的 list, 则其大小为


$$
P_t\cdot 2^{\sum_{i=1}^N\ell_i}
$$


#### 归约 $N\rightarrow 2$

当需要 merge 的 list 数量非常多时, 可将其归约为仅 merge 2 个 list. $N\ge 2 \rightarrow N=2$, 即 merge $L_A,L_B$.

