import os
import cv2
import mrcnn.model as modellib
from mrcnn.config import Config
from mrcnn import visualize
import time
import tensorflow as tf
import numpy as np


class InferenceConfig(Config):
    NAME = "balloon"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1 # Background + balloon

    # Maximum number of ground truth instances to use in one image
    MAX_GT_INSTANCES = 1000

    # Max number of final detections per image
    DETECTION_MAX_INSTANCES = 2000


with tf.device("/GPU:1"):
    config = InferenceConfig()
    config.display()

    MODEL_DIR = 'c:\\data\\log\\'
    model = modellib.MaskRCNN(mode='inference', model_dir=MODEL_DIR, config=config)

    COCO_MODEL = os.path.join(MODEL_DIR, 'mask_rcnn_balloon_0350.h5')
    model.load_weights(COCO_MODEL, by_name=True)
    print("Ready")



def run_mrcc(img_h, img_w):
    letter_dir = "D:/letter"
    result_dir = "D:/bbox"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    target_path = "D:/target"
    if not os.path.exists(letter_dir):
        os.mkdir(letter_dir)
    class_names = ['BG', 'hanja', 'seju']
    time.sleep(2)
    book_list = os.listdir(target_path)
    for book in book_list:
        book_path = os.path.join(target_path, book)
        img_list = os.listdir(book_path)
        for img in img_list:
            img_path = os.path.join(book_path, img)
            print(img_path)
            # img_path = os.path.join(target_dir, img_file_name)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            h, w = image.shape

            _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

            results = model.detect([image], verbose=1)

            mystat = os.stat(img_path)
            mysize  = mystat.st_size
            print('mystat : ', mysize)

            r = results[0]
            visualize.display_instances(mysize, letter_dir=letter_dir, result_dir=book, img_file_name=img, img_h=img_h, img_w=img_w,
                                        image=image, boxes=r['rois'], masks=r['masks'], class_ids=r['class_ids'],
                                        class_names=class_names, scores=r['scores'], figsize=(w, h))

    return "Done"
