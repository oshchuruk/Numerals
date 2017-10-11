import sqlite3

changables = ['0', '2', '3', '4', '1000', '1000000', '1000000000']
unchangables = ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200', '300', '400', '500', '600', '700', '800', '900']
zbirni = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '30', '40', '50', '60', '70', '80', '90']


digits = list()
ready_digits = list()
number = -1
mode = 1


def get_unchangable(num):
    conn = sqlite3.connect('myapp/functions/numeric.db')
    cur = conn.execute("""select word from cro_unchang where num ="""+num)
    form_raw = cur.fetchall()
    conn.close()

    form = [form_raw[0][0]]
    form_list = list()

    i = 0
    while i < 7:
        form_list.append(form)
        i += 1

    return form_list


def get_changable(num):
    conn = sqlite3.connect('myapp/functions/numeric.db')
    cur = conn.execute("""select stem1, ends from cro_stem
                            join cro_end on cro_stem.clas = cro_end.clas
                            where cro_stem.num =""" + num)
    form_raw = cur.fetchall()
    conn.close()

    if num == '2':
        form_list = dict()
        form_temp = list()
        for item in form_raw:
            form = item[0] + item[1]
            form_temp.append([form])
        form_list[1] = form_temp
        form_list[3] = form_temp

        conn = sqlite3.connect('myapp/functions/numeric.db')
        cur = conn.execute("""select stem2, ends from cro_stem
                                    join cro_end on cro_end.clas = 2
                                    where cro_stem.num = 2""")
        form_raw = cur.fetchall()
        conn.close()

        form_temp = list()
        for item in form_raw:
            form = item[0] + item[1]
            form_temp.append([form])
        form_list[2] = form_temp

    elif num in ['0', '1000', '1000000', '1000000000']:
        form_list = dict()
        form_temp = list()
        for item in form_raw:
            form = item[0] + item[1]
            form_temp.append([form])
        form_list[1] = form_temp

        conn = sqlite3.connect('myapp/functions/numeric.db')
        if num in ['0', '1000', '1000000000']:
            cur = conn.execute("""select stem1, ends from cro_stem
                                                join cro_end on cro_end.clas = 4
                                                where cro_stem.num = """ + num)
        else:
            cur = conn.execute("""select stem1, ends from cro_stem
                                                join cro_end on cro_end.clas = 6
                                                where cro_stem.num = """ + num)
        form_raw = cur.fetchall()
        conn.close()

        form_temp = list()
        for item in form_raw:
            form = item[0] + item[1]
            form_temp.append([form])
        form_list[2] = form_temp

    else:
        form_list = list()
        for item in form_raw:
            form = item[0] + item[1]
            form_list.append([form])

    return form_list


def get_one():
    stem = 'jedn'
    form_list = dict()
    conn = sqlite3.connect('myapp/functions/numeric.db')

    for num in range(1, 7):
        cur = conn.execute("""select end1, end2, end3 from cro_adj_end where gender = """ + str(num))
        form_raw = cur.fetchall()
        form_temp = list()
        for item in form_raw:
            form_temp_2 = list()
            for element in item:
                if element is not None:
                    if num == 1 and stem+str(element) == 'jedni':
                        form_temp_2.append('jedan')
                    else:
                        form_temp_2.append(stem+str(element))
            form_temp.append(form_temp_2)

        form_list[num] = form_temp

    conn.close()

    return form_list


def get_adj(num):
    form_list = dict()
    conn = sqlite3.connect('myapp/functions/numeric.db')
    cur = conn.execute("""select stem from cro_adj_stem where num = """ + num)
    stem = cur.fetchall()
    stem = str(stem[0][0])

    for num in range(1, 7):
        cur = conn.execute("""select end1, end2, end3 from cro_adj_end where gender = """ + str(num))
        form_raw = cur.fetchall()
        form_temp = list()
        for item in form_raw:
            form_temp_2 = list()
            for element in item:
                if element is not None:
                    form_temp_2.append(stem+str(element))
            form_temp.append(form_temp_2)

        form_list[num] = form_temp

    conn.close()

    #print(form_list)

    return form_list


def get_zbirni(num):
    conn = sqlite3.connect('myapp/functions/numeric.db')
    cur = conn.execute("""select stem, clas from cro_zbir_stem where num = """ + num)
    stem_raw = cur.fetchall()
    stem = str(stem_raw[0][0])
    cl = str(stem_raw[0][1])

    if cl == '2':
        form_list = list()
        cur = conn.execute("""select end1, end2 from cro_zbir_end where clas = 2""")
        ends = cur.fetchall()
        conn.close()

        for item in ends:
            form_raw = list()
            for element in item:
                if element is not None:
                    form_raw.append(stem+str(element))
            form_list.append(form_raw)

        return form_list

    elif cl == '1':
        form_list = dict()
        cur = conn.execute("""select tip, end1, end2 from cro_zbir_end where clas = 1""")
        ends = cur.fetchall()
        conn.close()

        j = 1
        while j < 4:
            form_raw = list()
            for item in ends:
                form_raw_2 = list()
                if item[0] == j:
                    for element in item:
                        if type(element) is str:
                            form_raw_2.append(stem+element)
                    form_raw.append(form_raw_2)
            form_list[j] = form_raw
            j += 1

        return form_list


def zbirni_true(num):
    global mode

    if mode == 3 and num in zbirni:
        return True
    else:
        return False


def special_adj(num):
    global mode

    if int(num) % 1000 == 0 and num[-3:] == '000' and mode == 2:
        return True
    else:
        return False


def make_digits(number):
    digits = list()

    if number in ['0', '1000000', '1000000000']:
        digits.append(number)
    else:
        if len(number) > 0:
            i = 0
            while i < len(number):
                item = number[::-1][i]
                if item != '0':
                    if i == 1 and item == '1':
                        if number[::-1][0] == '0':
                            item += '0'
                        else:
                            item += digits.pop()
                    elif i >= 1:
                        item += '0'*i
                    digits.append(item)
                i += 1

            digits = list(reversed(digits))

            i = 0
            change = False
            for item in digits:
                if int(item) % 1000 == 0 and number != '1000':
                    i += 1
                    digits[digits.index(item)] = item.replace('000', '')
                    change = True
            if change == True:
                digits.insert(i, '1000')

    #print(digits)

    i = 0

    while i < len(digits):
        if number != '10' and digits[i] == '10' and int(digits[i + 1]) in range(1, 10):
            digits[i] = str(int(digits[i]) + int(digits[i + 1]))
            del digits[i + 1]
        i += 1

    ready_digits = dict()

    for number in digits:
        if number in unchangables:
            ready_digits[number] = get_unchangable(number)
        elif number in changables:
            ready_digits[number] = get_changable(number)
        elif number == '1':
            ready_digits[number] = get_one()

    #print(ready_digits)

    return digits, ready_digits


def make_forms():
    global digits
    global ready_digits
    global mode

    end_forms = list()

    if len(digits) == 1:
        if mode == 2:
            end_forms_2 = get_adj(digits[0])
        elif mode == 3:
            if zbirni_true(digits[0]):
                end_forms_2 = get_zbirni(digits[0])
            else:
                end_forms_2 = []
        else:
            end_forms_2 = ready_digits[digits[0]]
        return end_forms_2

    elif len(digits) > 1:
        print(digits)
        forms1 = ready_digits[digits[0]]
        forms2 = ready_digits[digits[1]]

        if int(digits[0]) > 999 :
            if digits[1] == '1000' and(digits[0][-1] in ['1', '2'] and digits[0][-2:] not in ['12', '11']):
                forms1 = forms1[2]
            temp_l = []
            i = 0
            while i < 7:
                temp_l.append(forms1[0])
                i += 1
            forms1 = temp_l

        if digits[1] == '1000':
            # if int(digits[0])>9 and digits[0][-1] in ['1','2','3','4']:
            #     if digits[1] == '1000' and (digits[0][-1] == '1' or digits[0][-1] == '2'):
            #         forms1 = forms1[2]
            #     temp_l = []
            #     i = 0
            #     while i < 7:
            #         temp_l.append(forms1[0])
            #         i += 1
            #     forms1 = temp_l
            if digits[0][-1] in ['1', '2'] and digits[0][-2:] not in ['12', '11']:
                forms1 = forms1[2]

            if digits[0][-1] == '1' and digits[0][-2:] != '11':
                forms2 = forms2[1]
            elif digits[0][-1] in ['2','3','4'] and digits[0][-2:] not in ['12', '13', '14']:
                forms2 = forms2[2]
            else:
                forms2 = forms2[2]
                temp_l = []
                i = 0
                while i < 7:
                    temp_l.append(forms2[1])
                    i += 1
                forms2 = temp_l

            # print(forms1)
            # print(forms2)


        if mode == 2 and len(digits) == 2:
            forms_temp = list()
            i = 0
            while i < 7:
                forms_temp.append(forms1[0])
                i += 1
            forms1 = forms_temp
            forms2 = get_adj(digits[1])

        if mode == 3 and len(digits) == 2:
            if zbirni_true(digits[1]):
                forms2 = get_zbirni(digits[1])
            else:
                end_forms_2 = []
                return end_forms_2

        # print(forms1)
        # print(forms2)

        if type(forms2) is dict:
            end_forms = dict()
            j = 1

            while j <= len(list(forms2.keys())):

                    end_forms[j] = list()

                    i = 0

                    while i < 7:
                        temp_end_forms = list()
                        for item1 in forms1[i]:
                            for item2 in forms2[j][i]:
                                if special_adj(number) and number[-4] != '1' and len(digits) == 2:
                                    temp_end_forms.append(item1 + item2)
                                elif special_adj(number) and number[-4] == '1':
                                    item1 = item1.replace('jedna', 'jedan')
                                    temp_end_forms.append(item1 + ' ' + item2)
                                else:
                                    temp_end_forms.append(item1 + ' ' + item2)
                        end_forms[j].append(temp_end_forms)
                        i += 1
                    j += 1

        elif type(forms2) is list:
            i = 0

            while i < 7:
                temp_end_forms = list()
                for item1 in forms1[i]:
                    for item2 in forms2[i]:
                        temp_end_forms.append(item1 + ' ' + item2)
                end_forms.append(temp_end_forms)
                i += 1

        if len(digits) > 2:
            if digits[1] == '1000':
                digits.insert(0, str(int(digits[0]) * int(digits[1])))
            else:
                digits.insert(0, str(int(digits[0]) + int(digits[1])))
            # print(digits[1])
            del digits[1]
            # print(digits[2])
            del digits[1]
            ready_digits[digits[0]] = end_forms
            end_forms_2 = make_forms()

        else:
            end_forms_2 = end_forms
            return end_forms_2

        return end_forms_2


def make_numeral(num):
    global number
    global digits
    global ready_digits
    global mode

    big_result = []
    mode = 1

    while mode < 4:
        number = num
        # try:
        #     digits, ready_digits = make_digits(num)
        #     result = make_forms()
        # except:
        #     result = 'error'
        #     print('aaaaaaa')
        digits, ready_digits = make_digits(num)
        result = make_forms()
        big_result.append(result)
        mode += 1

    # print(mode)
    #print(big_result)

    return big_result[0], big_result[1], big_result[2]

# print(make_numeral('423'))