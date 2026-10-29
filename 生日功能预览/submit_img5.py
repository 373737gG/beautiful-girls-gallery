# -*- coding: utf-8 -*-
"""提交双背景兼容对比图 IMAGE item 到 Canvas Workspace"""
import subprocess
from pathlib import Path

workdir = Path(__file__).resolve().parent
workspace_id = "cws_60000804260844802"
asset_url = "https://aka.doubaocdn.com/s/we9A5jl5ly"

xml_text = f"""<item type="IMAGE" path="/deliverables/生日横幅方案/preview-v5" title="生日横幅双背景兼容效果图" brief="美少女图鉴生日横幅双背景兼容对比：同一半透明白玻璃横幅样式分别置于深色(#0d1117)与白色背景，仅「本月生日（X月）」金色、其余文字普通色，兼容双主题。文字示意存在AI误差（夏弥被写成夏阳），实际实现以代码文案为准。">
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

(workdir / "submit_img5.stdout.bin").write_bytes(result.stdout)
(workdir / "submit_img5.stderr.bin").write_bytes(result.stderr)
if result.returncode != 0:
    raise SystemExit(f"CLI 退出码 {result.returncode}")
print(result.stdout.decode("utf-8", errors="strict"))
