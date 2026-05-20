# List Merging

## Rebound Attack





对一个很大的 list, 长度为 $k$ bits, 可将其分为 若干个 $s$ bits 的小块, 而**需要 merge 的块数量为 $z$.** (**$zs \le k$**)

**注:** $z$ 可理解为有差分的位置.

**问题1:** 假设需要 merge $N$ 个 list $L_1,...,L_N$. $L_1,\dots, L_N$, 大小为 $2^{\ell_1},\dots, 2^{\ell_N}$, 每个 list 的元素都是从 $\lbrace 0,1\rbrace^k$ 中均匀随机独立采样. 

有 布尔 函数 $t: (\lbrace 0,1\rbrace^k)^N\rightarrow \lbrace0,1\rbrace$.

**注:** 这里的 list $L_i,\ i \in \lbrace 1,...,N \rbrace$ 可以理解为一个大的截断差分状态, 其0差分位置取值固定, 截断位置取值大小为 $2^{\ell_i}$ .

将 $N$ 拆为两半 $1,\dots,N',N'+1,\dots,N$, 则 $t$ 可以拆解为 3 个函数:


$$
\begin{aligned}
& t_j: \lbrace 0,1\rbrace^{2s} & \rightarrow & \lbrace0,1\rbrace\\
& f_j: (\lbrace 0,1\rbrace^k)^{N'} & \rightarrow & \lbrace0,1\rbrace^{s}\\
& f’_j: (\lbrace 0,1\rbrace^k)^{N-N'} & \rightarrow & \lbrace0,1\rbrace^{s}\\
\end{aligned}
$$

**注:** $(\overrightarrow{x_1},...\overrightarrow{x_N})\in{(\lbrace 0,1\rbrace^k)^{N}}=L_1\times ...\times L_N$.

对 **有效 (merging required)** 的分块数量 $z$, 取 $j=1,...,z$.


$$
t(\overrightarrow{x_1}, \ldots, \overrightarrow{x_N}) = 1 \quad \Leftrightarrow \quad \forall j = 1, \ldots, z,
\begin{cases} 
t_j(v_j, v'_j) = 1 \\ 
\text{with }\begin{cases} v_j = f_j(\overrightarrow{x_1}, \ldots, \overrightarrow{x_{N'}})\\ 
 v'_j = f'_j(\overrightarrow{x_{N'+1}}, \ldots, \overrightarrow{x_N}) \end{cases}
\end{cases}
$$

**注:** 将 函数 $f_j, f'_j$ 理解为对 list 元素是 $\overrightarrow{x_1}, \dots, \overrightarrow{x_N}$ 的**特征提取.**

假设成功 merge 上的概率为 $P_t \Leftarrow t(\overrightarrow{x_1},...,\overrightarrow{x_N})=1$, 记 $\mathcal{L}_{sol}$ 为 merged $N$ 个 list 之后的 list, 则其大小为


$$
P_t\cdot 2^{\sum_{i=1}^N\ell_i}
$$


#### 归约 $N\rightarrow 2$

当需要 merge 的 list 数量非常多时, 可将其归约为仅 merge 2 个 list. $N\ge 2 \rightarrow N=2$, 即 merge $L_A,L_B$.

步骤如下:

1. 建表 $T_A^*$:

    |                             KEY                              |                            VALUE                             |               注                |
    | :----------------------------------------------------------: | :----------------------------------------------------------: | :-----------------------------: |
    | $s$ 比特的串 $(\overrightarrow{v_1},...,\overrightarrow{v_j})$ | $e_A=(\overrightarrow{x_1}, \ldots, \overrightarrow{x_{N'}})$ 的某种取值 (或地址) | $f_j(e_A)=\overrightarrow{v_j}$ |

    因为每个表的大小 (size of $\overrightarrow{x_i}$) 为 $2^{\ell_i}$, 所以 $T_A^*$ 的总大小为 $2^{\ell_1}\times...\times2^{\ell_{N'}} = 2^{\sum_{i=1}^{N'}\ell_i}$.

    把 KEY 单独存一个表 $L_A$, 大小为 $2^{zs}$. 

    **注:** $f_j$ 不是双射 ($f_j:2^{k*N'} \rightarrow 2^s$), 输出 $z$ 个 $s$ 比特的串 $(v_1,...,v_z)$, 可能多个 $e_A$ 对应同一个 $v_j$

    **复杂度:** 

    * *Time*: 假设处理得到 1 比特 $s$ 的复杂度为 $O(1)$, 则产生 $s$ 比特需要时间复杂度 $O(s)$ ; 共需要判断共 $z$ 个 $s$ 比特的块, 复杂度为 $O(zs)$; 而每次处理一个大 list $(\overrightarrow{x_1}, \ldots, \overrightarrow{x_{N'}})$ 的复杂度为 $2^{\sum_{i=1}^{N'}\ell_i}$, 所有总时间复杂度为 $O(zs2^{\sum_{i=1}^{N'}\ell_i})$.
    * *Memory*: 对每个表, KEY 部分共有 $zs$ 个比特, VALUE 部分共有 $N'k$ 个比特, 共有 $2^{\sum_{i=1}^{N'}\ell_i}$ 个表, 所以总存储复杂度为 $O((zs+N'k)2^{\sum_{i=1}^{N'}\ell_i})$.

2. 建表 $T_B^*$:

    |              KEY               |                            VALUE                             |             注              |
    | :----------------------------: | :----------------------------------------------------------: | :-------------------------: |
    | $s$ 比特的串 $(v'_1,...,v'_j)$ | $e_B=(\overrightarrow{x_{N'+1}}, \ldots, \overrightarrow{x_{N}})$ 的某种取值 (或地址) | $f'_j(e_B)=(v'_1,...,v'_j)$ |

    同理, 表 $T_B^*$ 的大小为 $2^{\sum_{i={N'+1}}^{N}\ell_i}$.

    把 KEY 单独存一个表 $L_B$,  大小为 $2^{zs}$.

    **注:** $f_j$ 不是双射 ($f_j:2^{k*N'} \rightarrow 2^s$), 输出 $z$ 个 $s$ 比特的串 $(v_1,...,v_z)$, 可能多个 $e_A$ 对应同一个 $v_j$

    **复杂度:** 

    * *Time*: 假设处理得到 1 比特 $s$ 的复杂度为 $O(1)$, 则产生 $s$ 比特需要时间复杂度 $O(s)$ ; 共需要判断共 $z$ 个 $s$ 比特的块, 复杂度为 $O(zs)$; 而每次处理一个大 list $(\overrightarrow{x_1}, \ldots, \overrightarrow{x_{N'}})$ 的复杂度为 $2^{\sum_{i=N-N'}^{N}\ell_i}$, 所有总时间复杂度为 $O(zs2^{\sum_{i=N-N'}^{N}\ell_i})$.
    * *Memory*: 对每个表, KEY 部分共有 $zs$ 个比特, VALUE 部分共有 $(N-N')k$ 个比特, 共有 $2^{\sum_{i=N-N'}^{N}\ell_i}$ 个表, 所以总存储复杂度为 $O((zs+(N-N')k)2^{\sum_{i=N-N'}^{N}\ell_i})$.

3. Merge $L_A$ and $L_B$:

    也即, 计算 $\prod_{j=1}^z t_j$, where $t_j=(v_j,v'_j)\in\lbrace 0,1 \rbrace$, 这产生一个新的 list $\mathcal{L}\_{sol}$. 
    

    $\mathcal{L}_{sol}$ 里存的是所有 pairs $((v_1,...,v_z),(v'_1,...,v'_z))$, 当 $\prod_{j=1}^z t_j=1$ 时, 标记 $1$. 所以 $\mathcal{L_{sol}}$ 如:

    |               PAIRS               |                   FLAG                    |
    | :-------------------------------: | :---------------------------------------: |
    | $((v_1,...,v_z),(v'_1,...,v'_z))$ | $\prod_{j=1}^z t_j\in\lbrace 0,1 \rbrace$ |

    **复杂度:** 记时间复杂度为 $T_{merge}$, 存储复杂度为 $M_{merge}$.

4. 取出 $\mathcal{L_{sol}}$ 里 $\prod_{j=1}^z t_j=t=1$ 的项, 组成解 list $\mathcal{L}_{sol}^*$. (验证)

    将满足 $\prod_{j=1}^z t_j=t=1$ 所对应的 $((v_1,...,v_z),(v'_1,...,v'_z))$ 及其对应的原始 list $(x_1, \ldots, x_N, x_{N+1}, \ldots, x_N) \in T_A^* [(v_1, \ldots, v_z)] \times T_B^* [(v'_1, \ldots, v'_z)]$ 均存入 list $\mathcal{L}_{sol}^*$.

    **复杂度:** 由于这一步仅操作满足 $\prod_{j=1}^z t_j=t=1$ 的数据, 但数据量为所有 $N$ 个 list, 所以时间与存储复杂度均为 $O(P_t2^{\sum_{i={1}}^{N}\ell_i})$.

**总复杂度:**

* *Time:* $\mathcal{O}\left(sz2^{\sum_{i=1}^{N'} l_i} + sz2^{\sum_{i=N'+1}^{N} l_i }+ 2T_{\text{merge}} + P_t2^{\sum_{i=1}^{N} l_i}\right)$

* *Memory:* $\mathcal{O}\left((zs + N'k)2^{\sum_{i=1}^{N'}l_i} + (zs + (N - N')k)2^{\sum_{i=N'+1}^{N}l_i} + 2^{M_{\text{merge}}} + P_t2^{\sum_{i=1}^{N}l_i}\right)$
