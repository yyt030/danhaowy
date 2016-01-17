#!/usr/bin/env python
# coding: utf-8
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import string, random

fontPath = ""


# 获得随机五个字母
def getRandomChar():
    return [random.choice(string.letters) for _ in range(5)]

def getRandomNumber():
    numbers=random.sample(range(0,9), 4)
    print numbers
    return numbers
# 获得颜色
def getRandomColor():
    return (random.randint(30, 100), random.randint(30, 100), random.randint(30, 100))


# 获得验证码图片
def getCodePiture():
    width = 270
    height = 90
    bp = 1
    shadowcolor = 'green'
    bordercolor = (150, 150, 150)
    # 创建画布
    image = Image.new('RGB', (width, height), (255, 255, 255))
    font = ImageFont.truetype('msyh.ttc', 90)
    draw = ImageDraw.Draw(image)
    # 创建验证码对象
    code = getRandomNumber()
    # 把验证码放到画布上
    for t in range(4):
        draw.text((40 * t + 40, -20), str(code[t]), font=font, fill=shadowcolor)




    # # 模糊处理
    # image = image.filter(ImageFilter.BLUR)
    # 保存名字为验证码的图片
    # image.save("".join(code) + '.jpg', 'jpeg')
    return image, "".join([str(s) for s in code])
