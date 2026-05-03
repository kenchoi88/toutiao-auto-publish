---
name: Windows bat 中文编码坑
description: Claude Code 的 Write 写出的 bat 是 UTF-8 无 BOM，cmd 默认 GBK 解码直接乱码报错
type: feedback
originSessionId: 5b0a52f9-fbb7-461f-8c1d-c85a747257a3
---
给缺哥台机写 .bat 脚本时，**不要用中文 echo / 中文 title**。全英文，或 ASCII 字符。

**Why:** Write 工具写出的 bat 默认是 UTF-8（无 BOM）。Windows 10/11 的 cmd.exe 默认代码页是 936 (GBK)，读 UTF-8 bytes 会乱码，甚至把 `echo 清理` 中的乱码当成命令去执行，报 "'xxxx' 不是内部或外部命令"。缺哥 2026-04-20 被这个折磨了半天。

**How to apply:**
- 所有对外的 bat 脚本，echo / title / 注释用英文
- 真非要中文：bat 开头加 `chcp 65001 >nul`（但 title 和一些场景仍可能翻车），或手动保存为 GBK/CP936 编码
- **最稳：直接全英文**，反正 bat 输出用户看一眼就关，不用花里胡哨
- reg add / reg query 的路径本来就是 ASCII，不受影响；中文只在 echo 场合出事
