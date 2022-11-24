---
layout: post
title: "RISC-V 编程速查手册"
subtitle: "收集整理了一些常用的指令以及常用的ToolChain选项"
background: '/img/posts/01.jpg'
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
  
  指定整数和浮点的调用约束,需要配合`-march`使用，选项有`ilp32` `ilp32f` `ilp32d` `lp64` `lp64f` `lp64d`,例如`-march=rv32i -mabi=lp32`

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
  
  是否利用链接器(linker) 松弛来减少实现符号地址所需的指令数量。默认选项会开启`-mrelex`

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

#### 1.2.2.objdump选项

#### 1.2.3.objcopy选项

#### 1.2.4.size选项

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
| R型  | 算术指令格式   | add\sub\sll\xor\srl\sra\or\and                                 |
| I型  | 加载&立即数算术 | lb\lh\lw\ld\lbu\lhu\lwu\addi\slli\xori\srli\srai\ori\andi\jalr |
| S型  | 存储       | sb\sh\sw\sd                                                    |
| SB型 | 条件分支格式   | beq\bne\blt\bge\bltu\begu                                      |
| UJ型 | 无条件跳转    | lui                                                            |
| U型  | 打立即数格式   |                                                                |

##### 2.2.1.1整数算术指令

| 指令   | 示例              | 示例含义                 | 描述                    |
|:---- |:--------------- |:--------------------:| ---------------------:|
| addi | addi a0, a1, 20 | a0 = a1 + 20         | 用于加一个常数               |
| slti | slt a0, a1, 20  | a0 = a1 < 20 ? 1 : 0 | 比较a1与立即数，将bool结果给a0   |
| andi | andi a0, a1, 20 | a0 = a1 & 20         | 寄存器与常数按位与             |
| ori  | ori a0, a1, 20  | a0 = a1 \| 20        | 寄存器与常数按位或             |
| xori | xori a0, a1, 20 | a0 = a1 ^ 20         | 寄存器与常数按位异或            |
| slli | slli a0, a1, 3  | a0 = a1 << 3         | 根据立即数给定位数左移           |
| srli | srli a0, a1, 3  | a0 = a1 >> 3         | 根据立即数给定位数右移           |
| srai | srai a0, a1, 3  | a0 = a1 >> 3         | 根据立即数给定位数算术右移         |
| add  | add a0, a1, a2  | a0 = a1 + a2         | 加法指令                  |
| slta | slt a0, a1, a2  | a0 = a1 < a2 ? 1 : 0 | 比较a1与a2，将bool结果给a0    |
| sltu | sltu a0, a1, a2 | a0 = a1 < a2 ? 1 : 0 | 无符号比较a1与a2，将bool结果给a0 |
| and  | and a0, a1, a2  | a0 = a1 & a2         | 三寄存器操作数：按位与           |
| or   | or a0, a1, a2   | a0 = a1 \| a2        | 三寄存器操作数：按位或           |
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
| fence | fence iorw, iorw | 设备输入（I）、设备输出（O）、存储器读取（R）和存储器写入（W） | 用于隔离上下文 |

##### 2.2.1.5.环境调用指令

| 指令     | 示例     | 描述                                   |
| ------ | ------ | ------------------------------------:|
| ecall  | ecall  | 在U\S\M模式下执行可产生ecall异常，主要用于sbi接口调用等操作 |
| ebreak | ebreak | 调试器可使用它将控制权转移回调试环境，可产生一个ebreak异常     |

##### 2.2.1.5.伪指令

| 指令            | 示例                           | 示例含义                                                                 | 描述            |
| ------------- | ---------------------------- | -------------------------------------------------------------------- | -------------:|
| la            | la a0, symbol                | 格式和lla或者lga一致                                                        | 取地址，包含lla和lga |
| lla           | lla a0, symbol               | auipc a0, symbol[31:12]; addi a0 a0, symbol[11:0]                    | 取本地地址         |
| lga           | lga a0, symbol               | auipc a0, symbol@global[31:12]; l{w\|d} a0, symbol@global[11:0] (a0) | 取全局地址         |
| l{b\|h\|w\|d} | l{b\|h\|w\|d} a0, symbol     | auipc a0, symbol[31:12]; l{b\|h\|w\|d} a0, symbol[11:0] (a0)         | 取全局地址         |
| s{b\|h\|w\|d} | s{b\|h\|w\|d} a0, symbol, a1 | auipc a1, symbol[31:12]; s{b\|h\|w\|d} a0, symbol[11:0] (a1)         | 存全局地址         |
| fl{w\|d}      | fl{w\|d} f0, symbol, a0      | auipc a0, symbol[31:12]; fl{w\|d} f0, symbol[11:0] (a0)              | 浮点取全局地址       |
| fs{w\|d}      | fs{w\|d} f0, symbol, a0      | auipc a0, symbol[31:12]; fs{w\|d} f0, symbol[11:0] (a0)              | 浮点存全局地址       |
| nop           | nop                          | addi zero, zero, 0                                                   | 空指令           |
| li            | li a0, 20                    | addi a0, a0, 20                                                      | 将常数加载到整数寄存器   |
| mv            | mv a0, a1                    | addi a0, a1, 0                                                       | 拷贝寄存器         |
| not           | not a0, a1                   | xori a0, a1, -1                                                      | 1的补码          |
| neg           | neg a0, a1                   | sub a0,  zero, a1                                                    | 2的补码          |
| negw          | negw a0, a1                  | subw a0, zero, a1                                                    | 2的补码字         |
| sext.b        | sext.b a0, a1                | slli a0, a1, XLEN - 8; srai a0, a0, XLEN - 8                         | 扩展符号 字节       |
| sext.h        | sext.h a0, a1                | slli a0, a1, XLEN - 16; srai a0, a0, XLEN - 16                       | 扩展符号 半字       |
| sext.w        | sext.w a0, a1                | addiw a0, a1, 0                                                      | 扩展符号 字        |
| zext.b        | zext.b a0, a1                | andi a0, a1, 255                                                     | 扩零 字节         |
| zext.h        | zext.h a0, a1                | slli a0, a1, XLEN - 16; srli a0, a0, XLEN - 16                       | 扩零 半字         |
| zext.w        | zext.w a0, a1                | slli a0, a1, XLEN - 32; srli a0, a0, XLEN - 32                       | 扩零 字          |
| seqz          |                              |                                                                      |               |
| snez          |                              |                                                                      |               |
| sltz          |                              |                                                                      |               |
| sgtz          |                              |                                                                      |               |
| fmv.s         |                              |                                                                      |               |
| fabs.s        |                              |                                                                      |               |
| fneg.s        |                              |                                                                      |               |
| fmv.d         |                              |                                                                      |               |
| fabs.d        |                              |                                                                      |               |
| fneg.d        |                              |                                                                      |               |
| beqz          |                              |                                                                      |               |
| bnez          |                              |                                                                      |               |
| blez          |                              |                                                                      |               |
| bgez          |                              |                                                                      |               |
| bltz          |                              |                                                                      |               |
| bgtz          |                              |                                                                      |               |
| bgt           |                              |                                                                      |               |
| ble           |                              |                                                                      |               |
| bgtu          |                              |                                                                      |               |
| bleu          |                              |                                                                      |               |
| j             | j offset                     | jal zero, offset                                                     | 跳转            |
| jal           | jal offset                   | jal ra, offset                                                       | 跳转并链接         |
| jr            | jr a0                        | jalr zero, a0, 0                                                     | 跳转到寄存器的值      |
| jalr          | jalr rs                      | jalr ra, a0, 0                                                       | 跳转到寄存器并链接     |
| ret           | ret                          | jalr zero, ra, 0                                                     | 返回            |
| call          | call offset                  | auipc ra, offset[31:12]; jalr ra, ra, offset[11:0]                   | 远端调用          |
| tail          | tail offset                  | auipc a0, offset[31:12]; jalr zero, a0, offset[11:0]                 |               |
| fence         | fence                        | fence iorw, iorw                                                     |               |

##### 2.2.1.6.CSR伪指令

| 指令         | 示例  | 示例含义 | 描述  |
| ---------- | --- | ---- | ---:|
| rdinstret  |     |      |     |
| rdinstreth |     |      |     |
| rdcycle    |     |      |     |
| rdcycleh   |     |      |     |
| rdtime     |     |      |     |
| rdtimeh    |     |      |     |
| csrr       |     |      |     |
| csrw       |     |      |     |
| csrs       |     |      |     |
| csrc       |     |      |     |
| csrwi      |     |      |     |
| csrsi      |     |      |     |
| csrci      |     |      |     |
| frcsr      |     |      |     |
| fscsr      |     |      |     |
| frrm       |     |      |     |
| fsrm       |     |      |     |
| fsrmi      |     |      |     |
| frflags    |     |      |     |
| fsflags    |     |      |     |
| fsflagsi   |     |      |     |

##### 2.2.2.M扩展指令（乘法、除法、取模求余）

##### 2.2.3.F扩展指令（单精度浮点指令）

| 指令        | 示例                       | 示例含义                        | 描述                                      |
| --------- | ------------------------ | --------------------------- | ---------------------------------------:|
| flw       | flw f0, 40(a0)           | f0 = mem[a0+40]             | Load单精度字到浮点寄存器                          |
| fsw       | fsw f0, 40(a0)           | mem[a0+40] = f0             | Store单精度字到内存                            |
| fmadd.s   | fmadd.s f0, f1, f2, f3   | f0 = f1 \* f2 + f3          | 单精度浮点乘法后加法                              |
| fmsub.s   | fmsub.s f0, f1, f2, f3   | f0 = f1 \* f2 - f3          | 单精度浮点乘法后减法                              |
| fnmadd.s  | fnmadd.s f0, f1, f2, f3  | f0 = f1 \* f2 + f3          | 单精度浮点乘法后加法                              |
| fnmsub.s  | fnmsub.s f0, f1, f2 , f3 | f0 = f1 \* f2 - f3          | 单精度浮点乘法后减法                              |
| fadd.s    | fadd.s f0, f1, f2        | f0 = f1 + f2                | 单精度浮点加法                                 |
| fsub.s    | fsub.s f0, f1, f2        | f0 = f1 - f2                | 单精度浮点减法                                 |
| fmul.s    | fmul.s f0, f1, f2        | f0 = f1 \* f2               | 单精度浮点乘法                                 |
| fdiv.s    | fdiv.s f0, f1, f2        | f0 = f1 / f2                | 单精度浮点除法                                 |
| fsqrt.s   | fadd.s f0, f1            | f0 = √￣f1                   | 单精度浮点平方根                                |
| fsgnj.s   | fsgnj.s f0, f1, f2       | f0 = f2[31] + f1[30:0]      | 取f2的符号位与f1的数据位相加                        |
| fsgnjn.s  | fsgnjn.s f0, f1, f2      | f0 = ~f2[31] + f1[30:0]     | 取f2的符号位取反后与f1的数据位相加                     |
| fsgnjx.s  | fsgnjx.s f0, f1, f2      | f0 = f1[31]^f2[31]+f1[30:0] | 将f1的符号位与f2的符号位异或后与f1数据位相加               |
| fmin.s    | fmin f0, f1, f2          | f0 = (f1 > f2) ? f2: f1     | 单精度浮点比较取最小值                             |
| fmax.s    | fmax f0, f1 f2           | f0 = (f1 > f2) ? f1: f2     | 单精度浮点比较取最大值                             |
| fcvt.w\.s | fcvt.w\.s a0, f0         | a0 = (int32\_t) f0          | 单精度浮点转32bits整形                          |
| fcvt.wu.s | fcvt.wu.s a0, f0         | a0 = (uint32\_t) f0         | 单精度浮点转无符号32bits整形                       |
| fcvt.l.s  | fcvt.l.s a0, f0          | a0 = (int64\_t) f0          | 单精度浮点转64bits整形                          |
| fcvt.lu.s | fcvt.lu.s a0, f0         | a0 = (uint64\_t) f0         | 单精度浮点转无符号64bits整形                       |
| fcvt.s.w  | fcvt.s.w a0, f0          | f0 = (float32\_t) a0        | 32bits整形转单精度浮点                          |
| fcvt.s.wu | fcvt.s.wu a0, f0         | f0 = (float32\_t) a0        | 无符号32bits整形转单精度浮点                       |
| fcvt.s.l  | fcvt.s.l a0, f0          | f0 = (float64\_t) a0        | 64bits整形转单精度浮点                          |
| fcvt.s.lu | fcvt.s.lu a0, f0         | f0 = (float64\_t) a0        | 无符号64bits整形转单精度浮点                       |
| fmv.xw    | fmv.xw a0, f0            | a0 = sext(f0)               | 将浮点寄存器以IEEE 754-2008编码格式保存至整数寄存器        |
| fmv.wx    | fmv.wx f0, a0            | f0 = a0                     | 将以IEEE 754-2008编码格式的单精度值从整数寄存器移动到浮点寄存器中 |
| feq.s     | feq.s a0, f1, f2         | a0 = (f0==f1) ? 1 : 0       | 单精度浮点比较并将bool值给整数寄存器                    |
| flt.s     | flt.s a0, f1, f2         | a0 = (f0\<f1) ? 1 : 0       | 单精度浮点比较并将bool值给整数寄存器                    |
| fle.s     | fle.s a0, f1, f2         | a0 = (f0<=f1) ? 1 : 0       | 单精度浮点加法                                 |
| fclass.s  | fclass.s a0, f0          | f0 is type, a0 = type       | 单精度浮点分类，详情见[批注1](#1)                    |

<span id="1">批注[1]</span>
<ul>
<li  markdown="1">
![fclass](/img/posts/fclass.png)
</li>
</ul>

##### 2.2.4.D扩展指令（双精度浮点指令）

| 指令        | 示例                       | 示例含义                        | 描述                                      |
| --------- | ------------------------ | --------------------------- | ---------------------------------------:|
| fld       | flw f0, 40(a0)           | f0 = mem[a0+40]             | Load双精度到浮点寄存器                           |
| fsd       | fsw f0, 40(a0)           | mem[a0+40] = f0             | Store双精度符点到内存                           |
| fmadd.d   | fmadd.d f0, f1, f2, f3   | f0 = f1 \* f2 + f3          | 双精度浮点乘法后加法                              |
| fmsub.d   | fmsub.d f0, f1, f2, f3   | f0 = f1 \* f2 - f3          | 双精度浮点乘法后减法                              |
| fnmadd.d  | fnmadd.d f0, f1, f2, f3  | f0 = f1 \* f2 + f3          | 双精度浮点乘法后加法                              |
| fnmsub.d  | fnmsub.d f0, f1, f2 , f3 | f0 = f1 \* f2 - f3          | 双精度浮点乘法后减法                              |
| fadd.d    | fadd.d f0, f1, f2        | f0 = f1 + f2                | 双精度浮点加法                                 |
| fsub.d    | fsub.d f0, f1, f2        | f0 = f1 - f2                | 双精度浮点减法                                 |
| fmul.d    | fmul.d f0, f1, f2        | f0 = f1 \* f2               | 双精度浮点乘法                                 |
| fdiv.d    | fdiv.d f0, f1, f2        | f0 = f1 / f2                | 双精度浮点除法                                 |
| fsqrt.d   | fadd.d f0, f1            | f0 = √￣f1                   | 双精度浮点平方根                                |
| fsgnj.d   | fsgnj.d f0, f1, f2       | f0 = f2[31] + f1[30:0]      | 取f2的符号位与f1的数据位相加                        |
| fsgnjn.d  | fsgnjn.d f0, f1, f2      | f0 = ~f2[31] + f1[30:0]     | 取f2的符号位取反后与f1的数据位相加                     |
| fsgnjx.d  | fsgnjx.d f0, f1, f2      | f0 = f1[31]^f2[31]+f1[30:0] | 将f1的符号位与f2的符号位异或后与f1数据位相加               |
| fmin.d    | fmin f0, f1, f2          | f0 = (f1 > f2) ? f2: f1     | 双精度浮点比较取最小值                             |
| fmax.d    | fmax f0, f1 f2           | f0 = (f1 > f2) ? f1: f2     | 双精度浮点比较取最大值                             |
| fcvt.w\.d | fcvt.w\.d a0, f0         | a0 = (int32\_t) f0          | 双精度浮点转32bits整形                          |
| fcvt.wu.d | fcvt.wu.d a0, f0         | a0 = (uint32\_t) f0         | 双精度浮点转无符号32bits整形                       |
| fcvt.l.d  | fcvt.l.d a0, f0          | a0 = (int64\_t) f0          | 双精度浮点转64bits整形                          |
| fcvt.lu.d | fcvt.lu.d a0, f0         | a0 = (uint64\_t) f0         | 双精度浮点转无符号64bits整形                       |
| fcvt.d.w  | fcvt.d.w a0, f0          | f0 = (float32\_t) a0        | 32bits整形转双精度浮点                          |
| fcvt.d.wu | fcvt.d.wu a0, f0         | f0 = (float32\_t) a0        | 无符号32bits整形转双精度浮点                       |
| fcvt.d.l  | fcvt.d.l a0, f0          | f0 = (float64\_t) a0        | 64bits整形转双精度浮点                          |
| fcvt.d.lu | fcvt.d.lu a0, f0         | f0 = (float64\_t) a0        | 无符号64bits整形转双精度浮点                       |
| fmv.xd    | fmv.xd a0, f0            | a0 = sext(f0)               | 将浮点寄存器以IEEE 754-2008编码格式保存至整数寄存器        |
| fmv.dx    | fmv.dx f0, a0            | f0 = a0                     | 将以IEEE 754-2008编码格式的双精度值从整数寄存器移动到浮点寄存器中 |
| feq.d     | feq.d a0, f1, f2         | a0 = (f0==f1) ? 1 : 0       | 双精度浮点比较并将bool值给整数寄存器                    |
| flt.d     | flt.d a0, f1, f2         | a0 = (f0\<f1) ? 1 : 0       | 双精度浮点比较并将bool值给整数寄存器                    |
| fle.d     | fle.d a0, f1, f2         | a0 = (f0<=f1) ? 1 : 0       | 双精度浮点加法                                 |
| fclass.d  | fclass.d a0, f0          | f0 is type, a0 = type       | 双精度浮点分类，详情见[批注1](#1)                    |

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

## 参考资料

* 伯克利大学[riscv reference card](https://inst.eecs.berkeley.edu/\~cs61c/sp22/pdfs/resources/reference-card.pdf)

* [RISCV ISA Manual](https://github.com/riscv/riscv-isa-manual/releases)

* [RISCV ASM Manual](https://github.com/riscv-non-isa/riscv-asm-manual/blob/master/riscv-asm.md)

* [RISCV C API Doc](https://github.com/riscv-non-isa/riscv-c-api-doc/blob/master/riscv-c-api.md)
