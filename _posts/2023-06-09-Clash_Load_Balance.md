---
layout: post
title: "Clash Load Balance"
subtitle: "How to configure Clash load balance?"
background: '/img/posts/01.jpg'
---

# Clash负载均衡配置

## 增加预处理配置

设置->配置->预处理配置->编辑
```
parsers:
  - reg: 'slbable$'
    yaml:
      append-proxy-groups:
        - name: ⚖️ 负载均衡-散列
          type: load-balance
          url: 'http://www.google.com/generate_204'
          interval: 300
          strategy: consistent-hashing
        - name: ⚖️ 负载均衡-轮询
          type: load-balance
          url: 'http://www.google.com/generate_204'
          interval: 300
          strategy: round-robin
      commands:
        - proxy-groups.⚖️ 负载均衡-散列.proxies=[]proxyNames
        - proxy-groups.0.proxies.0+⚖️ 负载均衡-散列
        - proxy-groups.⚖️ 负载均衡-轮询.proxies=[]proxyNames
        - proxy-groups.0.proxies.0+⚖️ 负载均衡-轮询
```
保存配置
## 编辑订阅配置信息
配置->右键设置 在订阅链接尾部加上`#slbable`
然后Ok保存
配置->右键预处理配置 出现`1.reg(slbable$)`即设置完成

## 在代理中切换到负载均衡的节点