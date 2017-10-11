from django.shortcuts import render
import datetime
import myapp.functions.numeral as num
import myapp.functions.table_transformation as transform
import myapp.functions.analysis as analysis
import myapp.functions.cro_numeral as cro_num
import myapp.functions.phrasal as phrasal
from myapp.forms import mainForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def hello(request, inp_number):
    if not inp_number.isdigit():
        inp = inp_number
        dig = analysis.numeral_to_digits(inp_number, 'ukr')
        title = inp + ' - ' + dig
        header = '<p class="num">' + title + '</p>'
        try:
            temp = analysis.analyze_form(inp_number, analysis.numeral_to_digits(inp_number, 'ukr'), 'ukr')
            result = transform.make_analyzed_forms(temp, dig, 'ukr')
        except:
            return render(request, 'error_ukr.html')
        if result == '':
            return render(request, 'error_ukr.html')
        paradigm = '<p>Повна парадигма - див. <a href="../' + dig + '">' + dig + '</a>.</p>'
        return render(request, "analysis_ukr.html", {'title':title,"header": header, 'result':result, 'paradigm':paradigm, 'inp' : inp_number})

    else:
        l1, l2, l3 = num.make_numeral(str(inp_number))
        if l1 == 'error' or l2 == 'error' or l3 == 'error':
            return render(request, 'error_ukr.html')

        header, title = transform.make_header(inp_number,l1)
        cardinal = transform.make_table(l1, 1)
        ordinal = transform.make_table(l2, 2)
        zbirny = transform.make_table(l3, 3)
        if zbirny == []:
            zbirny = ''
        fraz = phrasal.get_phrasal(inp_number, 'ukr')

        return render(request, "synthesis_ukr.html", {'title':title,"header" : header, "cardinal" : cardinal,
                                                  "ordinal" : ordinal, "zbirny" : zbirny, 'fraz' : fraz, 'inp' : inp_number})


def hello_cro(request, inp_number):
    if not inp_number.isdigit():
        inp = inp_number
        dig = analysis.numeral_to_digits(inp_number, 'cro')
        title = inp + ' - ' + dig
        header = '<p class="num">' + title + '</p>'
        try:
            result = transform.make_analyzed_forms(analysis.analyze_form(inp_number, analysis.numeral_to_digits(inp_number, 'cro'), 'cro'), dig, 'cro')
        except:
            return render(request, 'error_cro.html')
        if result == '':
            return render(request, 'error_cro.html')
        paradigm = '<p>Paradigma - <a href="../' + dig + '">' + dig + '</a>.</p>'
        return render(request, "analysis_cro.html", {'title':title,"header": header, 'result':result, 'paradigm':paradigm, 'inp' : inp_number})
    else:
        l1, l2, l3 = cro_num.make_numeral(inp_number)
        # if l1 == 'error' or l2 == 'error' or l3 == 'error':
        #     return render(request, 'error_cro.html')
        header, title = transform.make_header(inp_number, l1)
        cardinal = transform.make_table_cro(l1, 1)
        ordinal = transform.make_table_cro(l2, 2)
        zbirny = transform.make_table_cro(l3, 3)
        if zbirny == []:
            zbirny = ''
        fraz = phrasal.get_phrasal(inp_number, 'cro')
        return render(request, "synthesis_cro.html", {'title':title,"header" : header, "cardinal" : cardinal,
                                                      "ordinal" : ordinal, "zbirny" : zbirny, 'fraz' : fraz, 'inp' : inp_number})


def insert(request):
    myform = mainForm(request.GET)
    number = myform.data['number']
    return redirect('hello', inp_number=number)


def insert_cro(request):
    myform = mainForm(request.GET)
    number = myform.data['number']
    return redirect('hello_cro', inp_number=number)
