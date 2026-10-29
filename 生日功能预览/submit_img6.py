# -*- coding: utf-8 -*-
"""提交方案一（多彩低饱和名字）效果图 IMAGE item 到 Canvas Workspace"""
import subprocess
from pathlib import Path

workdir = Path(__file__).resolve().parent
workspace_id = "cws_60000804260844802"
asset_url = "https://aka.doubaocdn.com/s/QH3HIG2hqD"

xml_text = f"""<item type="IMAGE" path="/deliverables/生日横幅方案/preview-v6" title="生日横幅方案一-多彩低饱和名字效果图" brief="美少女图鉴生日横幅方案一效果图：深色玻璃横幅+金色「本月生日（10月）共3人」+三个角色名各自低饱和柔色（夏弥粉/琳德蓝/真红紫）+蓝色查看全部。示意3人多彩效果。">
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

(workdir / "submit_img6.stdout.bin").write_bytes(result.stdout)
(workdir / "submit_img6.stderr.bin").write_bytes(result.stderr)
if result.returncode != 0:
    raise SystemExit(f"CLI 退出码 {result.returncode}")
print(result.stdout.decode("utf-8", errors="strict"))
