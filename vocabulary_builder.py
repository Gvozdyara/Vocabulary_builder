# coding: utf8
import time
from progress.bar import IncrementalBar




# делит список на отдельные слова, разделитель в списке punct
def extract_single_word(text):
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
        window_output = 'The analysis may take more than 20 min'
    elif len(list) > 80000:
        window_output = 'The analysis will be completed in more than 10 min'
    elif len(list) > 50000:
        window_output = 'The analysis will be completed in 5-10 min'
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
    #         bar.next()
    # bar.finish()
    return output_list


# Удаление повторяющихся слов из частотного списка и
##создание сортированного по встречаемости кортежа с указанием частоты
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


# функция для выведения списка в столбик
def print_column(list):
    for i in list:
        print(i)

window_output = ''

def run_analyze():
    global window_output
    window_output = 'Wait till Completed'
    lbl_proceed.config(text=window_output)
    f = open('input.txt', 'r', encoding='utf8')  # читаем файл с текстом
    input_text = f.read()
    f.close()
    list = extract_single_word(input_text)  # формируем строку из текста

    window_output = 'Extracted'
    lbl_proceed.config(text=window_output)
    list = group_same_words(list)  # группируем слова по идентичности

    window_output = 'Grouped'
    lbl_proceed.config(text=window_output)
    list = clear_list_make_counts_list(list)  # сортировка кортежа частот-слово
    window_output = 'Sorted'
    lbl_proceed.config(text=window_output)
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
    f = open('base.txt', 'w', encoding='utf8')
    for t in list:
        f.write(','.join(str(s) for s in t) + '\n')
    f.close()
    window_output = 'Completed'
    lbl_proceed.config(text=window_output)



# работа с файлом


# интерфейс консоли
# print('Text vocabulry builder by Gvozdyara v.0.5\n')
# i = 0
# while i == 0:  # дальнейшие инструкции писать внутри while
#     f = open('welcome_description.txt', 'r', encoding='utf8')  # читаем файл с текстом
#     welcome_text = f.read()
#     f.close()
#     print(welcome_text)
#     input()
#     print('If you want to merge two bases enter \'merge\' to get the instructions, else press Enter\n')
#     merge_or_no = input()
#     if merge_or_no == 'merge':
#         print(
#             'Save your existing base.txt as the output_new.txt file into the program directory, save and close the file and press Enter')
#         input()
#     else:
#         print('Wait till Completed')
#         f = open('input.txt', 'r', encoding='utf8')  # читаем файл с текстом
#         input_text = f.read()
#         f.close()
#         list = extract_single_word(input_text)  # формируем строку из текста
#         print('Extracted')
#         list = group_same_words(list)  # группируем слова по идентичности
#
#         print('Grouped')
#         list = clear_list_make_counts_list(list)  # сортировка кортежа частот-слово
#         print('Sorted')
#         f = open('output-new.txt', 'w', encoding='utf8')  # открытие файла на запись нового списка
#         for t in list:
#             f.write(','.join(str(s) for s in t) + '\n')
#         f.close()
#     f = open('base.txt', 'r', encoding='utf8')  # открытие базы и преобразование в два списка
#     input_old = f.read()
#     counts_old, word_old = split_file_to_double_list(input_old)
#     f.close()
#     f = open('output-new.txt', 'r', encoding='utf8')  # открытие нового списка и преобразование в два списка
#     input_new = f.read()
#     count_new, word_new = split_file_to_double_list(input_new)
#     f.close()
#     print('Writing into the file')
#     list = conjure_new_and_old_lists(counts_old, word_old, count_new, word_new)
#     f = open('base.txt', 'w', encoding='utf8')
#     for t in list:
#         f.write(','.join(str(s) for s in t) + '\n')
#     f.close()
#
#     print('Completed\n')
#     text = 'Enter "again" and press the Enter button to continue or just click Enter for exit\n'
#     if input(text) == str('again'):
#         continue
#     else:
#         break
##    
##
