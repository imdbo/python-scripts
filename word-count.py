import re 
import time 
import pandas as pd
import xlsxwriter

word_dict = {}
collocation_dict = {}
lista = input("write the full path to your text ")
coll_length = input("specify the number of surrounding words you want to see ")
coll_length = int(coll_length)

with open (lista, "r+") as l:
    whole_text = l.read()
    word_list = re.findall(r"\w+", whole_text)
    for w in range(len(word_list)):
        word_list[w] = word_list[w].lower()
        if  w >= coll_length:
            neg= coll_length
        else:
            neg = w

        if w + coll_length <= len(word_list):
            pos = coll_length
        else:
            pos = len(word_list)-w
        current_word = str(word_list[w])
        if word_list[w] not in word_dict:
            word_dict[current_word] = 1
            print(current_word+" " +str(word_dict[current_word]))
            collocation_dict[current_word] = [{1:[word_list[w-neg:w], word_list[(w+1):w+pos+1]]}]
        elif word_list[w] in word_dict:
            word_dict[current_word] = word_dict[current_word]+1
            print(current_word+" " +str(word_dict[current_word]))
            collocation_dict[current_word].append({word_dict[current_word]:[word_list[w-neg:w], word_list[(w+1):w+pos+1]]})

dict_sorted = {k: v for k, v in sorted(word_dict.items(), key=lambda x: x[1], reverse=True)}
print(word_dict)
with open("words_frequency.txt", "w+") as fl:
    fl.write(str(dict_sorted))
print("dictionary written to file words_frequency.txt")
while True:
    pattern = re.compile(r"[\d]+[\-][\d]+")
    word = input("type the  number(or range [xx-xx]) of(most common) words or the exact word you want to check: ")
    if pattern.match(word):
        print("pattern matched: "+word)
        start_end = word.split("-")
        print(start_end)
        dict = {k: dict_sorted[k] for k in list(dict_sorted)[int(start_end[0]):int(start_end[1])+1]}
        print(dict)
        ask_w = input("do you want to save the list in a excel file? y/n : ")
        if ask_w == "y" or ask_w == "yes":
            panda_pt = pd.DataFrame.from_dict(dict, orient="index").to_excel(str(word)+"-range.xlsx", header=False)
    elif word.isdecimal():
        word = int(word)
        dict = {k: dict_sorted[k] for k in list(dict_sorted)[:word]}
        print(dict)
        ask_w = input("do you want to save the list in a file? y/n : ")
        if ask_w == "y" or ask_w == "yes":
            panda_pt = pd.DataFrame.from_dict(dict, orient="index").to_excel(str(word)+"-words.xlsx", header=False)
    else:
        for k in dict_sorted:
            if word == k:
                print("Word: "+ word)
                print("frequency: "+ str(dict_sorted[word]))
                print(collocation_dict[word])
                ask_w = input("do you want to save all the concordances in a file? y/n : ")
                if ask_w == "y" or ask_w == "yes":
                    workbook = xlsxwriter.Workbook(word+".xlsx")
                    xlsheet = workbook.add_worksheet()
                    row = 0
                    pairing = 0
                    coll_list = []
                    for v in collocation_dict[word]:
                        for vl in v:
                            for e in v[vl]:
                                for w in e:
                                    if pairing is coll_length:
                                        xlsheet.write(row, pairing, word)
                                        pairing +=1
                                    if pairing > coll_length*2:
                                        pairing = 0
                                        row = row+1
                                        xlsheet.write(row, pairing, vl)
                                        row = row+1
                                    xlsheet.write(row, pairing, w)
                                    pairing += 1
                    workbook.close()
                else:
                    break
