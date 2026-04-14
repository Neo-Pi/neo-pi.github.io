---
layout: post
title: OpenWrt 编译环境与固件打包备忘
subtitle: 主机依赖、menuconfig；第三方 feed/包、产物 img 与写盘（含 x86）
---

## 构建主机依赖

在常见发行版上可先装齐基础工具链：

```bash
yum install gcc make pkg-config ncurses-devel diffutils flex bison git rsync
# 或
apt install gcc make pkg-config libncurses-dev diffutils flex bison git rsync
```

**说明：**官方与多数教程以 **Linux** 为首选；在 **macOS** 上全量编译常会遇到工具链/大小写/路径问题，可接受时用 **Docker / Linux 虚拟机** 跑同一套步骤更省事。下文 **macOS + ncurses** 段落保留给必须在本地跑 `menuconfig` 的场景。

## macOS：让 mconf 找到 ncurses

OpenWrt 的 `menuconfig` 依赖 ncurses。使用 Homebrew 安装后，需导出 `pkg-config` 搜索路径，例如：

```bash
export PKG_CONFIG_PATH="/opt/homebrew/opt/ncurses/lib/pkgconfig"
```

（Intel Mac 上 Homebrew 前缀可能是 `/usr/local`。）

## 内核模块：USB 音频

- `Kernel Modules -> Sound Support -> kmod-usb-audio`（注意拼写是 **audio**，不是 auido）
- 也可选用 `kmod-sound-mt7620`（PCM / I2S 路径）

## 故障：staging_dir 里的 pkg-config 找不到 ncurses

典型日志片段：

```text
Unable to find the ncurses package.
...
/openwrt/staging_dir/host/bin/pkg-config: line 4: /bin/pkg-config.real: No such file or directory
```

处理方式：删掉 OpenWrt 构建树里错误的 `pkg-config` 软链，改为指向本机可用的 `pkg-config`（例如 Homebrew）：

```bash
rm staging_dir/host/bin/pkg-config
sudo ln -s /opt/homebrew/bin/pkg-config staging_dir/host/bin/pkg-config
```

路径请按实际 `which pkg-config` 调整；仅在可信构建环境使用 `sudo`。

---

## 从源码到「带第三方软件的整包固件」（浅流程）

下面假设你已按官方说明 `git clone` 对应 **branch**（如 `openwrt-23.05`），并已装好依赖。

### 1. 拉取并登记 feed

```bash
./scripts/feeds update -a
./scripts/feeds install -a
```

- **`-a`**：把所有 feed 里的软件**登记**进构建树（生成 `package/feeds/...` 下的链接/拷贝），之后才能在 `menuconfig` 里搜到。
- 若只想装部分 feed，可只 `update`/`install` 指定 feed名，减少树大小。

### 2. 添加第三方 feed（示例）

编辑 **`feeds.conf.default`**（或复制为 `feeds.conf` 再改），增加一行，例如：

```text
src-git custom https://github.com/example/openwrt-custom-feed.git^main
```

然后：

```bash
./scripts/feeds update custom
./scripts/feeds install -a
```

具体 URL、分支以该第三方文档为准；闭源或本地目录可用 **`src-link`** 指向本机路径。

### 3. 菜单里勾选目标机、内核与软件包

```bash
make menuconfig
```

- **Target System / Subtarget**：选你的路由器或 **x86_64** 等。
- **LuCI / 插件**：在 `LuCI -> Applications` 或对应分类里勾选第三方提供的 `luci-app-*`。
- 保存生成 **`.config`**。

### 4. 全量编译与单包重编

```bash
make -j$(nproc) V=sc download world
# 或调试时
make -j1 V=s
```

只改某个包时（节省时间）：

```bash
make package/some-app/{clean,compile} V=s
```

依赖未变时，最终整包仍在 **`bin/targets/<target>/<subtarget>/`** 下生成。

### 5. 产物长什么样（和「iso」的关系）

OpenWrt **没有**像桌面发行版那样统一的「一个 ISO 装所有机型」。常见是：

| 场景 | 典型文件 | 用途 |
|------|-----------|------|
| 路由器 / 嵌入式 | `*-sysupgrade.bin` / `*-factory.bin` | **sysupgrade** 在线升级或厂商救砖流程见文档 |
| **x86 / 虚拟机** | `*-ext4-combined-*.img.gz`、`*-squashfs-combined-*.img.gz` 等 |解压或管道给 **`dd` 写盘**；注意 **EFI /非 EFI** 文件名 |
| 自定义 rootfs | 目录 `rootfs` + 内核等 | 高级用法，一般不必手搓 |

**说明：** x86 主流分发形态是 **combined `.img`（常 gzip）**，不是传统 **LiveCD ISO**。若你看到带 **iso** 字样的目标，以 **该版本 `make menuconfig` → Target Images** 与 **`bin/targets/...` 实际输出**为准。

---

## 第三方插件打进 img的两种强度

### A. 全流程自己编（上文）

`feeds` + `menuconfig` 勾选 → `make` → 在 **`bin/targets/...`** 取 **combined img** 或 **sysupgrade.bin**。适合改内核、改默认配置、闭源驱动等。

### B. 用 Image Builder「拼包进固件」（不编内核）

官方为部分平台提供 **Image Builder**（预编译的二进制集合）。你只有 **`.ipk` 列表**时，可用它生成带额外软件的新镜像，**不必**从内核重编。下载包与命令以 [OpenWrt Image Builder 文档](https://openwrt.org/docs/guide-user/additional-software/imagebuilder) 为准；版本需与运行固件 **大版本一致**。

---

## x86：把 combined 镜像「一键」写到硬盘（实质是 dd）

**警告：`dd` 写错盘会毁掉整盘数据，务必确认设备名（`lsblk` / `diskutil list`）。**

1. 在 `bin/targets/x86/64/`（路径随版本略变）找到 **`...-ext4-combined-...img.gz`**（或你 menuconfig 里勾选的镜像类型）。
2. 解压后写盘，或管道直接写：

```bash
# Linux 示例：确认 /dev/sdX 为目标硬盘整盘，而非分区
gzip -dc openwrt-*-combined-ext4.img.gz | sudo dd of=/dev/sdX bs=4M conv=fsync status=progress
```

3. 机器 BIOS/UEFI 设为从该盘启动；**EFI 镜像**需与固件启动方式匹配。

虚拟机可把 **同一份 `.img`** 挂成磁盘镜像启动，无需真实 `dd`。

---

## 嵌入式路由：sysupgrade（非 iso）

对已运行 OpenWrt 的设备，一般用 **LuCI → 系统 → 备份/升级** 上传 **`sysupgrade.bin`**，或 SSH：

```bash
sysupgrade -v /tmp/openwrt-*-sysupgrade.bin
```

**factory** 镜像多在原厂固件界面首次刷入时使用，具体以机型 Wiki 为准。

---

## 本地 `package/` 里放一个最小第三方包（指向）

若 feed 里没有，可在 **`package/mypkg/`** 放 **`Makefile`**（遵循 OpenWrt **package 模板**：`include $(TOPDIR)/rules.mk`、`define Package/...`、`define Build/Compile` 等）。官方入门见 [OpenWrt package documentation](https://openwrt.org/docs/guide-developer/packages/start)。编好后同样 `make menuconfig` 勾选，再 `make` 或单包 `compile`，最终仍会进同一 **`bin/targets/...`** 镜像。

---

**小结：** 第三方插件要进「整包」，核心是 **feeds + menuconfig 勾选** 后 **全量 `make`**；x86 安装盘形态多为 **combined img + `dd`**，不是通用 ISO；想少编译可用 **Image Builder**。本文与上层「浅记录」一致，具体文件名、分区、EFI 仍以 **当前 checkout 的 OpenWrt 文档与 `bin/targets` 实际输出**为准。
