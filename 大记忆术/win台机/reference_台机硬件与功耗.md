---
name: Win 台机硬件配置与功耗基线
description: 台机 5 块盘的盘符/类型映射、功耗实测、HDD 空闲停转配置(2026-05-02)
type: reference
originSessionId: eeacf55e-6903-452b-850e-f1bdd3f3be68
---
## 硬件配置(2026-05-02 实测)

- **CPU**: Intel i9-9900K(8C16T,3.6GHz,TDP 95W)
- **GPU**: NVIDIA RTX 2080 Ti(11G 显存,功耗上限 260W)
- **盘** 共 5 块:

| Disk# | 盘符 | 型号 | 类型 | 容量 |
|---|---|---|---|---|
| 0 | D | ST10000VN0004(IronWolf NAS) | HDD | 10T |
| 1 | E | ST4000DM000 | HDD | 4T |
| 2 | F | ST4000DM000 | HDD | 4T |
| 3 | C | Intel SSDPEDMW(NVMe) | SSD 系统盘 | 400G |
| 4 | G | Intel SSDPE2MW(NVMe) | SSD | 1.2T |

⚠️ **G 是 SSD 不是 HDD**,2026-05-02 一开始搞错被缺哥指正。

## 功耗实测

- **缺哥实测**:1 天 ≈ 3 度,平均 **125W**
- 待机/轻载 80-150W、重载(GPU 跑) 350-450W、满载 600W+
- 24h 不关机 ≈ 90 度/月 ≈ 50¥/月(0.55¥/度)
- 占大头:3 块 HDD 常转 ~20W、GPU、PSU 损耗 10-15%

## HDD 空闲停转(已配置)

2026-05-02 设了 `powercfg /change disk-timeout-ac 15`(15 分钟空闲停转)。

- 验证:`powercfg /query SCHEME_CURRENT SUB_DISK DISKIDLE` 看到 AC 索引 0x384 = 900s
- 影响:D/E/F 三块 HDD 不读写时停转,SSD 不受影响
- 副作用:首次访问 D/E/F 卡 3-5s 唤醒
- 预期省电:每天 ~0.5 度

## 测 I/O 命令

```powershell
Get-Counter -Counter '\PhysicalDisk(*)\Disk Bytes/sec','\PhysicalDisk(*)\% Idle Time' -SampleInterval 2 -MaxSamples 5
```

## 测 GPU 功耗

```powershell
nvidia-smi --query-gpu=name,power.draw,power.limit,utilization.gpu --format=csv
```

## 盘符映射查询

```powershell
Get-PhysicalDisk | Select-Object DeviceId, FriendlyName, MediaType
Get-Partition | Where-Object DriveLetter | Select-Object DiskNumber, DriveLetter
```

注意:`Get-Counter` 里 PhysicalDisk(N x:) 的 N 与 `Get-PhysicalDisk` 的 DeviceId 不一定对应,要看 `Get-Partition` 的 DiskNumber → 盘符映射。
