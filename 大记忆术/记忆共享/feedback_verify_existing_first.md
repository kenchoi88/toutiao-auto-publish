---
name: 先验证已有工具，再动手造新的
description: 遇到功能需求时，必须先检查已安装的skill和脚本能否满足，不能直接造轮子
type: feedback
originSessionId: 6d1e89eb-eddc-422c-b35c-b420271a3a68
---
遇到新需求，先列出已有的skill/脚本并测试，确认不满足后再开发。

**Why:** 重复同样的错误——有现成skill能查沪深两市实时行情，但直接搭了一套akshare + Flask API + SSH隧道，全是重复劳动。

**How to apply:** 收到"加某某功能"的需求时，第一步是检查已有skill和脚本，跑一个测试命令，通了就直接用，不通了再修或新建。不能跳过这一步。
