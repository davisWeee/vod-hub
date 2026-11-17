# vod-hub · 影视片源数据面

所有客户端（追光、映屿、影视盒 Android/TV/iOS/Mac、H5 壳）共用的**片源路由与 TVBox 配置**。客户端只读这里，不用为换源发版。

| 文件 | 给谁 | 内容 |
|---|---|---|
| `route.json` | 追光 / 映屿等原生客户端 | 按 `order` 逐源尝试；`last_resort` 末位兜底；每个源带 `adapter`（`dongpian` / `maccms`）与 `api` |
| `tvbox/config.json` | 影视盒（FongMi / tvbox-Swift）等 TVBox 类客户端 | 由「当前可用的 maccms 采集站」生成的标准 TVBox 配置（`sites` type 1 + `lives`） |
| `sources.json` | 人 / 工具 | 全量源清单与状态（active / standby / cooldown / retire-candidate） |
| `SUMMARY.md` | 人 | 最近一轮体检汇总：24h/7d 可用率、状态变化、待办 |

## 订阅地址（国内走 jsDelivr）
- 路由：`https://fastly.jsdelivr.net/gh/davisWeee/vod-hub@main/route.json`
- TVBox 配置：`https://fastly.jsdelivr.net/gh/davisWeee/vod-hub@main/tvbox/config.json`
- 备用：`https://raw.githubusercontent.com/davisWeee/vod-hub/main/<文件>`

## 数据怎么来的
体检在国内网络的机器上跑（用国内网络测，GitHub Actions 在海外，测国内源会误判），每 2 小时一轮：
找片 → 选集 → 取地址 → 拉 m3u8 → 取首个分片字节。状态机：连挂 3 次转 standby，被限流转 cooldown，连续 14 天无成功转退役候选，任何一次成功自动回 active。
发布脚本只在「可用源集合 / 死源名单变化」时提交，另有 24h 心跳；提交信息 `auto: …`。

## 数据面 + 两个客户端家族
- 数据面（本仓）：自有片源路由 + TVBox 配置。
- 家族 1：用本仓数据的客户端（追光、映屿、影视盒）。
- 家族 2：H5 壳（星河、赤焰）= 第三方站点 dongpian.ai 的显示层，站点本身也是 route.json 的 tier 1 源之一。

CI：每次推送校验 JSON 结构与 key 唯一性；每周对 `route.json` 里的源做海外可达性提示（仅提示，不作为判定依据）。
