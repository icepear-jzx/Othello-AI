from __future__ import print_function
from tkinter import *
import tkinter.font as tkFont
import copy


def initialize():
    global count
    global lst
    count = 0
    lst = []
    for i in range(8):
        for j in range(8):
            dic[(i, j)] = 0
    dic[(3, 4)] = dic[(4, 3)] = 1
    dic[(3, 3)] = dic[(4, 4)] = 2
    dic[(2, 3)] = dic[(3, 2)] = dic[(4, 5)] = dic[(5, 4)] = -1
    create_canvas()
    show()


def create_canvas():
    cv.create_image(250, 250, image=img_background, tag='background')
    for a in range(8):
        for b in range(8):
            cv.create_rectangle(10 + a * 60, 10 + b * 60, 70 + a * 60, 70 + b * 60, outline='gray', tag='lines')
    cv.create_rectangle(530, 440, 610, 480, outline='orange')
    cv.create_text((570, 460), text='Undo', font=('Verdana', 15))


def show():
    global count

    cv.delete('blank')
    cv.delete('available')
    cv.delete('black')
    cv.delete('white')
    for (i, j) in dic.keys():
        if dic[(i, j)] == 0:
            cv.create_image(i * 60 + 40, j * 60 + 40, image=img_blank, tag='blank')
        elif dic[(i, j)] == -1:
            cv.create_image(i * 60 + 40, j * 60 + 40, image=img_available, tag='available')
        elif dic[(i, j)] == 1:
            cv.create_image(i * 60 + 40, j * 60 + 40, image=img_black, tag='black')
        elif dic[(i, j)] == 2:
            cv.create_image(i * 60 + 40, j * 60 + 40, image=img_white, tag='white')

    cv.delete('player')
    if count % 2 == 0:
        cv.create_image(530, 280, image=img_available, tag='player')
        cv.create_image(530, 220, image=img_black, tag='player')
    else:
        cv.create_image(530, 280, image=img_white, tag='player')
        cv.create_image(530, 220, image=img_available, tag='player')

    cv.delete('text')
    count0, count_1, count1, count2 = count_chess(dic)
    cv.create_text((590, 220), text='%d' % count1, tag='text', font=ft)
    cv.create_text((590, 280), text='%d' % count2, tag='text', font=ft)


def count_chess(count_dic):
    global count
    count0 = 0
    count_1 = 0
    count1 = 0
    count2 = 0
    for item in count_dic.keys():
        if count_dic[item] == 0:
            count0 += 1
        elif count_dic[item] == -1:
            count_1 += 1
        elif count_dic[item] == 1:
            count1 += 1
        elif count_dic[item] == 2:
            count2 += 1
    return count0, count_1, count1, count2


def exchange_line(x1, y1, x2, y2, img, num):
    global dic
    if x1 == x2:
        x_step, y_step = 0, (y2 - y1) / abs(y2 - y1)
    elif y1 == y2:
        x_step, y_step = (x2 - x1) / abs(x2 - x1), 0
    else:
        x_step, y_step = (x2 - x1) / abs(x2 - x1), (y2 - y1) / abs(y2 - y1)
    m, n = x1, y1
    while m != x2 or n != y2:
        cv.create_image(40 + m * 60, 40 + n * 60, image=img)
        dic[(m, n)] = num
        m += x_step
        n += y_step


def find_available():
    for item in dic.keys():
        if dic[item] == -1:
            dic[item] = 0
    steps = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    if count % 2 == 0:
        for (x, y) in dic.keys():
            if dic[(x, y)] == 1:
                for x_step, y_step in steps:
                    _count = 0
                    x_temp, y_temp = x, y
                    x_temp += x_step
                    y_temp += y_step
                    while 0 <= x_temp <= 7 and 0 <= y_temp <= 7:
                        if dic[(x_temp, y_temp)] == 2:
                            _count = 1
                            x_temp += x_step
                            y_temp += y_step
                        elif dic[(x_temp, y_temp)] == 0 and _count == 1:
                            dic[(x_temp, y_temp)] = -1
                            break
                        else:
                            break
    else:
        for (x, y) in dic.keys():
            if dic[(x, y)] == 2:
                for x_step, y_step in steps:
                    _count = 0
                    x_temp, y_temp = x, y
                    x_temp += x_step
                    y_temp += y_step
                    while 0 <= x_temp <= 7 and 0 <= y_temp <= 7:
                        if dic[(x_temp, y_temp)] == 1:
                            _count = 1
                            x_temp += x_step
                            y_temp += y_step
                        elif dic[(x_temp, y_temp)] == 0 and _count == 1:
                            dic[(x_temp, y_temp)] = -1
                            break
                        else:
                            break


def judge():
    global count
    count0, count_1, count1, count2 = count_chess(dic)
    if count0 + count_1 == 0:
        result()
    elif count_1 == 0:
        count += 1
        find_available()
        if count_chess(dic)[1] == 0:
            result()


def result():
    count0, count_1, count1, count2 = count_chess(dic)
    if count1 > count2:
        print('black win')
        cv.create_text((570, 400), text='black win', font=('Verdana', 15))
    elif count1 < count2:
        print('white win')
        cv.create_text((570, 400), text='white win', font=('Verdana', 15))
    else:
        print('tie')
        cv.create_text((570, 400), text='tie', font=('Verdana', 15))


def change_color(x, y, img, color1, color2):
    steps = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for x_step, y_step in steps:
        x_temp, y_temp = x, y
        x_temp += x_step
        y_temp += y_step
        while 0 <= x_temp <= 7 and 0 <= y_temp <= 7:
            if dic[(x_temp, y_temp)] == color2:
                x_temp += x_step
                y_temp += y_step
            elif dic[(x_temp, y_temp)] == color1:
                exchange_line(x_temp, y_temp, x, y, img, color1)
                break
            else:
                break


def undo():
    global count
    global lst
    global dic
    count -= 1
    dic = copy.deepcopy(lst.pop())
    show()


def set_chess(event):
    global count
    global lst
    global dic
    x, y = int((event.x - 10) / 60), int((event.y - 10) / 60)
    score_max = -1000
    x_max = -1
    y_max = -1
    if 530 <= event.x <= 610 and 440 <= event.y <= 480:
        undo()
        return 0
    elif x < 0 or x > 7 or y < 0 or y > 7:
        return 0
    lst.append(copy.deepcopy(dic))
    if count % 2 == 0 and dic[(x, y)] == -1:
        dic[(x, y)] = 1
        change_color(x, y, img_black, 1, 2)
        count += 1
    elif count % 2 == 1:
        for item in dic.keys():
            if dic[item] == -1:
                dic_temp = copy.deepcopy(dic)
                dic_temp[item] = 2
                change_color_ai(dic_temp, item[0], item[1], 2, 1)
                find_available_ai(2, dic_temp)
                score_temp = ai(dic_temp, 2)
                if score_temp > score_max:
                    score_max = score_temp
                    x_max = item[0]
                    y_max = item[1]
        if x_max == -1:
            return 0
        dic[(x_max, y_max)] = 2
        change_color(x_max, y_max, img_white, 2, 1)
        count += 1
    find_available()
    judge()
    show()
    print("%f" % score_max)
    print("%f" % ai_score(dic))


def ai(dic_last, count_temp):
    score_max = -1000
    score_min = 1000
    if count_temp == 5:
        return ai_score(dic_last)
    count0, count_1, count1, count2 = count_chess(dic_last)
    if count1 + count2 == 64:
        if count1 > count2:
            return -200
        elif count2 > count1:
            return ai_score(dic_last)
        else:
            return 0
    elif count_1 == 0:
        return ai(dic_last, count_temp + 1)

    if count_temp % 2 == 1:
        for item in dic_last.keys():
            if dic_last[item] == -1:
                dic_temp = copy.deepcopy(dic_last)
                dic_temp[item] = 2
                change_color_ai(dic_temp, item[0], item[1], 2, 1)
                find_available_ai(count_temp + 1, dic_temp)
                score_temp = ai(dic_temp, count_temp + 1)
                if score_temp > score_max:
                    score_max = score_temp
        return score_max
    else:
        for item in dic_last.keys():
            if dic_last[item] == -1:
                dic_temp = copy.deepcopy(dic_last)
                dic_temp[item] = 1
                change_color_ai(dic_temp, item[0], item[1], 1, 2)
                find_available_ai(count_temp + 1, dic_temp)
                score_temp = ai(dic_temp, count_temp + 1)
                if score_temp < score_min:
                    score_min = score_temp
        return score_min


def ai_score(dic_temp):
    global list_proportion
    white_score = 0
    white_count = 0
    black_score = 0
    black_count = 0
    for item in dic_temp.keys():
        if dic_temp[item] == 1:
            black_count += 1
            black_score += list_proportion[item[0]][item[1]]
        elif dic_temp[item] == 2:
            white_count += 1
            white_score += list_proportion[item[0]][item[1]]
    if white_count == 0 and black_count != 0:
        return - black_score / black_count
    elif white_count != 0 and black_count == 0:
        return white_score / white_count
    elif white_count == 0 and black_count == 0:
        return 0
    else:
        return white_score / white_count - black_score / black_count


def find_available_ai(count_temp, dic_temp):
    find = 0
    for item in dic_temp.keys():
        if dic_temp[item] == -1:
            dic_temp[item] = 0
    steps = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    if count_temp % 2 == 0:
        for (x, y) in dic_temp.keys():
            if dic_temp[(x, y)] == 1:
                for x_step, y_step in steps:
                    _count = 0
                    x_temp, y_temp = x, y
                    x_temp += x_step
                    y_temp += y_step
                    while 0 <= x_temp <= 7 and 0 <= y_temp <= 7:
                        if dic_temp[(x_temp, y_temp)] == 2:
                            _count = 1
                            x_temp += x_step
                            y_temp += y_step
                        elif dic_temp[(x_temp, y_temp)] == 0 and _count == 1:
                            dic_temp[(x_temp, y_temp)] = -1
                            find = 1
                            break
                        else:
                            break
    else:
        for (x, y) in dic_temp.keys():
            if dic_temp[(x, y)] == 2:
                for x_step, y_step in steps:
                    _count = 0
                    x_temp, y_temp = x, y
                    x_temp += x_step
                    y_temp += y_step
                    while 0 <= x_temp <= 7 and 0 <= y_temp <= 7:
                        if dic_temp[(x_temp, y_temp)] == 1:
                            _count = 1
                            x_temp += x_step
                            y_temp += y_step
                        elif dic_temp[(x_temp, y_temp)] == 0 and _count == 1:
                            dic_temp[(x_temp, y_temp)] = -1
                            find = 1
                            break
                        else:
                            break
    return find


def change_color_ai(dic_temp, x, y, color1, color2):
    steps = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for x_step, y_step in steps:
        x_temp, y_temp = x, y
        x_temp += x_step
        y_temp += y_step
        while 0 <= x_temp <= 7 and 0 <= y_temp <= 7:
            if dic_temp[(x_temp, y_temp)] == color2:
                x_temp += x_step
                y_temp += y_step
            elif dic_temp[(x_temp, y_temp)] == color1:
                exchange_line_ai(dic_temp, x_temp, y_temp, x, y, color1)
                break
            else:
                break


def exchange_line_ai(dic_temp, x1, y1, x2, y2, num):
    if x1 == x2:
        x_step, y_step = 0, (y2 - y1) / abs(y2 - y1)
    elif y1 == y2:
        x_step, y_step = (x2 - x1) / abs(x2 - x1), 0
    else:
        x_step, y_step = (x2 - x1) / abs(x2 - x1), (y2 - y1) / abs(y2 - y1)
    m, n = x1, y1
    while m != x2 or n != y2:
        dic_temp[(m, n)] = num
        m += x_step
        n += y_step


# main
count = 0
list_proportion = [[30, 1, 8, 6, 6, 8, 1, 30],
                   [1, 2, 5, 3, 3, 5, 2, 1],
                   [8, 5, 8, 3, 3, 8, 5, 8],
                   [6, 3, 3, 4, 4, 3, 3, 6],
                   [6, 3, 3, 4, 4, 3, 3, 6],
                   [8, 5, 8, 3, 3, 8, 5, 8],
                   [1, 2, 5, 3, 3, 5, 2, 1],
                   [30, 1, 8, 6, 6, 8, 1, 30]]
dic = {}
lst = []
root = Tk()
root.title('Othello.PVP')
ft = tkFont.Font(family='Times New Roman', size=25)
cv = Canvas(root, heigh=500, width=650, bg='white')
cv.pack()
img_background = PhotoImage(file='background.gif')
img_black = PhotoImage(file='black.gif')
img_white = PhotoImage(file='white.gif')
img_available = PhotoImage(file='available.gif')
img_blank = PhotoImage(file='blank.gif')
initialize()
cv.bind('<Button-1>', set_chess)
mainloop()
