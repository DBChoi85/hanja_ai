from keras.models import load_model
from PIL import Image, ImageFile
import numpy as np
from keras_preprocessing import image
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True
save_path = "/content/drive/MyDrive/hanja_ai_model/log/"
label_path = "record_label_2nd.txt"

epochs = 40

print("model load 시작::")
model = load_model(save_path + '%d_AE_model.h5' % epochs)
print('model load 완료::')

f = open(label_path, 'r', encoding="utf-8")
line = f.readline()
dic_line = eval(line)
f.close()


def preprocess_input(x):
    x /= 255.
    return x


def detect_fn(img_path):
    input = Image.open(img_path)
    input = input.resize((100,100))
    input = input.convert('L')
    input_arr = image.img_to_array(input)
    input_arr = preprocess_input(input_arr)
    input_arr = np.array(([input_arr]))
    # print(input_arr)
    predict = model.predict((input_arr))
    unicode = str(list(dic_line)[np.argmax(predict)])
    return unicode


def create_unicode():
    tmp_list = str()
    txt_path =  "/content/drive/MyDrive/txt/"
    if not os.path.exists(txt_path):
        os.mkdir(txt_path)
    letter_dir = "/content/drive/MyDrive/letter/"
    book_dir_list = os.listdir(letter_dir) # [test]
    for book_dir in book_dir_list: 
        book_dir_path = os.path.join(letter_dir, book_dir)
        page_dir_list = os.listdir(book_dir_path) # [c2]
        print('page_dir_list', page_dir_list)
        for page_dir in page_dir_list: 
            page_dir_path = os.path.join(book_dir_path, page_dir)
            line_dir_list = os.listdir(page_dir_path)
            print('line_dir_list', line_dir_list)
            txt_result_path = os.path.join(txt_path, book_dir)
            if not os.path.exists(txt_result_path):
                os.mkdir(txt_result_path)
            txt_file = open(os.path.join(txt_result_path,'{}.txt'.format(page_dir)), 'w', encoding='utf-8')
            for line_dir in line_dir_list: #[0, 1]
                line_dir_path = os.path.join(page_dir_path, line_dir)
                print(line_dir_path)
                img_list = os.listdir(line_dir_path)
                for img in img_list:
                    img_path = os.path.join(line_dir_path, img)
                    unicode = detect_fn(img_path)
                    uni = '0x' + unicode[1:]
                    uni_to_txt = chr(int(uni, 16))
                    print(uni_to_txt)
                    tmp_list += uni_to_txt
                tmp_list += '\n'
            # print(unicode)
            print(tmp_list)
            txt_file.writelines(tmp_list)
            txt_file.close()
    return "Done"
