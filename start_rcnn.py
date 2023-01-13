import rcnn_model

if __name__ == "__main__":
    img_size = 100
    rcnn_resutl = rcnn_model.run_mrcc(img_h=img_size, img_w=img_size)

    print(rcnn_resutl)

