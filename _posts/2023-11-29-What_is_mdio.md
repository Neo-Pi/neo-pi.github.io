---
layout: post
title: MDIO 管理接口速记
subtitle: 帧格式与 PRE、ST、OP 等字段；软件侧轮询与寄存器偏移（整理自 IEEE 802.3）
---

资料来源：IEEE Std 802.3™-2018, *IEEE Standard for Ethernet* SECTION 2（Clause 22 管理帧等相关说明）。

## MDIO 在做什么

**MDIO（Management Data Input/Output）** 是 MAC 与 PHY 之间的**串行管理接口**，配合 **MDC（Management Data Clock）** 在二者之间传送**控制信息与状态**（读/写 PHY 内部寄存器），与承载以太网帧的 **MII/GMII/RGMII** 数据通路是分开的。

**MDC：** 规范对最小时钟周期有要求（例如常见表述为**最小周期约 400 ns**，对应约 **2.5 MHz** 量级上限思路；具体实现以所用 PHY 与 MAC IP 手册为准）。

<figure class="figure-full">
  <img src="/img/posts/01e1cf46-43fa-48b0-b91d-18033a3c1e10.png" alt="MDC 时钟与 MDIO 采样关系示意">
</figure>

## 管理帧里各字段（名词）

以下位宽与 Clause 22 **帧格式**一致（读/写事务在 MDIO 上的比特顺序）。

| 字段 | 含义 | 位宽（典型） |
|------|------|----------------|
| **PRE** | Preamble：事务前在 MDIO 上保持**高**的一段序列，常见为 **32 个 MDC 周期**（32 bit） | 32 |
| **IDLE** | 空闲：MDIO 为高阻，由 PHY 侧上拉为高；**1 bit** 量级描述的是进入帧前的空闲条件 | 1 |
| **ST** | Start of frame：由低到高的跳变，**起始帧**，2 bit | 2 |
| **OP** | Operation code：读为 `2'b10`，写为 `2'b01` | 2 |
| **PHYAD** | PHY Address：总线上多颗 PHY / 多端口时的 **PHY 编号** | 5 |
| **REGAD** | Register Address：目标 PHY 内**寄存器索引**；其中许多为 802.3 **公共定义** | 5 |
| **TA** | Turnaround：周转区间，避免多驱动冲突，**2 bit**（读事务中主机与 PHY 切换驱动） | 2 |
| **DATA** | 16 bit 数据 | 16 |

<figure class="figure-full">
  <img src="/img/posts/eae66c84-e3e2-40fd-b5b9-b8278b1d327b.png" alt="帧数据管理格式">
  <figcaption><sub>图：帧数据管理格式</sub></figcaption>
</figure>

<figure class="figure-full">
  <img src="/img/posts/575c00b8-ddcf-4e2e-8c49-7c247bee9935.png" alt="mdio读写时序">
  <figcaption><sub>图：mdio读写时序</sub></figcaption>
</figure>

## 软件侧：通过 MAC 侧 CSR 发起一次读

MAC 侧通常会暴露一组 **CSR（控制/状态寄存器）**，由软件写入 **PHY 地址、寄存器地址、分频、命令位** 等，硬件在 MDIO/MDC 上**自动拼出**符合 Clause 22 的波形。  
**基地址与寄存器排布因芯片而异**，下文中**不写出具体 SoC 的物理基址**，统一用符号 **`BASE`** 表示「该以太网 MAC/MDIO 控制器在系统地址映射中的基地址」；**偏移 `0x200` / `0x204` 仅示意「控制寄存器 / 数据寄存器」的相对关系**，实现时请**以你所用手册的绝对地址与位域为准**。

<figure class="figure-full">
  <img src="/img/posts/d39b77ff-395e-4c38-9124-6146f6d15c36.png" alt="GMII Busy 状态位示意">
  <figcaption><sub>图：GMII/MDIO 控制寄存器 busy（GB）相关位域示意，以所用 IP 手册为准</sub></figcaption>
</figure>

读写前一般需轮询 **忙/闲** 或 **GB（GMII Busy 等命名因 IP 而异）** 状态位，避免在上一次 MDIO 事务未完成时再次下发命令。

### 读操作流程（示例步骤）

以下 **Address** 均写作 **`BASE + 偏移`**；**Bit** 表示该 CSR 内的位域（示意，**务必对照 TRM**）。

1. **读 idle / busy 状态**  
   - Address: `BASE + 0x200`  
   - Bit: `[0]`（或手册定义的 busy 位）

2. **写 REGAD**：目标 PHY 内部寄存器地址  
   - Address: `BASE + 0x200`  
   - Bit: `[20:16]`（示意）

3. **写 PHYAD**：总线上的 PHY 地址（单 MAC 多 PHY 时区分器件）  
   - Address: `BASE + 0x200`  
   - Bit: `[25:21]`（示意）

4. **配置 MDC 分频**：相对 CSR 时钟的分频比  
   - Address: `BASE + 0x200`  
   - Bit: `[11:8]`（示意）

5. **写 GOC（GMII Operation Command，命名因 IP 而异）**  
   - Address: `BASE + 0x200`  
   - Bit: `[3:2]`  
   - 读命令：将 **Bit2、Bit3** 置为手册规定的读编码（原文示例为二者均置 1 表示读，**以手册为准**）

6. **置位 GB / Go**：启动一次 MDIO 事务  
   - Address: `BASE + 0x200`  
   - Bit: `[0]`（示意）

7. **等待硬件完成**：按手册要求插入延时或轮询 busy

8. **再次读 idle / busy**，确认事务结束

9. **读 DATA**  
   - Address: `BASE + 0x204`  
   - Bit: `[15:0]`

---

**小结：** MDIO 帧字段由 802.3 约束；**软件看到的是 MAC 侧 CSR**，其 **BASE 与位域完全依赖 SoC / IP**。本文已**隐去真实基地址**，只保留「控制寄存器 + 数据寄存器」的相对偏移思路，避免与特定芯片绑定。
