---
name: 4 Mac 三大件真版位置(本地副本)
description: air/neo/neo2/mini 的 gtg_*.py 实际跑哪条路径,别每次 ssh 现查
type: reference
originSessionId: 6198d8da-e501-4a0b-b8de-45446700703e
---
真版在 `c:\Users\kench\code\头条自动发布\shared_memory\reference_4mac真版位置.md`(已 commit 推 git)。

**速查:**

微头条+文章件(4 台同款,桌面真版):
- `~/Desktop/微头条自动发布/gtg_batch.py`
- `~/Desktop/文章自动发布/gtg_batch.py`

文章定时件(命名分两派,**仓库内**直接跑,不在桌面):
- air + mini → `~/code/头条自动发布/文章定时自动发布/gtg_timer.py`
- neo + neo2 → `~/code/头条自动发布/Mac文章定时自动发布/gtg_timer.py`(带 Mac 前缀)

SSH:
- air `kenair@100.67.252.1`
- neo `kenchoios@100.68.57.96`
- neo2 `kenchoineo2@100.96.153.17`
- mini `kenchoimini@100.70.22.7`

实际版本(v1101.X)看 grep 标记 + .bak 时间戳,本条只记位置。
