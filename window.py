import textwrap
import time
from tkinter import *

import tkinter as tk

permission = 0

def get_info():
    f=open('help.txt', 'r', encoding='utf8')
    help_text=f.read()
    f.close()
    window_help = tk.Tk()
    window_help.title('Help')
    lbl_help = Label(window_help, text=help_text, bg='#ACFDF8', justify=LEFT, font=14, fg='#228987')
    lbl_help.grid(column=0, row=0)




def extract_single_word(text):



    f = open('input.txt', 'r', encoding='utf8')  # читаем файл с текстом
    input_text = f.read()
    f.close()

    text = input_text
    text = text + str('.')
    i = 0
    word = ''
    list = []
    determiners = ['del', 'las', 'los', 'que', 'the', 'an']
    preposition = ['con', 'sin', ]
    pronombres = ['mio', 'tuyo', 'tuya', 'tus', 'mis', 'tuyos', 'you', 'they', 'them', 'their', 'она', 'они']
    exception = []
    exception.extend(determiners)
    exception.extend(preposition)
    exception.extend(pronombres)
    common_endings = ['la', 'las', 'lo', 'los', 'aba', 'nos', 'te', 'os']
    punct = [' ', ',', '.', '?', '!', '¿', '¡', '%', ':', ';', '\'', '\'', '\"', '«', '»', '-', '—', '\n', ')', '(',
             '*', '<', '>', '=', '–', '+']
    while i < len(text):
        if text[i] not in punct:
            word = word + text[i].lower()
            i = i + 1
        else:
            if word not in exception:
                if len(word) < 3:
                    i += 1
                    word = ''
                else:
                    list.append(word)
                    i += 1
                    word = ''
            else:
                word = ''
                i += 1
    if len(list) > 150000:
        lbl_status.config(text = 'The analysis may take more than 20 min')
        lbl_status.update()


    elif len(list) > 80000:
        lbl_status.config(text = 'The analysis will be completed in more than 10 min')
        lbl_status.update()

    elif len(list) > 50000:
        lbl_status.config(text = 'The analysis will be completed in 5-10 min')
        lbl_status.update()
    else:
        lbl_status.config(text='It will be done in a minute')
        lbl_status.update()

    return list


##одинаковые слова расположены рядом друг с другом: 1113333225555
def group_same_words(list):
    # bar = IncrementalBar('Processing', max=len(list))
    output_list = []
    i = 0
    while i < len(list):

        for r in range(len(list)):

            if list[i] not in output_list:
                j = 0
                while j < list.count(list[i]):
                    output_list.append(list[i])
                    j += 1
                i += 1
            else:
                i += 1
            str="{}/{}".format(i,len(list))

            lbl_status.config(text=str)
            lbl_status.update()
    lbl_status.config(text="It's almost done")

    #         bar.next()
    # bar.finish()bt


    return output_list

def clear_list_make_counts_list(list):
    i = 0

    counts_list = []
    while i < len(list):
        counts_list.append(list.count(list[i]))
        j = i
        while j < len(list):
            if j == len(list) - 1:
                break
            else:
                if list[j + 1] == list[j]:
                    list.pop(j + 1)
                else:
                    break
        i += 1

    tuple1 = sorted(zip(counts_list, list), reverse=True)
    return [i for i in tuple1]  # , [i for i in list], [i for i in counts_list]


def merge_first_step():
    btn_analyze['state'] = DISABLED
    btn_merge['state'] = DISABLED
    btn_help['state'] = DISABLED

    lbl_warning.configure(text='Wait till completed')
    lbl_warning.update()

    f = open('base.txt', 'r', encoding='utf8')  # открытие базы и преобразование в два списка
    input_old = f.read()
    counts_old, word_old = split_file_to_double_list(input_old)
    f.close()

    f = open('output-new.txt', 'r', encoding='utf8')  # открытие нового списка и преобразование в два списка
    input_new = f.read()
    count_new, word_new = split_file_to_double_list(input_new)
    f.close()

    window_output = 'Writing into the file'
    lbl_proceed.config(text=window_output)
    lbl_proceed.update_idletasks()
    time.sleep(2)

    list = conjure_new_and_old_lists(counts_old, word_old, count_new, word_new)
    f = open('base.txt', 'w', encoding='utf8')
    for t in list:
        f.write(','.join(str(s) for s in t) + '\n')
    f.close()

    window_output = 'Completed'
    lbl_proceed.config(text=window_output)
    lbl_proceed.update()
    time.sleep(2)

    btn_analyze['state'] = NORMAL
    btn_merge['state'] = NORMAL
    btn_help['state'] = NORMAL



##функция возвращающая два списка из существующей базы с новой
def split_file_to_double_list(string):
    integer = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    count_list = []
    word_list = []
    i = 0
    count = ''
    word = ''

    while i < len(string):
        if string[i] in integer:
            count = count + string[i]
            i += 1
        elif string[i] == ',':
            i += 1
        elif string[i] != '\n':
            word = word + string[i]
            i += 1
        elif string[i] == '\n' or i + 1 == len(string):
            count_list.append(count)
            word_list.append(word)
            word = ''
            count = ''
            i += 1
        else:
            i += 1
    return count_list, word_list  # на выходе два списка - число и слово


##соединение нового списка со списком из базы
def conjure_new_and_old_lists(count_old, word_old, count_new, word_new):
    count_base = []
    word_base = []
    i = 0

    while i < len(word_new):
        if word_new[i] in word_old:
            word = word_new[i]
            count = int(count_old[word_old.index(word)]) + int(count_new[i])
            count_base.append(count)
            word_base.append(word)

            j = word_old.index(word)
            word_old.pop(j)

            count_old.pop(j)
            i += 1
        else:
            word = word_new[i]
            count = count_new[i]
            count_base.append(count)
            word_base.append(word)
            i += 1
    count_base.extend(count_old)
    word_base.extend(word_old)

    count_base = [int(item) for item in count_base]

    tuple1 = sorted(zip(count_base, word_base), reverse=True)
    return tuple1

def run_analyze():
    lbl_warning.configure(text='Wait till completed')
    lbl_warning.update()

    btn_analyze['state'] = DISABLED
    btn_merge['state'] = DISABLED
    btn_help['state'] = DISABLED





    f = open('input.txt', 'r', encoding='utf8')  # читаем файл с текстом
    input_text = f.read()
    f.close()
    list = extract_single_word(input_text)  # формируем строку из текста
    time.sleep(2)

    window_output = '1 of 4'
    lbl_proceed.config(text=window_output)
    lbl_proceed.update()
    time.sleep(2)

    list = group_same_words(list)  # группируем слова по идентичности
    window_output = '2 of 4'
    lbl_proceed.config(text=window_output)
    lbl_proceed.update()
    time.sleep(2)

    list = clear_list_make_counts_list(list)  # сортировка кортежа частот-слово
    window_output = '3 of 4'
    lbl_proceed.config(text=window_output)
    lbl_proceed.update()
    time.sleep(2)

    f = open('output-new.txt', 'w', encoding='utf8')  # открытие файла на запись нового списка
    for t in list:
        f.write(','.join(str(s) for s in t) + '\n')
    f.close()

    f = open('base.txt', 'r', encoding='utf8')  # открытие базы и преобразование в два списка
    input_old = f.read()
    counts_old, word_old = split_file_to_double_list(input_old)
    f.close()

    f = open('output-new.txt', 'r', encoding='utf8')  # открытие нового списка и преобразование в два списка
    input_new = f.read()
    count_new, word_new = split_file_to_double_list(input_new)
    f.close()

    window_output = 'Writing into the file'
    lbl_proceed.config(text=window_output)
    list = conjure_new_and_old_lists(counts_old, word_old, count_new, word_new)
    lbl_proceed.update()

    f = open('base.txt', 'w', encoding='utf8')
    for t in list:
        f.write(','.join(str(s) for s in t) + '\n')
    f.close()
    window_output = 'Completed. Check base.txt'
    lbl_proceed.config(text=window_output)
    lbl_status.config(text='')

    btn_analyze['state'] = NORMAL
    btn_merge['state'] = NORMAL
    btn_help['state'] = NORMAL




window = tk.Tk()
window.title('Vocabulary Builder v. 2.0 by Cafe pAguantarme')
window.config(height=600, width=800,  bg='White')

window.iconbitmap('logo.ico')





text1 = 'Build your own vocabulary list \nto make language learning easier'
lbl_warning = Label(window, width=40, height=2, bg="#ACFDF8", fg='#228987', text=text1, font=12,  )
lbl_warning.grid(column=1, row=0)

lbl_status = Label(window, width=40, height=3, bg="#ACFDF8", fg='#228987', font=12)
lbl_status.grid(column=1, row=1)

lbl_proceed = Label(window, width=40, height=4, bg="#ACFDF8", fg='#228987', font=12)
lbl_proceed.grid(column=1, row=2)

frame_btn = Frame(window, bg="#66CDAA", )
frame_btn.grid(column=0, row=0, rowspan=4, sticky=NS)


btn_help = Button(frame_btn, bg="#66CDAA", text='HELP', fg='#ffffff', font=14, activebackground='#ACFDF8',
                  command=get_info, relief=FLAT, borderwidth=1,width=18, height=2)
btn_help.grid(column=0, row=0)

btn_analyze = Button(frame_btn, text='ANALYZE', bg="#66CDAA", fg='#ffffff', font=14, activebackground='#ACFDF8',
                     command= lambda: run_analyze(), relief=FLAT, borderwidth=1,width=18, height=2)
btn_analyze.grid(column=0, row=1)

# btn_continue = Button(window, padx=60, text="continue", command=lambda: group_same_words(do_analyze()))
# btn_continue_finish = Button(window, padx=60, text="continue", command=lambda: group_same_words(do_analyze()))

btn_merge =Button(frame_btn, width=18, height=2, bg="#66CDAA", fg='#ffffff', font=14, activebackground='#ACFDF8',
                  text="MERGE", relief=FLAT, borderwidth=1, command=lambda: merge_first_step())
btn_merge.grid(column=0, row=2)



window.resizable(False, False)

window.mainloop()
