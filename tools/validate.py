#!/usr/bin/env python3
"""校验 route.json / tvbox/config.json 结构（CI 与本地通用）。"""
import json, sys
r = json.load(open("route.json")); c = json.load(open("tvbox/config.json"))
errs = []
if not r.get("order"): errs.append("route.order 为空")
for sid in r.get("order", []):
    s = r.get("sources", {}).get(sid)
    if not s or not s.get("api") or s.get("adapter") not in ("dongpian", "maccms", "ledou"): errs.append(f"route 源 {sid} 缺 api/adapter")
keys = [s["key"] for s in c.get("sites", [])]
if len(keys) != len(set(keys)): errs.append("tvbox site key 重复")
for s in c.get("sites", []):
    if not str(s.get("api", "")).startswith("http") or s.get("type") != 1: errs.append(f"tvbox site {s.get('key')} 非法")
if not c.get("sites"): errs.append("tvbox sites 为空")
print("ERR:", errs) if errs else print(f"OK route={len(r['order'])} tvbox_sites={len(c['sites'])}")
sys.exit(1 if errs else 0)
