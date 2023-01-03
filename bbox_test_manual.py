from functools import reduce
from operator import itemgetter, add


def area_preprocess(target_list):
    for i in range(len(target_list)):
        y1 = int(target_list[i][0])
        x1 = int(target_list[i][1])
        y2 = int(target_list[i][2])
        x2 = int(target_list[i][3])
        width = x2 - x1
        height = y2 - y1
        if width < 0:
            target_list[i][3] = x1
            target_list[i][1] = x2
        if height < 0:
            target_list[i][0] = y2
            target_list[i][2] = y1

    return target_list



def line_cutting(target_list):
    line = []
    temp = []
    # print("linecutting", target_list)
    target_list.sort(key=itemgetter(1), reverse=True)
    target_list.sort(key=itemgetter(0))
    first_x = target_list[0][1]
    # print(first_x)
    width = target_list[0][3] - first_x
    center_x = int((first_x + target_list[0][3]) / 2)
    # print(width)

    for i, p in enumerate(target_list):
        target_center = int((target_list[i][1] + target_list[i][3]) / 2)
        # 정답은 1/3
        if (center_x + int(width * 0.5) >= target_center) and (target_center >= center_x - int(width * 0.5)):
            line.append(p)

    line.sort(key=itemgetter(0))
    # print("line", line)

    return line


def list_remove_item(list1, list2):
    temp1 = list1
    temp2 = list2
    for target in temp1:
        for item in temp2:
            if target == item:
                temp2.remove(item)
    return temp2


def page_line_extractor(t_list):
    page = area_preprocess(t_list)
    # print("page", page)
    # print("len", len(page))

    full_line = dict()
    temp = []
    for i in range(20):
        full_line['line_' + "{}".format(i)] = line_cutting(page)
        temp = full_line.values()
        temp = list(reduce(add, temp))
        # print("temp", temp)
        page = list_remove_item(temp, page)
        # print("i, page", i, page)
        if len(page) == 0:
            break

    full_line = sorted(full_line.values(), key=lambda item: item[0][1], reverse=True)
    final_line = list(reduce(add, full_line))
    length = len(full_line)
    tmp_list = []
    for idx in range(length):
        line_list = full_line[idx]
        line_len = len(line_list)
        # print(idx, line_len)
        tmp_list.append(line_len)
    # print('full_line', full_line)
    return final_line, tmp_list
