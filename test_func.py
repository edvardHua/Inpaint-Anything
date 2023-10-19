# -*- coding: utf-8 -*-
# @Time : 2023/10/19 11:53
# @Author : zihua.zeng
# @File : test_func.py

import numpy as np
from PIL import Image
from lama_inpaint import inpaint_img_with_lama

if __name__ == "__main__":
    img = Image.open("example/image.jpg")
    if img.mode == "RGBA":
        img = img.convert("RGB")
    mask = Image.open("example/mask.jpg")
    mask = mask.convert("L")

    # 黑色才是要 inpaint 的部分，但是 lama 是白色才是要 inpaint 的部分
    # 所以这里要做一个转换
    mask = np.array(mask)
    mask -= 255

    img_inpainted = inpaint_img_with_lama(
        np.array(img), np.array(mask), "./lama/configs/prediction/default.yaml",
        "big-lama", device="cpu"
    )
    Image.fromarray(img_inpainted.astype(np.uint8)).save("example/image_inpainted.jpg")
    pass
