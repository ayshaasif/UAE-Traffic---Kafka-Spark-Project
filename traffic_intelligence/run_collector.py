import os
import shutil
import subprocess
import sys
import logging
from pathlib import Path

logger = logging.getLogger("run_collector")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

ROOT = Path(__file__).resolve().parent

src = ROOT / "config" / "road_segments.yaml"
dst_dir = ROOT / "ingestion" / "schemas" / "config"
dst = dst_dir / "road_segments.yaml"

if not src.exists():
    logger.error(f"Source config not found: {src}")
    raise SystemExit(1)

dst_dir.mkdir(parents=True, exist_ok=True)
if not dst.exists():
    shutil.copy(src, dst)
    logger.info(f"Copied {src} -> {dst}")
else:
    logger.info(f"Config already present at {dst}")

# Run collector as a module so imports resolve correctly
cmd = [sys.executable, "-m", "ingestion.collector"]
logger.info(f"Running: {' '.join(cmd)} (cwd={ROOT})")
subprocess.run(cmd, cwd=str(ROOT))
