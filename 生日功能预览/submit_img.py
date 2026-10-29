# -*- coding: utf-8 -*-
"""提交横幅方案效果图 IMAGE item 到 Canvas Workspace"""
import json
import subprocess
from pathlib import Path

workdir = Path(__file__).resolve().parent
workspace_id = "cws_60000804260844802"
asset_url = "https://aka.doubaocdn.com/s/zxEn2i1FO6"

xml_text = f"""<item type="IMAGE" path="/deliverables/生日横幅方案/preview" title="生日横幅3方案效果图" brief="美少女图鉴生日横幅三套配色方案对比效果图（A粉色糖果风/B深金色醒目/C主题蓝色系），深色页面背景，供用户决策配色与文字风格。文字存在AI生成误差，待确认后修正。">
  <size width="2048" height="1152" />
  <asset url="{asset_url}" />
</item>"""

payload = xml_text.encode("utf-8")
argv = ["design-cli", "design-workspace", "+create",
        "--canvas-workspace-id", workspace_id, "--input", "-"]
try:
    result = subprocess.run(argv, input=payload, shell=False, cwd=workdir,
                            capture_output=True, timeout=120)
except subprocess.TimeoutExpired:
    raise SystemExit("写入超时")

(workdir / "submit_img.stdout.bin").write_bytes(result.stdout)
(workdir / "submit_img.stderr.bin").write_bytes(result.stderr)
(workdir / "submit_img.exitcode.txt").write_text(str(result.returncode), encoding="utf-8")
if result.returncode != 0:
    raise SystemExit(f"CLI 退出码 {result.returncode}")
print(result.stdout.decode("utf-8", errors="strict"))
