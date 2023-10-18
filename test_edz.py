# -*- coding: utf-8 -*-
# @Time : 2023/10/18 18:28
# @Author : zihua.zeng
# @File : test_edz.py

import ttkbootstrap as ttk
from tkinter import filedialog, DoubleVar
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageGrab

# defining global variables
WIDTH = 750
HEIGHT = 560
file_path = ""
pen_size = 3
pen_color = "black"


# function to open the image file
def open_image():
    global file_path

    myFileTypes = [('Image', '*.png *.gif *.jpg *.jpeg *.bmp'), ('All files', '*')]
    # filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
    file_path = filedialog.askopenfilename(title="Open Image File",
                                           filetypes=myFileTypes,
                                           initialdir="~/Downloads")
    print(file_path)
    if file_path:
        global image, photo_image
        image = Image.open(file_path)
        new_width = int((WIDTH / 2))
        image = image.resize((new_width, HEIGHT), Image.LANCZOS)

        image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=image)


def download_mask():
    pass


def image_inpaint():
    pass


def draw(event):
    global file_path
    pen_size = int(pen_size_dv.get())
    if file_path:
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)
        canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="", width=pen_size, tags="oval")


root = ttk.Window(themename="cosmo")
root.title("Image Editor")

pen_size_dv = DoubleVar()
pen_size_dv.set(3)

# 宽 x 高，+x+y，决定了窗口展示的位置
root.geometry("510x580+300+110")
root.resizable(0, 0)
icon = ttk.PhotoImage(file='btn_imgs/icon.png')
root.iconphoto(False, icon)

# the left frame to contain the 4 buttons
left_frame = ttk.Frame(root, width=200, height=600)
left_frame.pack(side="left", fill="y")

# the right canvas for displaying the image
canvas = ttk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()
# binding the Canvas to the B1-Motion event
canvas.bind("<B1-Motion>", draw)

# button for adding/opening the image file
image_button = ttk.Button(left_frame, text="Open Image", bootstyle="light", command=open_image)
inpaint_button = ttk.Button(left_frame, text="Inpaint", bootstyle="light", command=image_inpaint)
download_mask_button = ttk.Button(left_frame, text="Inpaint", bootstyle="light", command=download_mask)
s1 = ttk.Scale(left_frame, variable=pen_size_dv,
               from_=1, to=15,
               bootstyle="dark",
               orient=ttk.HORIZONTAL)

image_button.pack(pady=5)
s1.pack()
inpaint_button.pack(pady=5)
download_mask_button.pack(pady=5)
root.mainloop()
