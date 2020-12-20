import json


with open('kanjidic2.json', 'r', encoding="utf-8") as obj:
    data = json.load(obj)

def getKanjiDefinition(kanjiInput):
    KanjiDefition_Result = [elem for elem in data["kanjidic2"]["character"] if elem["literal"] == kanjiInput]

    # if result not null
    if KanjiDefition_Result:
        KanjiDefition_Result = KanjiDefition_Result[0]
        KanjiDef_stroke_count = ''
        KanjiDef_freq = ''
        KanjiDef_jlpt = ''
        KanjiDef_grade = ''
        KanjiDef_nelson_n = ''
        KanjiDef_heisig = ''
        KanjiDef_meaning = ''
        KanjiDef_Onyomi = ''
        KanjiDef_Kunyomi = ''
        KanjiDef_Pinyin = ''
        if 'stroke_count' in KanjiDefition_Result['misc']:
            KanjiDef_stroke_count = KanjiDefition_Result['misc']['stroke_count']
        if 'freq' in KanjiDefition_Result['misc']:
            KanjiDef_freq = KanjiDefition_Result['misc']['freq']
        if 'jlpt' in KanjiDefition_Result['misc']:
            KanjiDef_jlpt = KanjiDefition_Result['misc']['jlpt']
        if 'grade' in KanjiDefition_Result['misc']:
            KanjiDef_grade = KanjiDefition_Result['misc']['grade']
        if 'dic_number' in KanjiDefition_Result:
            if 'dic_ref'in KanjiDefition_Result['dic_number']:
                # nelson_n = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if elem["-dr_type"] == 'nelson_n']
                if isinstance(KanjiDefition_Result['dic_number']['dic_ref'],list):
                    KanjiDef_nelson_n = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if elem['-dr_type'] == 'nelson_n']
                    if KanjiDef_nelson_n:
                        KanjiDef_nelson_n = KanjiDef_nelson_n[0]
                    # KanjiDef_heisig = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if elem['-dr_type'] == 'heisig'][0]  . Old version that gave error if 'heisig' dict did not exist because you are trying to read 'heisig'][0]
                    KanjiDef_heisig = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if elem['-dr_type'] == 'heisig']
                    if KanjiDef_heisig:
                        KanjiDef_heisig = KanjiDef_heisig[0]

        if 'rmgroup' in KanjiDefition_Result['reading_meaning']:
            if 'meaning' in KanjiDefition_Result['reading_meaning']['rmgroup']:
                for mList in KanjiDefition_Result['reading_meaning']['rmgroup']['meaning']:
                    # english meaning is in str type whereas other meaning is in list type
                    if isinstance(mList, str):
                        KanjiDef_meaning = KanjiDef_meaning + mList + ', '

        print(KanjiDefition_Result)
        print('KanjiDef_stroke_count: %s' %KanjiDef_stroke_count)
        print('KanjiDef_freq: %s' % KanjiDef_freq)
        print('KanjiDef_jlpt: %s' % KanjiDef_jlpt)
        print('KanjiDef_grade: %s' % KanjiDef_grade)
        print('KanjiDef_nelson_n: %s' % KanjiDef_nelson_n)
        print('KanjiDef_heisig: %s' % KanjiDef_heisig)
        print('KanjiDef_meaning: %s' % KanjiDef_meaning)


        #print(KanjiDefition_Result['dic_number']['dic_ref'])


    # unicodeNumber
    # Onyomi
    # Kunyomi
    return KanjiDefition_Result


#print(data["kanjidic2"]["character"][0]["literal"])
#print(data["kanjidic2"]["character"][0])

for x in range(0,1):
    getKanjiDefinition('模')
    getKanjiDefinition('垬')
    getKanjiDefinition('幣')
    getKanjiDefinition('藍')
    getKanjiDefinition('獻')
    getKanjiDefinition('萊')
    getKanjiDefinition('譯')
    getKanjiDefinition('奪')
    getKanjiDefinition('燒')
    getKanjiDefinition('觸')
    getKanjiDefinition('課')
    getKanjiDefinition('牆')
    getKanjiDefinition('襲')
    getKanjiDefinition('罰')
    getKanjiDefinition('俠')
    getKanjiDefinition('廳')
    getKanjiDefinition('側')
    getKanjiDefinition('韓')
    getKanjiDefinition('債')
    getKanjiDefinition('慣')
    getKanjiDefinition('猶')
    getKanjiDefinition('掛')
    getKanjiDefinition('奬')
    getKanjiDefinition('紹')
    getKanjiDefinition('縱')
    getKanjiDefinition('訊')
    getKanjiDefinition('徹')
    getKanjiDefinition('烏')
    getKanjiDefinition('瑪')
    getKanjiDefinition('鏡')
    getKanjiDefinition('煩')
    getKanjiDefinition('簽')
    getKanjiDefinition('癥')
    getKanjiDefinition('傾')
    getKanjiDefinition('鳥')
    getKanjiDefinition('轟')

