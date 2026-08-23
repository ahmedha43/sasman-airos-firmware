#!/usr/bin/env python3
import json
import sys
from pathlib import Path

meta = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
rootfs = Path(sys.argv[2])
size = rootfs.stat().st_size
limit = next(p["allocated"] for p in meta["parts"] if p["name"] == "rootfs")
print(f"rootfs_size={size} rootfs_limit={limit} free={limit-size}")
if size > limit:
    raise SystemExit("modified rootfs exceeds official partition allocation")
