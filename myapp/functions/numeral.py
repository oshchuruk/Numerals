import sqlite3

def get_case(num):
    conn = sqlite3.connect('myapp/functions/numeric.db')

    cur = conn.execute(
        "select osnova_1, osnova_2, osnova_3, vidminok, stem_1, end_1, stem_2, end_2, stem_3, end_3 from numerals "
        "join classes on numerals.class = classes.class where numerals.id=" + num + ' group by vidminok')

    long_list = cur.fetchall()

    #print(long_list)

    conn.close()

    i = 0

    forms = list()

    while i != len(long_list):
        current_form = list()

        #current_form.append(long_list[i][3])  # vidminok
        #current_form.append(' - ')

        if long_list[i][3] == 4 and int(long_list[i][4]) in [98,99]:
            if int(long_list[i][4]) == 99:
                current_form = forms[0] + forms[1]
            elif int(long_list[i][4]) == 98:
                current_form = forms[0]
        else:
            if int(long_list[i][4]) == 1:  # osnova_1
                current_form.append(long_list[i][0] + long_list[i][5])
            elif int(long_list[i][4]) == 2:
                current_form.append(long_list[i][1] + long_list[i][5])
            elif int(long_list[i][4]) == 3:
                current_form.append(long_list[i][2] + long_list[i][5])

            if long_list[i][6] != '':
                #current_form.append(' / ')

                if int(long_list[i][6]) == 1:
                    current_form.append(long_list[i][0] + long_list[i][7])
                elif int(long_list[i][6]) == 2:
                    current_form.append(long_list[i][1] + long_list[i][7])
                elif int(long_list[i][6]) == 3:
                    current_form.append(long_list[i][1] + long_list[i][7])

            if long_list[i][8] != '':
                #current_form.append(' / ')

                if int(long_list[i][8]) == 1:
                    current_form.append(long_list[i][0] + long_list[i][9])
                elif int(long_list[i][8]) == 2:
                    current_form.append(long_list[i][1] + long_list[i][9])
                elif int(long_list[i][8]) == 3:
                    current_form.append(long_list[i][2] + long_list[i][9])

        forms.append(current_form)
        i += 1

    if num in ['0', '1000', '1000000', '1000000000']:
        form_raw = dict()
        form_raw[1] = list()
        form_raw[2] = list()
        for i in range(1, 3):
            for item in forms:
                form_raw[i].append([item[i-1]])
        forms = form_raw

    return forms

def get_one():
    conn = sqlite3.connect('myapp/functions/numeric.db')

    i = 1

    forms = dict()

    while i <= 4:
        j = 1
        temp_forms_gender = list()
        while j <= 6:
            cur = conn.execute('select form from one '
                               'where vidminok=' + str(j) + ' and gender=' + str(i))

            long_list = cur.fetchall()

            temp_forms_case = list()

            for item in long_list:
                temp_forms_case.append(item[0])

            temp_forms_gender.append(temp_forms_case)

            j += 1

        forms[i] = temp_forms_gender

        i += 1

    return forms


def get_adj(num):
    conn = sqlite3.connect('myapp/functions/numeric.db')

    cur = conn.execute("""select stem, gender, case_1, end_1 from adj_stem
                        join adj_end
                        on adj_stem.class == adj_end.class
                        where adj_stem.num == """ + num)

    all_list = cur.fetchall()
    conn.close()
    # print(all_list)

    forms = dict()

    j = 1

    while j <= 4:
        forms[j] = list()
        for item in all_list:
            if item[1] == j:
                temp_forms = list()
                if item[2] == 4 and item[3] == '99':
                    temp_forms.append(forms[j][0][0])
                    temp_forms.append(forms[j][1][0])
                elif item[2] == 4 and item[3] == '98':
                    temp_forms.append(forms[j][0][0])
                else:
                    temp_forms.append(item[0] + item[3])
                forms[j].append(temp_forms)
        j += 1

    return forms


def merge_last(forms):
    for item in forms:
        if len(item)>0:
            temp = str()
            for value in item:
                temp += value
                if item.index(value) != len(item)-1:
                    temp += ' / '
            forms[forms.index(item)] = temp

    return forms


def find_thousand(num):
    onetwolist = ['2', '3', '4']

    if num[-1] in onetwolist:
        if len(num) > 1 and num[-2] != '1':
            return True
        elif len(num) == 1:
            return True
        else:
            return False
    else:
        return False


zbirni = {
    2:['двоє'],
    3:["троє"],
    4:["четверо"],
    5:["п'ятеро"],
    6:['шестеро'],
    7:['семеро'],
    8:['восьмеро'],
    9:["дев'ятеро"],
    10:['десятеро'],
    11:['одинадцятеро'],
    12:['дванадцятеро'],
    13:['тринадцятеро'],
    14:['чотирнадцятеро'],
    15:["п'ятнадцятеро"],
    16:['шістнадцятеро'],
    17:['сімнадцятеро'],
    18:['вісімнадцятеро'],
    19:["дев'ятнадцятеро"],
    20:['двадцятеро'],
    30:['тридцятеро']
}


def special_adj(num):
    global mode

    if int(num)%1000 == 0 and num[-3:] == '000' and mode == 2:
        return True
    else:
        return False



def zb_true(num):
    if int(num) in list(zbirni.keys()) and mode == 3:
        return True
    else:
        return False

number = '-1'


def make_digits(number):

    #print(get_case(number))

    digits = list()

    if number in ['0','1000000', '1000000000']:
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

            i=0
            change = False
            for item in digits:
                if int(item) % 1000 == 0 and number != '1000':
                    #print(item)
                    i+=1
                    digits[digits.index(item)] = item.replace('000','')
                    change = True
            if change == True:
                digits.insert(i,'1000')

    #print(digits)

    i = 0

    while i < len(digits):
        if number != '10' and digits[i] == '10' and int(digits[i+1]) in range(1,10):
            digits[i] = str(int(digits[i]) + int(digits[i+1]))
            del digits[i+1]
        i+=1

    #print(digits)

    ready_digits = dict()

    for item in digits:
        #print(get_case(item))
        # if digits.index(item) == len(digits)-1 and mode == 2:
        #     ready_digits[item] = get_adj(item)
        if item == '1':
            ready_digits[item] = get_one()
        else:
            ready_digits[item] = get_case(item)

    #print(ready_digits)

    return digits, ready_digits

#print(ready_digits)

digits = list()
ready_digits = list()

def make_forms():
    global digits
    global ready_digits

    #print(digits)

    end_forms = list()
    #end_forms_2 = list()

    if len(digits) == 1: #one-digit number synthesis
        end_forms_2 = ready_digits[digits[0]]
        if zb_true(digits[0]): #zbirni
            end_forms_2[0] = zbirni[int(digits[0])] #nazyvnyy
            end_forms_2[3] = list() #znahidnyy
            end_forms_2[3].append(zbirni[int(digits[0])][0])
            end_forms_2[3].append(end_forms_2[1][0])
        elif mode == 3 and not zb_true(digits[0]):
            end_forms_2 = []
        elif mode == 2:
            end_forms_2 = get_adj(digits[0])
        elif mode == 1 and digits[0] == '1000':
            end_forms_2[2][0][0] = 'тисячі'
        return end_forms_2

    elif len(digits) > 1: #more than one digit
        if mode == 3 and len(digits) == 2 and not zb_true(digits[1]):
            end_forms_2 = []
            return end_forms_2

        if (digits[0][-1] == '1') and type(ready_digits[digits[0]]) == dict:
            forms1 = ready_digits[digits[0]][2] #feminine for thousands ???
        elif mode == 2: #adjectives
            #print(ready_digits[digits[0]][0])

            forms1 = list()
            i = 0

            if special_adj(number):
               #nominative_list = ready_digits[digits[0]][0][0].split()
               genitive_list = list()
               #print('!!!!',ready_digits[digits[0]])
               if type(ready_digits[digits[0]]) is list:
                   genitive_list = ready_digits[digits[0]][1][0].split()
               elif type(ready_digits[digits[0]]) is dict:
                   genitive_list = ready_digits[digits[0]][1][0].split()
               #print(genitive_list)
               new_form = ''
               j = 0
               while j<len(genitive_list):
                   new_form += genitive_list[j]
                   j+=1
               #new_form += genitive_list[-1]
               #print(new_form[0:3])
               if new_form[0:3] == 'ста':
                   new_form = new_form.replace('ста', 'сто')

               new_list = [new_form]
               while i < 6:
                   forms1.append(new_list)
                   i += 1

            else:
                while i < 6:
                    forms1.append(ready_digits[digits[0]][0]) #make all forms in nominative for adjective
                    i += 1
                #print(forms1)
        else:
            forms1 = ready_digits[digits[0]]

        if digits[1] == '1' and special_adj(number):
            forms2 = list()

            odno_count = 0
            while odno_count < 6:
                forms2.append(['одно'])
                odno_count += 1

        elif digits[1] == '1000' and not special_adj(number):
            forms2 = list()
            #print('wowowowo', ready_digits[digits[1]])
            # for item in ready_digits[digits[1]]:
            #     temp = list()
            #     if digits[0][-1] == '1':
            #         temp.append(item[0]) #singular
            #     else:
            #         temp.append(item[1]) #plural
            #     forms2.append(temp)
            if digits[0][-1] == '1':
                forms2 = ready_digits[digits[1]][1]
            else:
                forms2 = ready_digits[digits[1]][2]

        elif len(digits) == 2 and mode == 2:
            forms2 = get_adj(digits[1])

        else:
            forms2 = ready_digits[digits[1]]

        if zb_true(digits[1]) and digits[1] == digits[len(digits)-1]:
            forms2[0] = zbirni[int(digits[1])] #make nominative zbirni

        if type(forms2) is dict: # if 2nd digit is 1 or is adjective?
            #end_forms_2 = dict()
            end_forms = dict()

            j = 1

            while j <= 4:

                end_forms[j] = list()

                i = 0

                while i < 6:
                    temp_end_forms = list()
                    if i == 3: #znahidnyy
                        if 999 < int(number) < 1000000 and number[-4] == '1': #need to make singular znahidnyy
                            for item1 in forms1[3]:
                                for item2 in forms2[j][3]:
                                    if special_adj(number):
                                        temp_end_forms.append(item1 + item2)
                                    else:
                                        temp_end_forms.append(item1 + ' ' + item2)
                        else:
                            if j == 2: #for feminine
                                if special_adj(number) and len(digits) == 2:
                                    temp_end_forms.append(forms1[0][0] + forms2[j][3][0])
                                else:
                                    temp_end_forms.append(forms1[0][0] + ' ' + forms2[j][3][0])
                            else:
                                for item in end_forms[j][0]:
                                    temp_end_forms.append(item)
                                if forms1[3] != forms1[0] and forms2[j][3] != forms2[j][0] and digits[1] != '1000':
                                    for item in end_forms[j][1]:
                                        temp_end_forms.append(item)
                    else: #for other cases
                        for item1 in forms1[i]:
                            if item1 == 'два' and digits[1] == '1000': #do not make dva tysyachi ??
                                pass
                            else:
                                for item2 in forms2[j][i]:
                                    if i == 0 and digits[1] == '1000' and find_thousand(digits[0]) == True and not special_adj(number): #for 2-3-4
                                        item2 = 'тисячі'
                                    if special_adj(number) and len(digits) == 2:
                                        temp_end_forms.append(item1 + item2)
                                    else:
                                        temp_end_forms.append(item1 + ' ' + item2)

                    end_forms[j].append(temp_end_forms)
                    i += 1
                j += 1

        else: #for non-dict cases
            i = 0

            while i < 6:
                temp_end_forms = list()
                if i == 3: #znahidnyy
                    if 999 < int(number) < 1000000 and number[-4] == '1': #need to make singular znahidnyy????
                        for item1 in forms1[3]:
                            for item2 in forms2[3]:
                                temp_end_forms.append(item1 + ' ' + item2)
                    else:
                        for item in end_forms[0]:
                            temp_end_forms.append(item)
                        if forms1[3] != forms1[0] and forms2[3] != forms2[0] and digits[1] != '1000':
                            for item in end_forms[1]:
                                temp_end_forms.append(item)
                # elif len(forms1[i]) == 1 and len(forms2[i]) == 1:
                #     temp_end_forms.append(forms1[0][0] + ' ' + forms2[0][0])
                # elif len(forms1[i]) == 1 and len(forms2[i]) == 2:
                #     temp_end_forms.append(forms1[i][0] + ' ' + forms2[i][0])
                #     temp_end_forms.append(forms1[i][0] + ' ' + forms2[i][1])
                # elif len(forms1[i]) == 2 and len(forms2[i]) == 1:
                #     temp_end_forms.append(forms1[i][0] + ' ' + forms2[i][0])
                #     temp_end_forms.append(forms1[i][1] + ' ' + forms2[i][0])
                # else:
                #     temp_end_forms.append(forms1[i][0] + ' ' + forms2[i][0])
                #     temp_end_forms.append(forms1[i][1] + ' ' + forms2[i][1])
                else:
                    for item1 in forms1[i]:
                        if item1[-3:] == 'два' and digits[1] == '1000': #not dvi tysyach
                            pass
                        else:
                            for item2 in forms2[i]:
                                if i == 0 and digits[1] == '1000' and find_thousand(digits[0]) == True: # for 2-3-4
                                    item2 = 'тисячі'
                                temp_end_forms.append(item1 + ' ' + item2)

                end_forms.append(temp_end_forms)
                i += 1

        if len(digits) > 2:
            if digits[1] == '1000':
                digits.insert(0, str(int(digits[0]) * int(digits[1])))
            else:
                digits.insert(0, str(int(digits[0]) + int(digits[1])))
            #print(digits[1])
            del digits[1]
            #print(digits[2])
            del digits[1]
            ready_digits[digits[0]] = end_forms
            end_forms_2 = make_forms()

        else:
            end_forms_2 = end_forms
            return end_forms_2

        return end_forms_2

mode = 1

def make_numeral(num):
    global number
    global digits
    global ready_digits
    global mode

    big_result = []
    mode = 1

    while mode < 4:
        number = num
        try:
            digits, ready_digits = make_digits(num)
            result = make_forms()
        except:
            result = 'error'
        big_result.append(result)
        mode += 1

    # print(mode)
    # print(big_result)

    return big_result[0], big_result[1], big_result[2]

