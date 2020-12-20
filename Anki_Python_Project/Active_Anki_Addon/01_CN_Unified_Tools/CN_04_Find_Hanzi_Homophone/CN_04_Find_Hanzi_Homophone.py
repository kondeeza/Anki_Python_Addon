# -*- coding: utf-8 -*-
# Copyright: mo  <paradoxez919@gmail.com>
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

import pathlib

import os
"""
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')"""
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE
import sys
#reload(sys) #apparently this doesn't work in python3... 
#sys.setdefaultencoding('utf-8')
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE !!


modelName = ''
Pinyin_SrcField = ''
Hanzi_SrcField = ''
Output_SrcField = ''
OVERWRITE_DST_FIELD= ''
Fuzzy_Character_Mode_Enabled= ''
query_ALLMode = ''
query_CurrentMode = ''

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()
def reload_config(fieldmode):
    global modelName
    global Pinyin_SrcField
    global Hanzi_SrcField
    global Output_SrcField
    global OVERWRITE_DST_FIELD
    global Fuzzy_Character_Mode_Enabled
    global query_ALLMode
    global query_CurrentMode

    config = mw.addonManager.getConfig(__name__)
    modelName = config['04_01_modelName']
    Pinyin_SrcField = config['04_02_Pinyin_SrcField']
    Hanzi_SrcField = config['04_03_Hanzi_SrcField']
    OVERWRITE_DST_FIELD= config['04_05_OVERWRITE_DST_FIELD']
    
    if (fieldmode == "all"):
        Output_SrcField = config['04_04_Output_SrcField_ALLMode']
        Fuzzy_Character_Mode_Enabled= config['04_06_Fuzzy_Character_Mode_Enabled_ALLMode']
    else:
        Output_SrcField = config['04_04P2_Output_SrcField_CurrentMode']
        Fuzzy_Character_Mode_Enabled= config['04_06P2_Fuzzy_Character_Mode_Enabled_CurrentMode']
    query_ALLMode = config['04_07P1_query_ALLMode']
    query_CurrentMode = config['04_07P2_queryMode_CurrentMode']

def findNotes( query=None):
    if query is None:
        return []
    else:
        return list(map(int, mw.col.findNotes(query)))

def get_all_chinese_fuzzy_character(inputStr):
    fuzzyDicts = {'x':['x','q'],
    'sh':['sh','ch'],
    's':['s','c','z'],
    'j':['j','zh'],
    'l':['l','r'],
    'b':['b','p'],
    'd':['d','t'],
    'q':['x','q'],
    'ch':['sh','ch'],
    'z':['s','c'],
    'c':['s','c','z'],
    'zh':['j','zh'],
    'r':['l','r'],
    'p':['b','p'],
    't':['d','t'],
    'z':['s','c','z']}

    result = []
    twoCharactersDetected = False
    for i in fuzzyDicts:
        if len(i) == 2:
            if inputStr.startswith(i):
                twoCharactersDetected = True
                for x in fuzzyDicts[i]:
                    result.append(inputStr.replace(i,x))
                    
                
    if twoCharactersDetected == False:
        for i in fuzzyDicts:
            if inputStr.startswith(i):
                
                for x in fuzzyDicts[i]:
                    result.append(inputStr.replace(i,x))
                    
                
    if result == []:
        print("result is null")
        result.append(inputStr)
    print(twoCharactersDetected)
    return result

def get_all_chinese_tone(inputStr):
    ToneDicts = {'ā':['ā','á','ǎ','à'],
    'á':['ā','á','ǎ','à'],
    'ǎ':['ā','á','ǎ','à'],
    'à':['ā','á','ǎ','à'],
    'ō':['ō','ó','ǒ','ò'],
    'ó':['ō','ó','ǒ','ò'],
    'ǒ':['ō','ó','ǒ','ò'],
    'ò':['ō','ó','ǒ','ò'],
    'ē':['ē','é','ě','è'],
    'é':['ē','é','ě','è'],
    'ě':['ē','é','ě','è'],
    'è':['ē','é','ě','è'],
    'ī':['ī','í','ǐ','ì'],
    'í':['ī','í','ǐ','ì'],
    'ǐ':['ī','í','ǐ','ì'],
    'ì':['ī','í','ǐ','ì'],
    'ū':['ū','ú','ǔ','ù'],
    'ú':['ū','ú','ǔ','ù'],
    'ǔ':['ū','ú','ǔ','ù'],
    'ù':['ū','ú','ǔ','ù'],
    'ü':['ü','ǘ','ǚ','ǜ'],
    'ǘ':['ü','ǘ','ǚ','ǜ'],
    'ǚ':['ü','ǘ','ǚ','ǜ'],
    'ǜ':['ü','ǘ','ǚ','ǜ']}

    result = []
    for i in ToneDicts:
        if i in inputStr:
            for x in ToneDicts[i]:
                result.append(inputStr.replace(i,x))
                
            
    if result == []:
        print("result is null")
        result.append(inputStr)
    return result

    


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
def BulkGenerateHanziHomophoneList(nids,fieldmode):
    #showInfo(__name__)
    #return
    mw.checkpoint("Bulk-Generate TotalWordCount")
    reload_config(fieldmode)
    warning_counter = 0
    warning_ModelNotFound = 0
    warning_Pinyin_SrcField_NotFound = 0
    warning_Hanzi_SrcField_NotFound = 0
    warning_Output_SrcField_NotFound = 0
    Master_HomoPhone_Dicts = {'first':'string value'}

    showInfo ("Beginning with the following config:\n modelName: %s \n Pinyin_SrcField: %s \n Hanzi_SrcField: %s \n Output_SrcField: %s \n OVERWRITE_DST_FIELD: %s \n Fuzzy_Character_Mode_Enabled: %s " %(modelName,Pinyin_SrcField,Hanzi_SrcField,Output_SrcField,OVERWRITE_DST_FIELD,Fuzzy_Character_Mode_Enabled ))
    
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
        src_Hanzi = None
        if Pinyin_SrcField in note:
            src1 = Pinyin_SrcField
        if not src1:
            # no src1 field

            if warning_Pinyin_SrcField_NotFound == 1:
                  showInfo ("--> Field %s not found." % (Pinyin_SrcField))
            warning_counter += 1
            warning_Pinyin_SrcField_NotFound += 1
            continue
        if Hanzi_SrcField in note:
            src_Hanzi = Hanzi_SrcField
        if not src_Hanzi:
            # no src_Hanzi field
            if warning_Hanzi_SrcField_NotFound == 1:
                  showInfo ("--> Field %s not found." % (Hanzi_SrcField))
            warning_counter += 1
            warning_Hanzi_SrcField_NotFound += 1
            continue
        dst = None
        if Output_SrcField in note:
            dst = Output_SrcField
        if not dst:
            # no dst field
            if warning_Output_SrcField_NotFound == 1:
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
                 Master_HomoPhone_Dicts[note[src1]] = [note[src_Hanzi]]
            else:                 Master_HomoPhone_Dicts[note[src1]].append(note[src_Hanzi])

            #showInfo (Master_HomoPhone_Dicts[note[src1]][0])
            #TextOutput = note[src1]
            #note[dst]= str(TotalWordCount)
        except Exception as e:
            raise
        note.flush()
    ##ROUND two. this one assign compiled list to appropriate notes.
    showInfo ("--> Now on final part. Binding final output to dst !")
    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if modelName not in note.model()['name']:
            #showInfo ("--> Model mismatch: %s vs %s" %( modelName, note.model()['name']))
            continue
        src1 = None
        src_Hanzi = None
        if Pinyin_SrcField in note:
            src1 = Pinyin_SrcField
        if not src1:
            # no src1 field
            #showInfo ("--> Field %s not found." % (Pinyin_SrcField))
            continue
        if Hanzi_SrcField in note:
            src_Hanzi = Hanzi_SrcField
        if not src_Hanzi:
            # no src_Hanzi field
            #showInfo ("--> Field %s not found." % (Hanzi_SrcField))
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
            #showInfo ("--> %s not empty. Skipping!" % (Pinyin_SrcField))
            continue
        try:
            if Fuzzy_Character_Mode_Enabled == False:
                cur_TextOutput = ''
                mAllToneInput_List = get_all_chinese_tone(note[src1])
                for cur_Tone in mAllToneInput_List:
                     cur_TextOutput = cur_TextOutput + cur_Tone + ' : '
                     if cur_Tone in Master_HomoPhone_Dicts:
                           for cur_Val in Master_HomoPhone_Dicts[cur_Tone]:
                                cur_TextOutput = cur_TextOutput + cur_Val
                     cur_TextOutput = cur_TextOutput + '<br />'
                note[dst]= cur_TextOutput
                #showInfo (Master_HomoPhone_Dicts[note[src1]][0])
                #TextOutput = note[src1]
                #note[dst]= str(TotalWordCount)
            else:
                cur_TextOutput = ''
                mFuzz_List = get_all_chinese_fuzzy_character(note[src1])
                for cur_Fuzz in mFuzz_List:
                    mAllToneInput_List = get_all_chinese_tone(cur_Fuzz)
                    for cur_Tone in mAllToneInput_List:
                         cur_TextOutput = cur_TextOutput + cur_Tone + ' : '
                         if cur_Tone in Master_HomoPhone_Dicts:
                               for cur_Val in Master_HomoPhone_Dicts[cur_Tone]:
                                    cur_TextOutput = cur_TextOutput + cur_Val
                         cur_TextOutput = cur_TextOutput + '<br />'
                    if cur_Fuzz != mFuzz_List[-1]:
                        cur_TextOutput = cur_TextOutput + '<br />'
                note[dst]= cur_TextOutput
        except Exception as e:
            raise
        note.flush()

    showInfo ("--> Everything should have worked.\n warning_counter = %d \n warning_ModelNotFound = %d \n warning_Pinyin_SrcField_NotFound = %d \n warning_Hanzi_SrcField_NotFound = %d \n warning_Output_SrcField_NotFound = %d" %(warning_counter,warning_ModelNotFound,warning_Pinyin_SrcField_NotFound,warning_Hanzi_SrcField_NotFound,warning_Output_SrcField_NotFound))
    #showInfo (TextOutput)
    mw.progress.finish()
    mw.reset()


def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    c = menu.addAction('CN_04_Find_Hanzi_Homophone(Current)')
    c.triggered.connect(lambda _, b=browser: onBulkGenerateHanziHomophoneList(b,"current"))
    a = menu.addAction('CN_04_Find_Hanzi_Homophone(All)')
    a.triggered.connect(lambda _, b=browser: onBulkGenerateHanziHomophoneList(b,"all"))
    q = menu.addAction('CN_04_Find_Hanzi_Homophone(QUERY)')
    q.triggered.connect(lambda _, b=browser: onBulkGenerateHanziHomophoneList(b,"QUERY"))

def onBulkGenerateHanziHomophoneList(browser,fieldmode):
    reload_config(fieldmode)
    logger = open(SCRIPT_DIR / 'CN_04_Log.txt', 'w', encoding="utf-8")
    logger.write("os.getcwd():  " + os.getcwd()+ "\n")
    logger.write("sys.path:  " + str(sys.path)+ "\n")
    logger.write("__name__:  " + str(__name__)+ "\n")
    logger.write("SCRIPT_DIR:  " + str(SCRIPT_DIR)+ "\n")
    logger.write('test log2\n')
    logger.write('mw.col  :' + str(mw.col) + "\n" )
    logger.write("fieldmode:  " +  fieldmode  + "\n" )
    
    if (fieldmode == 'QUERY'):
        nids_ALLMode = findNotes(query_ALLMode)
        nids_CurrentMode = findNotes(query_CurrentMode)
        logger.write("len(nids_ALLMode):  " +  str(len(nids_ALLMode))  + "\n" + "len(nids_CurrentMode):  " +  str(len(nids_CurrentMode))  + "\n")
        BulkGenerateHanziHomophoneList(nids_ALLMode,"all")
        BulkGenerateHanziHomophoneList(nids_CurrentMode,"current")
    else:
        BulkGenerateHanziHomophoneList(browser.selectedNotes(),fieldmode)
    
    logger.close()

addHook("browser.setupMenus", setupMenu)
