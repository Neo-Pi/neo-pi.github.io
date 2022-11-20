---
layout: post
title: "RISC-V 汇编速查手册"
subtitle: "收集整理了一些常用的汇编指令"
background: '/img/posts/01.jpg'
---

## RISCV编程速查手册

该手册摘取自RISCV社区文档，仅负责翻译整理汇总，个别词意可能有误差，请配合官方文档阅读。

## 目录

[TOC]

## 1.C语言

### 1.1.数据类型大小

| C语言类型   | 描述         | RISCV32 | RISCV64 |
| ----------- | ------------ | ------: | ------: |
| char        | 字符型       |       1 |       1 |
| short       | 短整形       |       2 |       2 |
| int         | 整形         |       4 |       4 |
| long        | 长整形       |       4 |       8 |
| long long   | 超长整形     |       8 |       8 |
| void *      | 指针         |       4 |       8 |
| float       | 单精度浮点型 |       4 |       4 |
| double      | 双精度浮点型 |       8 |       8 |
| long double | 超精度浮点型 |      16 |      16 |

### 1.2.工具链选项

仅列出RISCV平台的内容或者常见通用的内容，如果找不到某个内容，请移步至GNU社区下载对应文档

#### 1.2.1.gcc编译选项(Version:12.2)

由于版本不同，某些选项会失效，请移步至GNU社区查阅对应版本的gcc文档

- `-mbranch-cost=N`

  分支预测的代价设置为n条指令

- `-mplt` `-mno-plt`

  在生成PIC代码时，执行是否允许使用plt。忽略了非pic的内容。默认值为“-mplt”

- `-mabi=ABI`

  指定整数和浮点的调用约束,需要配合`-march`使用，选项有`ilp32` `ilp32f` `ilp32d` `lp64` `lp64f` `lp64d`,例如`-march=rv32i -mabi=lp32`

- `-march=ISA`

  允许生成的指令的指令集，根据平台的指令集支持来配置参数，示例见上文

- `-mfdiv` `-mno-fdiv`

  是否使用硬件浮点除法和平方根指令。这需要对浮点寄存器的F或D扩展。默认情况下是在指定的体系结构中使用它们 有这些指令

- `-mdiv` `-mno-div`

  是否使用对整数除法的硬件指令。这就需要M的扩展。默认情况下，如果指定的体系结构有这些指令，则使用它们

- `-misa-spec=ISA-spec-string`

  指定非特权ISA文档版本，选项有`2.2` `20190608` `20191213`，默认是`20191213`

- `-mcpu=processor-string`

  指定内核型号，会根据型号做对应的优化，选项有`sifive-e20` `sifive-e21` `sifive-e24` `sifive-e31` `sifive-e34` `sifive-e76` `sifive-s21` `sifive-s51` `sifive-s54` `sifive-s76` `sifive-u54` `sifive-u74`

- `-mtune=processor-string`

  指定体系结构名称，会根据型号做对应的优化，选项有`sifive-3-series` `sifive-5-series` `sifive-7-series` `size`，`size`选项对应-Os

- `-mpreferred-stack-boundary=num`

  设置栈对齐大小，默认是4

- `-msmall-data-limit=N`

  将小于n字节的全局和静态数据放入一个特殊的部分（在某些目标上）

- `-msave-restore` `-mno-save-restore`

  是否使用库函数调用的较小但较慢的上下文。默认情况下是使用内联上下文

- `-mshorten-memrefs` `-mno-shorten-memrefs`

  是否将大偏移量的load store操作转换成一个小偏移量的操作，这么做会增加一些指令，以空间换时间，目前只支持32位整数load store

- `-mstrict-align` `-mno-strict-align`

  是否生成未对齐的内存访问。默认值取决于正在优化的处理器是否支持快速未对齐访问

- `-mcmodel=CODE_MODEL`

  为中低代码模型生成代码。程序及其静态定义的符号必须位于单个2 GiB地址范围内，`medlow`并且必须位于绝对地址−2 GiB和+2 GiB之间。程序可以是静态链接的或动态链接的。这是默认的代码模型，选项有`medlow` `medany`

- `-mexplicit-relocs` `-mno-explicit-relocs`

  在处理符号地址时，是否使用汇编程序重定位操作符。另一种选择是使用汇编程序宏，这可能会限制优化

- `-mrelax` `-mno-relax`

  是否利用链接器(linker) 松弛来减少实现符号地址所需的指令数量。默认选项会开启`-mrelex`

- `-memit-attribute` `-mno-emit-attribute`

  是否将RISCV属性记录到elf文件的额外信息中，要求binutils最低版本为2.32

- `-malign-data=type`

  控制GCC如何对齐数组、结构或共用体的变量和常量。类型支持的值是“xlen”，它使用x寄存器宽度作为对齐值，它使用2的n次幂对齐。默认值为“xlen”。

- `-mbig-endian`

  生成大端代码

- `-mlittle-endian`

  生成小端代码

- `-mstack-protector-guard=guard`

  `-mstack-protector-guard-reg=reg`

  `-mstack-protector-guard-offset=offset`

  使用canary at guard生成堆栈保护代码。仅适用于Linux

#### 1.2.2.objdump选项

#### 1.2.3.objcopy选项

#### 1.2.4.size选项

### 1.3函数属性

**gcc Version12.2**

- `__attribute__((naked))`

  没有上下文，类似inline，需要添加汇编`__asm ret`这种显式返回才能返回到调用的地方

- `__attribute__((interrupt))`

  声明该函数为中断函数，默认为machine特权，区别在于`ret`指令:`mret` `sret` `ret`

- `__attribute__((interrupt("user")))`

  声明user特权的中断函数

- `__attribute__((interrupt("supervisor")))`

  声明supervisor特权的中断函数

- `__attribute__((interrupt("machine")))`

  声明machine特权的中断函数

## 2.汇编

### 2.1.寄存器

#### 2.1.1.通用寄存器

| 寄存器  | ABI    | 描述                        | 全局   |
| ------- | :----- | --------------------------- | ------ |
| x0      | zero   | 硬件连线接0，无法写入       | 未定义 |
| x1      | ra     | 跳转指令返回地址            | 否     |
| x2      | sp     | 栈指针                      | 是     |
| x3      | gp     | 全局指针                    | 未定义 |
| x4      | tp     | 线程指针                    | 未定义 |
| x5~7    | t0~t2  | 临时寄存器0~2               | 否     |
| x8      | s0/fp  | 全局寄存器0或者作为帧指针   | 是     |
| x9      | s1     | 全局寄存器1                 | 是     |
| x10~x11 | a0~a1  | 返回值或者是函数调用参数0~1 | 否     |
| x12~x17 | a2~a7  | 函数调用参数2~7             | 否     |
| x18~x27 | s2~s11 | 全局寄存器2~11              | 是     |
| x28~x31 | t3~t6  | 临时寄存器3~6               | 否     |
| pc      | (none) | 程序计数器                  | 未定义 |

#### 2.1.2.浮点寄存器

| 寄存器  | ABI      | 描述                            | 全局 |
| ------- | -------- | ------------------------------- | ---- |
| f0~f7   | ft0~ft7  | 浮点临时寄存器0~7               | 否   |
| f8~f9   | fs0~fs1  | 浮点全局寄存器器0～1            | 是   |
| f10~f11 | fa0~fa1  | 浮点返回值或者是函数调用参数0~1 | 否   |
| f12~f17 | fa2~fa7  | 浮点函数调用参数2~7             | 否   |
| f18~f27 | fs2~fs11 | 浮点全局寄存器2~11              | 是   |
| f28~f31 | ft8~ft11 | 浮点临时寄存器8~11              | 否   |

### 2.2.指令集

#### 2.2.1.基础指令

##### 2.2.1.1整数算术指令

| 指令 | 示例           | 示例含义             | 描述     |
| ---- | -------------- | -------------------- | -------- |
| addi |                |                      |          |
| slti |                |                      |          |
| sltu |                |                      |          |
| andi |                |                      |          |
| ori  |                |                      |          |
| xori |                |                      |          |
| slli |                |                      |          |
| srli |                |                      |          |
| srai |                |                      |          |
| lui  |                |                      |          |
| aupc |                |                      |          |
| add  | add a0, a1, a2 | a0 = a1 + a2         | 加法指令 |
| slt  | slt a0, a1, a2 | a0 = a1 < a2 ? 1 : 0 |          |
| sltu |                |                      |          |
| and  | and a0, a1, a2 | a0 = a1 & a2         |          |
| or   | or a0, a1, a2  | a0 = a1 \| a2        |          |
| xor  | xor a0, a1, a2 | a0 = a1 ^ a2         |          |
| sll  | sll a0, a1, a2 | a0 = a1 >> a2        |          |
| srl  | srl a0, a1, a2 | a0 = a1 >> a2        |          |
| sub  | sub a0, a1, a2 | a0 = a1 - a2         | 减法指令 |
| sra  | sra a0, a1, a2 | a0 = a1 >> a2        |          |

##### 2.2.1.2.控制指令

###### 2.2.1.2.1跳转指令

| 指令 | 示例 | 示例含义 | 描述 |
| ---- | ---- | -------- | ---- |
| jal  |      |          |      |
| jalr |      |          |      |

###### 2.2.1.2.分支指令

| 指令 | 示例 | 示例含义 | 描述 |
| ---- | ---- | -------- | ---- |
| beq  |      |          |      |
| bne  |      |          |      |
| blt  |      |          |      |
| bltu |      |          |      |
| bge  |      |          |      |
| bgeu |      |          |      |

##### 2.2.1.3.Load Store指令

###### 2.2.1.3.1.Load指令

| 指令 | 示例         | 示例含义 | 描述                         |
| ---- | ------------ | -------- | ---------------------------- |
| lb   | lw a0, a1(4) |          | Load一个字节8bits到全局对象  |
| lh   | lh a0, a1(4) |          | Load一个半字16bits到全局对象 |
| lw   | lw a0, a1(4) |          | Load一个字32bits到全局对象   |
| ld   | ld a0, a1(4) |          | Load一个双字64bits到全局对象 |

###### 2.2.1.3.2.Store指令

| 指令 | 示例             | 示例含义 | 描述                          |
| ---- | ---------------- | -------- | ----------------------------- |
| sb   | sb a0, a1(4), a3 |          | Store一个字节8bits到全局对象  |
| sh   | sh a0, a1(4), a3 |          | Store一个半字16bits到全局对象 |
| sw   | sw a0, a1(4), a3 |          | Store一个字32bits到全局对象   |
| sd   | sd a0, a1(4), a3 |          | Store一个双字64bits到全局对象 |

##### 2.2.1.4.内存指令

| 指令  | 示例 | 示例含义 | 描述 |
| ----- | ---- | -------- | ---- |
| fence |      |          |      |

##### 2.2.1.5.环境调用指令

| 指令   | 示例 | 示例含义 | 描述 |
| ------ | ---- | -------- | ---- |
| ecall  |      |          |      |
| ebreak |      |          |      |

##### 2.2.1.5.伪指令

| 指令   | 示例 | 示例含义 | 描述 |
| ------ | ---- | -------- | ---- |
| la     |      |          |      |
| lla    |      |          |      |
| lga    |      |          |      |
| nop    |      |          |      |
| li     |      |          |      |
| mv     |      |          |      |
| not    |      |          |      |
| neg    |      |          |      |
| negw   |      |          |      |
| sext.b |      |          |      |
| sext.h |      |          |      |
| sext.w |      |          |      |
| zext.b |      |          |      |
| zext.h |      |          |      |
| zext.w |      |          |      |
| seqz   |      |          |      |
| snez   |      |          |      |
| sltz   |      |          |      |
| sgtz   |      |          |      |
| fmv.s  |      |          |      |
| fabs.s |      |          |      |
| fneg.s |      |          |      |
| fmv.d  |      |          |      |
| fabs.d |      |          |      |
| fneg.d |      |          |      |
| beqz   |      |          |      |
| bnez   |      |          |      |
| blez   |      |          |      |
| bgez   |      |          |      |
| bltz   |      |          |      |
| bgtz   |      |          |      |
| bgt    |      |          |      |
| ble    |      |          |      |
| bgtu   |      |          |      |
| bleu   |      |          |      |
| j      |      |          |      |
| jal    |      |          |      |
| jr     |      |          |      |
| jalr   |      |          |      |
| ret    |      |          |      |
| call   |      |          |      |
| tail   |      |          |      |
| fence  |      |          |      |

##### 2.2.1.6.CSR伪指令

| 指令       | 示例 | 示例含义 | 描述 |
| ---------- | ---- | -------- | ---- |
| rdinstret  |      |          |      |
| rdinstreth |      |          |      |
| rdcycle    |      |          |      |
| rdcycleh   |      |          |      |
| rdtime     |      |          |      |
| rdtimeh    |      |          |      |
| csrr       |      |          |      |
| csrw       |      |          |      |
| csrs       |      |          |      |
| csrc       |      |          |      |
| csrwi      |      |          |      |
| csrsi      |      |          |      |
| csrci      |      |          |      |
| frcsr      |      |          |      |
| fscsr      |      |          |      |
| frrm       |      |          |      |
| fsrm       |      |          |      |
| fsrmi      |      |          |      |
| frflags    |      |          |      |
| fsflags    |      |          |      |
| fsflagsi   |      |          |      |

##### 2.2.2.M扩展指令（乘法、除法、取模求余）

##### 2.2.3.F扩展指令（单精度浮点指令）

##### 2.2.4.D扩展指令（双精度浮点指令）

##### 2.2.5.Q扩展指令（四倍精度浮点指令）

##### 2.2.6.A扩展指令（原子操作指令）

##### 2.2.7.C扩展指令（压缩指令）

##### 2.2.8.P扩展指令（单指令多数据`Packed-SIMD`指令）

##### 2.2.9.B扩展指令（位操作指令）

##### 2.2.10.H扩展指令（支持`Hypervisor`管理指令）

##### 2.2.11.J扩展指令（支持动态翻译语言指令）

##### 2.2.12.L扩展指令（十进制浮点指令）

##### 2.2.13.N扩展指令（用户中断指令）

##### 2.2.14.G通用指令（包含I、M、A、F、D指令）