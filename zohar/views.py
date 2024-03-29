# -*- coding: utf-8 -*-
from django.shortcuts import render
import os
import re
import io
import sys
import unicodedata
import collections


ALEPHBET = u'[אבגדהוזחטיכךלמםנןסעפףצץקרשתﭏ]'
#RESULTS = collections.OrderedDict()

def index(request):
    debug = []
    debug2= []
    found_verses = []
    count = 0
    filter = request.GET.get('filter')
    value = request.GET.get('criteria', '').strip()
    title_lib1 = request.GET.get('title_lib1', '')
    title_lib2 = request.GET.get('title_lib2', '')
    lib = request.GET.get('library', '')
    book=''
    docs=1
    
    if lib != '':
        main_lib = True if lib=='lib1' else False 
    
    #remove BOM
    if title_lib1.startswith(u'\ufeff'):
        title_lib1 = title_lib1[1:]
    
    if value != '':
        debug, found_verses = search(value, main_lib, filter)
        #count = len(found_verses)
    elif title_lib1 != '':
        docs = list_of_resources(True)
        debug, book = get_book(docs,title_lib1)
    elif title_lib2 != '':
        docs = list_of_resources(False)
        debug, book = get_book(docs,title_lib2)
    
    """
    if False:
        docs = list_of_resources(False)
        ex = re.compile(ur'(?<=")\d{1,4}', re.UNICODE)
        
        for doc in docs:
            with io.open(doc, 'r+', encoding='utf-8-sig') as doc:
                    text = doc.read()
                    found = ex.search(text)
                    if found:
                        text = ex.sub('['+'\g<0>'+']',text)
                    doc.seek(0)
                    doc.write(text)
                    doc.truncate()
                    doc.close()
    """
    
    length = get_len_of_dict_content(found_verses)

    context = {'found_verses':found_verses, 'count':length, 'value':value, 'master_map':MASTER_MAP, 'book':book, 'debug':debug, 'debug2':debug2}
    return render(request, 'zohar/main.html', context)

def get_book(docs,title):
    debug = []
    book=[]
    hebrew_pattern = re.compile(ALEPHBET, re.UNICODE)
#     footnote_pattern = re.compile(ur'\[\d{1,4}\]', re.UNICODE)
    footnote_pattern = re.compile(r'\[\d{1,4}\]', re.UNICODE)
    title = unicodedata.normalize('NFC', title)
    
    for doc in docs:
        with io.open(doc, 'r', encoding='utf-8-sig') as doc:
            line_number = 1
            for line in doc:
                if title != line.strip():
                    break
                else:
                    
#                     modified_title = '<h2 id="title">{0}</h2>'.format(title.encode('utf-8-sig'))
                    modified_title = '<h2 id="title">{0}</h2>'.format(title)
                    book.append(modified_title)
                    
                    for l in doc:
                        line_number+=1
                        
                        #find all hebrew and bold them
                        found = hebrew_pattern.search(l)
                        if found:
                            l = hebrew_pattern.sub('<span xml:lang="he" lang="he" class="ezra">'+'\g<0>'+'</span>',l)
                        
                        #find all footnotes and link them
                        found = footnote_pattern.search(l)
                        if found:
                            if l.startswith('['):
                                l = footnote_pattern.sub('<a id="cite_note-\g<0>" href="#cite_ref-\g<0>">&uarr;</a> \g<0> ',l)
                            else:
                                l = footnote_pattern.sub('<sup id="cite_ref-\g<0>"><a href="#cite_note-\g<0>">\g<0></a></sup>',l)    
                        
                        book.append('<span id="'+str(line_number)+'">'+l+'</span>')
    
    return debug, book

def search(words, main_lib, filter):
    key_words = []
    debug = []
    found_verses = collections.OrderedDict()

    for book in BOOKS:
#         found_verses[book.decode("utf-8-sig").encode("utf-8")]=[]
        found_verses[book.encode("utf-8")]=[]
    
    docs = list_of_resources(main_lib)
    which_lib = 'title_lib1' if main_lib else 'title_lib2'
    
    if filter == 'filter_1':
        key_words.append(words)
    else:
        key_words = words.split()
    
    if len(key_words)==1:
        pattern = set_pattern(key_words[0], filter)

    for doc in docs:
        with io.open(doc, 'r', encoding='utf-8-sig') as opened_doc:
            line_number = 0
            get_title = True
            for line in opened_doc:
                line_number+=1
                if get_title:
                    title = line.rstrip()
                    get_title = False
                    continue
                
                if len(key_words)>1:
                    for word in key_words:
                        pattern = set_pattern(word, filter)
                        found = pattern.search(line)
                        if not found and filter != 'filter_2':
                            break
                        elif found and filter == 'filter_2':
                            break
                else:
                    found = pattern.search(line)
                
                if found:
                    for word in key_words:
                        pattern = set_pattern(word, filter)
                        line = pattern.sub('<span class="highlightme">'+'\g<0>'+'</span>',line)

                    try:
                        found_verses[title.encode("utf-8")].append('<a href="/zohar/?'+which_lib+'='+title+'#'+str(line_number)+'"><b>'+title+'</b></a></br>'+line)
                    except:
                        found_verses[title.encode("utf-8")]=[]
                        found_verses[title.encode("utf-8")].append('<a href="/zohar/?'+which_lib+'='+title+'#'+str(line_number)+'"><b>'+title+'</b></a></br>'+line)

    return debug, found_verses

def set_pattern(key, filter):
    if filter == 'filter_1' or filter == 'filter_2':
        pattern = re.compile(key, re.I|re.UNICODE)
    elif filter == 'filter_3':
        pattern = re.compile(key, re.UNICODE)
    elif filter == 'filter_4':
#         pattern = re.compile(ur'\b{0}\b'.format(key), re.I|re.UNICODE)
        pattern = re.compile(r'\b{0}\b'.format(key), re.I|re.UNICODE)
    else:
        pattern = re.compile(key, re.I|re.UNICODE)
    return pattern

def list_of_resources(main_lib=True):
    res = []

    if main_lib:
        docs_dir = os.path.join(os.path.dirname(__file__),'lib1')
    else:
        docs_dir = os.path.join(os.path.dirname(__file__),'lib2')

    # Windows
    # for folder, subs, files in os.walk(unicode(docs_dir, 'utf-8')):
    #     for filename in files:
    #         if not filename.startswith('.'):
    #             file_path = os.path.join(folder, filename)
    #             res.append(file_path)

    for doc in os.listdir(docs_dir):
        if not doc.startswith('.'):
            res.append(os.path.join(docs_dir,doc))

    return res

def get_len_of_dict_content(dict):
    length = 0
    try:
        for k,v in dict.items():
            length+=len(v)
    except:
        pass
    return length

MASTER_MAP = [('בְּרֵאשִׁית',	'Берешит', ['Зоhар Брейшит I','Зоhар Брейшит II'],['Зоhар Брейшит']),
              ('נֹחַ	', 'Ноах', ['Зоhар Ноах'],['Зоhар Ноах']),
              ('לֶךְ-לְךָ	', 'Лех Леха', ['Зоhар Лех Леха'],['Зоhар Лех Леха']),
              ('וַיֵּרָא	', 'Ва-Иера', ['Зоhар Ва-йера'],['Зоhар Ва-йера']),
              ('חַיֵּי שָׂרָה	', 'Хайей Сара', ['Зоhар Хайей Сара'],['Зоhар Хайей Сара']),
              ('תּוֹלְדֹת	', 'Толдот', ['Зоhар Толдот'],['Зоhар Толдот']),
              ('וַיֵּצֵא	', 'Ва-Иеце', ['Зоhар Ва-йеце'],['Зоhар Ваеце']),
              ('וַיִּשְׁלַח	', 'Ва-Йишлах', ['Зоhар Ва-йишлах'],['Зоhар Ваишлах']),
              ('וַיֵּשֶׁב	', 'Ва-Иешев', ['﻿Зоhар Ва-йешев'],['Зоhар Вейшев']),
              ('מִקֵּץ	', 'Ми-Кец', ['Зоhар Ми-кец'],['Зоhар Микец']),
              ('וַיִּגַּשׁ	', 'Ва-Йиггаш', ['Зоhар Ваигаш'],['Зоhар Ваигаш']),
              ('וַיְחִי	', 'Ва-Иехи', ['Зоhар Вайехи'],['Зоhар Ваехи I','Зоhар Ваехи II','Зоhар Ваехи III']),
              ('שְׁמוֹת	', 'Шмот', [],['Зоhар Шемот']),
              ('וָאֵרָא	', 'Ва-Эра', [],['Зоhар Ва-Эра']),
              ('בֹּא	', 'Бо', [],['Зоhар Бо']),
              ('בְּשַׁלַּח	', 'Бе-Шаллах', [],['Зоhар Бешалах II']),
              ('יִתְרוֹ	', 'Итро', [],['Зоhар Итро I','Зоhар Итро II','Зоhар Итро III']),
              ('מִשְׁפָּטִים	', 'Мишпатим', [],['Зоhар Мишпатим I','Зоhар Мишпатим II']),
              ('תְּרוּמָה	', 'Трума', [],['Зоhар Трума I','Зоhар Трума II']),
              ('תְּצַוֶּה	', 'Тецавве', [],['Зоhар Тецаве']),
              ('כִּי תִשָּׂא	', 'Ки Тисса', [],['Зоhар Ки Тиса']),
              ('וַיַּקְהֵל	', 'Ва-Якхел', [],['Зоhар Ваикаэль']),
              ('פְּקוּדֵי	', 'Пкудей', [],['Зоhар Пкудей']),
              ('וַיִּקְרָא	', 'Ва-Йикра', [],['Зоhар Ваикра']),
              ('צַו	', 'Цав', [],['Зоhар Цав I','Зоhар Цав II']),
              ('שְׁמִינִי	', 'Шмини', [],['Зоhар Шмини']),
              ('תַּזְרִיעַ	 ', 'Тазриа', [],['Зоhар Тазриа']),
              ('מְצֹרָע	', 'Мецора', [],[ 'Зоhар Мецора']),
              ('אַחֲרֵי מוֹת	', 'Ахарей Мот', [],[]),
              ('קְדֹשִׁים	', 'Кдошим', [],[]),
              ('אֱמֹר	', 'Эмор', [],[]),
              ('בְּהַר	', 'Бе-Хар', [],['Зоhар Беhар']),
              ('בְּחֻקֹּתַי	', 'Бе-Хукотай', [],['Зоhар Бехукотай']),
              ('בְּמִדְבַּר	', 'Бе-Мидбар', [],['Зоhар Бемидбар']),
              ('נָשֹׂא	', 'Насо', [],[]),
              ('בְּהַעֲלֹתְךָ	 ', 'Бе-Хаалотха', [],['Зоhар Беhаалотеха']),
              ('שְׁלַח-לְךָ	 ', 'Шлах Леха', [],[]),
              ('קֹרַח	', 'Корах', [],['Зоhар Корах']),
              ('חֻקַּת	', 'Хукат', [],['Зоhар Хукат']),
              ('בָּלָק	', 'Балак', [],[]),
              ('פִּינְחָס	', 'Пинхас', [],[]),
              ('מַטּוֹת	', 'Матот', [],[]),
              ('מַסְעֵי	', 'Масей', [],[]),
              ('דְּבָרִים	', 'Дварим', [],[]),
              ('וָאֶתְחַנַּן	', 'Ва-Этханан', [],[]),
              ('עֵקֶב	', 'Экев', [],['Зоhар Экев']),
              ('רְאֵה	', 'Реэ', [],[]),
              ('שֹׁפְטִים	', 'Шофтим', [],['Зоhар Шофтим']),
              ('כִּי תֵצֵא	', 'Ки Теце', [],[]),
              ('כִּי תָבוֹא	', 'Ки Таво', [],[]),
              ('נִצָּבִים	', 'Ниццавим', [],[]),
              ('וַיֵּלֶך	', 'Ва-Иелех', [],[]),
              ('הַאֲזִינוּ	', 'Хаазину', [],[]),
              ('וְזֹאת הַבְּרָכָה	', 'Ве-Зот ха-браха', [],[])]

BOOKS = ['Сефер Ецира',
         'Бахир',
         'Зоhар hакдама',
         'Зоhар Акдамат I',
         'Зоhар Акдамат II',
         'Зоhар Брейшит',
         'Зоhар Брейшит I',
         'Зоhар Брейшит II',
         'Зоhар Ноах',
         'Зоhар Лех Леха',
         'Зоhар Ва-йера',
         'Зоhар Ва-йера',
         'Зоhар Хайей Сара',
         'Зоhар Хайей Сара',
         'Зоhар Толдот',
         'Зоhар Ва-йеце',
         'Зоhар Ваеце',
         'Зоhар Ва-йишлах',
         'Зоhар Ваишлах',
         '﻿Зоhар Ва-йешев',
         'Зоhар Вейшев',
         'Зоhар Ми-кец',
         'Зоhар Микец',
         'Зоhар Ваигаш',
         'Зоhар Вайехи',
         'Зоhар Ваехи I',
         'Зоhар Ваехи II',
         'Зоhар Ваехи III',
         'Зоhар Шемот',
         'Зоhар Ва-Эра',
         'Зоhар Бо',
         'Зоhар Бешалах II',
         'Зоhар Итро I',
         'Зоhар Итро II',
         'Зоhар Итро III',
         'Зоhар Мишпатим I',
         'Зоhар Мишпатим II',
         'Зоhар Трума I',
         'Зоhар Трума II',
         'Зоhар Тецаве',
         'Зоhар Ки Тиса',
         'Зоhар Ваикаэль',
         'Зоhар Пкудей',
         'Зоhар Ваикра',
         'Зоhар Цав I',
         'Зоhар Цав II',
         'Зоhар Шмини',
         'Зоhар Тазриа',
         'Зоhар Мецора',
         'Зоhар Беhар',
         'Зоhар Бехукотай',
         'Зоhар Бемидбар',
         'Зоhар Беhаалотеха',
         'Зоhар Корах',
         'Зоhар Хукат',
         'Зоhар Экев',
         'Зоhар Шофтим'
         ]
