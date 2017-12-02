import pymorphy2
import myapp.functions.numeral


def getDate(word):
    dates_list = [
        'січень',
        "лютий",
        "березень",
        "квітень",
        "травень",
        "червень",
        "липень",
        "серпень",
        "вересень",
        "жовтень",
        "листопад",
        "грудень",
        "рок"
    ]

    if word in dates_list:
        return True
    else:
        return False


def replaceform(num, noun, gender, previous, date):
    if date:
        raw_forms = myapp.functions.numeral.make_numeral(num)[1][1]
    else:
        raw_forms = myapp.functions.numeral.make_numeral(num)[0]
    #print(myapp.functions.numeral.make_digits(num))
    last_digit = myapp.functions.numeral.make_digits(num)[0][len(myapp.functions.numeral.make_digits(num)[0])-1]
    #print(last_digit)
    change_dict = {
        'loct': 5,
        'ablt': 4,
        'datv': 2,
        'gent': 1,
        'nomn': 0,
        'accs': 3,
        'masc': 1,
        'femn': 2,
        'neut': 3,
        'plur': 4
    }

    if int(last_digit) > 4:
        if (previous == 1 and noun.case == 'gent') or date:
            pass
        else:
            change_dict['gent'] = 0
        return raw_forms[change_dict[noun.case]][0]

    if int(last_digit) == 2:
        if (noun.case == 'nomn' or noun.case == 'accs') and gender == 'femn':
            return raw_forms[change_dict[noun.case]][1]
        else:
            return raw_forms[change_dict[noun.case]][0]

    if int(last_digit) == 1:
        return raw_forms[change_dict[noun.gender]][change_dict[noun.case]][0]

    return raw_forms[change_dict[noun.case]][0]

def transform_numeral(s):

    morph = pymorphy2.MorphAnalyzer(lang='uk')

    noun = ''
    gender = ''
    current = 0
    previous = 0

    for item in s.split():
        res = morph.parse(item)
        for element in res:
            if element.tag.POS == 'ADVB':
                #print(item)
                current = 1
                break
            else:
                previous = current
                current = 0

        if item.isdigit():
            num = item
            #print(previous)


            for item in s[(s.index(num[0])+len(num)):].split():
                if item[-1] == '.':
                    item = item.replace('.','')
                flag = 0
                res = morph.parse(item)
                for element in res:
                    if element.tag.POS == 'NOUN':
                        if num[-1] != '1' and element.tag.number == 'plur':
                            noun = element.tag
                            flag = 1
                            ##print(element)

                            gender = morph.parse(element.normal_form)
                            gender = gender[0].tag.gender
                            date = getDate(element.normal_form)
                            #print(element.normal_form)
                            #print(num)
                            #print(date)
                            break
                        elif num[-1] == '1' and element.tag.number != 'plur':
                            noun = element.tag
                            flag = 1
                            #print(element)

                            gender = morph.parse(element.normal_form)
                            gender = gender[0].tag.gender
                            date = getDate(element.normal_form)
                            #print(element.normal_form)
                            #print(num)
                            #print(date)
                            break
                        elif num[-1] != '1' and element.tag.number != 'plur' and getDate(element.normal_form):
                            noun = element.tag
                            flag = 1
                            # print(element)

                            gender = morph.parse(element.normal_form)
                            gender = gender[0].tag.gender
                            date = getDate(element.normal_form)
                            #print(element.normal_form)
                            #print(noun.case)
                            #print(num)
                            #print(date)
                            break
                if flag == 1:
                    break

            s = s.replace(num, replaceform(num, noun, gender, previous, date))


    # print(noun)
    # print(gender)
    # print(myapp.functions.numeral.make_numeral(num)[0])


    return s


#print(transform_numeral("За словами Лаврова, комплекс заходів, узгоджений у Мінську в лютому 2015 року був одноголосно схвалений РБ ООН і досі лишається абсолютно безальтернативним документом, який дозволяє врегулювати цю кризу."))
