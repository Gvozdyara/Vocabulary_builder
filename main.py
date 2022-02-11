import time
from tkinter import *
import re

import tkinter as tk


# opens a window with the text from help.txt
def get_info():
    with open("help.txt", "r", encoding="utf8") as f:
        help_text=f.read()
    window_help = tk.Tk()
    window_help.title('Help')
    lbl_help = Label(window_help, text=help_text, bg='#ACFDF8', justify=LEFT, font=14, fg='#228987')
    lbl_help.grid(column=0, row=0)


# change a string to lower case
def to_lowercase(text):
    text_lower = str()
    for letter in text:
        text_lower += letter.lower()
    return text_lower


# change the text to lower case with to_lowercase and split to single word list
def split_text(text):
    delim = [' ', '\,', '\.', '\?', '\!', '\¿', '\¡', '\%', '\:', '\;', '\'', '\'', '\"', '\«', '\»', '\-', '\—', '\n', '\)', '\(',
             '\*', '\<', '\>', '\=', '\–', '\+', '\|', '\&', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    text = to_lowercase(text)

    all_words_list_raw = re.split("|".join(item for item in delim), text)
    all_words_list = []
    for item in all_words_list_raw:
        if item != '':
            all_words_list.append(item)
        else:
            continue

    return all_words_list


# making the tuple (count,word) from a given list
def group_same_words(list):
    dict = {}
    for i in list:
        try:
            count = dict.get(i)
            count += 1
            dict[i] = count
        except:
            dict[i] = 1
    listword = []
    for key in dict:
        listword.append((dict.get(key), key))
    listword.sort(key=lambda i:i[0], reverse=True)

    # debug
    total_words=0
    for i in listword:
        total_words += i[0]
    #debug
    print(total_words,  "in grouped")
    return listword


# starts the process of the text analysis
def run_analyze():
    lbl_warning.configure(text='Wait till completed')
    lbl_warning.update()

    btn_analyze['state'] = DISABLED
    btn_merge['state'] = DISABLED
    btn_help['state'] = DISABLED

    with open('input.txt', 'r', encoding='utf8') as f:
        input_text = f.read()
    all_words_list = split_text(input_text)
    input_text_length = len(input_text)
    lbl_warning.configure(text=f"The text length is {input_text_length}")
    lbl_warning.update()
    time.sleep(0.5)

    window_output = '1 of 4 is completed'
    lbl_run_status.config(text=window_output)
    lbl_run_status.update()
    time.sleep(0.5)

    count_word_list_of_tuple = group_same_words(all_words_list)
    lbl_run_status.config(text='2 of 4 is completed')
    lbl_run_status.update()
    time.sleep(0.5)

    with open('output-new.txt', 'w', encoding='utf8') as f:
        for key in count_word_list_of_tuple:
            f.write('{},{}\n'.format(key[0],key[1]))

        # debug
        print("last item in output_new is ",count_word_list_of_tuple[-1])

    with open("base.txt", 'r', encoding="utf8") as file:
        base_list = [item for item in file.read().split("\n")]
    count_old = []
    word_old = []
    for item in base_list:
        try:
            count_old.append(item.split(",")[0])
            word_old.append(item.split(",")[1])
        except:
            print("wrong line")
            continue
    # debug
    print(len(base_list))

    with open("output-new.txt", 'r', encoding="utf8") as file:
        output_new_list = [item for item in file.read().split("\n")]
    count_new = []
    word_new = []
    for item in output_new_list:
        try:
            count_new.append(item.split(",")[0])
            word_new.append(item.split(",")[1])
        except:
            print("wrong line")
            continue
    print(len(output_new_list), " output_new len, ", len(count_new), "cont new len")




    with open("base.txt", "w", encoding="utf8") as file:
        base_old_list = [item for item in file.read().split("\n")]
        count_base = []
        word_base = []
        for item in output_new_list:
            try:
                count_base.append(item.split(",")[0])
                word_base.append(item.split(",")[1])
            except:
                print("wrong line")
                continue
        print(len(base_new_list), " base new len, ", len(count_base), "cont base len")


    window_output = 'Writing into the file'
    lbl_run_status.config(text=window_output)
    list = conjure_new_and_old_lists(counts_old, word_old, count_new, word_new)
    lbl_run_status.update()

    f = open('base.txt', 'w', encoding='utf8')
    for t in list:
        f.write(','.join(str(s) for s in t) + '\n')
    f.close()
    window_output = 'Completed. Check base.txt'
    lbl_run_status.config(text=window_output)
    lbl_status.config(text='')

    btn_analyze['state'] = NORMAL
    btn_merge['state'] = NORMAL
    btn_help['state'] = NORMAL














if __name__ == "__main__":
    root = Tk()
    root.title('Vocabulary Builder v. 2.0 by Cafe pAguantarme')
    root.config(height=600, width=800, bg='White')

    root.iconbitmap('logo.ico')

    text1 = 'Build your own vocabulary list \nto make language learning easier'
    lbl_warning = Label(root, width=40, height=2, bg="#ACFDF8", fg='#228987', text=text1, font=12, )
    lbl_warning.grid(column=1, row=0)
    lbl_status = Label(root, width=40, height=3, bg="#ACFDF8", fg='#228987', font=12)
    lbl_status.grid(column=1, row=1)
    lbl_run_status = Label(root, width=40, height=4, bg="#ACFDF8", fg='#228987', font=12)
    lbl_run_status.grid(column=1, row=2)

    frame_btn = Frame(root, bg="#66CDAA", )
    frame_btn.grid(column=0, row=0, rowspan=4, sticky=NS)
    btn_help = Button(frame_btn, bg="#66CDAA", text='HELP', fg='#ffffff', font=14, activebackground='#ACFDF8',
                      command=get_info, relief=FLAT, borderwidth=1, width=18, height=2)
    btn_help.grid(column=0, row=0)
    btn_analyze = Button(frame_btn, text='ANALYZE', bg="#66CDAA", fg='#ffffff', font=14, activebackground='#ACFDF8',
                         command=lambda: run_analyze(), relief=FLAT, borderwidth=1, width=18, height=2)
    btn_analyze.grid(column=0, row=1)
    btn_merge = Button(frame_btn, width=18, height=2, bg="#66CDAA", fg='#ffffff', font=14, activebackground='#ACFDF8',
                       text="MERGE", relief=FLAT, borderwidth=1, command=lambda: merge_first_step())
    btn_merge.grid(column=0, row=2)
    root.resizable(False, False)
    root.mainloop()





