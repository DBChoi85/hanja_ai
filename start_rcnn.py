import rcnn_model
import tkinter as tk


img_h = 100
img_w = 100
rcnn_resutl = rcnn_model.run_mrcc(img_h=img_h, img_w=img_w)

print(rcnn_resutl)

