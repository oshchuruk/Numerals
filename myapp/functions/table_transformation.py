import myapp.functions.numeral as numeral
import myapp.functions.cro_numeral as cro_numeral
import myapp.functions.analysis as analysis

cases_list = ["Н", "Р", "Д", "З", "О", "М", "К"]
cases_list_plus = ['азивний', 'одовий', 'авальний', 'нахідний', 'рудний', 'ісцевий', 'личний']
gender_list = ['чоловічий', "жіночий", "середній", "множина"]
numbers_list = ['однина', "множина"]
forms_list = ['кількісний числівник', "порядковий прикметник", "збірний числівник"]

cro_cases_list = ['N', 'G', 'D', 'A', 'V', 'L', 'I']
cro_cases_list_plus = ['ominativ', 'enitiv', 'ativ', 'kuzativ', 'okativ', 'okativ', 'nstrumental']
cro_gender_list_1 = ['muški rod jednine', 'ženski rod jednine', 'sredni rod jednine', 'muški rod množine', 'zenski rod množine', 'sredni rod množine']
cro_gender_list_2 = ['muški rod', 'ženski rod', 'sredni rod']
cro_gender_list_3 = ['promjenljivo, osoba', 'promjenljivo, ostalo', 'nepromjenljivo uz nebrojive imenice']
cro_gender_list_4 = ['jednina', 'množina']
cro_forms_list = ['glavni broj', 'redni pridjev', 'zbirni broj']


def make_header(obj, forms):
    result = '<p class="num">'
    result += obj + ' - '
    title = obj + ' - '
    if type(forms) is list:
        result += forms[0][0] + '</p>'
        title += forms[0][0]
    else:
        result += forms[1][0][0] + '</p>'
        title += forms[1][0][0]
    return result, title


def make_table(obj, iterat):
    html_st = str()
    if iterat == 1:
        html_st += """<div class="content">\n
        <a href="javascript:hideshow(document.getElementById('cardinal'),document.getElementById('1p'))" class='content'><span id='1p'>▼</span> Кількісний числівник</a>\n
        </div>\n

            <div id='cardinal' style='display:block'> \n """
    elif iterat == 2:
        html_st += """<div class="content">\n
        <a href="javascript:hideshow(document.getElementById('ordinal'),document.getElementById('2p'))" class='content'><span id='2p'>▶</span> Порядковий прикметник</a>\n
        </div>\n

        <div id='ordinal' style='display:none'>\n  """
    elif iterat == 3:
        html_st += """<div class="content">\n
        <a href="javascript:hideshow(document.getElementById('zbirni'),document.getElementById('3p'))" class='content'><span id='3p'>▶</span> Збірний числівник</a>\n
        </div>\n

        <div id='zbirni' style='display:none'> \n """

    html_st += '<table>\n'
    i = 0

    if obj == []:
        return obj

    if type(obj) is list:
        for sublist in obj:
            html_st += '<tr>\n<td>\n'
            html_st += cases_list[i] + '\n'
            html_st += '</td>\n<td>\n'
            for item in sublist:
                if sublist.index(item) == 0:
                    if i == 5:
                        html_st += 'на '
                    html_st += item
                else:
                    html_st += '<p style="margin:10px 0 0 0">'
                    if i == 5:
                        html_st += 'на '
                    html_st += item + '</p>'
                if sublist.index(item) != len(sublist)-1:
                    html_st += '\n\n'
            html_st += '</td>\n</tr>\n'
            i += 1
        html_st += '<tr>\n<td>\n'
        html_st += cases_list[6] + '\n'
        html_st += '</td>\n<td>\n'
        html_st += obj[0][0] + '\n'
        html_st += '</td>\n</tr>\n'

    elif type(obj) is dict:
        res_list = list()
        if len(list(obj.keys())) == 4:
            res_list = gender_list
        elif len(list(obj.keys())) == 2:
            res_list = numbers_list
        html_st += '<tr>\n<td>\n</td>\n'
        for item in res_list:
            html_st += '<td>\n'+item + '\n'
        html_st += '</tr>'
        i = 0
        while i < 6:
            html_st += '<tr>\n<td>\n'
            html_st += cases_list[i] + '\n</td>\n'
            j = 1
            while j <= len(list(obj.keys())):
                html_st += '<td>\n'
                for item in obj[j][i]:
                    if obj[j][i].index(item) == 0:
                        if i == 5:
                            html_st += 'на '
                        html_st += item
                    else:
                        html_st += '<p style="margin:10px 0 0 0">'
                        if i == 5:
                            html_st += 'на '
                        html_st += item + '</p>'
                    if obj[j][i].index(item) != len(obj[j][i]) - 1:
                        html_st += '\n\n'
                html_st += '</td>\n'
                j += 1
            html_st += '</tr>'
            i += 1
        html_st += '<tr>\n<td>\n'
        html_st += cases_list[6] + '\n'
        html_st += '</td>\n'
        j = 1
        while j <= len(list(obj.keys())):
            html_st += '<td>\n'
            for item in obj[j][0]:
                html_st += item
                if obj[j][0].index(item) != len(obj[j][0]) - 1:
                    html_st += '\n\n'
            html_st += '</td>\n'
            j += 1
        html_st += '</tr>\n'
    html_st += '</table>\n<br>\n'

    html_st +='</div>'

    return html_st


def make_table_cro(obj, tip):
    if obj == []:
        return obj

    html_st = str()

    if tip == 1:
        html_st += """<div class="content">\n
        <a href="javascript:hideshow(document.getElementById('cardinal'),document.getElementById('1p'))" class='content'><span id='1p'>▼</span> Glavni broj</a>\n
        </div>\n

            <div id='cardinal' style='display:block'> \n """
    elif tip == 2:
        html_st += """<div class="content">\n
        <a href="javascript:hideshow(document.getElementById('ordinal'),document.getElementById('2p'))" class='content'><span id='2p'>▶</span> Redni pridjev</a>\n
        </div>\n

        <div id='ordinal' style='display:none'>\n  """
    elif tip == 3:
        html_st += """<div class="content">\n
        <a href="javascript:hideshow(document.getElementById('zbirni'),document.getElementById('3p'))" class='content'><span id='3p'>▶</span> Zbirni broj</a>\n
        </div>\n

        <div id='zbirni' style='display:none'> \n """

    html_st += '<table>\n'
    i = 0

    if type(obj) is list:
        for sublist in obj:
            html_st += '<tr>\n<td>\n'
            html_st += cro_cases_list[i] + '\n'
            html_st += '</td>\n<td>\n'
            for item in sublist:
                if sublist.index(item) == 0:
                    if i == 5:
                        html_st += 'na '
                    html_st += item
                else:
                    html_st += '<p style="margin:10px 0 0 0">'
                    if i == 5:
                        html_st += 'na '
                    html_st += item + '</p>'
                if sublist.index(item) != len(sublist)-1:
                    html_st += '\n\n'
            html_st += '</td>\n</tr>\n'
            i += 1

    elif type(obj) is dict:
        res_list = list()
        if len(list(obj.keys())) == 6:
                res_list = cro_gender_list_1
        elif len(list(obj.keys())) == 3:
            if tip == 1:
                res_list = cro_gender_list_2
            elif tip == 3:
                res_list = cro_gender_list_3
        elif len(list(obj.keys())) == 2:
            res_list = cro_gender_list_4

        html_st += '<tr>\n<td>\n</td>\n'
        for item in res_list:
            html_st += '<td>\n'+item + '\n'
        html_st += '</tr>'
        i = 0
        while i < 7:
            html_st += '<tr>\n<td>\n'
            html_st += cro_cases_list[i] + '\n</td>\n'
            j = 1
            while j < len(res_list)+1:
                html_st += '<td>\n'
                for item in obj[j][i]:
                    if obj[j][i].index(item) == 0:
                        if i == 5:
                            html_st += 'na '
                        html_st += item
                    else:
                        html_st += '<p style="margin:10px 0 0 0">'
                        if i == 5:
                            html_st += 'na '
                        html_st += item + '</p>'
                    if obj[j][i].index(item) != len(obj[j][i]) - 1:
                        html_st += '\n\n'
                html_st += '</td>\n'
                j += 1
            html_st += '</tr>'
            i += 1
    html_st += '</table>\n<br>\n'

    html_st +='</div>'


    return html_st


def make_analyzed_forms(raw, num, lang):
    res_str = ''
    typ = -1
    gend = -1
    if raw != []:
        res_str = '<ul>\n'
        for item in raw:
            item_str = ''
            print(item)
            if item[0] != typ or item[1] != gend:
                if res_str[-2:] == '/ ':
                    res_str = res_str[:-2]
                item_str += '</li>\n'
                if lang == 'ukr':
                    item_str += '<li> ' + forms_list[item[0]]
                elif lang == 'cro':
                    item_str += '<li> ' + cro_forms_list[item[0]]
                typ = item[0]
                item_str += ', '
                gend = item[1]
                if item[1] != 0:
                    if lang == 'ukr':
                        if num in ['0', '1000', '1000000', '1000000000'] and item[0] == 0:
                            item_str += numbers_list[item[1]-1] + ', '
                        else:
                            item_str += gender_list[item[1]-1]
                            item_str += ' рід, '
                    elif lang == 'cro':
                        if item[0] == 0:
                            if num in ['0', '1000', '1000000', '1000000000']:
                                item_str += cro_gender_list_4[item[1] - 1] + ', '
                            elif num == '2':
                                item_str += cro_gender_list_2[item[1] - 1] + ', '
                            elif num == '1':
                                item_str += cro_gender_list_1[item[1] - 1] + ', '
                        elif item[0] == 1:
                            item_str += cro_gender_list_1[item[1] - 1] + ', '
                        elif item[0] == 2:
                            item_str += cro_gender_list_3[item[1] - 1] + ', '
            if lang == 'ukr':
                item_str += cases_list[item[2]] + cases_list_plus[item[2]] + ' в. / '
            elif lang == 'cro':
                item_str += cro_cases_list[item[2]] + cro_cases_list_plus[item[2]] + ' / '
            res_str += item_str
        if res_str[-2:] == '/ ':
            res_str = res_str[:-2]
        res_str += '</li>\n</ul>\n'

    return res_str

# res = analysis.analyze_form("двадцяти дев'яти",'29')
# print(res)
#
# print(make_analyzed_forms(res))