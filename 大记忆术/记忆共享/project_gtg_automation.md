---
name: 创作罐头批量发布自动化
description: 四个脚本（neo+Air各文章+微头条），通过CDP控制罐头批量发布，已全部跑通
type: project
originSessionId: 6d1e89eb-eddc-422c-b35c-b420271a3a68
---
## 四个脚本位置

| 机器 | 类型 | 路径 | 启动 |
|------|------|------|------|
| neo（192.168.10.243，kenchoios） | 图文文章 | `~/Desktop/Mac文章自动发布/gtg_batch.py` | 双击 go.command |
| neo | 微头条 | `~/Desktop/Mac微头条自动发布/gtg_batch.py` | 双击 go.command |
| Air（192.168.10.239，kenair） | 图文文章 | `~/Desktop/Mac文章自动发布/gtg_batch.py` | 双击 go.command |
| Air | 微头条 | `~/Desktop/Mac微头条自动发布/gtg_batch.py` | 双击 go.command |

---

## 核心运行逻辑

1. **罐头必须已打开**，CDP连接读 `~/Library/Application Support/创作罐头/DevToolsActivePort`
2. 收集罐头侧边栏账号列表（自动滚动懒加载）
3. 过滤：skip.txt → sent.txt → include_mac.txt
4. 配额轮转：总篇数 ÷ 账号数 = 每账号配额，随机抽文章
5. 每账号：切换账号 → 检查系统通知 → 导入文档 → 读信用分 → 设首发 → 发布
6. 账号累计失败5次（MAX_ACC_RETRY=5）自动放弃

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `素材/` | 放 .docx 待发文件 |
| `素材/已发送/` | 发成功自动移入 |
| `账号配置.xlsx` | **统一账号配置文件（2026-04-13改版，原4个txt合并）** |
| `运行报告/YYYYMMDD/` | 日志/汇总/失败记录/信用分/通知/违规/高阅读 |

### 账号配置.xlsx 的4个sheet

| Sheet | 原txt | 说明 |
|-------|-------|------|
| `不首发` | nofirst.txt | 强制不首发的账号 |
| `永久跳过` | skip.txt | 永久排除账号（禁言/低分） |
| `本轮已发` | sent.txt | 本轮已发记录，**放新素材前手动清空A2往下** |
| `白名单` | include_mac.txt | 只跑这些账号，空=发全部 |

**sent逻辑**：发成功的账号实时追加进"本轮已发"，循环内漏发的下轮补发。每次放新素材前必须手动清空"本轮已发"sheet的A2往下内容，等于重置本轮记录。这是小齐原设计，逻辑未变。

---

## 首发逻辑

- 信用分 ≥ 95 → 勾选头条首发
- 信用分 < 95 或在 nofirst.txt → 取消首发
- 信用分格式："信用分 80分"，5的倍数（5-100），长度<20

---

## neo vs Air 差异（2026-04-18 已同步）

neo 已用 Air 脚本直接覆盖，账号配置.xlsx 也同步过去，两台现在完全一致。

---

## 脚本改动记录（2026-04-18）

**篇间随机等待恢复（5台机器全部）：**
- 位置：主循环 `close_current_tab` 之后
- 代码：`_d = random.randint(8, 20); log(f"  篇间等待 {_d} 秒..."); time.sleep(_d)`
- 背景：等待被去掉后平台识别批量机器行为，导致推荐量从4月9号起暴跌，详见 project_toutiao_traffic_drop.md

**剩余篇数显示（5台机器全部）：**
- 位置：主循环发布那行 `log(f"\n  {name}  ->  ...")`
- 改为：`log(f"\n  [剩余 {len(doc_pool)} 篇]  {name}  ->  {os.path.basename(doc)}")`
- 显示的是上一篇移走后的真实剩余数

**最后一个账号必败问题（暂不修复）：**
- 每台机器标签最底部的账号必定失败（侧边栏懒加载视口坐标问题，账号太多66-99个）
- 当前方案：缺哥手工补发最后一个账号，不影响整体流程

---

## 账号分工（2026-04-12更新）

- **不再对半分**，Air 全量拿所有账号
- 当前 include_mac.txt：**149个账号**（150个里排除青春小馆1个母账号）
- 不发的账号缺哥写进 skip.txt，include_mac.txt 里不在 skip 的就正常发
- **账号会经常增减，需要定期重新抓**

## 账号更新方法（标准流程）

账号有变动时，直接用 CDP 连罐头账号管理页面翻页抓取：

```python
# 导航到账号管理页面
Page.navigate → https://www.czgts.cn/v1/account/account
# 账号名 selector（管理表格专用，不是侧边栏）
[class*="accountTableAccount-"]
# 翻页按钮
.arco-pagination-item-next（disabled 时停止）
# 每页100条，翻完所有页，去重合并
# 排除母账号：{"青春小馆"}
# 写入文章+微头条两个 include_mac.txt（内容相同）
```

**注意**：侧边栏的 `.account-RALrbJ` 是懒加载，只渲染可见部分，不能用来全量抓取。账号管理表格才是完整列表，且有分页。

---

## 技术要点

- CDP WebSocket，suppress_origin=True
- cliclick真实鼠标点击（罐头自定义组件不响应CDP虚拟事件）
- 首发复选框：`LABEL.byte-checkbox` 的 `byte-checkbox-checked` class判断
- 文档导入Mac版：cliclick → fill_dialog线程（pbcopy+Cmd+Shift+G+Cmd+A+Cmd+V+回车×2）
- 文档导入Windows版（台机）：**不检测窗口**，点"选择文档"后等1.5秒，直接发 Ctrl+A+Ctrl+V+Enter（只发一次Enter！两次会触发弹窗重新打开）。publish_article函数签名需带name参数，否则NOFIRST_ACCOUNTS判断报NameError
- 失败计数：fail_records内存追踪，success_accounts去重，最终只写真正失败的到xlsx

---

## macneo2 部署完成（2026-04-14）

- Python 3.12.7 已装（/usr/local/bin/python3.12），go.command 用绝对路径
- cliclick 从 Air scp 过去安装（GitHub网络不通，用此方法）
- 所有依赖已装（websocket, requests, openpyxl, docx, psutil）
- 辅助功能+自动化权限已开（自动化需先双击go.command触发一次才会出现）
- 两个脚本（Mac文章自动发布+Mac微头条自动发布）已就位，账号配置.xlsx待填白名单

## 机器分工变更（2026-04-13）

- **发文任务迁移到mini**：文章+微头条自动发布改由mini那边负责，Air暂时等新账号
- **Air的launchd定时已停**：`launchctl unload ~/Library/LaunchAgents/com.xiaoguan.article.plist`，plist文件保留，以后需要时 `load` 即可
- **mini部署**：两个脚本（Mac文章自动发布+Mac微头条自动发布）需搬到mini，账号配置.xlsx一并带过去

## Air 自动发布历史记录

- go.command已验证可从阿良直接触发
- macOS Automation权限已处理（2026-04-12）
- 头条数据定时导出仍在Air跑（每天23:50，见 project_data_export.md）
