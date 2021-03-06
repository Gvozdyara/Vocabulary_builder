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
    # print(total_words,  "in grouped")
    return listword


# merge output_new and base from files to one file
def merge():
    with open("base.txt", 'r', encoding="utf8") as file:
        base_list = [item for item in file.read().split("\n")]
    count_old = []
    word_old = []
    for item in base_list:
        try:
            count_old.append(item.split(",")[0])
            word_old.append(item.split(",")[1])
        except:
            # print("wrong line")
            continue
    # debug
    # print(len(base_list), " <= len of base list")
    # print(len(count_old), " count", len(word_old), " words")

    with open("output-new.txt", 'r', encoding="utf8") as file:
        output_new_list = [item for item in file.read().split("\n")]
    count_new = []
    word_new = []
    for item in output_new_list:
        try:
            count_new.append(item.split(",")[0])
            word_new.append(item.split(",")[1])
        except:
            # print("empty line")
            continue
    # debug
    # print(len(output_new_list), " <= len of output_new_list")
    # print(len(count_new), " count new len", len(word_new), " words new len")

    base_dict = dict()
    for word in word_old:
        try:
            base_dict[word] = count_old[word_old.index(word)]
        except:
            # print("base_dict throws an exception")
            continue
    # debug
    # print(base_dict)

    new_dict = dict()
    for word in word_new:
        try:
            new_dict[word] = count_new[word_new.index(word)]
        except:
            # print("new_dict throws an exception")
            continue

    #debug
    # print(new_dict)

    for key in new_dict:
        try:
            total_key_count = int(base_dict.get(key)) + int(new_dict.get(key))
            base_dict[key]=total_key_count
        except:
            base_dict[key] = new_dict.get(key)
            continue

    # debug
    # print(len(base_dict), " len base_dict to write")

    base_to_write = []
    with open("base.txt", "w", encoding="utf8") as file:
        for key in base_dict:
            file.writelines(f"{base_dict.get(key)},{key}\n")


# run merge by clicking merge button
def merge_click():
    btn_analyze['state'] = DISABLED
    btn_merge['state'] = DISABLED
    btn_help['state'] = DISABLED
    btn_get_unknown_words['state'] = DISABLED

    lbl_warning.configure(text='Wait till completed')
    lbl_warning.update()

    merge()

    window_output = 'Completed'
    lbl_run_status.config(text=window_output)
    lbl_run_status.update()
    time.sleep(0.5)

    btn_analyze['state'] = NORMAL
    btn_merge['state'] = NORMAL
    btn_help['state'] = NORMAL
    btn_get_unknown_words['state'] = NORMAL


# takes list of known words and returns list of unknown words
def make_list_unknown_words():
    with open("base.txt", 'r', encoding="utf8") as file:
        base_list = [item for item in file.read().split("\n")]
    count_old = []
    word_old = []
    for item in base_list:
        try:
            count_old.append(item.split(",")[0])
            word_old.append(item.split(",")[1])
        except:
            # print("wrong line")
            continue
    # debug
    # print(len(base_list), " <= len of base list")
    # print(len(count_old), " count", len(word_old), " words")

    with open("known_words.txt", "r") as file:
        known_words = [item for item in file.read().split("\n")]

    base_dict = dict()
    for word in word_old:
        try:
            base_dict[word] = count_old[word_old.index(word)]
        except:
            # print("base_dict throws an exception")
            continue
    # debug
    #print(base_dict)
    unknown_words = list()
    for key in base_dict:
        if key not in known_words:
            unknown_words.append(key)

    with open("unknown_words.txt", "w", encoding="utf8") as file:
        for i in unknown_words:
            file.writelines(f"{i}\n")


def make_list_unknown_words_clicked():
    btn_analyze['state'] = DISABLED
    btn_merge['state'] = DISABLED
    btn_help['state'] = DISABLED
    btn_get_unknown_words['state'] = DISABLED

    lbl_warning.configure(text='Wait till completed')
    lbl_warning.update()

    make_list_unknown_words()

    window_output = 'Completed'
    lbl_run_status.config(text=window_output)
    lbl_run_status.update()
    time.sleep(0.5)

    btn_analyze['state'] = NORMAL
    btn_merge['state'] = NORMAL
    btn_help['state'] = NORMAL
    btn_get_unknown_words['state'] = NORMAL


# starts the process of the text analysis
def run_analyze():
    lbl_warning.configure(text='Wait till completed')
    lbl_warning.update()

    btn_analyze['state'] = DISABLED
    btn_merge['state'] = DISABLED
    btn_help['state'] = DISABLED
    btn_get_unknown_words['state'] = DISABLED

    with open('input.txt', 'r', encoding='utf8') as f:
        input_text = f.read()
    all_words_list = split_text(input_text)
    input_text_length = len(input_text)
    lbl_warning.configure(text=f"The text length is {input_text_length} characters")
    lbl_warning.update()
    time.sleep(0.5)

    window_output = '1 of 3 is completed'
    lbl_run_status.config(text=window_output)
    lbl_run_status.update()
    time.sleep(0.5)

    count_word_list_of_tuples = group_same_words(all_words_list)
    lbl_run_status.config(text='2 of 3 is completed')
    lbl_run_status.update()
    time.sleep(0.5)

    with open('output-new.txt', 'w', encoding='utf8') as f:
        for key in count_word_list_of_tuples:
            f.write('{},{}\n'.format(key[0],key[1]))

        # debug
        # print("last item in output_new is ",count_word_list_of_tuples[-1])

    merge()

    window_output = 'Writing into the file'
    lbl_run_status.config(text=window_output)
    lbl_run_status.update()

    window_output = 'Completed. Check base.txt'
    lbl_run_status.config(text=window_output)
    lbl_status.config(text='')

    btn_analyze['state'] = NORMAL
    btn_merge['state'] = NORMAL
    btn_help['state'] = NORMAL
    btn_get_unknown_words['state'] = NORMAL


if __name__ == "__main__":
    root = Tk()
    root.title('Vocabulary Builder v. 2.0 by Cafe pAguantarme')
    root.config(height=600, width=800, bg='White')

    root.iconbitmap('logo.ico')

    text1 = 'Build your own vocabulary list \nto make language learning easier'
    lbl_warning = Label(root, width=40, height=4, bg="#ACFDF8", fg='#228987', text=text1, font=12, )
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
                       text="MERGE", relief=FLAT, borderwidth=1, command=lambda: merge_click())
    btn_merge.grid(column=0, row=2)
    btn_get_unknown_words = Button(frame_btn, width=18, height=2, bg="#66CDAA", fg='#ffffff', font=14, activebackground='#ACFDF8',
                       text="NEW WORDS", relief=FLAT, borderwidth=1, command=lambda: make_list_unknown_words_clicked())
    btn_get_unknown_words.grid(column=0, row=3)

    root.resizable(False, False)
    root.mainloop()





