# -*- coding: utf-8 -*-
"""更新 brief（+update 顶层 brief 字段）"""
import subprocess
from pathlib import Path

workdir = Path(__file__).resolve().parent
workspace_id = "cws_60000804260844802"
item_id = "qsAJrjm6-4RMt3e6MnS-0201"

xml_text = f"""<item item_id="{item_id}" type="TEXT" path="/deliverables/生日横幅方案/brief" title="生日横幅方案Brief" brief="美少女图鉴生日横幅玻璃质感效果图：白色页面背景，横幅为磨砂玻璃质感（glassmorphism，半透明+模糊+细边框+上缘高光），金色文字「🎂 本月生日（10月）共1人：夏弥(10.30) · 查看全部 →」。基于用户确认的v2预览横幅风格迭代，供决策横幅最终配色与质感。">
  <size width="900" height="320" />
  <inline>
    <contents>
      <content line_break="false">生日横幅玻璃质感效果图 Brief：白色页面背景，横幅采用磨砂玻璃质感（glassmorphism：半透明白玻璃、背后柔光斑、细边框、上缘高光、柔和阴影），横幅文字为金色（琥珀金/深金）：「🎂 本月生日（10月）共1人：夏弥(10.30)　查看全部 →」。干净现代优雅，供用户决策横幅最终效果。</content>
    </contents>
    <style font_size="16" font_family="Source Han Sans SC VF" font_weight="400" color="#3A3A3A" align="left" line_height="24" />
  </inline>
</item>"""

payload = xml_text.encode("utf-8")
argv = ["design-cli", "design-workspace", "+update",
        "--canvas-workspace-id", workspace_id, "--input", "-"]
try:
    result = subprocess.run(argv, input=payload, shell=False, cwd=workdir,
                            capture_output=True, timeout=120)
except subprocess.TimeoutExpired:
    raise SystemExit("写入超时")

(workdir / "update_brief.stdout.bin").write_bytes(result.stdout)
(workdir / "update_brief.stderr.bin").write_bytes(result.stderr)
if result.returncode != 0:
    raise SystemExit(f"CLI 退出码 {result.returncode}")
print(result.stdout.decode("utf-8", errors="strict"))
