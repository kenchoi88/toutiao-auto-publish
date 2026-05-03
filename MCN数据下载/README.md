# MCN 数据下载

每天从头条 mp 后台拉「小馆矩阵」+「迦境矩阵」+「收益」三类数据,追加今日列到 `流量对比汇总.xlsx`。Win 台机 / Mac 双端通用。

## 触发词

缺哥说**「下载 MCN 数据」/「拉今天 MCN」/「跑下载.bat」** → 直接跑。

## 前置

1. **罐头登录两个矩阵母账号**:
   - 小馆矩阵(Partition `7477169161966321683`)
   - 迦境矩阵(Partition `7601367523329638450`)
2. 桌面 `MCN数据下载/` 目录里有 `流量对比汇总<月日>.xlsx`(从 air 拷过来或 Win 台机本地累计)。

## 跑

**Win 台机**:
```bash
cd C:/Users/kench/Desktop/MCN数据下载
python data_pull.py
```
或双击 `下载.bat`。

**Mac air**:
```bash
cd ~/Desktop/MCN数据下载
bash go.command
```

## 参数

```bash
下载.bat                  # 默认:统计日=今天,补数据到昨天发布日
下载.bat --today          # 同时追加今天的发布日行(看实时)
下载.bat 2026-04-26       # 指定统计日
```

## 输出

`流量对比汇总<月日>.xlsx` 多 sheet:
- 小馆头条 / 小馆文章 / 小馆收益
- 迦境头条 / 迦境文章 / 迦境收益

每跑一次追加新一列(对应统计日)。重复跑同一天会被中止(防覆盖快照),要重跑先手动清空该列。

## 工具脚本

- `data_pull.py` — 主拉取,从罐头 cookies 拿 mp.toutiao.com session,调统计 API,写 xlsx
- `fill_30.py` — 补漏工具(2026-05-02 缺哥用过):某天没跑 / 数据缺失时,从子目录手工下载的 xlsx 反向填回汇总表的某列
- `下载.bat` — Win 启动器
- `go.command` — Mac 启动器(同款)

## 失败排查

| 报错 | 原因 | 修法 |
|---|---|---|
| cookie 没读到 | 罐头未登录矩阵账号 | 罐头里重新登录两个母账号 |
| 找不到流量对比汇总.xlsx | xlsx 还没在桌面 | 从 air 拷一份过来 |
| 重复跑被中止 | 防覆盖快照机制 | 手动清空该列再跑 |

## 跨端差异

- Win 罐头 cookies 路径多 `Network/` 一层(脚本自动检测 platform)
- 启动器:Win = `下载.bat`,Mac = `go.command`
- 脚本本身两端通用

## 关联文档

- `shared_memory/project_MCN数据每日下载.md` — Win 台机每日跑节奏
