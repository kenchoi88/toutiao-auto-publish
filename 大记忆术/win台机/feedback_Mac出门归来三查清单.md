---
name: Mac 出门连陌生网回家三查清单
description: air/mac 切 SSID(移动热点/咖啡馆 WiFi/酒店等)回家后,小火箭+Tailscale 互相搞坏,先查 3 项不要瞎重启
type: feedback
originSessionId: 9d19d23b-db65-4712-96ac-91a7a3b3783b
---
# Mac 出门连陌生网回家三查清单

(2026-05-06 立条,基于阿良 air 5-05 跟着缺哥出街连移动热点回家后,Tailscale 走 SFO relay + tailscaled daemon 拿 fake-IP 198.18.x 卡死的实战教训)

## 故障重现路径
```
缺哥带 air 出门
  → air 接移动热点 / 别 WiFi
  → Shadowrocket 切配置/重连/规则重载
  → tailscaled daemon 重新连 controlplane.tailscale.com
       但 Shadowrocket fake-DNS 把它解到 198.18.x
       → daemon connect timeout → 节点掉线 → fallback DERP relay
回家接回 AX3 LAN
  → 物理同 LAN 但 Tailscale 还困在 relay 状态
  → 跨机 ssh 走 SFO 中转 RTT 370ms
```

## 三查清单 (按顺序,不查直接重启会越搞越乱)

### 第一查: Shadowrocket 是否还在劫 daemon

```bash
# air 上跑
ps aux | grep -iE "shadowrocket|MacPacket" | grep -v grep
# 看进程在,说明 Shadowrocket 还在跑(不能轻关,关了 air 也连不上 Anthropic API)

# 看 tailscaled 是否走 1082 HTTP 代理
sudo launchctl print system/com.tailscale.tailscaled | grep -A2 EnvironmentVariables
# 应看到 HTTPS_PROXY = http://127.0.0.1:1082

# 测代理通不通
curl -x http://127.0.0.1:1082 https://controlplane.tailscale.com/health -m 10
# 返回 404 unknown endpoint = 通(GET 不被 endpoint 接受是预期,关键是 HTTPS 握手成)

# 看 daemon 状态
/opt/homebrew/bin/tailscale status 2>&1 | head -3
# 不应是 "Logged out." — 是的话执行第二查
```

### 第二查: Tailscale 是否走 direct (LAN) 还是 relay (SFO)

```bash
# air 上跑
/opt/homebrew/bin/tailscale ping 100.86.79.39  # 台机 IP
# 期望: pong from ken-choi via [...:41641] direct
# 如果是: pong from ken-choi via DERP(sfo) → 还在中转
```

direct 但走 IPv6 P2P 也算正常(实测 5ms 同 LAN ✓)。如果是 relay:
```bash
# 软修 (无副作用,不重新认证)
sudo /opt/homebrew/bin/tailscale down
sleep 2
sudo /opt/homebrew/bin/tailscale up --hostname=air --ssh
# 让 daemon 重新协商 endpoint
```

### 第三查: db 三层放行还在不在 (切 SSID 不影响 db,但 5-06 之前 mini+neo 缺过,审计一下)

```bash
sqlite3 ~/Library/Containers/com.liguangming.Shadowrocket/Data/Documents/Databases/default.db \
  "SELECT docid, name, value FROM config WHERE docid IN (2,3);"
# docid=2 skip-proxy 必须含 100.64.0.0/10
# docid=3 tun-excluded-routes 必须含 100.64.0.0/10
```

详见 `feedback_shadowrocket_skip_proxy.md`,缺则按那条修法 UPDATE。

## 不要做的事

- ❌ 不要 quit Shadowrocket → air 同时失去出墙能力,Anthropic API 挂,阿良死
- ❌ 不要 sudo tailscale up --reset → 会让 daemon logout 触发重新 web 认证(旧 hostname 可能被 admin 后台占用,自动加 -1 后缀注册成新节点,清理麻烦)
- ❌ 不要 hostname 改名规避冲突(如 airLE) → admin 后台手改回正确名才能保持 magic DNS 一致

## How to apply

- 缺哥 + 任何 mac 出门连过陌生 WiFi 后回家,**第一动作三查**,不查不重启,不重装
- 不查就 reauth 是上次 air 的傻逼路径,搞出 3 个 air 节点(air / kenchoiair / air-1) admin 后台清理一晚上
- 出门前可选预防: Shadowrocket 切到 "按规则" 模式 + 关 fake-DNS / 自动模式切换,但目前 5 mac 没全验证过这个,继续沿用三查

## 历史教训

- 2026-05-05 晚 air 出移动热点回 AX3,Tailscale 卡 SFO relay 5+ 小时
- 阿良无三查直接 sudo tailscale up --reset → daemon logout → 多个 tailscaled 进程冲突 → 修了 1 小时
- 修通后台多出 air-1 / kenchoiair 两个影子节点 + 旧 air,缺哥手 admin 删
- 后续才发现根因是 Shadowrocket TUN fake-DNS 拦 controlplane,出 plist HTTPS_PROXY 修法
