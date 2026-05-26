# List Merging

## Rebound Attack

包括 inbound 和 outbound 两部分, 采用类 MITM 的逻辑构造区分器(inbound)

**Inbound:** 

选定中间部分 (截断), 向两端扩展至稀疏, 将 起始/终止==>中间 看作一个**大 Sbox**.

从起始/终止选数据, 传到中间, 要求构成的差分不为 0 , 即保持截断性质. 这个概率为 $2^{-1}$.





## List Merging

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

**注:** *将 函数 $f_j,f'_j$ 理解为对 list 元素是 $\overrightarrow{x_1}, \ldots, \overrightarrow{x_N}$ 的**特征提取.*** 

假设成功 merge 上的概率为 $P_t \Leftarrow t(\overrightarrow{x_1},...,\overrightarrow{x_N})=1$, 记 $\mathcal{L}_{sol}$ 为 merged $N$ 个 list 之后的 list, 则其大小为


$$
P_t\cdot 2^{\sum_{i=1}^N\ell_i}
$$


## 归约 $N\rightarrow 2$

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

    |                             KEY                              |                            VALUE                             |             注              |
    | :----------------------------------------------------------: | :----------------------------------------------------------: | :-------------------------: |
    | $s$ 比特的串 $(\overrightarrow{v'_1},...,\overrightarrow{v'_j})$ | $e_B=(\overrightarrow{x_{N'+1}}, \ldots, \overrightarrow{x_{N}})$ 的某种取值 (或地址) | $f'_j(e_B)=(v'_1,...,v'_j)$ |

    同理, 表 $T_B^*$ 的大小为 $2^{\sum_{i={N'+1}}^{N}\ell_i}$.

    把 KEY 单独存一个表 $L_B$,  大小为 $2^{zs}$.

    **注:** $f_j$ 不是双射 ($f_j:2^{k*N'} \rightarrow 2^s$), 输出 $z$ 个 $s$ 比特的串 $(v_1,...,v_z)$, 可能多个 $e_A$ 对应同一个 $v_j$

    **复杂度:** 

    * *Time*: 假设处理得到 1 比特 $s$ 的复杂度为 $O(1)$, 则产生 $s$ 比特需要时间复杂度 $O(s)$ ; 共需要判断共 $z$ 个 $s$ 比特的块, 复杂度为 $O(zs)$; 而每次处理一个大 list $(\overrightarrow{x_1}, \ldots, \overrightarrow{x_{N'}})$ 的复杂度为 $2^{\sum_{i=N-N'}^{N}\ell_i}$, 所有总时间复杂度为 $O(zs2^{\sum_{i=N-N'}^{N}\ell_i})$.
    * *Memory*: 对每个表, KEY 部分共有 $zs$ 个比特, VALUE 部分共有 $(N-N')k$ 个比特, 共有 $2^{\sum_{i=N-N'}^{N}\ell_i}$ 个表, 所以总存储复杂度为 $O((zs+(N-N')k)2^{\sum_{i=N-N'}^{N}\ell_i})$.

3. **Merge $L_A$ and $L_B$:**

    也即, 计算 $\prod_{j=1}^z t_j$, where $t_j=(v_j,v'_j) \in \lbrace 0,1 \rbrace$, 这产生一个新的 list $\mathcal{L}_{sol}$. 

    $\mathcal{L}_{sol}$ 里存的是所有 pairs $((v_1,...,v_z),(v'_1,...,v'_z))$, 当 $\prod_{j=1}^z t_j=1$ 时, 标记 $1$. 所以 $\mathcal{L_{sol}}$ 如:

    |                            PAIRS                             |                   FLAG                    |
    | :----------------------------------------------------------: | :---------------------------------------: |
    | $((\overrightarrow{v_1},...,\overrightarrow{v_z}),(\overrightarrow{v'_1},...,\overrightarrow{v'_z}))$ | $\prod_{j=1}^z t_j\in\lbrace 0,1 \rbrace$ |

    **复杂度:** 记时间复杂度为 $T_{merge}$, 存储复杂度为 $M_{merge}$.

4. 取出 $\mathcal{L_{sol}}$ 里 $\prod_{j=1}^z t_j=t=1$ 的项, 组成解 list $\mathcal{L}_{sol}^*$. (验证)

    将满足 $\prod_{j=1}^z t_j=t=1$ 所对应的 $((\overrightarrow{v_1},...,\overrightarrow{v_z}),(\overrightarrow{v'_1},...,\overrightarrow{v'_z}))$ 及其对应的原始 list $(x_1, \ldots, x_N, x_{N+1}, \ldots, x_N) \in T_A^* [(v_1, \ldots, v_z)] \times T_B^* [(v'_1, \ldots, v'_z)]$ 均存入 list $\mathcal{L}_{sol}^*$.

    **复杂度:** 由于这一步仅操作满足 $\prod_{j=1}^z t_j=t=1$ 的数据, 但数据量为所有 $N$ 个 list, 所以时间与存储复杂度均为 $O(P_t2^{\sum_{i={1}}^{N}\ell_i})$.

**总复杂度:**

* *Time:* $\mathcal{O}\left(sz2^{\sum_{i=1}^{N'} l_i} + sz2^{\sum_{i=N'+1}^{N} l_i }+ 2T_{\text{merge}} + P_t2^{\sum_{i=1}^{N} l_i}\right)$

* *Memory:* $\mathcal{O}\left((zs + N'k)2^{\sum_{i=1}^{N'}l_i} + (zs + (N - N')k)2^{\sum_{i=N'+1}^{N}l_i} + 2^{M_{\text{merge}}} + P_t2^{\sum_{i=1}^{N}l_i}\right)$



**注:** $\overrightarrow{v_1},...,\overrightarrow{v_z}$ 的形式为 
$$
\begin{matrix}
v_{1,1} & \cdots & v_{z,1} \\
\vdots  &  & \vdots  \\
v_{1,s} & \cdots & v_{z,s}
\end{matrix}
$$


---

对 Merging 部分 (步骤3)

----



### Brute Force

*Time:* $2^{l_A+l_B}$

*Memory:* $2^{l_A}+2^{l_B}$

### Instant Matching

**算法 1 Instant Matching：**

1. 对每个 $\overrightarrow{v'_j}$ (of size $2^s$), where $j\in\lbrace 1,...,z \rbrace$, 创建 hash table $T_j$; 对每个 $v'_i \in \lbrace \overrightarrow{v'_j} \rbrace$, where $i\in \lbrace 1,...,s \rbrace$ 搜集 $v_i \in \lbrace \overrightarrow{v_j} \rbrace$, where $i\in \lbrace 1,...,s \rbrace$ and $t_j(v_j,v'_j)=1$.

   所以 size of $T_j\le 2^{2s}$, $T_j$ 如:

   |                       KEY                        |                     VALUE                      |     Condition     |
   | :----------------------------------------------: | :--------------------------------------------: | :---------------: |
   | $v'_i \in \lbrace \overrightarrow{v'_j} \rbrace$ | $v_i \in \lbrace \overrightarrow{v_j} \rbrace$ | $t_j(v_j,v'_j)=1$ |

   **复杂度:** 对每个 $T_j$ 建表需要的时间和存储均为 $\mathcal{O}(2^{2s})$, 所以对所有 $z$ 个 $T_j$, 总 *Time=Memory=$\mathcal{O}(z2^{2s})$*.

   

2. 逐个取出 $L_B$ 中的元素 $(\overrightarrow{v'_1},...,\overrightarrow{v'_z})$ , 对每个 $(v'_1,...,v'_z)$, 检查各个 $T_j$ 表:

   * 如果有某个 $T_j[v'_j]$ 为空, 则丢弃该 $(v'_1,...,v'_z)$.
   * 如果每个 $T_j[v'_j]$ 均不为空, 则对每个 $T_j[v'_j]$ 中的 $\overrightarrow{v_j}$ 做笛卡尔积, 将组合过的 list 存入 表 $L_{aux}$.
   * 在 $L_{aux}$ 中查找每个 $L_A$ 中的 $(v_1,...,v_z)$, 每查到一个就将其存入 $\mathcal{L}_{sol}$.

   **注1:** 假设对所有 $\overrightarrow{v'_j}$, 找到 $t_j(\overrightarrow{v_j},\overrightarrow{v'_j})$ 的概率为 $2^{-p_j}$, (所有 $j\in\{1,...,z\}$ 都满足的概率为 $P_t$), 所以 $\sum_{j=1}^z p_j=-log_2(P_t)$. 而 $\overrightarrow{v'_j}$ 的长度是 $s$ 比特, 所以每个 $T_j[v_j]$ 里的大小为 $2^{s-p_j}$, $T_j$ 的大小为 $2^{s-\sum_{j=1}^z p_j}$, $T$ 的大小为 $2^{zs-\sum_{j=1}^z p_j}$.

   **注:** 对 $L_B$ 中的每个元素, 都有一个表 $L_{aux}$. 每次生成 $L_{aux}$ 就立即对 $L_A$ 进行匹配.

   **复杂度:** 

   *Time:* 

   * 对 $L_B$ 中每个元素操作, 复杂度 $\mathcal{O}(2^{l_B})$; 
   * $T$ 中的元素数量 $2^{zs-\sum_{j=1}^z p_j}$, 每个元素需要操作的次数 $z$ (即 操作 $v'_1,...,v'_z$), 复杂度 $z2^{zs-\sum_{j=1}^z p_j}$.

   *Memory:*

   需要存 $L_A, L_B, merged(L_A,L_B)$, 共 $\mathcal{O}(2^{l_A}+2^{l_B}+P_t2^{L_A+L_B})$

**总复杂度:**

*Time:* $\mathcal{O}(z2^{2s}+zP_t2^{zs+l_B})$

*Memory:* $\mathcal{O}(z2^{2s}+2^{l_A}+2^{l_B}+P_t2^{L_A+L_B})$



#### 例子: 4*4 Sbox Instant Matching

假设 $l_A = |L_A|=l_B = |L_B| = 2^{24.18}$. merging 需要匹配 $(v,v')$ 的 $10$ bits 条件. (其中固定位置的 6 个 Sbox 可以提取特征)



**穷搜:** 需要 $2^{24.18*2}=2^{48.36}$ 次操作.

**Instant Matching:** 

* 提取 6 bits 的特征: 建表 $T_j$, $j\in\{1,...,6\}$. 最坏情况每个表大小 $2^{2s}=2^8$.

  特征提取概率 $p_j=3.91$, ($-log_2{P_t}=\sum_{j=1}^zp_j=2^{-23.46}$) 则每个 $v_j$ 内的数据量为 $2^{s-p_j}=2^{0.09}$, 6 个表的总 ($L_{aux}$) 大小为 $6*2^{0.09}=2^{0.54}\approx 1.45$.

  **注:** 这里的剪枝是效率提升的关键.

  **复杂度:** *Time/Memory of building $T_j$*: $\mathcal{O}(z2^s=2^{6.58})$.

* 操作每个 $(\overrightarrow{v'_1},...,\overrightarrow{v'_z})\in L_B$, 对有特征的 6 个 Sbox, 查 $T_j$, 丢弃空表, 对非空做笛卡尔积, 得到:
  $$
  T_1[v'_1]\times...\times T_6[v'_6]
  $$
  从而得到完整的 $(v_1,...,v_6)$, 作为完整的 KEY, 立即去 $L_A$ 中查找 VALUE, 从而进行 merge.

  Merge 得到的 pairs 数量为 $2^{24.9}$ , 对每个 pair，去验证剩余的 4 bits 条件，复杂度为 $\mathcal{O}(2^{24.9})$.

  **复杂度:** 
  
  * *Time of iterating $L_B$:* $\mathcal{O}(zP_t2^{l_b+zs}=2^{27.6})$. **Major**
  * *Time of merging $L_A$:* $\mathcal{O}(2^{l_A+l_B}/P_t=2^{48.36-23.46}=2^{24.9})$.

  **复杂度:** 

  *Time:* $2^{27.6}$ 

  *Memory:* $l_A,l_b=2^{24.18}$
  

**注:** Instant Matching 适用于 $|L_{aux}| < (l_A,l_B)$ 的情况. 当 $P_t2^{zs}>l_A$ 时, *Time of iterating $L_B$:* $\mathcal{O}(zP_t2^{l_b+zs}>2^{l_A+l_B})$, 即比穷搜更差.



### Gradual Matching

**算法 2 Gradual Matching:**

1. 对每个 $\overrightarrow{v'_j}$ (of size $2^s$), where $j\in\lbrace 1,...,z \rbrace$, 创建 hash table $T_j$; 对每个 $v'_i \in \lbrace \overrightarrow{v'_j} \rbrace$, where $i\in \lbrace 1,...,s \rbrace$ 搜集 $v_i \in \lbrace \overrightarrow{v_j} \rbrace$, where $i\in \lbrace 1,...,s \rbrace$ and $t_j(v_j,v'_j)=1$.

   所以 size of $T_j\le 2^{2s}$, $T_j$ 如:

   |                       KEY                        |                     VALUE                      |     Condition     |
   | :----------------------------------------------: | :--------------------------------------------: | :---------------: |
   | $v'_i \in \lbrace \overrightarrow{v'_j} \rbrace$ | $v_i \in \lbrace \overrightarrow{v_j} \rbrace$ | $t_j(v_j,v'_j)=1$ |

   **复杂度:** 对每个 $T_j$ 建表需要的时间和存储均为 $\mathcal{O}(2^{2s})$, 所以对所有 $z$ 个 $T_j$, 总 *Time=Memory=$\mathcal{O}(z2^{2s})$*.

2. 对 $\alpha \in \{\alpha_1,...,\alpha_{z'}\}\in(\{0,1\}^s)^{z'}$:

   1. 从 $L_B$ 中逐个取 $(v_1,...,v_{z'})=\alpha$;

   2. 与 *算法1, Step 2* 相同, 用笛卡尔积构造 $L_{aux}$; (每个 $L_{aux}$ 的大小为 $|L_{aux}|=2^{z's-\sum_{i=1}^{z'}p_j}$)

      **注:** 这一步之后, $z'$ 个条件以及匹配完成, 可作为后续的筛选条件 ($2^{z's}$).

   3. 从 $L_{aux}$ 中取出每个元素, 记 $\gamma=(\gamma_1,...,\gamma_{z'})$:

      1. 在 $L_A$ 中逐个查找 $(v_1,...,v_{z'})=\gamma$;
      2. Merge $L_A(\gamma)$ and $L_B(\alpha)$, 条件为 $t'=\prod_{j=z'+1}^z(t_j)$.
      3. 将结果存入 $\mathcal{L}_{sol}$.

   **注:** 这里的 $\alpha,\gamma$ 都只是为了定位 $z'$ 个向量. 
