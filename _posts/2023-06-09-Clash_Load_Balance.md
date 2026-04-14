---
layout: post
title: Clash / mihomo 负载均衡配置
subtitle: 以 mihomo 内核的 proxy-groups 为准；附旧版 Clash for Windows 预处理说明
---

## 背景（为什么旧文容易「对不上」）

早年文章写的是 **Clash for Windows（CFW）** 里的 **预处理 / `parsers`**：用正则匹配订阅名、再 `append-proxy-groups`、用 `commands` 改 `proxy-groups`。如今常见栈是 **[mihomo](https://github.com/MetaCubeX/mihomo)**（原 **Clash Meta**）+ **Clash Verge Rev / Mihomo Party** 等客户端，配置以 **主配置 YAML**（或 Merge 覆写）为主，**不再依赖 CFW 那套 parsers 语法**。

下面以 **mihomo 官方文档**中的 `load-balance` 为准；健康检查 URL 等与内核行为一致即可，与具体 GUI 无关。

## 在配置里增加 `load-balance` 组

在 `proxy-groups` 下增加类型为 `load-balance` 的组，并列出要参与的节点（或引用 `proxy-providers`）。

### 示例：手写节点列表

```yaml
proxy-groups:
  - name: "负载均衡-散列"
    type: load-balance
    proxies:
      - 节点A
      - 节点B
      - 节点C
    url: https://www.gstatic.com/generate_204
    interval: 300
    strategy: consistent-hashing
    # lazy: true   # 可选：仅在被使用时测延迟

  - name: "负载均衡-轮询"
    type: load-balance
    proxies:
      - 节点A
      - 节点B
      - 节点C
    url: https://www.gstatic.com/generate_204
    interval: 300
    strategy: round-robin
```

节点名须与 **`proxies` 里已有名字**一致，或与 `proxy-providers` 展开后的名字一致。

### 示例：从 `proxy-providers` 引用一批节点

若订阅通过 `proxy-providers` 注入，可用 `use` 整组引用（具体字段以你当前配置为准）：

```yaml
proxy-groups:
  - name: "负载均衡"
    type: load-balance
    use:
      - my-provider # 与 proxy-providers 下某段 name 对应
    url: https://www.gstatic.com/generate_204
    interval: 300
    strategy: consistent-hashing
```

## 策略说明（mihomo）

根据 [mihomo 文档：Load-balance](https://wiki.metacubex.one/en/config/proxy-groups/load-balance/)：

| `strategy` | 行为简述 |
|------------|----------|
| `consistent-hashing` | **相同目标地址**（域名用顶级域参与匹配）走**同一节点**，适合要登录、怕 IP 乱跳的站点。 |
| `round-robin` | 在组内节点间**轮询**，多连接下载等场景可能更「散」，但容易触发风控。 |
| `sticky-sessions` | **相同源地址 + 相同目标地址**在一段时间内（文档称约 10 分钟）固定到同一节点；介于两者之间。 |

未写 `strategy` 时由内核默认行为决定，**建议显式写上**，避免升级内核后语义变化。

## 健康检查与 URL

- `url`：用于延迟测试；常用 `https://www.gstatic.com/generate_204`（与文档示例一致即可）。  
- `interval`：探测间隔（秒）。  
- `lazy`：为 `true` 时通常只在**该组被使用**时再测，省流量。

## 在客户端里怎么「改配置」（不写 CFW）

- **Clash Verge Rev**：在配置编辑 / 覆写（Merge）里加入上述 `proxy-groups` 片段，或在图形界面里增加策略组后导出对照 YAML。  
- **Mihomo Party** 等：同样以最终生成的 **mihomo 可加载 YAML** 为准。  

各客户端菜单位置会变，**可靠做法是看生成配置里 `proxy-groups` 是否出现你的 `load-balance` 段**。

## 使用方式

在规则或策略组中，把需要走负载均衡的流量 **指向** 你起的组名（例如 `负载均衡-散列`），与配置普通 `url-test` / `select` 组相同。

---

## 附录：旧版 Clash for Windows「预处理」思路（存档）

若你仍在使用 CFW 且 parsers 可用，当年做法是：在「预处理配置」里用 `reg: 'slbable$'` 匹配订阅名，再 `append-proxy-groups` 并 `commands` 把 `proxyNames` 塞进组。该语法**不是 mihomo 规范的一部分**，换客户端后应改为主配置或 Merge 中的 **`proxy-groups` 写法**，与上文一致即可。
