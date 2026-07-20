# Parallel Partition



## Differential MITM Attack
> from Section 2.2 of Paper [22-CC-Differential Meet-In-The-Middle Cryptanalysis](https://link.springer.com/chapter/10.1007/978-3-031-38548-3_9)

### 原理与假设

$n$-bit 分组密码 $E$，有如下图的区分器与扩展：

<p align="center">
<img src="https://github.com/user-attachments/assets/93471796-555c-41da-9b9e-9fad9f48de36" width = "300" height = "500" div align=center />
<\p>

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



## Basic Parallel Partitioning in Differential MITM

> Based on Section 2.2 of  [22-CC-Differential Meet-In-The-Middle Cryptanalysis](https://link.springer.com/chapter/10.1007/978-3-031-38548-3_9)
>
> 下文忽略影响成功率的常数因子，并以基本加密、解密或列表处理操作为时间复杂度单位。（refined by AI）

### 1. 基本设定

考虑一个分组长度为 $n$ 的分组密码，以及一个概率为 $2^{-p}$ 的差分区分器，其中 $p>0$ 是区分器概率的负对数。

基础 differential MITM（D-MITM）攻击需要处理大约 $2^p$ 个独立的基准明密文实例 $(P_\ell,C_\ell)$，从而期望至少有一个实例对应的消息对通过该差分区分器。

记：

| 符号                                                  | 含义                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| $k_{\mathrm{in}}$                                     | 从明文侧构造候选消息对所需的密钥信息                         |
| $k_{\mathrm{out}}$                                    | 从密文侧构造候选消息对所需的密钥信息                         |
| $I=\lvert k_{\mathrm{in}}\cap k_{\mathrm{out}}\rvert$ | 两侧公共密钥信息的比特数                                     |
| $k$                                                   | 主密钥长度                                                   |
| $m$                                                   | 新增轮中受轮密钥加影响的状态比特数                           |
| $k_m$                                                 | 不能由 $k_{\mathrm{in}}\cup k_{\mathrm{out}}$ 确定的新增轮密钥信息量 |

> [!IMPORTANT]
> 这里的 $2^p$ 是需要覆盖的**基准 D-MITM 实例数**，并不一定等于攻击的数据复杂度。
>
> 对于基础 D-MITM，数据复杂度通常为
>
> $$
> D=\min\left(2^n,2^{p+\min(\lvert k_{\mathrm{in}}\rvert,\lvert k_{\mathrm{out}}\rvert)}\right).
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

首先猜测两侧公共的 $I$ 比特密钥信息。

* 对于每个公共密钥猜测：

- 枚举 $X$ 的 $2^m$ 个取值，并枚举 $k_{\mathrm{out}}\setminus k_{\mathrm{in}}$，得到候选列表，大小为

$$
\lvert L_X\rvert = 2^{m+\lvert k_{\mathrm{out}}\rvert-I}
$$

- 枚举 $Y$ 的 $2^m$ 个取值，并枚举 $k_{\mathrm{in}}\setminus k_{\mathrm{out}}$，得到候选列表，大小为

$$
\lvert L_Y\rvert = 2^{m+\lvert k_{\mathrm{in}}\rvert-I}
$$

这里使用 $X$-side 和 $Y$-side，而不固定称为 upper part 或 lower part，因为在攻击首部或尾部添加 partition 时，两侧的命名可能互换。

两个列表的笛卡尔积包含

$$
2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I+2m}
$$

组候选匹配，比单个基础 D-MITM 实例增加了 $2^{2m}$ 倍。

### 5. Partition 提供的匹配条件

对于来自两个列表的候选

$$
(X,\widetilde X,j)
\qquad\text{和}\qquad
(Y,\widetilde Y,i),
$$

需要验证它们是否能通过同一个轮密钥 $K_r$ 连接。

#### 5.1 不受密钥影响部分 ($n-m$) bits filter

由于这 $n-m$ 个比特不经过密钥加，原始状态的这些比特已经由 partition 固定。对于关联状态，还需要满足

$$
\widetilde X_{\mathrm{free}} = \widetilde Y_{\mathrm{free}}.
$$

这提供 $n-m$ 比特的过滤。

#### 5.2 差分一致性 ($m$) bits filter

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
X_{\mathrm{key}}\oplus\widetilde X_{\mathrm{key}} = Y_{\mathrm{key}}\oplus\widetilde Y_{\mathrm{key}}.
$$

该条件提供 $m$ 比特的过滤。

#### 5.3 轮密钥一致性 ($m-k_m$) bits filter

候选状态还必须给出正确的新增轮密钥：

$$
K_r = X_{\mathrm{key}}\oplus Y_{\mathrm{key}} = \widetilde X_{\mathrm{key}}\oplus\widetilde Y_{\mathrm{key}}.
$$

若相关的 $m$ 比特轮密钥均可由 $k_{\mathrm{in}}\cup k_{\mathrm{out}}$ 确定，即 $k_m=0$，则该条件再提供 $m$ 比特过滤。

若其中有 $k_m$ 个独立比特不能由已有密钥信息确定，则这些比特只能由状态关系推导或额外猜测，因而轮密钥一致性只提供

$$
m-k_m
$$

比特的有效过滤。



因此，parallel partitioning 的**总过滤量**为

$$
(n-m)+m+(m-k_m) = n+m-k_m.
$$

在理想情形 $k_m=0$ 下，总过滤量为

$$
n+m.
$$

---

### 6. 为什么匹配数量不会增加

对于每个 partition 和每个公共密钥猜测，匹配前有候选数量为：

$$
2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I+2m}
$$

经过 $n+m-k_m$ 比特过滤后，期望剩余

$$
2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I+2m-(n+m-k_m)} = 2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I+m-n+k_m}
$$

组候选。

再乘以 $2^I$ 个公共密钥猜测以及 $2^{p-m}$ 个 partition，得到总候选数

$$
2^{p+\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert -I-n+k_m}.
$$

当 $k_m=0$ 时，该数量化为

$$
2^{p+\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-I-n},
$$

*与基础 D-MITM 攻击完全相同*。



也可以直接比较：

- 分别执行 $2^m$ 次基础 D-MITM 时，匹配候选数为

$$
2^m\cdot 2^{\lvert k_{\mathrm{in}}\rvert+\lvert k_{\mathrm{out}}\rvert-2I-n};
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

> [!NOTE]
>
> 当 $p>m$，这一基础条件满足，且以下两条件满足其一，使用 parallel partition 与基础 D-MITM 时间复杂度相同：
>
> 1. 当 $k_m=0$ ，即 $m$ bits extra key 可全部由 $k_{in} \cup k_{out}$ 推导出时，时间复杂度保持与 Basic D-MITM 完全相同；
>
> 2. 但当 $k_m >0$ ，当 Matching 部分的时间复杂度不为 时间复杂度 的主导项时，时间复杂度依然可以保持。

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
\mathcal{T}_{\mathrm{PP}} = 
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
\mathcal{T}_{\mathrm{PP}} =
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
\mathcal{M}_{\mathrm{PP}} =
2^{m+\min(
\lvert k_{\mathrm{in}}\rvert-I,\,
\lvert k_{\mathrm{out}}\rvert-I
)}.
$$

相比基础 D-MITM，内存通常增加 $2^m$ 倍。因此，parallel partitioning 并非在所有复杂度指标上完全免费。

在相同的数据获取模型下，总数据复杂度保持为

$$
\mathcal{D}_{\mathrm{PP}} =
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
---

## Improved Parallel Partition in D-MITM

> From Section 4.1 of Paper [24-EC-Improved Differential Meet-in-the-Middle Cryptanalysis](https://link.springer.com/chapter/10.1007/978-3-031-58716-0_10)

### Truncated Differentials

在介绍 improved parallel partition 之前，先明确 truncated differential 的含义。

普通 differential 通常固定一对具体差分，而 truncated differential 考虑的是输入、输出差分集合： $\Delta_{in},\Delta_{out}\subseteq\mathbb{F}_2^n.$

记 $|\Delta_{in}|=2^{\delta_{in}},|\Delta_{out}|=2^{\delta_{out}}.$ 即 给定一个 $P\in\{\Delta_{in}\}$ 可以张成大小为 $|\Delta_{in}|$ 的空间.

其中，集合中的差分通常具有相同的 word-wise activity pattern，但其具体差分值可以不同.

#### 1. 有效截断差分

对于理想的 $n$-bit permutation，在给定输入差分属于 $\Delta_{in}$ 的条件下，输出差分落入 $\Delta_{out}$ 的基准概率为

$$P_{\mathrm{rand}}=\frac{|\Delta_{out}|}{2^n}=2^{\delta_{out}-n}.$$

因此，一个正向截断差分只有在满足

$$P\left(\Delta_{in}\stackrel{E}{\longrightarrow}\Delta_{out}\right)>\frac{|\Delta_{out}|}{2^n}$$

时，才可以相对于随机置换提供有效区分。

若其正向概率记为 $P\left(\Delta_{in}\stackrel{E}{\longrightarrow}\Delta_{out}\right)=2^{-p},$ 则有效性条件等价于 $p<n-\delta_{out}.$

#### 2. 截断差分具有方向性

由于输入和输出差分集合的大小可能不同，截断差分的正向和反向概率通常不相等。具体地，

$$P\left(\Delta_{out}\stackrel{E^{-1}}{\longrightarrow}\Delta_{in}\right)=P\left(\Delta_{in}\stackrel{E}{\longrightarrow}\Delta_{out}\right)\times\frac{|\Delta_{in}|}{|\Delta_{out}|}.$$

若反向概率记为 $2^{-p'}$，则 $p'=p+\delta_{out}-\delta_{in}.$

#### 3. 所需 pair 数量

若截断差分的概率为 $2^{-p}$，为了期望获得一个 right pair，需要测试约 $2^p$ 个有效 differential pairs。

对于一个固定的基础明文 $P$ 和一个固定的正确 $k_{in}$，集合 $\Delta_{in}$ 中的每个差分都对应一个候选 $\widetilde P$。因此，每个 $P$ 可以产生 $|\Delta_{in}|=2^{\delta_{in}}$ 个 differential pairs。故期望获得一个 right pair 时，基础明文 $P$ 的数量为 $2^{p-\delta_{in}}.$

更一般地，若期望获得 $s$ 个 right pairs，则需要约 $s2^p$ 个有效 pairs，或约 $s2^{p-\delta_{in}}$ 个基础明文。

### Truncated Differential MITM

设密码分解为 $E=E_{out}\circ E_m\circ E_{in},$ 其中中间部分 $E_m$ 存在概率为 $2^{-p}$ 的截断差分 $\Delta_{in}\stackrel{E_m}{\longrightarrow}\Delta_{out}.$

记：

- $k_{in}$：从明文端生成满足 $\Delta_{in}$ 的候选 pair 所需的密钥信息；
- $k_{out}$：从密文端生成满足 $\Delta_{out}$ 的候选 pair 所需的密钥信息；
- $k_{in}\cap k_{out}$：两侧密钥信息之间可由 key schedule 建立的公共独立信息。

对于每个基础明文和固定的公共密钥信息，上侧和下侧分别产生 $2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|}$ 和 $2^{|k_{out}|+\delta_{out}-|k_{in}\cap k_{out}|}$ 个候选。

#### 复杂度分析

因为每个 $P$ 可以产生 $2^{\delta_{in}}$ 个空间, 所以需要重复的次数为 $2^{p-\delta_{in}}$;

- 对每个选择的明文, 先猜测 $2^{|k_{in}\cap k_{out}|}$ 密钥, 对上下部分分别进行加解密 $2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|}+2^{|k_{out}|+\delta_{out}-|k_{in}\cap k_{out}|}$
- 对每个猜测的明文, 及猜测 $2^{|k_{in}\cap k_{out}|}$ 密钥, Matching: $2^{|k_{in}|+\delta_{in}+|k_{out}|+\delta_{out}-2|k_{in}\cap k_{out}|-n}$

时间复杂度:

$$\mathcal{T}=2^{p-\delta_{in}}\times2^{|k_{in}\cap k_{out}|}\left(2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|}+2^{|k_{out}|+\delta_{out}-|k_{in}\cap k_{out}|}\right)+2^{p-\delta_{in}}\times2^{|k_{in}\cap k_{out}|}\left(2^{|k_{in}|+\delta_{in}+|k_{out}|+\delta_{out}-2|k_{in}\cap k_{out}|-n}\right).$$

数据复杂度:

$$D=\min\{2^n,2^{p-\delta_{in}+\min{|k_{in}|+\delta_{in},|k_{out}|+\delta_{out}}}\}.$$

内存复杂度:

$$M=\min\{2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|},2^{|k_{out}|+\delta_{out}-|k_{in}\cap k_{out}|}\}.$$

### Improved Parallel Partition

Improved parallel partition 可以应用于普通 D-MITM 和 truncated D-MITM。它将原来主要适用于 partial-state key addition 的 parallel partition 推广到以下两种情形:

对具有 whole-state key addition 的 SPN，可以额外扩展一轮；

对具有 partial-state key addition 的 SPN，可以扩展多于一轮；(如 SKINNY 中可扩展两轮)

<p align="center">
<img src="https://github.com/user-attachments/assets/cac6c058-c804-423c-8010-9dd2b87fc7c1" width="500" height="300" div align="center" />
<\p>

基本设置

设密码状态由 $W$ 个 $s$-bit words 组成，因此 $n=Ws.$

记:

- $A$：原 D-MITM 攻击的末尾状态;
- $B$：在 $A$ 之后额外**扩展一轮或多轮**得到的状态;
- $F$：施加独立条件的 word 数量;
- $(W-F)s$：施加条件后仍然自由的状态比特数.

==> 若不施加任何条件, $A$ 和 $B$ 各有 $2^{Ws}$ 种可能取值.

==> 现在在新增轮的内部状态上施加 $Fs$ 个独立条件，[例如: 1) 将某些 words 固定为特定值；2) 对若干内部 words 施加线性关系.] 这些条件将 $A$ 和 $B$ 的可能取值数分别缩减为 $2^{(W-F)s}.$ 这些可能值分别构成一对大小为 $2^{(W-F)s}$ 的 **initial structures**.

**所选的 $Fs$-bit 条件应满足**: 结合 $k_{in}$, 能够从一侧**唯一确定** $B$ 的等价 $Fs$ bits；结合 $k_{out}$，能够从另一侧**唯一确定** $A$ 的等价 $Fs$ bits.

#### Parallel treatment

对于每一对**大小为 $2^{(W-F)s}$ 的 structures**，同时执行上侧和下侧的 D-MITM 计算.

在 truncated D-MITM 中，对每个 $k_{in}\cap k_{out}$ 的猜测:

- 上侧产生 $2^{(W-F)s}\times2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|}$ 个候选；

- 下侧产生 $2^{(W-F)s}\times2^{|k_{out}|+\delta_{out}-|k_{in}\cap k_{out}|}$ 个候选.

由于每次 parallel treatment **同时覆盖 $2^{(W-F)s}$ 个基础状态**, 攻击的重复次数从 $2^{p-\delta_{in}}$ 减少为 $2^{p-(W-F)s-\delta_{in}}.$ structure 的大小与重复次数相互抵消: $2^{(W-F)s}\times2^{p-(W-F)s-\delta_{in}}=2^{p-\delta_{in}}.$

换言之，parallel partition 重新组织了数据和计算方式:

==> 产生 $2^{p-(W-F)s-\delta_{in}}$ 个 initial structure, 每个 structure 包含 $2^{(W-F)s}$ 个明文 $P$, 而每个 $P$ (在每次固定的密钥猜测下) 可张成 $2^{\delta_{in}}$ 个 $\widetilde P$.

#### Matching and sieving

合并两侧候选列表时使用两类相互独立的过滤条件。

1. **Starting-point matching**

在施加初始条件的 $F$ 个 words 上, 两侧计算出的 **$\widetilde A$ 和 $\widetilde B$ 所对应的 $Fs$ bits 必须一致**, 因此得到 **$2^{-Fs}$ 的过滤因子**. 这些 $Fs$ bits 可能需要借助候选中的 $k_{in}$ 和 $k_{out}$ 才能计算. 若检查它们需要额外的独立密钥信息, 则这些密钥信息必须计入 $k_{in}$ 或 $k_{out}$. 准确地说, 若需要**额外猜测 $|k_F|$ bits (固定部分涉及的额外密钥量)**, 而 matching 提供 $Fs$ bits 的过滤, 则对应的**候选数量净因子为 $2^{|k_F|-Fs}.$** 如果 $k_F$ 可以由已经涉及的 $k_{in}\cup k_{out}$ 推导, 即 $|k_F|=0$, 则不会引入新的独立密钥猜测.

2. **Additional linear relations**

除上述 $Fs$-bit matching 外, $A$ 与 $B$ 之间以及 $\widetilde A$ 与 $\widetilde B$ 之间还可能存在 $L$ 个独立线性关系，由此得到额外的 $2^{-L}$ 过滤因子.

这两类条件的作用不同:

- $Fs$-bit matching 检查 initial structure 的起始条件是否由两侧一致满足;
- $L$-bit sieving 使用新增轮所提供的、独立于起始条件的线性关系, 其中 $L\leq 2(W-F)s.$ (新增一轮或两轮的确定性轮函数在 $A,B,\widetilde A, \widetilde B$ 之间诱导出的**精确一致性方程**。对于正确的状态与密钥候选，这些方程必然成立；错误候选以约 $2^{−L}$ 的概率通过)

当能够获得完整的 sieving potential 时，希望找到总计 $2(W-F)s$ 个独立线性关系。若这些关系的验证需要额外密钥信息，则相应密钥 bits 也必须加入 $k_{in}$ 或 $k_{out}$；若关系能够消去未知轮密钥，则无需额外猜测。

适用条件: 结构并行化本身要求 $(W-F)s\leq p,$ 否则一次 structure 覆盖的状态数超过了区分器所需的有效尝试数。

但该条件本身不足以保证总体攻击复杂度不变。还需要保证:

1. $Fs$-bit matching 和 $L$-bit linear relations 提供足够的候选过滤;
2. 为检查这些条件而新增的独立密钥信息不会提高攻击复杂度的主项;
3. 最终剩余候选数低于穷举搜索的复杂度.


$$
\begin{aligned}
\mathcal{T}=&2^{p-(W-F)s-\delta_{in}+|k_{in}\cap k_{out}|}\times\\
&\left(2^{(W-F)s}\times2^{|k_{in}|+\delta_{in}-|k_{in}\cap k_{out}|}+2^{(W-F)s}\times2^{|k_{out}|+\delta_{out}-|k_{in}\cap k_{out}|}+2^{|k_{in}|+\delta_{in}+|k_{out}|+\delta_{out}+2(W-F)s-Fs-L-2|k_{in}\cap k_{out}|}\right).
\end{aligned}
$$


其中：

- 前两项分别对应上侧和下侧候选列表的生成;
- 第三项对应两侧列表合并后，在 $Fs+L$ bits 条件下剩余的候选数量;
- 若检查 linear relations 需要额外密钥 bits, 则应将其加入 $|k_{in}|$ 或 $|k_{out}|$ 后重新评估复杂度.
