---
name: Tailscale扩展文稿推送网络
description: 计划用Tailscale把妈家、兼职等外网机器接入推送体系，实现跨网络文稿分发
type: project
originSessionId: d9f8b5f9-03c2-4858-9968-27347bc05f82
---
## 计划

用 Tailscale 把局域网外的机器接入文稿推送体系，让 dispatch.py 能推到任何地方。

**Why:** 当前推送只限家里局域网。缺哥有妈家电脑、未来可能有兼职（代发文章）需求，电信动态IP不稳定，开SSH公网端口有安全风险，Tailscale是最优解。

**How to apply:** 需要接入新机器时，方案固定用Tailscale：
1. 对方机器安装 Tailscale（Mac/Win均支持）
2. 加入缺哥的 Tailnet（邀请链接或邮件）
3. 获取对方虚拟IP（100.x.x.x格式），写入 dispatch.py 的 MACS 配置
4. 免费版支持100台，IP永久固定不变

## 待接入机器

- [ ] 妈家电脑（电信网络）
- [ ] 未来兼职代发文员的机器
