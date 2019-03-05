# -*- coding: utf-8 -*-
# Copyright: mo  <fickle_123@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# I made this on my free time. Been ages since I do any coding. Expect messy codes & ensure back up is in place.
# Bulk generate Homophone List based on input Hanzi
#for example, 他 will yield:
#tā : 他她它塌
#tá : 
#tǎ : 塔
#tà : 踏
#if Fuzzy_Character_Mode_Enabled is set to true then similar consonant will also be included;
#dā : 搭
#dá : 达答
#dǎ : 打
#dà : 大

##########################################################################
#"deck:00_Hanzi::Most Common 3000 Hanzi" (Pinyin:"zhǐ" or Pinyin:"dì")
# USE LOWERCASE. Model name must contain this.

#Output_SrcField = 'Auto Note_Current'
# if data exists in Output_SrcField, should we overwrite it?
#OVERWRITE_DST_FIELD=True
#Fuzzy_Character_Mode_Enabled=False
##########################################################################
from aqt.qt import *
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning, showInfo
import re
import platform
import re
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE
import sys
import fnmatch
#reload(sys) #apparently this doesn't work in python3... 
#sys.setdefaultencoding('utf-8')
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE !!

# added dot for importing relative module package.
from .hangul_jamo import is_syllable, is_jamo_character, compose_jamo_characters, decompose_syllable, compose, decompose


modelName = ''
Vocab_SrcField = ''
Meaning_SrcField = ''
Output_SrcField = ''
OVERWRITE_DST_FIELD= ''
Fuzzy_Character_Mode_Enabled= ''
debugMode = False

def reload_config():
    global modelName
    global Vocab_SrcField
    global Meaning_SrcField
    global Output_SrcField
    global OVERWRITE_DST_FIELD
    global Fuzzy_Character_Mode_Enabled
    global debugMode

    config = mw.addonManager.getConfig(__name__)
    modelName = config['01_modelName']
    Vocab_SrcField = config['02_Vocab_SrcField']
    Meaning_SrcField = config['03_Meaning_SrcField']
    Output_SrcField = config['04_Output_SrcField']
    OVERWRITE_DST_FIELD= config['05_OVERWRITE_DST_FIELD']
    Fuzzy_Character_Mode_Enabled= config['06_Fuzzy_Character_Mode_Enabled']
    debugMode = config['07_debugMode']


def get_singleChar_da_hada_Patterns(inputStr):
    # Example , input is '가'
    # Output is  ['가', '가다', '가하다']
    # Example , input is '내다'
    # Output is  ['내','내다', '내하다']
    # Example , input is '지내다'
    # Output is  ['지', '지다', '지하다','내','내다', '내하다']
    result = []
    for x in inputStr:
        if (x not in '하가다한시'):
            if (x not in '이오국기' and len(inputStr)<3):
                #don't want something like '?이' for long word. ?이 not helpful 
                result.extend([x,x+'다',x+'하다'])
                result.extend([x+'[!다]','?'+x])
            
    return result
    
def get_wildcard_Patterns(inputStr):
    # Example , input is '가'
    # Output is  ['']
    # Example , input is '내다' (&&NOT 하다)
    # Output is  ['*내다*']
    # Example , input is '지내다' (&&NOT 하다)
    # Output is  ['지*다', '*내다', '지내*']
    result = []
    if (len(inputStr) ==2 and inputStr[0] !='하'):
        result.append('*'+inputStr+'*')
    elif (len(inputStr) >=3):
        result.extend([inputStr,inputStr[0]+'*'+inputStr[-1],inputStr[0:2]+'*','*'+inputStr[-2:]])
    
    # remove duplicate done at other stage
    return result

def get_Search_List_Patterns(inputStr):
    # Example , input is '가'
    # Output is  ['가', '카', '까']

    fuzzyJungseongDicts = {'ㅏ': ['ㅏ', 'ㅑ', 'ㅘ'],
                           'ㅑ': ['ㅏ', 'ㅑ', 'ㅘ'],
                           'ㅘ': ['ㅏ', 'ㅑ', 'ㅘ'],
                           'ㅓ': ['ㅓ', 'ㅕ', 'ㅝ', 'ㅗ'],
                           'ㅕ': ['ㅓ', 'ㅕ', 'ㅝ'],
                           'ㅝ': ['ㅓ', 'ㅕ', 'ㅝ'],
                           'ㅗ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ','ㅓ'],
                           'ㅛ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ'],
                           'ㅜ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ'],
                           'ㅠ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ'],
                           'ㅔ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅐ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅖ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅒ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅞ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅙ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅚ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅣ': ['ㅣ', 'ㅟ'],
                           'ㅟ': ['ㅣ', 'ㅟ']}


    result = []

    # Test input validity
    if len(inputStr) == 1:
        if is_syllable(inputStr):
            jamo = decompose_syllable(inputStr)
            # if exist in dict
            if fuzzyJungseongDicts.get(jamo[1]):
                for a in fuzzyJungseongDicts.get(jamo[1]):
                    result.append(compose_jamo_characters(jamo[0], a, jamo[2]))

    if result == []:
        print("result is null")
        result.append(inputStr)
    return result
    
    

def get_fuzzyJungseongList(inputStr):
    # Example , input is '가'
    # Output is  ['가', '카', '까']

    fuzzyJungseongDicts = {'ㅏ': ['ㅏ', 'ㅑ', 'ㅘ'],
                           'ㅑ': ['ㅏ', 'ㅑ', 'ㅘ'],
                           'ㅘ': ['ㅏ', 'ㅑ', 'ㅘ'],
                           'ㅓ': ['ㅓ', 'ㅕ', 'ㅝ', 'ㅗ'],
                           'ㅕ': ['ㅓ', 'ㅕ', 'ㅝ'],
                           'ㅝ': ['ㅓ', 'ㅕ', 'ㅝ'],
                           'ㅗ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ','ㅓ'],
                           'ㅛ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ'],
                           'ㅜ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ'],
                           'ㅠ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ'],
                           'ㅔ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅐ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅖ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅒ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅞ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅙ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅚ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ', 'ㅚ'],
                           'ㅣ': ['ㅣ', 'ㅟ'],
                           'ㅟ': ['ㅣ', 'ㅟ']}


    result = []

    # Test input validity
    if len(inputStr) == 1:
        if is_syllable(inputStr):
            jamo = decompose_syllable(inputStr)
            # if exist in dict
            if fuzzyJungseongDicts.get(jamo[1]):
                for a in fuzzyJungseongDicts.get(jamo[1]):
                    result.append(compose_jamo_characters(jamo[0], a, jamo[2]))

    if result == []:
        print("result is null")
        result.append(inputStr)
    return result

def get_fuzzyChoseongList(inputStr):
    # Example , input is '가'
    # Output is  ['가', '카', '까']

    fuzzyChoseongDicts = {'ㄱ': ['ㄱ', 'ㅋ', 'ㄲ'],
                          'ㅋ': ['ㄱ', 'ㅋ', 'ㄲ'],
                          'ㄲ': ['ㄱ', 'ㅋ', 'ㄲ'],
                          'ㄷ': ['ㄷ', 'ㅌ', 'ㄸ'],
                          'ㅌ': ['ㄷ', 'ㅌ', 'ㄸ'],
                          'ㄸ': ['ㄷ', 'ㅌ', 'ㄸ'],
                          'ㅂ': ['ㅂ', 'ㅍ', 'ㅃ'],
                          'ㅍ': ['ㅂ', 'ㅍ', 'ㅃ'],
                          'ㅃ': ['ㅂ', 'ㅍ', 'ㅃ'],
                          'ㅅ': ['ㅅ', 'ㅈ','ㅊ', 'ㅆ', 'ㅉ'], 
                          'ㅈ': ['ㅅ', 'ㅈ','ㅊ', 'ㅆ', 'ㅉ'], 
                          'ㅊ': ['ㅅ', 'ㅈ','ㅊ', 'ㅆ', 'ㅉ'], 
                          'ㅆ': ['ㅅ', 'ㅈ','ㅊ', 'ㅆ', 'ㅉ'], 
                          'ㅉ': ['ㅅ', 'ㅈ','ㅊ', 'ㅆ', 'ㅉ'], 
                          'ㅇ': ['ㅇ', 'ㅎ'],
                          'ㅎ': ['ㅇ', 'ㅎ']}

    result = []

    # Test input validity
    if len(inputStr) == 1:
        if is_syllable(inputStr):
            jamo = decompose_syllable(inputStr)
            # if exist in dict
            if fuzzyChoseongDicts.get(jamo[0]):
                for a in fuzzyChoseongDicts.get(jamo[0]):
                    result.append(compose_jamo_characters(a, jamo[1], jamo[2]))

    if result == []:
        print("result is null")
        result.append(inputStr)
    return result

    
def bold_HTML(input):
    return '<b>'+input+'</b>'
    

def Optional_Generate_AllHanzi_Homophone_List_As_HTML(Master_HomoPhone_Dicts):
    showInfo ("Optional_Generate_AllHanzi_Homophone_List_As_HTML")
    HtmlOutput = ''
    for mKey in Master_HomoPhone_Dicts:
        HtmlOutput = HtmlOutput + mKey + ' : '
        for mVal in Master_HomoPhone_Dicts[mKey]:
            HtmlOutput = HtmlOutput + mVal
        HtmlOutput = HtmlOutput + '<br />'
    #for XY in get_all_chinese_tone('chìfanX'):
    #    TextOutput = TextOutput + XY + ", "
    #showInfo(TextOutput)
    #Debug_Quick_Save_info_to_Note(nids,TextOutput)
    return HtmlOutput
def BulkGenerateSimilarHanguelWordList(nids):
    mw.checkpoint("Bulk-Generate TotalWordCount")
    mw.progress.start()
    reload_config()
    warning_counter = 0
    warning_ModelNotFound = 0
    warning_Vocab_SrcField_NotFound = 0
    warning_Meaning_SrcField_NotFound = 0
    warning_Output_SrcField_NotFound = 0
    Master_HomoPhone_Dicts = {'first':'string value'}
    Pattern_Cache_Dicts = {'first':'string value'} #fnmatch with wild cards can be costly, so we cache the searched pattern results to optimise time


    showInfo ("Beginning with the following config:\n modelName: %s \n Vocab_SrcField: %s \n Meaning_SrcField: %s \n Output_SrcField: %s \n OVERWRITE_DST_FIELD: %s \n Fuzzy_Character_Mode_Enabled: %s " %(modelName,Vocab_SrcField,Meaning_SrcField,Output_SrcField,OVERWRITE_DST_FIELD,Fuzzy_Character_Mode_Enabled ))
    
    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if modelName not in note.model()['name']:
            if warning_ModelNotFound == 0:
                  showInfo ("--> Model mismatch: %s vs %s" %( modelName, note.model()['name']))
            warning_counter += 1
            warning_ModelNotFound += 1
            continue
        src1 = None
        src_Meaning = None
        if Vocab_SrcField in note:
            src1 = Vocab_SrcField
        if not src1:
            # no src1 field

            if warning_Vocab_SrcField_NotFound == 0:
                  showInfo ("--> Field %s not found." % (Vocab_SrcField))
            warning_counter += 1
            warning_Vocab_SrcField_NotFound += 1
            continue
        if Meaning_SrcField in note:
            src_Meaning = Meaning_SrcField
        if not src_Meaning:
            # no src_Meaning field
            if warning_Meaning_SrcField_NotFound == 0:
                  showInfo ("--> Field %s not found." % (Meaning_SrcField))
            warning_counter += 1
            warning_Meaning_SrcField_NotFound += 1
            continue
        dst = None
        if Output_SrcField in note:
            dst = Output_SrcField
        if not dst:
            # no dst field
            if warning_Output_SrcField_NotFound == 0:
                  showInfo ("--> Field %s not found." % (Output_SrcField))
            warning_counter += 1
            warning_Output_SrcField_NotFound += 1
            continue
        if note[dst] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            #showInfo ("--> %s not empty. Skipping!" % (Output_SrcField))
            continue
        try:
            
            # showInfo ("--> Everything should have worked. Trying Regex")
            if note[src1] not in Master_HomoPhone_Dicts:
                 Master_HomoPhone_Dicts[note[src1]] = [note[src_Meaning]]
            else:
                Master_HomoPhone_Dicts[note[src1]].append(note[src_Meaning])
            #showInfo (Master_HomoPhone_Dicts[note[src1]][0])
            #TextOutput = note[src1]
            #note[dst]= str(TotalWordCount)
        except Exception as e:
            raise
        note.flush()
    ##ROUND two. this one assign compiled list to appropriate notes.
    showInfo ("--> Now on final part. Binding final output to dst !")
    debugcount = 0
    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        debugcount += 1
        note = mw.col.getNote(nid)
        if modelName not in note.model()['name']:
            #showInfo ("--> Model mismatch: %s vs %s" %( modelName, note.model()['name']))
            continue
        src1 = None
        src_Meaning = None
        if Vocab_SrcField in note:
            src1 = Vocab_SrcField
        if not src1:
            # no src1 field
            #showInfo ("--> Field %s not found." % (Vocab_SrcField))
            continue
        if Meaning_SrcField in note:
            src_Meaning = Meaning_SrcField
        if not src_Meaning:
            # no src_Meaning field
            #showInfo ("--> Field %s not found." % (Meaning_SrcField))
            continue
        dst = None
        if Output_SrcField in note:
            dst = Output_SrcField
        if not dst:
            #showInfo ("--> Field %s not found!" % (Output_SrcField))
            # no dst field
            continue
        if note[dst] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            #showInfo ("--> %s not empty. Skipping!" % (Vocab_SrcField))
            continue
        try:
            #dct = {'this':1,'is':2,'just':3,'tazvikst':4,'test':5,'tzxct':6,'test':7}
            #filtered = fnmatch.filter(dct, 't*t')
            # (result =)filtered => ['tazvikst', 'test', 'tzxct']
            if (Fuzzy_Character_Mode_Enabled == False):
                cur_TextOutput = ''
                mAllToneInput_List = get_singleChar_da_hada_Patterns(note[src1])
                mAllToneInput_List.extend(get_wildcard_Patterns(note[src1])) #extend list
                #mAllToneInput_List = list(set(mAllToneInput_List)) #remove duplicate. Obsolete, doesn't preserve order
                mAllToneInput_List = list(dict.fromkeys(mAllToneInput_List)) #remove duplicate
                if(debugMode and debugcount<=5):
                    showInfo ("generated pattern list :" + str(mAllToneInput_List))
                
                for cur_Tone in mAllToneInput_List:
                     if cur_Tone in Pattern_Cache_Dicts:#pattern previously searched,i.e  "*먹다*", use cache instead of fnmatch.filter(Dict) which is cpu intensive
                        filteredLst = Pattern_Cache_Dicts.get(cur_Tone)
                     else:
                        filteredLst = fnmatch.filter(Master_HomoPhone_Dicts, cur_Tone)
                        Pattern_Cache_Dicts[cur_Tone] = filteredLst #add result to cache dict for later use
                        
                     if (len(filteredLst)>0 and len(filteredLst)<40 ):
                         #Skips null result . e.g skips 먹하다 (match nothing) , also if len exceed 40 it's too common, don't want
                         cur_TextOutput = cur_TextOutput + bold_HTML('&emsp;' +cur_Tone + ' ('+str(len(filteredLst))+')<br />')+  '<ol>' #i.e  *먹다* (4)
                         #only the first 7 is taken
                         for filtered in filteredLst[:7]:
                            x = Master_HomoPhone_Dicts[filtered][0] #need the [0] because dict result is stored in list e.g. ['to suffer a big loss, be cheated']. this will convert it to string 
                            #filtered == Hanguelword, x = Meaning
                            x = x.replace("<div>","").replace("</div>","")  #won't work with  e.g. <div style="background-color:lightblue"> . this sufficient enough for me. will regex later
                            cur_TextOutput = cur_TextOutput + '<li>'+ filtered + ": "+str(x)+"</li>"
                         cur_TextOutput += '</ol>'
                     
                note[dst]= cur_TextOutput
                #showInfo (Master_HomoPhone_Dicts[note[src1]][0])
                #TextOutput = note[src1]
                #note[dst]= str(TotalWordCount)
            else:
                cur_TextOutput = ''
                mFuzz_List = get_fuzzyJungseongList(note[src1])
                for cur_Fuzz in mFuzz_List:
                    mAllToneInput_List = get_fuzzyChoseongList(cur_Fuzz)
                    for cur_Tone in mAllToneInput_List:
                         cur_TextOutput = cur_TextOutput + cur_Tone + ' : '
                         if cur_Tone in Master_HomoPhone_Dicts:
                               #showInfo("value of Master_HomoPhone_Dicts[cur_Tone] is : %s, length is : %d"  % (str(Master_HomoPhone_Dicts[cur_Tone]),len(Master_HomoPhone_Dicts[cur_Tone]))) 
                               for cur_Val in Master_HomoPhone_Dicts[cur_Tone]:
                                    cur_TextOutput = cur_TextOutput + cur_Val
                                    
                         cur_TextOutput = cur_TextOutput + '<br />'
                         #else:
                               # if hanja list is blank e.g. 춍 : 쑝 : 쭁 :  then no need to break <br /> to save space
                               #cur_TextOutput = cur_TextOutput
                    if cur_Fuzz != mFuzz_List[-1]:
                        cur_TextOutput = cur_TextOutput + '<br />'
                note[dst]= cur_TextOutput
        except Exception as e:
            raise
        note.flush()

    showInfo ("--> Everything should have worked.\n warning_counter = %d \n warning_ModelNotFound = %d \n warning_Vocab_SrcField_NotFound = %d \n warning_Meaning_SrcField_NotFound = %d \n warning_Output_SrcField_NotFound = %d" %(warning_counter,warning_ModelNotFound,warning_Vocab_SrcField_NotFound,warning_Meaning_SrcField_NotFound,warning_Output_SrcField_NotFound))
    #showInfo (TextOutput)
    mw.progress.finish()
    mw.reset()


def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Bulk-Generate Similar Hanguel Word List')
    a.triggered.connect(lambda _, b=browser: onBulkGenerateSimilarHanguelWordList(b))


def onBulkGenerateSimilarHanguelWordList(browser):
    BulkGenerateSimilarHanguelWordList(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
