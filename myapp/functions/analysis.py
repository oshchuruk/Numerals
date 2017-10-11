import sqlite3
import myapp.functions.numeral as numeral
import myapp.functions.cro_numeral as cro_num


def analyze_form(form, number, lang):
    if lang == 'ukr':
        ordn, adj, zbirn = numeral.make_numeral(number)
    elif lang == 'cro':
        ordn, adj, zbirn = cro_num.make_numeral(number)

    founds = []
    j = 0

    for l in [ordn, adj, zbirn]:

        element = l

        if type(element) == list:
            temp = element
            element = dict()
            element[0] = temp

        for key in element.keys():
            i = 0
            for item in element[key]:
                for word in item:
                    if word == form:
                        founds.append((j,key,i))
                i += 1
        j += 1

    return founds


def numeral_to_digits(num, lang):

    num = num.split(' ')

    #print(num)

    if lang == 'ukr':

        conn = sqlite3.connect('myapp/functions/numeric.db')

        cur = conn.execute('''select id, osnova_1, osnova_2, osnova_3, stem from numerals
                                    left join adj_stem on numerals.id == adj_stem.num''')

        all_list = cur.fetchall()

        conn.close()


    elif lang == 'cro':
        conn = sqlite3.connect('myapp/functions/numeric.db')

        cur = conn.execute('''select cro_adj_stem.num, cro_adj_stem.stem, cro_stem.stem1, cro_stem.stem2,
                                cro_unchang.word, cro_zbir_stem.stem from cro_adj_stem
                                left join cro_stem on cro_adj_stem.num = cro_stem.num
                                left join cro_unchang on cro_adj_stem.num = cro_unchang.num
                                left join cro_zbir_stem on cro_adj_stem.num = cro_zbir_stem.num''')

        all_list = cur.fetchall()
        conn.close()

    all_dict = dict()

    for item in all_list:
        all_dict[item[0]] = list()
        for element in item:
            if element is not None and type(element) != int:
                all_dict[item[0]].append(element)

    if lang == 'ukr':
        all_dict[1] = ['од', 'перш']
    elif lang == 'cro':
        all_dict[1].append('jedn')
        all_dict[1].append('jedan')

    match_list = list()

    i = 0

    for word in num:
        match = False
        match_list.append([])
        while len(word) > 1 and match is False:
            for key in reversed(sorted(all_dict.keys())):
                for item in all_dict[key]:
                    if word == item:
                        #match = True
                        match_list[i].append(key)
                        #print(key)
            word = word[:-1]
        i += 1

    #print(match_list)

    for item in match_list:
        item = set(item)

    #print(match_list)

    for item in match_list:
        if len(item) > 1:
            for digit in item:
                #print('!!!!' + ' ' + str(digit) + ' ' + num[match_list.index(item)])
                res = analyze_form(num[match_list.index(item)], str(digit), lang)
                #print(res)
                if res == []:
                    while digit in item:
                        item.remove(digit)
    #print(match_list)

    result = 0

    for item in match_list:
        if item[0] == 1000 and len(match_list)>1:
            result = result * item[0]
        else:
            result += item[0]

    return str(result)


# res = analyze_form("чотирмастами сімдесятьома п'ятьома",'475')
# print(res)