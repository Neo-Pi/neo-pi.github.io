---
layout: post
title: "Build RISCV Toolchain"
subtitle: "build riscv toolchain in macos m1"
background: '/img/posts/01.jpg'
---

## Environment
💻OS: MacOS 13.0  
🔨ARCH: Apple M1  
💾DISK:**Case-sensitive** (Very Important)

## Install Homebrew
国内源
```
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```
官方源
```
/bin/zsh -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
## Install Environment
```
$ brew install python3 gawk gnu-sed gmp mpfr libmpc isl zlib expat texinfo
$ brew tap discoteq/discoteq
$ brew install flock
```
**!!!Add texinfo in your PATH**  
## Config Toolchain
```
$ mkdir /opt/riscv64
$ ./configure --enable-multilib --prefix=/opt/riscv64
```
## Build Toolchain
```
$ make install -j8
```