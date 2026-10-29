# -*- coding: utf-8 -*-
"""提交玻璃质感横幅效果图 IMAGE item 到 Canvas Workspace"""
import subprocess
from pathlib import Path

workdir = Path(__file__).resolve().parent
workspace_id = "cws_60000804260844802"
asset_url = "https://aka.doubaocdn.com/s/7R0IBH8esL"

xml_text = f"""<item type="IMAGE" path="/deliverables/生日横幅方案/preview-v2" title="生日横幅玻璃质感效果图" brief="美少女图鉴生日横幅玻璃质感效果图：白色页面背景，磨砂玻璃质感横幅，金色文字「🎂 本月生日（10月）共1人：夏弥(10.30) 查看全部 →」。供用户决策横幅最终效果。">
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

(workdir / "submit_img2.stdout.bin").write_bytes(result.stdout)
(workdir / "submit_img2.stderr.bin").write_bytes(result.stderr)
if result.returncode != 0:
    raise SystemExit(f"CLI 退出码 {result.returncode}")
print(result.stdout.decode("utf-8", errors="strict"))
