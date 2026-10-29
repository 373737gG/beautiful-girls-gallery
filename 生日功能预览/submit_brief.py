# -*- coding: utf-8 -*-
"""提交 brief XML 到 Canvas Workspace"""
import json
import subprocess
from pathlib import Path

workdir = Path(__file__).resolve().parent
workspace_id = "cws_60000804260844802"

xml_text = """<item type="TEXT" path="/deliverables/生日横幅方案/brief" title="生日横幅方案Brief" brief="美少女图鉴生日横幅3套配色方案效果图任务Brief">
  <size width="900" height="320" />
  <inline>
    <contents>
      <content line_break="false">生日横幅3方案效果图 Brief：为美少女图鉴(index.html)生日横幅提供三套配色方案对比效果图——A粉色糖果风、B深金色醒目、C跟随主题蓝色系。深色页面背景(#0d1117风格)，横幅为圆角条带，含文字「🎂 本月生日（10月）共1人：夏弥(10.30) · 查看全部 →」。用途：用户决策配色与文字风格。</content>
    </contents>
    <style font_size="16" font_family="Source Han Sans SC VF" font_weight="400" color="#FFFFFF" align="left" line_height="24" />
  </inline>
</item>"""

payload = xml_text.encode("utf-8")
argv = ["design-cli", "design-workspace", "+create",
        "--canvas-workspace-id", workspace_id, "--input", "-"]
try:
    result = subprocess.run(argv, input=payload, shell=False, cwd=workdir,
                            capture_output=True, timeout=120)
except subprocess.TimeoutExpired:
    raise SystemExit("写入超时")

(workdir / "submit.stdout.bin").write_bytes(result.stdout)
(workdir / "submit.stderr.bin").write_bytes(result.stderr)
(workdir / "submit.exitcode.txt").write_text(str(result.returncode), encoding="utf-8")
if result.returncode != 0:
    raise SystemExit(f"CLI 退出码 {result.returncode}")
print(result.stdout.decode("utf-8", errors="strict"))
