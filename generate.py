"""Génère les images d'une part de prompts.json avec FLUX.1 schnell (stable-diffusion.cpp)."""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

SHARD, SHARDS = int(os.environ["SHARD"]), int(os.environ["SHARDS"])
MODELS = Path(os.environ.get("MODELS", "models"))
OUT = Path("out")
OUT.mkdir(exist_ok=True)

prompts = json.loads(Path("prompts.json").read_text())
mine = [p for i, p in enumerate(prompts) if i % SHARDS == SHARD]
done = []
for item in mine:
    target = OUT / f"{item['id']}.png"
    started = time.time()
    cmd = [
        "./sd/sd-cli",
        "--diffusion-model", str(MODELS / "flux.gguf"),
        "--vae", str(MODELS / "ae.safetensors"),
        "--clip_l", str(MODELS / "clip_l.safetensors"),
        "--t5xxl", str(MODELS / "t5.gguf"),
        "-p", item["prompt"],
        "--cfg-scale", "1.0",
        "--sampling-method", "euler",
        "--steps", "4",
        "-W", str(item.get("width", 768)),
        "-H", str(item.get("height", 576)),
        "-s", str(item.get("seed", 42)),
        "-t", str(os.cpu_count() or 4),
        "--disable-image-metadata",
        "-o", str(target),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    seconds = round(time.time() - started)
    if result.returncode != 0 or not target.exists():
        print(f"ÉCHEC {item['id']} ({seconds} s)\n{result.stdout[-3000:]}\n{result.stderr[-3000:]}", file=sys.stderr)
        continue
    print(f"{item['id']} : {seconds} s")
    done.append({**item, "model": "flux-schnell", "file": target.name, "seconds": seconds})

Path(OUT / f"manifest-{SHARD}.json").write_text(json.dumps(done, ensure_ascii=False, indent=1))
print(f"{len(done)}/{len(mine)} image(s) générée(s).")
