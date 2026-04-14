---
layout: post
title: "RISC-V 编程速查手册"
subtitle: "收集整理了一些常用的指令以及常用的ToolChain选项"
---

## RISCV编程速查手册

该手册摘取自RISCV社区文档，仅负责翻译整理汇总，个别词意可能有误差，请配合官方文档阅读。

## 目录
* TOC
{:toc}

## 1.C语言

### 1.1.数据类型大小

| C语言类型       | 描述     | RISCV32 | RISCV64 |
| ----------- | ------ | -------:| -------:|
| char        | 字符型    | 1       | 1       |
| short       | 短整形    | 2       | 2       |
| int         | 整形     | 4       | 4       |
| long        | 长整形    | 4       | 8       |
| long long   | 超长整形   | 8       | 8       |
| void \*     | 指针     | 4       | 8       |
| float       | 单精度浮点型 | 4       | 4       |
| double      | 双精度浮点型 | 8       | 8       |
| long double | 超精度浮点型 | 16      | 16      |

### 1.2.工具链选项

仅列出RISCV平台的内容或者常见通用的内容，如果找不到某个内容，请移步至GNU社区下载对应文档

#### 1.2.1.gcc编译选项(Version:12.2)

由于版本不同，某些选项会失效，请移步至GNU社区查阅对应版本的gcc文档

* `-mbranch-cost=N`
  
  分支预测的代价设置为n条指令

* `-mplt` `-mno-plt`
  
  在生成PIC代码时，执行是否允许使用plt。忽略了非pic的内容。默认值为“-mplt”

* `-mabi=ABI`
  
  指定整数和浮点的调用约束,需要配合`-march`使用，选项有`ilp32` `ilp32f` `ilp32d` `lp64` `lp64f` `lp64d`,例如`-march=rv32i -mabi=ilp32`

* `-march=ISA`
  
  允许生成的指令的指令集，根据平台的指令集支持来配置参数，示例见上文

* `-mfdiv` `-mno-fdiv`
  
  是否使用硬件浮点除法和平方根指令。这需要对浮点寄存器的F或D扩展。默认情况下是在指定的体系结构中使用它们 有这些指令

* `-mdiv` `-mno-div`
  
  是否使用对整数除法的硬件指令。这就需要M的扩展。默认情况下，如果指定的体系结构有这些指令，则使用它们

* `-misa-spec=ISA-spec-string`
  
  指定非特权ISA文档版本，选项有`2.2` `20190608` `20191213`，默认是`20191213`

* `-mcpu=processor-string`
  
  指定内核型号，会根据型号做对应的优化，选项有`sifive-e20` `sifive-e21` `sifive-e24` `sifive-e31` `sifive-e34` `sifive-e76` `sifive-s21` `sifive-s51` `sifive-s54` `sifive-s76` `sifive-u54` `sifive-u74`

* `-mtune=processor-string`
  
  指定体系结构名称，会根据型号做对应的优化，选项有`sifive-3-series` `sifive-5-series` `sifive-7-series` `size`，`size`选项对应-Os

* `-mpreferred-stack-boundary=num`
  
  设置栈对齐大小，默认是4

* `-msmall-data-limit=N`
  
  将小于n字节的全局和静态数据放入一个特殊的部分（在某些目标上）

* `-msave-restore` `-mno-save-restore`
  
  是否使用库函数调用的较小但较慢的上下文。默认情况下是使用内联上下文

* `-mshorten-memrefs` `-mno-shorten-memrefs`
  
  是否将大偏移量的load store操作转换成一个小偏移量的操作，这么做会增加一些指令，以空间换时间，目前只支持32位整数load store

* `-mstrict-align` `-mno-strict-align`
  
  是否生成未对齐的内存访问。默认值取决于正在优化的处理器是否支持快速未对齐访问

* `-mcmodel=CODE_MODEL`
  
  为中低代码模型生成代码。程序及其静态定义的符号必须位于单个2 GiB地址范围内，`medlow`并且必须位于绝对地址−2 GiB和+2 GiB之间。程序可以是静态链接的或动态链接的。这是默认的代码模型，选项有`medlow` （相对于0的寻址模式）`medany`（相对于pc的寻址模式）

* `-mexplicit-relocs` `-mno-explicit-relocs`
  
  在处理符号地址时，是否使用汇编程序重定位操作符。另一种选择是使用汇编程序宏，这可能会限制优化

* `-mrelax` `-mno-relax`
  
  是否利用链接器(linker) 松弛来减少实现符号地址所需的指令数量。默认会开启 `-mrelax`

* `-memit-attribute` `-mno-emit-attribute`
  
  是否将RISCV属性记录到elf文件的额外信息中，要求binutils最低版本为2.32

* `-malign-data=type`
  
  控制GCC如何对齐数组、结构或共用体的变量和常量。类型支持的值是“xlen”，它使用x寄存器宽度作为对齐值，它使用2的n次幂对齐。默认值为“xlen”。

* `-mbig-endian`
  
  生成大端代码

* `-mlittle-endian`
  
  生成小端代码

* `-mstack-protector-guard=guard`
  
  `-mstack-protector-guard-reg=reg`
  
  `-mstack-protector-guard-offset=offset`
  
  使用canary at guard生成堆栈保护代码。仅适用于Linux

#### 1.2.2.objdump 常用选项

反汇编与查看 ELF 结构（与目标架构无关的选项同样适用于 RISC-V 交叉 `riscv*-objdump`）。

| 选项 | 含义 |
|------|------|
| `-d` | 反汇编可执行段（`.text` 等含代码的段） |
| `-D` | 反汇编**所有**段（数据段会按指令解码，慎用） |
| `-S` | 交织 C 源码（需编译时带 `-g`） |
| `-l` | 反汇编中显示行号与文件名 |
| `-h` | 打印段头（Section headers） |
| `-x` | 打印全部头信息（含程序头等） |
| `-t` / `--syms` | 符号表 |
| `-r` | 重定位表 |
| `-C` | 解码 C++ 符号（demangle） |
| `--visualize-jumps` | 用颜色/标记显示跳转目标（新版本 binutils） |
| `-M no-aliases` | 不展开伪指令，显示**真实**指令编码 |
| `-M numeric` | 寄存器显示为 `x0`–`x31` 数字而非 ABI 名 |

示例：

```bash
riscv64-unknown-elf-objdump -d -M no-aliases a.out
riscv64-unknown-elf-objdump -h -t firmware.elf
```

#### 1.2.3.objcopy 常用选项

| 选项 | 含义 |
|------|------|
| `-O binary` | 输出原始二进制（如 `image.bin`） |
| `-O ihex` | 输出 Intel HEX |
| `-j .text` | 只拷贝指定段（可多次 `-j`） |
| `--strip-all` | 去掉所有符号与重定位 |
| `--strip-debug` | 仅去掉调试信息 |
| `-S` / `--strip-all` 与 `-g` 组合 | 按需求裁剪 |

示例：只导出 `.text`+`.data` 为烧录镜像（按链接脚本决定段名）：

```bash
riscv64-unknown-elf-objcopy -O binary -S firmware.elf firmware.bin
```

#### 1.2.4.size 常用选项

| 选项 | 含义 |
|------|------|
| （默认） | 按对象/可执行文件列出 text / data / bss 占用 |
| `-A` / `--format=sysv` | System V 风格，每段一行 |
| `-d` / `--radix=10` | 十进制显示 |
| `-x` / `--radix=16` | 十六进制显示 |

```bash
riscv64-unknown-elf-size -A a.out
```

### 1.3函数属性

**gcc Version12.2**

* `__attribute__((naked))`
  
  没有上下文，类似inline，需要添加汇编`__asm ret`这种显式返回才能返回到调用的地方

* `__attribute__((interrupt))`
  
  声明该函数为中断函数，默认为machine特权，区别在于`ret`指令:`mret` `sret` `ret`

* `__attribute__((interrupt("user")))`
  
  声明user特权的中断函数

* `__attribute__((interrupt("supervisor")))`
  
  声明supervisor特权的中断函数

* `__attribute__((interrupt("machine")))`
  
  声明machine特权的中断函数

## 2.汇编

### 2.1.寄存器

#### 2.1.1.通用寄存器

| 寄存器      | ABI     | 描述               | 调用时是否保存 |
|:-------- |:------- |:----------------:| -------:|
| x0       | zero    | 硬件连线接0，无法写入      | 不适用     |
| x1       | ra      | 跳转指令返回地址         | 是       |
| x2       | sp      | 栈指针              | 是       |
| x3       | gp      | 全局指针             | 是       |
| x4       | tp      | 线程指针             | 是       |
| x5\~7    | t0\~t2  | 临时寄存器0\~2        | 否       |
| x8       | s0/fp   | 全局寄存器0或者作为帧指针    | 是       |
| x9       | s1      | 全局寄存器1           | 是       |
| x10\~x11 | a0\~a1  | 返回值或者是函数调用参数0\~1 | 否       |
| x12\~x17 | a2\~a7  | 函数调用参数2\~7       | 否       |
| x18\~x27 | s2\~s11 | 全局寄存器2\~11       | 是       |
| x28\~x31 | t3\~t6  | 临时寄存器3\~6        | 否       |
| pc       | (none)  | 程序计数器            | 不适用     |

#### 2.1.2.浮点寄存器

| 寄存器      | ABI       | 描述                 | 调用时是否保存 |
|:-------- |:--------- |:------------------:| -------:|
| f0\~f7   | ft0\~ft7  | 浮点临时寄存器0\~7        | 否       |
| f8\~f9   | fs0\~fs1  | 浮点全局寄存器器0～1        | 是       |
| f10\~f11 | fa0\~fa1  | 浮点返回值或者是函数调用参数0\~1 | 否       |
| f12\~f17 | fa2\~fa7  | 浮点函数调用参数2\~7       | 否       |
| f18\~f27 | fs2\~fs11 | 浮点全局寄存器2\~11       | 是       |
| f28\~f31 | ft8\~ft11 | 浮点临时寄存器8\~11       | 否       |

### 2.2.指令集

#### 2.2.1.基础指令

指令类型说明

| 类型  | 描述       | 包含指令                                                           |
|:--- |:-------- | --------------------------------------------------------------:|
| R型  | 算术指令格式   | add、sub、sll、xor、srl、sra、or、and 及 M 扩展 mul/div 等      |
| I型  | 加载与立即数   | lb、lh、lw、ld、lbu、lhu、lwu、addi、slli、xori、srli、srai、ori、andi、jalr 等 |
| S型  | 存储       | sb、sh、sw、sd                                                 |
| SB型 | 条件分支格式   | beq、bne、blt、bge、bltu、bgeu                                   |
| UJ型 | 无条件跳转    | jal |
| U型  | 高位立即数     | lui、auipc（PC 相对高位立即数） |

##### 2.2.1.1整数算术指令
| 指令  | 示例           | 示例含义               | 描述                     |
|-------|----------------|----------------------|--------------------------|
| add   | add rd, rs1, rs2 | rd = rs1 + rs2        | 将rs1和rs2相加并存储结果到rd   |
| sub   | sub rd, rs1, rs2 | rd = rs1 - rs2        | 将rs1和rs2相减并存储结果到rd   |
| mul   | mul rd, rs1, rs2 | rd = rs1 * rs2        | 将rs1和rs2相乘并存储结果到rd   |
| div   | div rd, rs1, rs2 | rd = rs1 / rs2        | 将rs1除以rs2并存储结果到rd     |
| rem   | rem rd, rs1, rs2 | rd = rs1 % rs2        | 将rs1除以rs2的余数存储到rd    |


| 指令   | 示例              | 示例含义                 | 描述                    |
|:---- |:--------------- |:--------------------:| ---------------------:|
| addi | addi a0, a1, 20 | a0 = a1 + 20         | 用于加一个常数               |
| slti | slti a0, a1, 20 | a0 = a1 < 20 ? 1 : 0 | 有符号：a1 与**符号扩展**立即数比较 |
| sltiu | sltiu a0, a1, 20 | a0 = a1 < 20 ? 1 : 0 | 无符号：a1 与**零扩展**立即数比较 |
| andi | andi a0, a1, 20 | a0 = a1 & 20         | 寄存器与常数按位与             |
| ori  | ori a0, a1, 20  | a0 = a1 | 20         | 寄存器与常数按位或             |
| xori | xori a0, a1, 20 | a0 = a1 ^ 20         | 寄存器与常数按位异或            |
| slli | slli a0, a1, 3  | a0 = a1 << 3         | 根据立即数给定位数左移           |
| srli | srli a0, a1, 3  | a0 = a1 >> 3         | 根据立即数给定位数右移           |
| srai | srai a0, a1, 3  | a0 = a1 >> 3         | 根据立即数给定位数算术右移         |
| add  | add a0, a1, a2  | a0 = a1 + a2         | 加法指令                  |
| slt | slt a0, a1, a2  | a0 = a1 < a2 ? 1 : 0 | 比较a1与a2，将bool结果给a0    |
| sltu | sltu a0, a1, a2 | a0 = a1 < a2 ? 1 : 0 | 无符号比较a1与a2，将bool结果给a0 |
| and  | and a0, a1, a2  | a0 = a1 & a2         | 三寄存器操作数：按位与           |
| or   | or a0, a1, a2   | a0 = a1 | a2         | 三寄存器操作数：按位或           |
| xor  | xor a0, a1, a2  | a0 = a1 ^ a2         | 三寄存器操作数：按位异或          |
| sll  | sll a0, a1, a2  | a0 = a1 << a2        | 按寄存器给定位数左移            |
| srl  | srl a0, a1, a2  | a0 = a1 >> a2        | 按寄存器给定位数右移            |
| sub  | sub a0, a1, a2  | a0 = a1 - a2         | 减法指令                  |
| sra  | sra a0, a1, a2  | a0 = a1 >> a2        | 按寄存器给定位数算术右移          |

##### 2.2.1.2.控制指令

###### 2.2.1.2.1跳转指令

| 指令   | 示例               | 示例含义                    | 描述                                        |
| ---- | ---------------- | ----------------------- | -----------------------------------------:|
| jal  | jal ra, 100      | ra = pc+4;goto (pc+100) | 将当前语句的pc+4隐式保存到ra，然后跳转到pc+100的位置，一般用于过程调用 |
| jalr | jalr ra, 100(a0) | ra = pc+4;goto(a0+100)  | 将当前语句的pc+4隐式保存到ra，然后跳转到a0+100的位置，一般用于过程返回 |

###### 2.2.1.2.分支指令

| 指令   | 示例               | 示例含义                        | 描述                     |
| ---- | ---------------- | --------------------------- | ----------------------:|
| beq  | beq a0, a1, 100  | if (a0 == a1) goto (pc+100) | 若寄存器数值相等则跳转到pc+100     |
| bne  | bne a0, a1, 100  | if (a0 != a1) goto (pc+100) | 若寄存器数值不等则跳转到pc+100     |
| blt  | blt a0, a1, 100  | if (a0 < a1) goto (pc+100)  | 若a0小于a1则跳转到pc+100      |
| bltu | bltu a0, a1, 100 | if (a0 < a1) goto (pc+100)  | 若a0小于a1则跳转到pc+100无符号   |
| bge  | bge a0, a1, 100  | if (a0 >= a1) goto (pc+100) | 若a0大于等于a1则跳转到pc+100    |
| bgeu | bgeu a0, a1, 100 | if (a0 >= a1) goto (pc+100) | 若a0大于等于a1则跳转到pc+100无符号 |

##### 2.2.1.3.Load Store指令

###### 2.2.1.3.1.Load指令

| 指令    | 示例                | 示例含义                    | 描述                    |
| ----- | ----------------- | ----------------------- | ---------------------:|
| lb    | lb a0, 40(a1)     | a0 = mem\[a1+40]        | Load一个字节8bits到寄存器     |
| lbu   | lbu a0, 40(a1)    | a0 = mem\[a1+40]        | Load一个无符号字节8bits到寄存器  |
| lh    | lh a0, 40(a1)     | a0 = mem\[a1+40]        | Load一个半字16bits到寄存器    |
| lhu   | lhu a0, 40(a1)    | a0 = mem\[a1+40]        | Load一个无符号半字16bits到寄存器 |
| lw    | lw a0, 40(a1)     | a0 = mem\[a1+40]        | Load一个字32bits到寄存器     |
| lwu   | lwu a0, 40(a1)    | a0 = mem\[a1+40]        | Load一个无符号字32bits到寄存器  |
| ld    | ld a0, 40(a1)     | a0 = mem\[a1+40]        | Load一个双字64bits到寄存器    |
| lui   | lui a0, 0x12345   | a0 = 0x12345000         | Load左移12位后的20位立即数     |
| auipc | auipc a0, 0x12345 | a0 = pc + (0x12345<<12) | 立即数高20位与PC相加，将结果写入寄存器 |

###### 2.2.1.3.2.Store指令

| 指令  | 示例            | 示例含义             | 描述                  |
| --- | ------------- | ---------------- | -------------------:|
| sb  | sb a0, 40(a1) | mem\[a1+40] = a0 | Store一个字节8bits到存储器  |
| sh  | sh a0, 40(a1) | mem\[a1+40] = a0 | Store一个半字16bits到存储器 |
| sw  | sw a0, 40(a1) | mem\[a1+40] = a0 | Store一个字32bits到存储器  |
| sd  | sd a0, 40(a1) | mem\[a1+40] = a0 | Store一个双字64bits到存储器 |

##### 2.2.1.4.内存指令

| 指令    | 示例               | 示例含义                              | 描述      |
| ----- | ---------------- | --------------------------------- | -------:|
| fence | fence iorw, iorw | 前后序：对 predecessor / successor 集合中的 I、O、R、W 访问排序 | 设备与内存访问次序屏障 |
| fence.tso | fence.tso | 全局内存 TSO 次序（与 `fence rw, rw` 在基础 ISA 中语义相关） | 多核可见性，详见 ISA Memory Model 章节 |
| fence.i | fence.i | 指令流与 I-cache 一致性（与 Zifencei 一致） | 自修改代码、JIT、加载新程序后常用 |

##### 2.2.1.5.环境调用指令

| 指令     | 示例     | 描述                                   |
| ------ | ------ | ------------------------------------:|
| ecall  | ecall  | 在U\S\M模式下执行可产生ecall异常，主要用于sbi接口调用等操作 |
| ebreak | ebreak | 调试器可使用它将控制权转移回调试环境，可产生一个ebreak异常     |

##### 2.2.1.6.伪指令

| 指令         | 示例                | 示例含义                             | 描述                          |
| ------------ | ------------------- | ------------------------------------ | ----------------------------- |
| la           | la a0, symbol       | auipc a0, symbol[31:12]; addi a0, a0, symbol[11:0] | 取地址，包含lla和lga     |
| lla          | lla a0, symbol      | auipc a0, symbol[31:12]; addi a0, a0, symbol[11:0] | 取本地地址                 |
| lga          | lga a0, symbol      | auipc a0, symbol@global[31:12]; l{w\|d} a0, symbol@global[11:0] (a0) | 取全局地址     |
| l{b\|h\|w\|d} | l{b\|h\|w\|d} a0, symbol | auipc a0, symbol[31:12]; l{b\|h\|w\|d} a0, symbol[11:0] (a0) | 取全局地址       |
| s{b\|h\|w\|d} | s{b\|h\|w\|d} a0, symbol, a1 | auipc a1, symbol[31:12]; s{b\|h\|w\|d} a0, symbol[11:0] (a1) | 存全局地址     |
| fl{w\|d}     | fl{w\|d} f0, symbol, a0 | auipc a0, symbol[31:12]; fl{w\|d} f0, symbol[11:0] (a0) | 浮点取全局地址 |
| fs{w\|d}     | fs{w\|d} f0, symbol, a0 | auipc a0, symbol[31:12]; fs{w\|d} f0, symbol[11:0] (a0) | 浮点存全局地址 |
| nop          | nop                 | addi zero, zero, 0                   | 空指令                       |
| li           | li a0, 20           | addi a0, zero, 20                    | 将常数加载到整数寄存器       |
| mv           | mv a0, a1           | addi a0, a1, 0                       | 拷贝寄存器                   |
| not          | not a0, a1          | xori a0, a1, -1                      | 1的补码                      |
| neg          | neg a0, a1          | sub a0, zero, a1                     | 取负                        |



##### 2.2.1.7.CSR伪指令

| 指令    | 示例                    | 示例含义                          | 描述                              |
| ------- | -----------------------| --------------------------------- | --------------------------------- |
| rdinstret | rdinstret rd          | rd = CSR[instret]                 | 读取指令执行计数寄存器              |
| rdinstreth| rdinstreth rd         | rd = CSR[instreth]                | 读取指令执行计数寄存器的高位         |
| rdcycle  | rdcycle rd            | rd = CSR[cycle]                   | 读取时钟周期计数寄存器              |
| rdcycleh | rdcycleh rd           | rd = CSR[cycleh]                  | 读取时钟周期计数寄存器的高位         |
| rdtime   | rdtime rd             | rd = CSR[time]                    | 读取实时计时寄存器                  |
| rdtimeh  | rdtimeh rd            | rd = CSR[timeh]                   | 读取实时计时寄存器的高位             |
| csrr     | csrr rd, csr          | rd = CSR[csr]                     | 读取指定CSR寄存器的值               |
| csrw     | csrw csr, rs          | CSR[csr] = rs                     | 将寄存器rs的值写入指定CSR寄存器     |
| csrs     | csrs csr, rs          | CSR[csr] = CSR[csr] \| rs         | 对指定CSR寄存器进行按位或操作        |
| csrc     | csrc csr, rs          | CSR[csr] = CSR[csr] & (~rs)       | 对指定CSR寄存器进行按位与非操作      |
| csrwi    | csrwi csr, imm        | CSR[csr] = imm                    | 将立即数imm写入指定CSR寄存器        |
| csrsi    | csrsi csr, imm        | CSR[csr] = CSR[csr] \| imm        | 对指定CSR寄存器进行按位或立即数操作  |
| csrci    | csrci csr, imm        | CSR[csr] = CSR[csr] & (~imm)      | 对指定CSR寄存器进行按位与非立即数操作|
| frcsr    | frcsr rd              | rd = CSR[fcsr]                    | 读取浮点控制和状态寄存器             |
| fscsr    | fscsr rd              | CSR[fcsr] = rd                    | 将寄存器rd的值写入浮点控制和状态寄存器|
| frrm     | frrm rd               | rd = CSR[frm]                     | 读取浮点舍入模式寄存器               |
| fsrm     | fsrm rs               | CSR[frm] = rs                     | 将寄存器rs的值写入浮点舍入模式寄存器 |
| fsrmi    | fsrmi imm             | CSR[frm] = imm                    | 将立即数imm写入浮点舍入模式寄存器    |
| frflags  | frflags rd            | rd = CSR[fflags]                  | 读取浮点异常标志寄存器               |
| fsflags  | fsflags rs            | CSR[fflags] = rs                  | 将寄存器rs的值写入浮点异常标志寄存器 |
| fsflagsi | fsflagsi imm          | CSR[fflags] = imm                 | 将立即数imm写入浮点异常标志寄存器    |

##### 2.2.2.M 扩展指令（整数乘除）

原子访存（`lr`/`sc`/`amo*`）属于 **A 扩展**，见 §2.2.6。

| 指令 | 示例 | 含义（直觉） |
| ------ | ------------------ | ------------ |
| mul | mul rd, rs1, rs2 | 低 XLEN 位：**有符号** × **有符号** |
| mulh | mulh rd, rs1, rs2 | 高 XLEN 位：**有符号** × **有符号** |
| mulhsu | mulhsu rd, rs1, rs2 | 高 XLEN 位：**有符号** rs1 × **无符号** rs2 |
| mulhu | mulhu rd, rs1, rs2 | 高 XLEN 位：**无符号** × **无符号** |
| div | div rd, rs1, rs2 | 有符号除法（向 0 舍入） |
| divu | divu rd, rs1, rs2 | 无符号除法 |
| rem | rem rd, rs1, rs2 | 有符号余数，与 `div` 配对 |
| remu | remu rd, rs1, rs2 | 无符号余数 |

**除法注意：**`div`/`rem` 对除数为 0 或 `INT_MIN / -1` 等溢出情形，结果由规范固定（通常不 trap）。

##### 2.2.3.F 扩展指令（单精度浮点）

| 指令 | 示例 | 示例含义 | 描述 |
| --------- | ------------------------ | --------------------------- | --------------------------------------- |
| flw | flw f0, 40(a0) | f0 = mem[a0+40] | Load 单精度 |
| fsw | fsw f0, 40(a0) | mem[a0+40] = f0 | Store 单精度 |
| fmadd.s | fmadd.s f0, f1, f2, f3 | f0 = f1×f2+f3 | 融合乘加（FMA），单操作数异常按一次运算 |
| fmsub.s | fmsub.s f0, f1, f2, f3 | f0 = f1×f2−f3 | 融合乘减 |
| fnmadd.s | fnmadd.s f0, f1, f2, f3 | f0 = −(f1×f2+f3) | 融合负乘加 |
| fnmsub.s | fnmsub.s f0, f1, f2, f3 | f0 = −(f1×f2−f3) | 融合负乘减 |
| fadd.s | fadd.s f0, f1, f2 | f0 = f1+f2 | 加法 |
| fsub.s | fsub.s f0, f1, f2 | f0 = f1−f2 | 减法 |
| fmul.s | fmul.s f0, f1, f2 | f0 = f1×f2 | 乘法 |
| fdiv.s | fdiv.s f0, f1, f2 | f0 = f1/f2 | 除法 |
| fsqrt.s | fsqrt.s f0, f1 | f0 = sqrt(f1) | 平方根（注意助记符是 `fsqrt.s`） |
| fsgnj.s | fsgnj.s f0, f1, f2 | f0 = {sign(f2)} \| {f1 的 [30:0]} | IEEE 单精度：符号在 bit 31，[30:0] 为指数+有效数域 |
| fsgnjn.s | fsgnjn.s f0, f1, f2 | 符号取反后拼接 | 同上，符号为 `~sign(f2)` |
| fsgnjx.s | fsgnjx.s f0, f1, f2 | 符号为 `sign(f1) XOR sign(f2)` | XOR 符号 |
| fmin.s | fmin.s f0, f1, f2 | f0 = minNum(f1,f2) | 按 IEEE minNum语义（含 NaN 传播规则） |
| fmax.s | fmax.s f0, f1, f2 | f0 = maxNum(f1,f2) | 按 IEEE maxNum 语义 |
| fcvt.w.s | fcvt.w.s a0, f0 | a0 = (int32_t) f0 | 浮点→有符号 32 位整数 |
| fcvt.wu.s | fcvt.wu.s a0, f0 | a0 = (uint32_t) f0 | 浮点→无符号 32 位 |
| fcvt.l.s | fcvt.l.s a0, f0 | a0 = (int64_t) f0 | RV64：→有符号 64 位 |
| fcvt.lu.s | fcvt.lu.s a0, f0 | a0 = (uint64_t) f0 | RV64：→无符号 64 位 |
| fcvt.s.w | fcvt.s.w f0, a0 | f0 = (float) (int32_t) a0 | 有符号 32 位→单精度 |
| fcvt.s.wu | fcvt.s.wu f0, a0 | f0 = (float) (uint32_t) a0 | 无符号 32位→单精度 |
| fcvt.s.l | fcvt.s.l f0, a0 | f0 = (float) (int64_t) a0 | RV64：有符号 64 位→单精度 |
| fcvt.s.lu | fcvt.s.lu f0, a0 | f0 = (float) (uint64_t) a0 | RV64：无符号 64 位→单精度 |
| fmv.x.w | fmv.x.w a0, f0 | a0 = f0 的按位 IEEE 编码（符号扩展） | RV32：`fmv.x.w`；RV64 另有 `fmv.x.d`（配合 D） |
| fmv.w.x | fmv.w.x f0, a0 | f0 = a0 的低32 位按位解释为单精度 | 位模式搬运，不做数值转换 |
| feq.s | feq.s a0, f1, f2 | a0 = (f1 == f2) ? 1 : 0 | 相等比较；±0 视为相等；NaN 为假 |
| flt.s | flt.s a0, f1, f2 | a0 = (f1 < f2) ? 1 : 0 | 有序小于 |
| fle.s | fle.s a0, f1, f2 | a0 = (f1 ≤ f2) ? 1 : 0 | 有序小于等于 |
| fclass.s | fclass.s a0, f0 | a0 = 10 类掩码位之一 | 分类 NaN/Inf/零/次正规等，见下图 |

<span id="1">批注[1]</span>
<ul>
<li markdown="1">
![fclass](/img/posts/fclass.png)
</li>
</ul>

##### 2.2.4.D 扩展指令（双精度浮点）

与 F 指令一一对应，助记符后缀为 `.d`，操作数为64 位。常用额外转换：`fcvt.s.d`（双→单）、`fcvt.d.s`（单→双）。

| 指令 | 示例 | 示例含义 | 描述 |
| --------- | ------------------------ | --------------------------- | --------------------------------------- |
| fld | fld f0, 40(a0) | f0 = mem[a0+40] | Load 双精度 |
| fsd | fsd f0, 40(a0) | mem[a0+40] = f0 | Store 双精度 |
| fmadd.d | fmadd.d f0, f1, f2, f3 | f0 = f1×f2+f3 | 双精度 FMA |
| fmsub.d | fmsub.d f0, f1, f2, f3 | f0 = f1×f2−f3 | 双精度融合乘减 |
| fnmadd.d | fnmadd.d f0, f1, f2, f3 | f0 = −(f1×f2+f3) | 双精度负 FMA |
| fnmsub.d | fnmsub.d f0, f1, f2, f3 | f0 = −(f1×f2−f3) | 双精度负融合乘减 |
| fadd.d | fadd.d f0, f1, f2 | f0 = f1+f2 | 加法 |
| fsub.d | fsub.d f0, f1, f2 | f0 = f1−f2 | 减法 |
| fmul.d | fmul.d f0, f1, f2 | f0 = f1×f2 | 乘法 |
| fdiv.d | fdiv.d f0, f1, f2 | f0 = f1/f2 | 除法 |
| fsqrt.d | fsqrt.d f0, f1 | f0 = sqrt(f1) | 平方根 |
| fsgnj.d | fsgnj.d f0, f1, f2 | f0 = {f2 的 bit63符号} \| {f1 的 62:0} | 双精度：符号在最高位 |
| fsgnjn.d | fsgnjn.d f0, f1, f2 | 符号取反后拼接 | 同上 |
| fsgnjx.d | fsgnjx.d f0, f1, f2 | 符号 XOR | 同上 |
| fmin.d | fmin.d f0, f1, f2 | f0 = minNum(f1,f2) | |
| fmax.d | fmax.d f0, f1, f2 | f0 = maxNum(f1,f2) | |
| fcvt.w.d | fcvt.w.d a0, f0 | 浮点→有符号 32 位 | |
| fcvt.wu.d | fcvt.wu.d a0, f0 | 浮点→无符号 32 位 | |
| fcvt.l.d | fcvt.l.d a0, f0 | RV64：→64 位整数 | |
| fcvt.lu.d | fcvt.lu.d a0, f0 | RV64：无符号 64 位 | |
| fcvt.d.w | fcvt.d.w f0, a0 | 有符号 32 位→双精度 | |
| fcvt.d.wu | fcvt.d.wu f0, a0 | 无符号 32 位→双精度 | |
| fcvt.d.l | fcvt.d.l f0, a0 | RV64：有符号 64 位→双精度 | |
| fcvt.d.lu | fcvt.d.lu f0, a0 | RV64：无符号 64 位→双精度 | |
| fcvt.s.d | fcvt.s.d f0, f1 | 双精度→单精度 | 需同时有 F+D |
| fcvt.d.s | fcvt.d.s f0, f1 | 单精度→双精度 | |
| fmv.x.d | fmv.x.d a0, f0 | 整数寄存器 ← IEEE 双精度位模式 | RV64 常用 |
| fmv.d.x | fmv.d.x f0, a0 | 浮点寄存器 ← 整数位模式 | |
| feq.d | feq.d a0, f1, f2 | 相等比较 | 语义同单精度 |
| flt.d | flt.d a0, f1, f2 | 有序小于 | |
| fle.d | fle.d a0, f1, f2 | 有序小于等于 | |
| fclass.d | fclass.d a0, f0 | 分类 | 掩码语义同 `fclass.s` |

##### 2.2.5.Q 扩展指令（四倍精度浮点，Quad）

**Q** 在现行 RISC-V 规范中指 **IEEE 754 四倍精度（128-bit）浮点** 子扩展，助记符后缀为 `.q`（如 `fadd.q`、`flq`、`fsq`），指令形态与 F/D 类似。实现较少，工具链需显式 `-march` 支持。

**与向量区别：** SIMD/向量运算由 **V 扩展**（`vsetvl`、`vle32.v` 等）定义，**不是** Q。若你需要向量速查，应查阅 [Vector spec](https://github.com/riscv/riscv-v-spec) 或单独整理 V 扩展表。

##### 2.2.6.A 扩展指令（原子内存操作）

**LR/SC 对：**`lr.w` / `sc.w`（字）与 `lr.d` / `sc.d`（双字，RV64）实现 **保留加载 / 条件存储**。`sc` 成功则 rd=0，失败则 rd≠0 且不写内存。用于实现无锁数据结构。

**AMO：**`amoswap`、`amoadd`、`amoxor`、`amoand`、`amoor`、`amomin`、`amomax`、`amominu`、`amomaxu` 均可带 `.w` 或 `.d` 后缀。语义：`*addr` 与 rs2 做运算（或交换），**旧值**写入 rd。

| 指令 | 示例 | 直觉 |
| ------ | ---------------------- | ------ |
| lr.w | lr.w rd, (rs1) | rd = *rs1；在该地址建立 reservation |
| sc.w | sc.w rd, rs2, (rs1) | 尝试 *rs1 = rs2（仅当 reservation 仍有效） |
| amoswap.w | amoswap.w rd, rs2, (rs1) | t=*rs1; *rs1=rs2; rd=t |
| amoadd.w | amoadd.w rd, rs2, (rs1) | t=*rs1; *rs1=t+rs2; rd=t |
| amoxor.w等 | amoxor.w rd, rs2, (rs1) | 按位运算版本同理 |
| amomin.w 等 | amomin.w rd, rs2, (rs1) | 有符号/无符号 min/max 版本见 `amominu`/`amomaxu` |

**内存顺序：**配合 §2.2.1.4 的 `fence` / `fence.i` 使用；与 C11 atomic 映射时需关注 acquire/release 语义。

##### 2.2.7.C 扩展指令（压缩指令，RVC）

16-bit 编码，与32-bit 指令可混排。常见：`c.lw`/`c.sw`、`c.ld`/`c.sd`（RV64）、`c.addi`、`c.li`、`c.mv`、`c.j`/`c.jal`（RV32）、`c.jr`/`c.jalr`、`c.addi16sp`、`c.lui`，以及浮点压缩访存 `c.flw` 等（视扩展组合而定）。

**例：**`c.mv a0, a1` 常用于寄存器间移动，可视为 `add a0, zero, a1`；在偏移合法时 `c.lw a0, 4(a1)` 等价于 `lw a0, 4(a1)`。

##### 2.2.8.P 扩展（Packed-SIMD，已弃用）

早期 **P** 提案为 **Packed-SIMD**；现行路线已转向 **V 向量扩展**与 **Zve*** 嵌入式向量配置。**新设计不建议再跟 P 草案**，遗留二进制需查具体芯片文档。

##### 2.2.9.B 扩展（位操作，Zb*）

通常指 **Zbb**（基本位操作）、**Zba**（地址生成）、**Zbc**（进位乘）等组合。示例：

| 类别 | 指令 | 含义 |
|------|------|------|
| Zbb | clz, ctz, popcnt | 前导/尾随 0计数、1 的个数 |
| Zbb | andn, orn, xnor | 组合位逻辑 |
| Zbb | min, max, minu, maxu | 整数 min/max |
| Zba | sh1add, sh2add, sh3add | `(rs1 << k) + rs2`，用于地址计算 |
| Zbc | clmul, clmulh, clmulr | 进位无关乘法（CRC/GF(2) 等） |

具体助记符与编码以所用工具链的 `-march`字符串为准（如 `zbba` / `zbb`）。

##### 2.2.10.H 扩展（Hypervisor）

为 **虚拟化** 增加 **HS 模式**、两阶段地址翻译、虚拟中断委托等。应用层汇编较少直接手写；调试/固件需对照 *Hypervisor* 章节与 CSR（如 `htval`、`vsatp` 等）。

##### 2.2.11.J 扩展（语言/运行时相关命名）

公开规范中 **并无** 与 I/M/A同级别的单一 “J 扩展” 速查表；文档里的 **J** 多指 **自定义扩展槽位** 或历史提案。若涉及 **JIT**、**指针认证** 等，应查具体扩展包名（如指针认证相关 BoM 文档）。

##### 2.2.12.L 扩展（十进制浮点）

**L** 曾用于十进制浮点（decimal floating-point）提案，生态极小众。除非目标核明确实现，一般可忽略。

##### 2.2.13.N 扩展（用户级中断）

**N** 扩展为 **User-mode interrupts**（用户态扩展中断），与 **U模式** CSR（如 `ustatus`、`uepc`）配合。未实现时用户态不可用中断入口。

##### 2.2.14.G 与常见 ABI 命名

**G** 是约定俗成的 **集合名**：**I + M + A + F + D**，并隐含需要 **Zicsr**（CSR 指令）与 **Zifencei**（`fence.i`）以构成典型 **Unix 级** 应用配置（与 **RV32GC** / **RV64GC** 中的 **G** 同义）。

速记：**G ≠一条指令**；写 `-march=rv64gc` 时即包含上述整数、乘除、原子、双精度浮点及 CSR/指令缓存同步。

## 参考资料

* 伯克利大学[riscv reference card](https://inst.eecs.berkeley.edu/\~cs61c/sp22/pdfs/resources/reference-card.pdf)

* [RISCV ISA Manual](https://github.com/riscv/riscv-isa-manual/releases)

* [RISCV ASM Manual](https://github.com/riscv-non-isa/riscv-asm-manual/blob/master/riscv-asm.md)

* [RISCV C API Doc](https://github.com/riscv-non-isa/riscv-c-api-doc/blob/master/riscv-c-api.md)
