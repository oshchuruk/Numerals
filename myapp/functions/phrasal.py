import sqlite3


def get_phrasal(num, lang):
    conn = sqlite3.connect('myapp/functions/numeric.db')
    if lang == 'ukr':
        cur = conn.execute("""select id,phrasal, meaning, synonym from phrasal_ukr where num =""" + num)
    elif lang == 'cro':
        cur = conn.execute("""select id,phrasal, meaning, synonym from phrasal_cro where num =""" + num)
    result = cur.fetchall()
    conn.close()

    phrasals = []
    synonyms_id = []
    for item in result:
        if item[0] not in synonyms_id:
            phrasals_raw = []
            synonyms_raw = []
            phrasals_raw.append(item[1])
            if item[2] is not None:
                phrasals_raw.append(item[2])
            if item[3] == 999:
                for element in result:
                    if element[3] == item[0]:
                        synonyms_raw.append(element[1])
                        synonyms_id.append(element[0])
                phrasals_raw.append(synonyms_raw)
            phrasals.append(phrasals_raw)

    res_str = str()
    if phrasals != []:
        res_str += '''<div class="content">\n
                   <a href="javascript:hideshow(document.getElementById('fraz'),document.getElementById('4p'))" class='content'>'''
        if lang == 'ukr':
            res_str += '''<span id='4p'>▶</span> Фразеологізми</a>\n'''
        elif lang == 'cro':
            res_str += '''<span id='4p'>▶</span> Frazemi</a>\n'''
        res_str +=   '''
            </div>\n

            <div id='fraz' style='display:none'>\n  '''


    for item in phrasals:
        #print(item)
        res_str += '<p>'
        res_str += '<strong>' + item[0] + '</strong> '
        res_str += item[1]
        if len(item) == 3:
            if lang == 'ukr':
                res_str += ' <u>Синоніми:</u> \n'
            elif lang == 'cro':
                res_str += ' <u>Sinonimi:</u> \n'
            for element in item[2]:
                if item[2].index(element) != 0:
                    element_l = element.lower()
                else:
                    element_l = element
                res_str += '<strong>' + element_l + '</strong>'
                if len(item[2]) > 1:
                    if item[2].index(element)+1 == len(item[2]):
                        res_str += '.' + '</strong>'
                    else:
                        res_str += '; '
                else:
                    res_str += '.'
        res_str += '</p>\n'

    if phrasals != []:
        res_str += '''<br>\n
                    </div>\n'''

    return res_str
