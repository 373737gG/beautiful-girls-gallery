# -*- coding: utf-8 -*-
from PIL import Image

img = Image.open(r'D:\zhumian\工作区\项目归档\美少女图鉴\images\吸血鬼\芙劳拉_原始.jpg')
width, height = img.size
print(f'图片尺寸: {width} x {height}')

# 左下角水印区域（Baidu百科logo）
# 裁剪掉左下角一小块，或者用周围颜色覆盖
# 水印大概在左下角 0~200, height-150~height 区域

# 用白色覆盖水印区域
from PIL import ImageDraw
draw = ImageDraw.Draw(img)

# 水印位置：左下角
# 估算：x: 0-200, y: height-150-height
watermark_box = (0, height - 150, 200, height)
draw.rectangle(watermark_box, fill=(255, 255, 255))

# 转成RGB模式再保存
img = img.convert('RGB')
output_path = r'D:\zhumian\工作区\项目归档\美少女图鉴\images\吸血鬼\芙劳拉_1.jpg'
img.save(output_path, quality=95)
print(f'已保存去水印图: {output_path}')
