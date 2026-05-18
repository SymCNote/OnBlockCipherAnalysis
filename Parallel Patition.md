# Parallel Partition



## Differential MITM Attack
> from Section 2.2 of Paper [22-CC-Differential Meet-In-The-Middle Cryptanalysis](https://link.springer.com/chapter/10.1007/978-3-031-38548-3_9)

### 原理与假设

$n$-bit 分组密码 $E$，有如下图的区分器与扩展：

<img src="https://github.com/user-attachments/assets/93471796-555c-41da-9b9e-9fad9f48de36" width = "300" height = "500" div align=center />

### 方法与步骤

随机选一个明文 $P$，加密得到相应的密文 $C=E_K(P)$ ；

依上图规则，根据 $k_{in}$ 将 $P$ 部分加密，然后 $\oplus\Delta_x$ ，最后解密到 $\widetilde{P}$，即

$$
\begin{align}
& Upper:\qquad & P\stackrel{k_{in}}{\longrightarrow} \oplus\Delta_x \stackrel{k_{in}}{\longrightarrow} \widetilde{P} \qquad & (E_{k_{in}}(P)\oplus E_{k_{in}}(\widetilde{P})=\Delta_x)\\
& Lower:\qquad & C\stackrel{k_{out}}{\longrightarrow} \oplus\Delta_y \stackrel{k_{out}}{\longrightarrow} \widetilde{C}\qquad & (E^{-1}_{k_{out}}(C)\oplus E^{-1}_{k_{out}}(\widetilde{C})=\Delta_y)
\end{align}
$$

所以组成的 Pairs 数量为 $2^{|k_{in}|}$ 个 $(P,\widetilde{P},k_{in})$， $2^{|k_{out}|}$ 个 $(C,\widetilde{C},k_{out})$

得到的 $\widetilde{P}$ 之后可以加密得到相应的密文 $\widehat{C}$, 将 $(P,(\widetilde{P},\widehat{C}),k_{in})$ 存入 Hash 表（索引为 $\widehat{C}$），在 Lower 部分同时生成 $\widetilde{C}$ 之后，寻找 $(\widehat{C},\widetilde{C})$ 相等的碰撞。找到，即为正确 Pairs.

### 复杂度分析


$$
\mathcal{T}=2^p\times(2^{|k_{in}|}+2^{|k_{out}|})+2^{|k_{in}\cup k_{out}|-n+p}+2^{k-n+p}.
$$




## Basic Parallel Partition in D-MITM

> from Section 2.2 of Paper [22-CC-Differential Meet-In-The-Middle Cryptanalysis](https://link.springer.com/chapter/10.1007/978-3-031-38548-3_9)



### 原理与假设

假设有概率为 $2^{-p}$ 的差分区分器，其中 $p$ 为区分器概率的负对数（$p>0$）

$\bigstar$ 当分组密码的密钥加不是加在全状态上的时候（**非全状态密钥加（Non-Full Key Addition）**，典型算法有$\texttt{SKINNY, GIFT, SIMON}$，parallel partition可以用来在增加复杂度的情况下增加攻击轮数，**ONE** round.

如下图所示，在区分器末尾添加一轮，密钥只加在 $m$ bits 状态上，若 $p>m$，则以上加一轮条件可以被满足.

<img src="https://github.com/user-attachments/assets/41a6a985-4011-481a-a627-f37cd4677d02" width = "500" height = "300" div align=center />

### 方法与步骤

如上图，在攻击最后添加一轮， $X$ 和 $Y$ 分别是 Key Addition 前后的状态（其中有 $n-m$ bits 未被 Key Addition 影响）

$\blacktriangleright$ 由于需要 $2^p$ 个明文来保证至少找到一个正确 pair，假设现有数据量即为 $2^p$，则在上图 $S_{r-1}$ 处即有 $2^p$ 个数据。将 $2^n$（实际是 $2^p$ 种情况） 在 $X$ 和 $Y$ 处进行划分，可化为 $2^m \times 2^{p-m}$ 两组，其中 $2^m$ 对应受密钥影响的部分；<u>$2^{p-m}$ 对应不受密钥影响的部分</u>，这部分同样需要多次取值（<u>但不受密钥影响，每次不同取值对应 $2^m$ 次 basic D-MITM 的操作</u>）来达到数据要求.

* 对每个不同取值的 $p-m$ 部分的 $X$ 和 $Y$ （复杂度 $2^{p-m}$），执行以下操作：

  * 对 $X$，由于有 $2^m$ 个 $P$，即有 $2^m$ 个 $C$ , 所以 $(C,\widetilde{C},k_{out})$ 的数量要 $\times 2^m$，即为 $2^{m+k_{out}}$ 个 Pairs.
  * 对 $Y$，由于其是密文，可将其<u>解密至明文</u>，然后执行明文部分的部分加密操作。同上，有 $2^{m+k_{in}}$  个 Pairs.
  * 匹配 $X$ 和 $Y$，匹配后的数量为 $2^{|k_{in}|+|k_{out}|+2m}$ ，比之前多了 $2^{2m}$ .
    * 因为 $X$ 和 $Y$ 之间只有一层 Key Addition, 所以 应该满足 $(X\oplus k_m)\oplus (X'\oplus k_m)=Y\oplus Y'$ , 即 $X\oplus X' = Y\oplus Y'$ , 这对应着 $2^{-m}$ 的过滤效果. 
    * 如果 $2^m$ 部分对应密钥猜测是（部分）免费的（通常可以用 $k_{in}\cup k_{out}$ 推出来），则又对应过滤效果 $2^{k_{in}-m}$；
  * 因此，匹配后的数量为 $2^{|k_{in}|+|k_{out}|+2m-m-m}=2^{|k_{in}|+|k_{out}|}$ 没变（假设 $k_{m}=0$）.


### 复杂度分析


$$
\mathcal{T}=2^{p-m}\times(2^{|k_{in}|+m}+2^{|k_{out}|+m}+2^{|k_{in}|+|k_{out}|-|k_{in}\cap k_{out}|+(2m-m+k_m-m)-n+p})+2^{k-n+p}
$$


注：为保证至少存在一个正确 Pair，最终生成的 Pairs 数量应该保持与 Basic D-MITM 攻击一致. 所以由于在 Upper 和 Lower 所产生的 Pairs 数量增加 $2^{|k_{in}|}\rightarrow 2^{|k_{in}|+m}$，所以重复的次数减少 $2^p\rightarrow 2^{p-m}$ .

## Improved Parallel Partition in D-MITM

> from Section 4.1 of Paper [24-EC-Improved Differential Meet-in-the-Middle Cryptanalysis](https://link.springer.com/chapter/10.1007/978-3-031-58716-0_10)



### Truncated Differential (notes)

在 improved Parallel Partition 之前，需要先厘清 truncated differential 是什么. 以下介绍几个小点，对比其与 differential (characteristic) 的不同：

注意： $\Delta_{in}$ 和 $\Delta_{out}$ 可以不为差分特征，即 $|\Delta_{in}|\ge 1$ 和/或 $\Delta_{out}\ge 1$.

1. 判断截断差分轨迹是否有效（将其与 PRP 对比）：

$$
\begin{align}
P(\Delta_{in}\stackrel{E}{\longrightarrow}\Delta_{out})>P(\Delta_{in}\stackrel{E}{\longrightarrow}\Delta_{out})=\frac{|\Delta_{out}|}{n}
\end{align}
$$

2. 截断差分有方向：

   
$$
\begin{align}
P(\Delta_{in}\stackrel{E^{-1}}{\longrightarrow}\Delta_{out})=P(\Delta_{in}\stackrel{E}{\longrightarrow}\Delta_{out})\times \frac{|\Delta_{in}|}{|\Delta_{out}|}
\end{align}
$$

3. 截断差分在组 Pairs 之后（全猜密钥）数据量为：

   期望获得的正确 Pair 数量为 $s$ 

   
$$
\begin{align}
s \times |\Delta_{in}|\ (resp. |\Delta_{out}|)
\end{align}
$$



### Truncated D-MITM



#### 复杂度分析

$$
\begin{aligned}
\mathcal{T} & =2^{p-\delta_{in}}\times2^{|k_{in}\cap k_{out}|}(2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|}+2^{|k_{out}|+\delta_{out}-|k_{in}\cap k_{out}|}) \\
 & +2^{p-\delta_{in}}\times2^{|k_{in}\cap k_{out}|}(2^{|k_{in}|+\delta_{in}+|k_{out}|+\delta_{out}-2|k_{in}\cap k_{out}|-n})
\end{aligned}
$$



### Improved Parallel Partition (more generic)

**（For Truncated Differential）**

两方面改进（sharing 相同的逻辑）：

1. 对全状态密钥加 （Full Key Addition） 也可以用 Parallel Partition 扩展 1 轮；
2. 对非全状态密钥加 （Non-Full Key Addition） 可以用 Parallel Partition 扩展 2 轮.



<img src="https://github.com/user-attachments/assets/cac6c058-c804-423c-8010-9dd2b87fc7c1" width = "500" height = "300" div align=center />



#### 原理与假设

如上图，在攻击最后添加 1-2 轮，D-MITM 攻击末尾状态为 $A$ , 加 1-2 轮后状态为 $B$. 对 Full Key Addition 的分组密码，可在 D-MITM 攻击末尾加上一轮. 

如上图，通过固定 $A,B$ 上 $F$ 个 words，可以实现和 basic parallel partition 类似的效果:

* 当固定的 $F$ 个 words 所对应的 $k_F$ 可以由 $k_{in} \cup k_{out}$ 推出，则该方法与 basic parallel partition 相同；
* 当固定的 $F$ 个 words 所对应的 $k_F$ 不能（全部）由 $k_{in} \cup k_{out}$ 推出，则匹配后留下的 Pairs 变多，具体的下面解释.



因为是截断差分，所以状态有 $W$ 个 words, 假设每个 word 的大小为 $s$ bits, 则 $n=Ws$. 若没有任何条件，则扩展 1-2 轮的代价为需要将攻击重复 $2^{Ws}$ 次，数据量为 $2^p$.（若只期望留下一个正确 Pair，则未进行扩展时需要重复攻击的次数为 1 , 且数据量为 $2^p$ ）现假设将 $W$ 中 $F$ 个 words 固定下来，则所需要重复的攻击次数缩减为 $2^{p-(W-F)s}$，数据量为 $2^p$. 或，理解为有 $2^{(W-F)s}$ 个 structure，每个 structure 包含 $2^p$ 的数据量.

#### 方法与步骤

有区分器概率为 $2^p<1$，扩展后，在末尾（也可以在首部）增加 1-2 轮. 固定 $Fs$ bits 数据，并标记这些位置涉及的密钥 $k_F$ .

由于额外的扩展轮，但有 $Fs$ bits 数据被固定，所以在两端产生的 Paris 数量增加 $2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|}\rightarrow 2^{(W-F)s}\times2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|}$. 为满足至少找到 1 个正确 Pair，重复计算的次数减少 $2^{p-\delta_{in}+|k_{in}\cap k_{out}|}\rightarrow 2^{p-(W-F)s-\delta_{in}+|k_{in}\cap k_{out}|}$ .

将扩展产生的额外涉及状态，以 word 为单位分为两组 $2^{W}=2^{F}\times 2^{W-F}$ , 其中 $F$ words 选为固定位置，$W-F$ words 为随机位置. 对 $2^{(W-F)s}$ 个 structures 里的每一个，进行如下操作：

* 并行的，对 $A$ ，由于有 $2^{(W-F)s}$ 个 $P\rightarrow A$ ，所以 $(A,\widetilde{A},k_{out})$ 的数量为  $2^{(W-F)s}\times2^{|k_{out}|+\delta_{out}-|k_{in}\cap k_{out}|}$  个.
* 并行的，对 $B$ ，将其解密到明文 $(P,\widetilde{P},k_{in})$ , 然后计算到 $\widehat{A}$，与上面同理, $(B,\widetilde{B},\widehat{A},k_{in})$ 的数量为 $2^{(W-F)s}\times2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|}$ .
* 匹配 $\widetilde{A}$ 与 $\widehat{A}$ ：
  * 因为匹配时需要满足 $A\oplus B = \widetilde{A} \oplus \widetilde{B}$ 的条件，所以有 $2^{-F}$ bits 的条件可用于过滤.
  * 若固定部分 $F$ 个 words 上涉及的密钥 $k_F$ 能够被 $k_{in}, k_{out}$ 推出，则在匹配时会产生 $2^{k_f-F}$ bits 条件用于过滤.
  * 此外，$A,B$ 之间还可能存在 $2^L$ bits 的线性条件，==和上面一条有什么关系？==



#### 复杂度分析


$$
\begin{aligned}
\mathcal{T}=& 2^{p-(W-F)s-\delta_{in}+|k_{in}\cap k_{out}|}\times(2^{(W-F)s}\times2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|}+\\
& 2^{(W-F)s}\times2^{|k_{out}|+\delta_{out}-|k_{in}\cap k_{out}|}+2^{|k_{in}|+\delta_{in}+|k_{out}|+\delta_{out}+2(W-F)s-Fs-L-2|k_{in}\cap k_{out}|}).
\end{aligned}
$$
