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

假设有概率为 $2^{-p}$ 的差分区分器，其中 $p$ 为区分器概率的负对数（ $p>0$ ）

$\bigstar$ 当分组密码的密钥加不是加在全状态上的时候（**非全状态密钥加（Non-Full Key Addition）**，典型算法有 $\texttt{SKINNY, GIFT, SIMON}$ ，parallel partition可以用来在增加复杂度的情况下增加攻击轮数，**ONE** round.

如下图所示，在区分器末尾添加一轮，密钥只加在 $m$ bits 状态上，若 $p>m$，则以上加一轮条件可以被满足.

<img src="https://github.com/user-attachments/assets/41a6a985-4011-481a-a627-f37cd4677d02" width = "500" height = "300" div align=center />

### 方法与步骤

如上图，在攻击最后添加一轮， $X$ 和 $Y$ 分别是 Key Addition 前后的状态（其中有 $n-m$ bits 未被 Key Addition 影响）

$\blacktriangleright$ 由于需要 $2^p$ 个明文来保证至少找到一个正确 pair，假设现有数据量即为 $2^p$，则在上图 $S_{r-1}$ 处即有 $2^p$ 个数据。将 $2^n$（实际是 $2^p$ 种情况） 在 $X$ 和 $Y$ 处进行划分，可化为 $2^m \times 2^{p-m}$ ：

* 其中 $2^m$ 对应受密钥影响的部分；
* $2^{p-m}$ 对应不受密钥影响的部分</u>，这部分同样需要多次取值（但不受密钥影响，每次不同取值对应 $2^m$ 次 basic D-MITM 的操作）来达到数据要求.

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

---

## Basic Parallel Partitioning in Differential MITM

> Based on Section 2.2 of  
> [22-CC-Differential Meet-In-The-Middle Cryptanalysis](https://link.springer.com/chapter/10.1007/978-3-031-38548-3_9)
>
> 下文忽略影响成功率的常数因子，并以基本加密、解密或列表处理操作为时间复杂度单位。

### 1. 基本设定

考虑一个分组长度为 $n$ 的分组密码，以及一个概率为 $2^{-p}$ 的差分区分器，其中 $p>0$ 是区分器概率的负对数。

基础 differential MITM（D-MITM）攻击需要处理大约 $2^p$ 个独立的基准明密文实例 $(P_\ell,C_\ell)$，从而期望至少有一个实例对应的消息对通过该差分区分器。

记：

| 符号 | 含义 |
|---|---|
| $k_{\mathrm{in}}$ | 从明文侧构造候选消息对所需的密钥信息 |
| $k_{\mathrm{out}}$ | 从密文侧构造候选消息对所需的密钥信息 |
| $I=\lvert k_{\mathrm{in}}\cap k_{\mathrm{out}}\rvert$ | 两侧公共密钥信息的比特数 |
| $k$ | 主密钥长度 |
| $m$ | 新增轮中受轮密钥加影响的状态比特数 |
| $k_m$ | 不能由 $k_{\mathrm{in}}\cup k_{\mathrm{out}}$ 确定的新增轮密钥信息量 |

> [!IMPORTANT]
> 这里的 $2^p$ 是需要覆盖的**基准 D-MITM 实例数**，并不一定等于攻击的数据复杂度。
>
> 对于基础 D-MITM，数据复杂度通常为
>
> $$
> D=\min\left(2^n,\;2^{p+\min(\lvert k_{\mathrm{in}}\rvert,\lvert k_{\mathrm{out}}\rvert)}\right).
> $$

---

### 2. 适用条件

假设在基础 D-MITM 攻击的末尾添加一轮。将该轮中密钥加之前和之后的状态分别记为 $X$ 和 $Y$，满足

$$
Y=X\oplus K_r.
$$

轮密钥 $K_r$ 只作用于状态中的 $m<n$ 个比特；剩余 $n-m$ 个比特不受密钥加影响。因此，在这些位置上恒有

$$
X_{\mathrm{free}}=Y_{\mathrm{free}}.
$$

典型的 partial-state key addition 算法包括 `SKINNY` 和 `GIFT`。对于 `SIMON` 等 Feistel/AndRX 密码，也可以利用类似思想，但需要根据其轮函数结构重新描述 partition。

基础 parallel partitioning 通常要求：

1. $p>m$，使一个大小为 $2^m$ 的 partition 可以代替 $2^m$ 次基础 D-MITM 操作；
2. 新增轮密钥的相关部分能够由 $k_{\mathrm{in}}\cup k_{\mathrm{out}}$ 确定，即理想情况下 $k_m=0$；
3. 密钥加之后的公开可逆操作已经被消去，或被吸收到状态 $Y$ 的定义中，使新增部分可表示为 $Y=X\oplus K_r$。

在这些条件下，parallel partitioning 可以增加一轮攻击，而不增加主导的时间和数据复杂度。峰值内存复杂度通常会增加。

<p align="center">
  <img src="https://github.com/user-attachments/assets/41a6a985-4011-481a-a627-f37cd4677d02" width="500" alt="Basic parallel partitioning in differential MITM">
</p>

---

### 3. Partition 的构造

对于一个 partition：

1. 固定 $X$ 和 $Y$ 中不受密钥加影响的 $n-m$ 个比特；
2. 让受密钥加影响的其余 $m$ 个比特遍历全部 $2^m$ 个取值。

因此，一个 partition 同时包含 $2^m$ 个基准状态，而不是只处理一个状态。

为了总共覆盖约 $2^p$ 个基准实例，只需构造

$$
2^{p-m}
$$

个不同的 partition。

换言之，parallel partitioning 并没有减少需要覆盖的基准实例总数，而是将原本的 $2^p$ 次独立操作组织为

$$
2^{p-m}\times 2^m=2^p
$$

个实例，并在每个 partition 内并行处理其中的 $2^m$ 个实例。

> [!NOTE]
> $2^{p-m}$ 不是“不受密钥影响部分的取值数”本身，而是所需的 partition 数量。每个 partition 由一组新的固定比特值定义，并包含 $2^m$ 个自由变化的状态。

---

### 4. 两侧候选列表的生成

首先猜测两侧公共的 $I$ 比特密钥信息。对于每个公共密钥猜测：

- 枚举 $X$ 的 $2^m$ 个取值，并枚举 $k_{\mathrm{out}}\setminus k_{\mathrm{in}}$，得到大小为

  $$
  \lvert L_X\rvert
  =
  2^{m+\lvert k_{\mathrm{out}}\rvert-I}
  $$

  的候选列表；

- 枚举 $Y$ 的 $2^m$ 个取值，并枚举 $k_{\mathrm{in}}\setminus k_{\mathrm{out}}$，得到大小为

  $$
  \lvert L_Y\rvert
  =
  2^{m+\lvert k_{\mathrm{in}}\rvert-I}
  $$

  的候选列表。

这里使用 $X$-side 和 $Y$-side，而不固定称为 upper part 或 lower part，因为在攻击首部或尾部添加 partition 时，两侧的命名可能互换。

两个列表的笛卡尔积包含

$$
2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I+2m}
$$

组候选匹配，比单个基础 D-MITM 实例增加了 $2^{2m}$ 倍。

但是，一个 partition 同时代替了 $2^m$ 次基础 D-MITM 操作。因此，与分别执行这 $2^m$ 次操作相比，真正需要抵消的额外候选增长只有 $2^m$ 倍。

---

### 5. Partition 提供的匹配条件

对于来自两个列表的候选

$$
(X,\widetilde X,j)
\qquad\text{和}\qquad
(Y,\widetilde Y,i),
$$

需要验证它们是否能通过同一个轮密钥 $K_r$ 连接。

#### 5.1 不受密钥影响部分

由于这 $n-m$ 个比特不经过密钥加，原始状态的这些比特已经由 partition 固定。对于关联状态，还需要满足

$$
\widetilde X_{\mathrm{free}}
=
\widetilde Y_{\mathrm{free}}.
$$

这提供 $n-m$ 比特的过滤。

#### 5.2 差分一致性

在受密钥影响的 $m$ 个比特上，同一个轮密钥会在差分中抵消：

$$
\begin{aligned}
Y\oplus\widetilde Y
&=(X\oplus K_r)\oplus(\widetilde X\oplus K_r)\\
&=X\oplus\widetilde X.
\end{aligned}
$$

因此必须满足

$$
X_{\mathrm{key}}\oplus\widetilde X_{\mathrm{key}}
=
Y_{\mathrm{key}}\oplus\widetilde Y_{\mathrm{key}}.
$$

该条件提供 $m$ 比特的过滤。

#### 5.3 轮密钥一致性

候选状态还必须给出正确的新增轮密钥：

$$
K_r
=
X_{\mathrm{key}}\oplus Y_{\mathrm{key}}
=
\widetilde X_{\mathrm{key}}\oplus\widetilde Y_{\mathrm{key}}.
$$

若相关的 $m$ 比特轮密钥均可由 $k_{\mathrm{in}}\cup k_{\mathrm{out}}$ 确定，即 $k_m=0$，则该条件再提供 $m$ 比特过滤。

若其中有 $k_m$ 个独立比特不能由已有密钥信息确定，则这些比特只能由状态关系推导或额外猜测，因而轮密钥一致性只提供

$$
m-k_m
$$

比特的有效过滤。

因此，parallel partitioning 的总过滤量为

$$
(n-m)+m+(m-k_m)
=
n+m-k_m.
$$

在理想情形 $k_m=0$ 下，总过滤量为

$$
n+m.
$$

---

### 6. 为什么匹配数量不会增加

对于每个 partition 和每个公共密钥猜测，匹配前有

$$
2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I+2m}
$$

组候选。

经过 $n+m-k_m$ 比特过滤后，期望剩余

$$
2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I
+2m-(n+m-k_m)}
=
2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I
+m-n+k_m}
$$

组候选。

再乘以 $2^I$ 个公共密钥猜测以及 $2^{p-m}$ 个 partition，得到总候选数

$$
2^{p+\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert
-I-n+k_m}.
$$

当 $k_m=0$ 时，该数量化为

$$
2^{p+\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-I-n},
$$

与基础 D-MITM 攻击完全相同。

也可以直接比较：

- 分别执行 $2^m$ 次基础 D-MITM 时，匹配候选数为

  $$
  2^m\cdot
  2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I-n};
  $$

- 使用一个 parallel partition 时，匹配候选数为

  $$
  2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I+2m}
  \cdot 2^{-(n+m)}.
  $$

两者均等于

$$
2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I+m-n}.
$$

---

### 7. 时间复杂度

parallel partitioning 的时间复杂度可以写为

$$
\begin{aligned}
\mathcal{T}_{\mathrm{PP}}
={}&
2^{p-m}\cdot 2^I
\Big(
2^{\lvert k_{\mathrm{in}}\rvert-I+m}
+
2^{\lvert k_{\mathrm{out}}\rvert-I+m}\\
&\qquad\qquad+
2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert
-2I+2m-(n+m-k_m)}
\Big)
+
2^{k-n+p}.
\end{aligned}
$$

其中，最后一项表示在得到 $k_{\mathrm{in}}\cup k_{\mathrm{out}}$ 后，对剩余主密钥信息进行穷举验证的成本；仅在需要恢复剩余密钥位时计入。

化简可得

$$
\boxed{
\mathcal{T}_{\mathrm{PP}}
=
2^{p+\lvert k_{\mathrm{in}}\rvert}
+
2^{p+\lvert k_{\mathrm{out}}\rvert}
+
2^{p+\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-I-n+k_m}
+
2^{k-n+p}
}.
$$

在理想情形 $k_m=0$ 下，

$$
\mathcal{T}_{\mathrm{PP}}
=
2^{p+\lvert k_{\mathrm{in}}\rvert}
+
2^{p+\lvert k_{\mathrm{out}}\rvert}
+
2^{p+\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-I-n}
+
2^{k-n+p},
$$

与基础 D-MITM 攻击的时间复杂度相同。

因此，“免费增加一轮”更准确的含义是：

> 当 $k_m=0$ 且其他适用条件成立时，新增轮不会增加攻击的主导时间复杂度和数据复杂度。

---

### 8. 内存和数据复杂度

在每个 partition 中，若存储两个列表中较小的一个，则峰值内存复杂度约为

$$
\mathcal{M}_{\mathrm{PP}}
=
2^{m+\min(
\lvert k_{\mathrm{in}}\rvert-I,\,
\lvert k_{\mathrm{out}}\rvert-I
)}.
$$

相比基础 D-MITM，内存通常增加 $2^m$ 倍。因此，parallel partitioning 并非在所有复杂度指标上完全免费。

在相同的数据获取模型下，总数据复杂度保持为

$$
\mathcal{D}_{\mathrm{PP}}
=
\min\left(
2^n,\,
2^{p+\min(
\lvert k_{\mathrm{in}}\rvert,\,
\lvert k_{\mathrm{out}}\rvert
)}
\right),
$$

与基础 D-MITM 相同。

---

### 9. 一个小例子

设

$$
n=16,\qquad
m=4,\qquad
p=12,
$$

并假设

$$
\lvert k_{\mathrm{in}}\rvert
=
\lvert k_{\mathrm{out}}\rvert
=
8,\qquad
I=2,\qquad
k_m=0.
$$

#### 基础 D-MITM

攻击需要执行约

$$
2^{12}
$$

次基准操作。

两侧列表生成的总成本分别为

$$
2^{12+8}=2^{20}.
$$

匹配后候选数量为

$$
2^{12+8+8-2-16}
=
2^{10}.
$$

#### 使用 parallel partitioning

每个 partition 包含

$$
2^4=16
$$

个基准状态，因此只需

$$
2^{12-4}=2^8
$$

个 partition。

对于每个公共密钥猜测，每侧列表大小为

$$
2^{8-2+4}=2^{10}.
$$

两个列表的笛卡尔积大小为

$$
2^{20}.
$$

parallel partition 提供

$$
n+m=16+4=20
$$

比特过滤，所以每个 partition、每个公共密钥猜测期望剩余一个候选。

总候选数量为

$$
2^8\cdot 2^2
=
2^{10},
$$

与基础 D-MITM 完全相同。

两侧列表生成的总成本也分别为

$$
2^8\cdot 2^2\cdot 2^{10}
=
2^{20},
$$

同样与基础攻击相同。

但每个 partition 中需要保存的列表从基础攻击的

$$
2^{8-2}=2^6
$$

增加至

$$
2^{8-2+4}=2^{10},
$$

即峰值内存增加了 $2^4$ 倍。

---

### 10. 核心理解

parallel partitioning 的本质不是减少差分区分器所需的 $2^p$ 个基准实例，而是：

> 将 $2^m$ 次相互独立的基础 D-MITM 操作合并到一个 structure 中，并利用新增轮的差分一致性和轮密钥一致性，抵消列表笛卡尔积带来的额外候选。

因此，在 $k_m=0$ 时，可以用更大的单次列表和更高的峰值内存，换取少 $2^m$ 倍的外层重复次数，从而在不提高主导时间和数据复杂度的情况下增加一轮攻击。

---




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
