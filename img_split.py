import cv2 as cv
import os
from tkinter import filedialog
import tkinter as tk

root=tk.Tk()

root.title('이미지 자르기')
root.geometry("250x100")

def open_folder():
    img_dir = filedialog.askdirectory()
    result_dir = "D:/split_fin"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    img_file_list = os.listdir(img_dir)

    for img_file in img_file_list:
        file = os.path.basename(img_file)
        f_name = file.split('.')
        target = os.path.join(img_dir, img_file)
        print(target)
        src = cv.imread(target, cv.IMREAD_UNCHANGED)
        height, width, _ = src.shape
        test_width = width/2
        width = int(width)
        height = int(height)
        test_width = int(test_width)

        dst = src.copy()
        dst1 = src[0:height, 0:test_width]
        dst2 = src[0:height, test_width:width]

        right_page_name = f_name[0] + 'A.jpg'
        left_page_name = f_name[0] + 'B.jpg'


        A_path = os.path.join(result_dir, right_page_name)
        B_path = os.path.join(result_dir, left_page_name)

        cv.imwrite(A_path, dst1)
        cv.imwrite(B_path, dst2)

        print('complete:', file)
        root.destroy()


base = tk.Button(root, text="이미지 분할 폴더 선택", width=30, height=1, background="Red",command=open_folder)
base.grid(row=0, column=0, padx=10, pady=10)

root.mainloop()
