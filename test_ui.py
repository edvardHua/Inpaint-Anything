# -*- coding: utf-8 -*-
# @Time : 2023/10/18 18:28
# @Author : zihua.zeng
# @File : test_edz.py

import tkinter as tk
import ttkbootstrap as ttk
import numpy as np
from lama_inpaint import inpaint_img_with_lama
from tkinter import filedialog, DoubleVar
from PIL import Image, ImageDraw, ImageTk

# defining global variables
WIDTH = 750
HEIGHT = 560
file_path = ""
pen_color = "blue"
image_mask = None
image_rz = None
image_inpainted = None
photo_image = None


def open_image():
    global file_path, image_mask, image_rz, photo_image

    myFileTypes = [('Image', '*.png *.gif *.jpg *.jpeg *.bmp'), ('All files', '*')]
    # filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
    file_path = filedialog.askopenfilename(title="Open Image File",
                                           filetypes=myFileTypes,
                                           initialdir="~/Downloads")
    print(file_path)
    if file_path:
        image = Image.open(file_path)
        if image.width < image.height:
            new_width = int((WIDTH / 2))
            scale_factor = new_width / float(image.width)
            new_height = int((float(image.height) * float(scale_factor)))

            if new_height > HEIGHT:
                scale_factor = HEIGHT / float(new_height)
                new_height = int((float(new_height) * float(scale_factor)))
                new_width = int((float(new_width) * float(scale_factor)))

            image_rz = image.resize((new_width, new_height), Image.LANCZOS)
            photo_image = ImageTk.PhotoImage(image_rz)
        else:
            scale_factor = HEIGHT / float(image.height)
            new_width = int((float(image.width) * float(scale_factor)))
            new_height = HEIGHT
            if new_width > WIDTH:
                scale_factor = WIDTH / float(new_width)
                new_width = int((float(new_width) * float(scale_factor)))
                new_height = int((float(new_height) * float(scale_factor)))

            image_rz = image.resize((new_width, new_height), Image.LANCZOS)
            photo_image = ImageTk.PhotoImage(image_rz)
        print("HxW", new_width, new_height)
        image_rz.save("example/image.jpg")
        image_mask = Image.new("RGB", (new_width, new_height), (0, 0, 0))
        canvas.create_image(0, 0, anchor="nw", image=photo_image)


def download_mask():
    global image_mask
    image_mask.save("example/mask.jpg")


def image_inpaint():
    global image_mask, image_rz, image_inpainted, photo_image

    if image_rz != None and image_mask != None:
        if image_rz.mode == "RGBA":
            image_rz = image_rz.convert("RGB")
        used_mask = image_mask.convert("L")
    else:
        return
    # image_mask.save("example/mask.jpg")
    img_inpainted = inpaint_img_with_lama(
        np.array(image_rz), np.array(used_mask), "./lama/configs/prediction/default.yaml",
        "big-lama", device="cpu"
    )
    img_inpainted = Image.fromarray(img_inpainted.astype(np.uint8))
    # img_inpainted.save("example/image_inpainted.jpg")
    # 先删除掉全部的 oval
    canvas.delete("oval")

    # 然后更新
    photo_image = ImageTk.PhotoImage(img_inpainted)
    canvas.create_image(0, 0, anchor="nw", image=photo_image)


def draw(event):
    global file_path, image_mask, pen_size_dv, pen_color
    pen_size = int(pen_size_dv.get())
    if file_path:
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)

        pil_draw = ImageDraw.Draw(image_mask)
        if x1 < image_mask.width and x2 < image_mask.width \
                and y1 < image_mask.height and y2 < image_mask.height:
            pil_draw.ellipse([x1, y1, x2, y2], fill=(255, 255, 255))

        canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="", width=pen_size, tags="oval")


root = ttk.Window(themename="cosmo")
root.title("")

pen_size_dv = DoubleVar()
pen_size_dv.set(3)

# 宽 x 高，+x+y，决定了窗口展示的位置
root.geometry("950x580+300+110")
root.resizable(0, 0)
icon = ttk.PhotoImage(file='ui_imgs/icon.png')
root.iconphoto(False, icon)

# up_frame = ttk.Frame(root, width=950, height=50)
title = ttk.Label(root, text="Image Inpaint", anchor="center")
title.pack(padx=5, pady=10, fill=tk.BOTH)
ttk.Separator(root).pack(padx=5, pady=5, fill=tk.X)

# the left frame contain operator buttons
left_frame = ttk.Frame(root, width=200, height=600)
left_frame.pack(side="left", fill="y")

# the right canvas for displaying the image
canvas = ttk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()
# binding the Canvas to the B1-Motion event
canvas.bind("<B1-Motion>", draw)

# 加载按钮对应的图标
icon_open = ttk.PhotoImage(file='ui_imgs/btn_open_image.png').subsample(6, 6)
icon_pen = ttk.PhotoImage(file='ui_imgs/btn_pen.png').subsample(6, 6)

image_button = ttk.Button(left_frame, text="Open Image", compound="left", bootstyle="info-outline", command=open_image,
                          image=icon_open)

label_burst = ttk.Label(left_frame, text='Burst Size', compound='right')

s1 = ttk.Scale(left_frame, variable=pen_size_dv,
               from_=1, to=15,
               bootstyle="dark",
               orient=ttk.HORIZONTAL)
inpaint_button = ttk.Button(left_frame, text="Inpaint", bootstyle="light", command=image_inpaint)
download_mask_button = ttk.Button(left_frame, text="GetMask", bootstyle="light", command=download_mask)

image_button.pack(padx=5, pady=5)
label_burst.pack()
s1.pack()
inpaint_button.pack(padx=5, pady=5)
download_mask_button.pack(pady=5)
root.mainloop()
