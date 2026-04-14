---
layout: post
title: 将 Newlib 用于 RISC-V 裸机与交叉工具链
subtitle: configure 链路备忘；printf 落到硬件 UART 的 syscalls 案例（riscv*-unknown-elf）
---

## 实验环境（备忘）

- **Newlib**：4.4.0（版本随工具链源码树而变）
- **工具链**：`riscv32-unknown-elf` / `riscv64-unknown-elf` 思路相同，下文统称 **riscv*-unknown-elf**
- **ISA 示例**：`rv32imac` / `ilp32` 等，以你的 `-march/-mabi` 为准
- **GNU Autoconf**：2.69一类版本常与官方 newlib 构建脚本匹配；换版本若报错需对照发行说明

## Newlib 编译链里几个文件的关系（原文档）

`configure`：由 `autoconf` 生成的 shell 脚本，检查构建环境并生成 Makefile等。运行 `./configure` 即执行它。

`configure.ac`：`autoconf` 的输入（宏描述），`autoconf` 据此生成 `configure`。

`configure.host`：在交叉编译等场景里提供**宿主/目标**相关片段，供 `configure` 包含使用，用于生成针对特定主机或目标的 Makefile规则。

关系概括：`configure.ac` →（autoconf）→ `configure`；执行 `./configure` 时再结合 `configure.host` 等生成最终构建树。

---

## 先分清两条路：改工具链 vs 只在工程里接桩

| 做法 | 适用 |
|------|------|
| **应用工程里**提供 `syscalls.c`（实现 `_write`、`_sbrk` 等），与 **官方编好的** `riscv*-unknown-elf-gcc` + newlib 链接 | 最常见；printf 走 UART、heap 用链接脚本符号，**不必 fork newlib** |
| **在 riscv-gnu-toolchain 源码树里改 newlib/libgloss**，再 `make` 全量或部分重编 | 多项目统一默认行为、或要改 **libc 本身**（非仅 OS接口层）时 |

下面 **printf → UART** 的例子两种路都适用：逻辑一样，差别只是 `syscalls.c` 放在你的 app 里链接，还是预先编进/补丁进发行版 libgloss。

---

## printf 是怎样碰到硬件的（数据流）

在 **裸机 + newlib** 下，没有 Linux `write(2)`，C 库里会把 `printf` 缓冲后走到 **`write()`**，最终由 **libgloss / syscalls** 里的 **`_write(int fd, const void *buf, size_t count)`** 把字节交给你实现。

典型关系：

`printf` →（newlib stdio）→ `write(fd=1, ...)` → **`_write`** → 你的 **UART 发送寄存器**。

因此「把 printf 接到 UART」**核心是实现 `_write`**（至少处理 `fd == 1` / `2`，即 stdout/stderr）。若使用 **`-specs=nano.specs`**，stdio 更省 flash，但 `_write` 仍需要。

---

## 案例：MMIO UART + 最小 syscalls

以下地址与寄存器布局**仅为示例**，请换成你 SoC TRM 中的 **UART 基址与 THR/LSR**定义。

### 1. 极简 UART 发送（轮询）

```c
/* uart_hal.h / uart_hal.c —— 示例，非真实芯片 */
#include <stdint.h>

#define UART_BASE ((uintptr_t)0x60000000)   /* 示例：请改为手册中的基址 */
#define UART_THR    (*(volatile uint32_t *)(UART_BASE + 0x00)) /* 发送保持，视位宽而定 */
#define UART_LSR    (*(volatile uint32_t *)(UART_BASE + 0x14)) /* 状态：示例偏移 */
#define LSR_THRE    (1u << 5)                 /* 发送 FIFO 空，以手册为准 */

void uart_putc(char c) {
  while ((UART_LSR & LSR_THRE) == 0)
    ;
  UART_THR = (uint32_t)(unsigned char)c;
}
```

很多16550 风格 UART 是 **8-bit 寄存器**；若你的 IP 是 32-bit 对齐访问，把 `volatile uint8_t` 或掩码按 TRM 调整。

### 2. 实现 `_write`（stdout/stderr 走 UART）

```c
/* syscalls.c —— 与 newlib 链接 */
#include <errno.h>
#include <unistd.h>
#include <stddef.h>

extern void uart_putc(char c);  /* 上面实现 */

int _write(int fd, const void *buf, size_t count) {
  if (fd != STDOUT_FILENO && fd != STDERR_FILENO) {
    errno = EBADF;
    return -1;
  }
  const char *p = (const char *)buf;
  for (size_t i = 0; i < count; i++)
    uart_putc(p[i]);
  return (int)count;
}
```

若你希望 `printf` **无缓冲**（便于最早期的 boot 调试），在 UART 初始化后尽早：`#include <stdio.h>` 并调用 `setvbuf(stdout, NULL, _IONBF, 0);`。

### 3. `_sbrk`（若使用 `malloc` / printf 某些路径）

链接脚本里通常导出 **`_end`**（或 `__heap_start`）作为 bss 结束；向 **`_heap_end` / RAM顶** 生长：

```c
#include <errno.h>
#include <unistd.h>

extern char _end;   /* ld 脚本里 PROVIDE；名称以你的 .ld 为准 */
static char *heap_ptr = &_end;

void *_sbrk(ptrdiff_t incr) {
  extern char __stack[];      /* 栈底符号，按你链接脚本定义 */
  char *prev = heap_ptr;
  if (heap_ptr + incr > __stack) {
    errno = ENOMEM;
    return (void *)-1;
  }
  heap_ptr += incr;
  return prev;
}
```

**注意：** 符号名（`_end`、`end`、`__heap_start`、`__stack`）必须与 **实际 `.ld`** 一致；很多 RISC-V 示例用 `PROVIDE(_heap_start = .);` 等，以你工程为准。

### 4. 其它常见桩

- **`_exit`**：死循环或写复位寄存器，避免链接报错。
- **`_read`**：若不用 `scanf`，可返回 `0` 或 `-1` 并设 `errno`。
- **`_getpid` / `_kill`**等：nosys 或最小实现，满足链接即可。

使用 **`--specs=nosys.specs`** 时，部分桩由 nosys 提供，但仍常需 **自己实现 `_write`** 才能真上 UART。

### 5. 编译链接示例

```sh
riscv32-unknown-elf-gcc -march=rv32imac -mabi=ilp32 -Os -g \
  -T your_linker.ld \
  crt0.S main.c uart_hal.c syscalls.c \
  -lc -lgcc
```

若使用 **nano newlib**，加上编译器驱动传入的 **`--specs=nano.specs`**（以及配套的 `nosys`/`rdimon` 视需求而定），具体以工具链 `riscv32-unknown-elf-gcc -print-file-name=...` 打印的路径为准。

---

## 若要把这类修改「做进」riscv-gnu-toolchain 里的 newlib

思路与「应用里放 `syscalls.c`」相同，只是把默认实现放进源码树再安装：

- 在 **`riscv-gnu-toolchain` 解压/克隆目录** 中，newlib 通常在 **`newlib/`** 下；与裸机板级相关的大量桩在 **`libgloss/`**（含各 `sys` / 架构子目录）。
- 可为你的板子增加 **board 目录** 或在现有 **riscv** 相关 `libgloss` 里加入 **`syscalls.c`**，使安装后的 **`crt0` + 默认库** 已带 UART `_write`（团队内统一工具链时常这么做）。
- 修改后常见做法是 **仅重编 newlib**（若构建系统支持）或 **`make -j` 全量**，以该仓库 README 为准；安装前缀与 **PATH** 指向新生成的 `riscv*-unknown-elf-gcc`。

Autoconf 层面仍涉及前文的 **`configure` / `configure.host`**：交叉构建 newlib 时 host=构建机、target=`riscv32-unknown-elf`，具体选项与 **riscv-gnu-toolchain顶层 `configure`** 一致即可，一般不必单独深入 newlib 子目录手跑一遍，除非你在做 **深度改 libc**。

---

## 小结

- **printf → UART** 的关键是 **`_write`** + 你的 **MMIO 发字符**；再按需补 **`_sbrk`**、**`_exit`** 等。
- **多数情况**不必改 newlib 源码：在应用里链接 **`syscalls.c`** 即可；**统一工具链**时再把同一套文件并入 **libgloss** 并重编安装。
- **UART 寄存器与链接脚本符号**必须以 **TRM +自己 `.ld`** 为准，本文地址与位域仅作结构示例。
