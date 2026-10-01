#!/usr/bin/env python3
# Build today's Bruno Brief feed.json + deepdives.json (2026-10-02).
# Data kept in a sibling module loaded from /tmp to keep this file small.
import json, os, importlib.util, sys

BASE = "/home/rory/Projects/news-pwa"
TODAY = "2026-10-02"

spec = importlib.util.spec_from_file_location("dt", "/tmp/bruno_dt_20261002.py")
dt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dt)
stories = dt.stories
D = dt.D

deep = {}
for s in stories:
    slug = s["slug"]
    deep[slug] = {
        "headline": s["headline"],
        "summary": s["summary"],
        "detail": D[slug],
        "sources": s["sources"],
        "source_urls": s["source_urls"],
    }

feed_path = os.path.join(BASE, "feed.json")
with open(feed_path) as f:
    feed = json.load(f)
days = [d for d in feed["days"] if d["date"] != TODAY]
days.insert(0, {"date": TODAY, "stories": stories})
days = days[:60]
feed["days"] = days
with open(feed_path, "w") as f:
    json.dump(feed, f, ensure_ascii=False, indent=2)

dd_path = os.path.join(BASE, "deepdives.json")
with open(dd_path) as f:
    ddc = json.load(f)
ddc["deepdives"][TODAY] = deep
with open(dd_path, "w") as f:
    json.dump(ddc, f, ensure_ascii=False, indent=2)

bad = [slug for slug, e in deep.items() if len(e["detail"].strip()) <= 300]
print("today stories:", len(stories))
print("newest day:", days[0]["date"], "| total days:", len(days))
print("deepdives for today:", len(deep), "| short detail:", bad)
print("RESULT:", "OK" if not bad else "FIX")