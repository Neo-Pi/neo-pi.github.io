---
layout: post
title: "构建 RISC-V GNU 工具链"
subtitle: "在 macOS（Apple Silicon）上从源码编译 riscv-gnu-toolchain；注意 Xcode / 命令行工具"
---

## 环境

- 系统：macOS
- 架构：Apple Silicon（M 系列）或 Intel
- 磁盘：**区分大小写的卷**（`case-sensitive`）可避免构建过程中路径/工具问题，尽量使用

## Xcode / 命令行工具（与复现强相关）

从源码编译 `riscv-gnu-toolchain` 时，**宿主编译器**用的是 macOS 上的 **Apple Clang**（来自 **Xcode** 或 **Command Line Tools for Xcode**）。GCC 交叉编译器本身是一步步用宿主编译器引导出来的，因此：

- **升级 Xcode、只更新 CLT、或换 major 的 macOS** 后，Clang 版本、SDK 路径和默认警告行为都会变，同一套源码可能出现**上次能编、这次报错**。
- 典型表现：`-Werror`、头文件/内建函数行为差异、链接阶段找不到某符号等，堆栈往往落在 **正在编 stage1/host 工具** 或 **编 libgcc 某文件** 时。

**建议先固定并记下当前工具链版本，便于排查：**

```sh
xcode-select -p
clang --version
# 若装了完整 Xcode，还可看：
xcodebuild -version 2>/dev/null || true
```

若未安装 CLT，执行 `xcode-select --install` 按提示安装。文档里若写「某次成功环境」，最好同时写上 **当时 `clang --version` 一行输出**。

**若升级后出现新的编译错误，可依次尝试：**

1. **干净重编**：`make distclean`（或删掉构建目录后重新 `configure && make`），避免混用旧对象文件。
2. **换用 Homebrew 的 GCC 作宿主编译器**（部分 Clang 版本对上游 GCC 源码更「挑剔」时有效）：
   ```sh
   brew install gcc
   ls "$(brew --prefix gcc)/bin/gcc-"* "$(brew --prefix gcc)/bin/g++-"*
   # 按上面列出的带版本号可执行文件填写 CC/CXX（勿用无后缀的 `gcc`，通常仍指向 Apple Clang）
   G="$(brew --prefix gcc)/bin"
   export CC="$G/gcc-14" CXX="$G/g++-14"   # 14 改为与你机器 ls 结果一致
   ./configure ...   # 见下文
   make -j"$(sysctl -n hw.ncpu)"
   ```
3. 到 [riscv-gnu-toolchain Issues](https://github.com/riscv-collab/riscv-gnu-toolchain/issues) 搜索 **macOS / Xcode / clang** 与报错片段，上游常有针对某版 Xcode 的补丁或 `CFLAGS` 讨论。

**若不需要自己改 GCC / 多版本对比**，可直接用 Homebrew 装预编译交叉编译器，避免绑死本机 Xcode 细节：

```sh
brew install riscv64-elf-gcc
```

与源码安装的 `prefix`、多库（multilib）组合可能不完全一致，按项目需求选择。

## 安装 Homebrew

国内源（可选，脚本来自第三方，请自行判断信任度）：

```sh
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```

官方安装脚本：

```sh
/bin/zsh -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## 安装依赖

```sh
brew install python3 gawk gnu-sed gmp mpfr libmpc isl zlib expat texinfo git
brew tap discoteq/discoteq
brew install flock
```

**务必把 texinfo 提供的工具加入 PATH**（例如 `brew --prefix texinfo` 下的 `bin`），否则可能找不到 `makeinfo`。

## 获取源码

官方仓库：[riscv-collab/riscv-gnu-toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain)

```sh
git clone https://github.com/riscv-collab/riscv-gnu-toolchain.git
cd riscv-gnu-toolchain
git submodule update --init --recursive
```

## 配置

指定安装前缀（示例为 `/opt/riscv64`，需有写权限；也可用 `$HOME/riscv` 等路径）：

```sh
sudo mkdir -p /opt/riscv64
sudo chown "$(whoami)" /opt/riscv64
./configure --enable-multilib --prefix=/opt/riscv64
```

若只关心 Newlib / Linux 等特定目标，可在仓库 README 中查看 `--with-arch` / `--with-abi` 等选项组合。

## 编译安装

```sh
make -j"$(sysctl -n hw.ncpu)"
make install
```

完成后把 `bin` 加入 `PATH`，例如：

```sh
export PATH="/opt/riscv64/bin:$PATH"
```

用 `riscv64-unknown-elf-gcc -v`（或你配置的目标三元组对应的 `*-gcc -v`）验证安装是否成功。

---

**小结：** macOS 上复现源码构建时，把 **Xcode / CLT 与 `clang --version`** 和 **是否使用 Homebrew `gcc` 作为 CC/CXX** 记下来，能大幅减少「文章步骤一样却编不过」的差异；若只求能用的 RISC-V 工具链，优先考虑 `brew install riscv64-elf-gcc`。
