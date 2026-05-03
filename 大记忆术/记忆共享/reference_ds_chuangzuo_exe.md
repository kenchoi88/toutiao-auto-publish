---
name: DS创作 洗稿工具（台机）
description: 缺哥桌面上的 DS创作V1.1.0.exe 洗稿工具——PROMPT 外置、火山 bot API、自动下图组装 docx
type: reference
---
缺哥台机桌面有一个封装好的头条洗稿工具，可直接复用其框架做不同风格的批量产文。

## 工具位置（台机）
- exe 本体：`C:\Users\kench\Desktop\台机DS创作新文章\DS创作V1.1.0.exe`
- 配置：同目录 `config.ini`
- 输入：同目录 `台机洗稿.xlsx`（链接列表）
- 输出：同目录 `YYYY年MM月DD日-HH时MM分SS秒-N篇/` 子目录，含 docx + `api_logs/` 子目录

## 工作流（从 config.ini 和 api_logs 逆推）
1. 读 `台机洗稿.xlsx` 里的链接列表
2. 抓每条链接的原文（标题+正文+图片）
3. 把原文塞进 `config.ini` 的 `PROMPT` 模板（`{原文内容}` 占位符替换）
4. POST 到 `config.ini` 的 `APIADDR`（火山 Ark `bots/chat/completions`），Bearer = `API_KEY`
5. 收 Markdown 返回（# 标题 + 正文）
6. 下载原文图片，与 AI 生成的文字组装成 docx
7. 文件名含 `0.09_xxx` 的小数——是原创相似度分（越低越远离原文）

## 关键配置项（config.ini [DEFAULT]）
- `PROMPT` —— **唯一的风格开关**，改它等于换人设
- `MODEL` —— 当前是 `bot-20260331185851-9fn8j`（火山自定义 bot，后台可能自带 system prompt）
- `TEMPERATURE = 0.9`
- `MINWORDS` —— 最少字数，防止 AI 偷懒
- `BEGINNER_MODE` / `MAX_ARTICLES` / `ISWTT` / `TAGS` / `VERBOSE` / `DEBUG`

## 改造思路
要换洗稿风格（比如从"家居花草中年网民"改成"唐驳虎式评论员"）：
1. 首选：复制一份 `台机DS创作新文章/` 目录成 `台机DS创作新文章_<风格名>/`，改新目录里的 `config.ini` 的 PROMPT——不动原版
2. 注意：MODEL 是火山 bot，后台可能有 system prompt 覆盖 user prompt。如果改 PROMPT 后风格还是不对，要去火山控制台新建一个干净的 bot（或切换成基础 chat/completions 接口）

## docx 提图自动化
生产出来的 docx 里图片走标准 Office XML：
- ZIP 打开后，图片在 `word/media/image*.ext`
- 排列顺序靠 `word/document.xml` 里 `r:embed="rId..."` 的出现顺序 + `word/_rels/document.xml.rels` 映射
- `蒸馏/生成稿件.py` 的 `extract_images()` 已经实现了按原文顺序提取，可直接复用

**Why:** 缺哥付钱买了火山 API + 做好了抓文+下图+组装的流水线 exe，自建一套成本太高。任何做"批量头条产文"的 agent 都应该先复用这个 exe，只在 PROMPT 层做差异化。

**How to apply:** 别再给他另写抓文+下图的脚本。要跑新风格的洗稿批次，就告诉他"复制一份目录+改 PROMPT"即可。只有需要完全脱离火山 bot（比如换模型厂商）时才考虑重写。
