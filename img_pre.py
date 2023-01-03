import os
import numpy as np
import cv2
from tkinter import filedialog
import tkinter as tk

root = tk.Tk()
root.title("이미지 여백 제거기")
root.geometry("400x200")
lab1 = tk.Label(root)
lab1["text"] = "경계 값을 입력하시오"
lab1.pack()

ent1 = tk.Entry(root)
ent1.insert(0, "200")
ent1.pack()

def select_img_folder():
    global img_dir_path
    img_dir_path = filedialog.askdirectory()

def img_preprocessing(limit=200):
    limit=ent1.get()
    limit=int(limit)
    re_dir_path = "D:/pre_fin"
    if not os.path.exists(re_dir_path):
        os.mkdir(re_dir_path)
    img_list = os.listdir(img_dir_path)
    for idx, img in enumerate(img_list):
        img_path = os.path.join(img_dir_path, img)
        im = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        print(im.shape)
        h, w, c = im.shape
        na = np.array(im)
        side = np.sum(na, axis=0) / h
        top_down = np.sum(na, axis=1) / w

        t_x = np.where(side < limit)
        t_y = np.where(top_down < limit)
        left, right = t_x[0][0], t_x[0][-1]
        top, bottom = t_y[0][0], t_y[0][-1]

        ROI = im[top:bottom, left:right]
        #
        fin_name = os.path.join(re_dir_path, img)
        cv2.imwrite(fin_name, ROI)
    
    root.destroy()



btn1 = tk.Button(root, text="폴더 선택", width=20, height=1, background="Blue", foreground='white', command=select_img_folder)
btn1.pack(padx=10, pady=10)
btn2 = tk.Button(root, text="실행", width=10, height=1, background="Red", foreground='white', command=img_preprocessing)
btn2.pack(padx=10, pady=10)

root.mainloop()