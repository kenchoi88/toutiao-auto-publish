---
name: PowerShell 中文乱码时不要瞎猜目录/文件名
description: PowerShell 控制台默认 GBK 输出中文乱码,从乱码反推目录名是赌博,赌错就 glob 不上、误判结构、白干活 — 必须用 Python -X utf8 列真名
type: feedback
originSessionId: 65e7943b-4b50-4d8f-8d15-a85ca3997cff
---
**踩过的坑 (2026-05-11)**: PowerShell `Get-ChildItem -Recurse` 显示 `C:\Users\kench\Desktop\̨��ר���Զ�����\���¶�ʱ�Զ�����\���б���\20260509` — 我从乱码反推叫"历史备份",写 glob 用 `历史备份/*/last_published.txt` 全机 [SKIP]"没有 last_published.txt"。实际真名是 **`运行报告`**(缺哥早就在指令里说"运行报告中的TXT全部重置",我把"运行报告"当泛词不当具体目录名)。结果: 重打了 3 次脚本被骂 "草泥马 / 你眼瞎吗 / 清你麻痹根本没清"。

**根因**: 中文反推不是 1:1 映射 — 乱码 `���б���` 长得像"历史备份"也可能是"运行报告"/"目录备份"/"备份记录"等任何 4 字中文。瞎猜 = 赌博。

**铁律**:

1. 任何**中文路径** glob/查找,**先用 Python 列真名**:
```bash
py -X utf8 -c "import os; [print(d) for d in sorted(os.listdir(r'<path>'))]"
```

2. 用户的**指令措辞**就是路径线索 — 缺哥说"运行报告" = 目录名就是"运行报告",别当形容词。

3. 写脚本前先 **把候选名字直接 print 出来** ,看到真名再写 glob。绝不"猜得差不多就跑"。

4. PowerShell 跑脚本要看中文输出加 `& py -X utf8` 或 `chcp 65001` (但仍可能挂 — 优先 -X utf8)。

**为何重要**: 中文目录名错一个字 → glob 全 miss → 脚本自信报"[SKIP] 没有" → 我以为完成了 → 用户看到真目录里东西没动 → 信任崩。
