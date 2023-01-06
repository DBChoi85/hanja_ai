import os
import sys
import cv2
import numpy as np
import bbox_test_manual


def apply_mask_white(image, mask):
    """Apply the given mask to the image.
    """
    ima = image
    for c in range(3):
        ima[:, :, c] = np.where(mask == 0, 255, ima[:, :, c])#mask==1이면 X 아니면 Y 적용

    return ima


def display_instances(mysize, letter_dir, bbox_dir, result_dir, img_file_name, image, boxes, masks, class_ids, class_names, scores=None, title="", img_h=100, img_w=100, figsize=(16, 16), ax=None, show_mask=True, show_bbox=True, colors=None, captions=None):

    # Number of instances
    # print(boxes)
    N = boxes.shape[0]
    # print("N : ", N)
    if not N:
        print("\n*** No instances to display *** \n")
    else:
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

        boxes = boxes.tolist()
        # print("len boxes : ", len(boxes))
        # print(boxes)
        boxes, line_list = bbox_test_manual.page_line_extractor(boxes)
        # print("len boxes : ", len(boxes))
        N = len(boxes)

        h = img_h
        w = img_w

        line_idx = 0
        line_count = 0

        copy = image.copy()
        for i in range(N):


            # Bounding box
            if not np.any(boxes[i]):
                # Skip this instance. Has no bbox. Likely lost in image cropping.
                continue
            y1, x1, y2, x2 = boxes[i]

            w1 = x2 - x1
            h1 = y2 - y1

            if w1 >= w or h1 >= h:
                pass

            # print(boxes[i])
            if show_bbox:

                blank_img = np.zeros((h, w, 3), np.uint8)


                copy_mask = masks
                crop_im = copy[y1:y2, x1:x2, :].copy()
                crop_im = cv2.bitwise_not(crop_im)
                blank_img_h, blank_img_w, blank_img_c = blank_img.shape
                target_img_h, target_img_w, target_img_c = crop_im.shape
                if target_img_h > h or target_img_w > w:
                    print("passed py size")
                    print(target_img_h, target_img_w)
                    pass
                else:
                    x = (blank_img_h - target_img_h) // 2
                    y = (blank_img_w - target_img_w) // 2

                    roi = blank_img[x: x + target_img_h, y:y + target_img_w]
                    # print(roi.shape)
                    # print(crop_im.shape)
                    result = cv2.add(roi, crop_im)
                    np.copyto(roi, result)

                    blank_img = cv2.bitwise_not(blank_img)

                    crop_ma = copy_mask[y1:y2, x1:x2,i].copy()
                    img = apply_mask_white(crop_im, crop_ma)

                    img_name = img_file_name.split('.')[0]
                    dst_path = os.path.join(letter_dir, result_dir)
                    if not os.path.exists(dst_path):
                        os.mkdir(dst_path)
                    if line_count == line_list[line_idx]:
                        line_idx += 1
                        line_count = 1
                        fin_path = os.path.join(dst_path, img_name)
                        if not os.path.exists(fin_path):
                            os.mkdir(fin_path)
                        tmp_result_path = os.path.join(fin_path, str(line_idx))
                        if not os.path.exists(tmp_result_path):
                            os.mkdir(tmp_result_path)
                        cv2.imwrite(tmp_result_path + '\\' + "%s_%s.jpg" % (img_name, str(i).zfill(3)), blank_img)
                    else:
                        fin_path = os.path.join(dst_path, img_name)
                        if not os.path.exists(fin_path):
                            os.mkdir(fin_path)
                        tmp_result_path = os.path.join(fin_path, str(line_idx))
                        if not os.path.exists(tmp_result_path):
                            os.mkdir(tmp_result_path)
                        cv2.imwrite(tmp_result_path + '\\' + "%s_%s.jpg" % (img_name, str(i).zfill(3)), blank_img)
                        line_count += 1

            bbox_path = bbox_dir
            bbox_result_dir = os.path.join(bbox_path, result_dir)
            if not os.path.exists(bbox_result_dir):
                os.mkdir(bbox_result_dir)
            cv2.rectangle(image, (x1, y1), (x2, y2), [255,0,0], 2)
            cv2.imwrite(bbox_result_dir + '\\' + 'Bbox_%s' % (img_file_name), image)

