# 罐头爆款头条下载

Win 台机自动下载创作罐头「低粉爆款」数据,用于洗稿素材源。

## 触发词

缺哥说**「下载爆款」/「下载爆款数据」** → 直接跑,不再问。

## 前置

罐头 CDP 9223 在线。报错时双击 `~/Desktop/台机专用自动发布/<件>/debug_launch.bat` 启动罐头(带 `--remote-debugging-port=9223`)。

## 跑

```bash
cd C:/Users/kench/Desktop/罐头爆款下载
python 罐头爆款下载.py
```

或双击 `下载.bat`(同款)。

## 固化参数

- 页面:罐头 → 创作工具 → 低粉爆款
- 媒体平台:今日头条
- 内容类型:短图文
- 发布时间:**2 天内**(写死,line 160)
- 内容排序:阅读量
- 粉丝量:全部
- 领域(19 个,line 24-29):
  ```
  国际 / 职业职场 / 军事 / 教育 / 健康 / 养老 / 美食 / 三农 / 综艺
  育儿 / 旅游 / 音乐 / 运动健身 / 动物宠物 / 房产 / 科普 / 游戏 / 动漫 / 家居家装
  ```
  **领域改动史**:2026-04-29 删「科学科技」 / 2026-05-02 删「法律」加「综艺」

## 输出

`C:\Users\kench\Desktop\罐头爆款下载\罐头爆款_<YYYYMMDD>\`:
- `罐头爆款_<YYYYMMDD>_<HHMMSS>.xlsx` — 工作版(v0 自动筛后,~1500 条)
- `罐头爆款_<YYYYMMDD>_<HHMMSS>_原始.xlsx` — 原始 2000 条备份
- `罐头爆款_<YYYYMMDD>_<HHMMSS>_urls.txt` — URL 列表
- 自动跑 `我的删法_v0.py` 做第一轮分类器删

需要让缺哥从删除集挑误杀:跑 diff 脚本输出 `_被删除.xlsx`,缺哥过一遍捡回错杀。

## 后续 Claude 二筛(可选)

按 [feedback_罐头爆款删除17类规则](shared_memory/feedback_罐头爆款删除集学到的15类规则.md) 17 类(A-O + P 法律 + Q 科学科技 整领域)做语义二筛,输出精筛 xlsx 给缺哥三轮挑。

## 改领域时

直接编辑 `罐头爆款下载.py` line 24-29 的 `TARGET_DOMAINS` 列表,改完跑即可(脚本会按新清单勾选)。

## 关联文档

- `shared_memory/reference_罐头爆款下载流程.md` — 流程权威版
- `shared_memory/feedback_罐头爆款删除集学到的15类规则.md` — Claude 二筛 17 类规则
- `shared_memory/project_素材筛选流水线节奏.md` — 罐头 2000 → v0 → Claude → 用户三筛
