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
#("note:Korean Vocab" or  note:Toktogi) and -Auto_SimilarWord:
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
from aqt.utils import showWarning, showInfo, tooltip
import re
import platform
import re
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE
import sys
import fnmatch
import time
#reload(sys) #apparently this doesn't work in python3... 
#sys.setdefaultencoding('utf-8')
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE !!

# added dot for importing relative module package.
from .hangul_jamo import is_syllable, is_jamo_character, compose_jamo_characters, decompose_syllable, compose, decompose


modelName = ''
Vocab_SrcField = ''
Meaning_SrcField = ''
Pinyin_SrcField = ''
Output_SrcField = ''
OVERWRITE_DST_FIELD= ''
Fuzzy_Character_Mode_Enabled= ''
debugMode = False

def reload_config():
    global modelName
    global Vocab_SrcField
    global Meaning_SrcField
    global Pinyin_SrcField
    global Output_SrcField
    global OVERWRITE_DST_FIELD
    global Fuzzy_Character_Mode_Enabled
    global debugMode

    config = mw.addonManager.getConfig(__name__)
    modelName = config['01_modelName']
    Vocab_SrcField = config['02_Vocab_SrcField']
    Meaning_SrcField = config['03_Meaning_SrcField']
    Pinyin_SrcField = config['08_Pinyin_SrcField']
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
            if (x not in '이오국기' or len(inputStr)<3):
                #don't want something like '?이' for long word. ?이 not helpful 
                result.extend([x,x+'다',x+'하다'])
                result.extend([x+'[!다]','?'+x])
                result.append('*'+x+'*')
            
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
        result.append(inputStr[0]+'*'+inputStr[1])
    elif (len(inputStr) >=3):
        result.extend([inputStr,inputStr[0]+'*'+inputStr[-1],inputStr[0:2]+'*','*'+inputStr[-2:]])
    
    # remove duplicate done at other stage
    return result


def hasComposite_jongseong(input):
    Composite_jamo_Dicts = {'ㄲ':  ['ㄱ', 'ㄲ', 'ㄳ'],
                  'ㄳ': ['ㄱ', 'ㄲ', 'ㄳ'],
                  'ㄵ': ['ㄴ', 'ㄵ', 'ㄶ'],
                  'ㄶ': ['ㄴ', 'ㄵ', 'ㄶ'],
                  'ㄺ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄻ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄼ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄽ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄾ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄿ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㅀ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㅄ': ['ㅂ', 'ㅄ'],
                  'ㅆ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
                  'ㅍ': ['ㅍ', 'ㅌ', 'ㅋ'],
                  'ㅌ': ['ㅍ', 'ㅌ', 'ㅋ'],
                  'ㅋ': ['ㅍ', 'ㅌ', 'ㅋ']}
    #  ['ㅍ', 'ㅌ', 'ㅋ'] not composite but i want to keep tracl of them
    result = False
    if len(input) == 1:
        if is_syllable(input):
            if decompose_syllable(input)[2] in Composite_jamo_Dicts:
                result = decompose_syllable(input)[2]
    return result

def get_fuzzyJongseongList(inputStr):
    # Example , input is '가'
    # Output is  ['가', '카', '까']

    fuzzyJongseongDicts = {'ㄱ': ['ㄱ', 'ㄲ', 'ㄳ'],
                  'ㄲ':  ['ㄱ', 'ㄲ', 'ㄳ'],
                  'ㄳ':  ['ㄱ', 'ㄲ', 'ㄳ'],
                  'ㄴ': ['ㄴ', 'ㄵ', 'ㄶ'],
                  'ㄵ': ['ㄴ', 'ㄵ', 'ㄶ'],
                  'ㄶ': ['ㄴ', 'ㄵ', 'ㄶ'],
                  'ㄹ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄺ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄻ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄼ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄽ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄾ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㄿ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㅀ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
                  'ㅂ': ['ㅂ', 'ㅄ'],
                  'ㅄ': ['ㅂ', 'ㅄ'],
                  'ㅅ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
                  'ㅆ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
                  'ㅈ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
                  'ㅊ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
                  'ㅋ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
                  'ㅌ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ']}



    result = []

    # Test input validity
    if len(inputStr) == 1:
        if is_syllable(inputStr):
            jamo = decompose_syllable(inputStr)
            # if exist in dict
            if fuzzyJongseongDicts.get(jamo[2]):
                for a in fuzzyJongseongDicts.get(jamo[2]):
                    result.append(compose_jamo_characters(jamo[0],jamo[1], a))

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

def get_fuzzyJamoList(inputStr):
    # Example , input is '있'
    # Output is  ['잇', '있', '잊', '잋', '잌', '잍', '윗', '윘', '윚', '윛', '윜', '윝', '힛', '힜', '힞', '힟', '힠', '힡', '휫', '휬', '휮', '휯', '휰', '휱']

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

    fuzzyJongseongDicts = {'ㄱ': ['ㄱ', 'ㄲ', 'ㄳ'],
              'ㄲ':  ['ㄱ', 'ㄲ', 'ㄳ'],
              'ㄳ':  ['ㄱ', 'ㄲ', 'ㄳ'],
              'ㄴ': ['ㄴ', 'ㄵ', 'ㄶ'],
              'ㄵ': ['ㄴ', 'ㄵ', 'ㄶ'],
              'ㄶ': ['ㄴ', 'ㄵ', 'ㄶ'],
              'ㄹ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
              'ㄺ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
              'ㄻ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
              'ㄼ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
              'ㄽ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
              'ㄾ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
              'ㄿ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
              'ㅀ': ['ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ'],
              'ㅂ': ['ㅂ', 'ㅄ'],
              'ㅄ': ['ㅂ', 'ㅄ'],
              'ㅅ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
              'ㅆ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
              'ㅈ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
              'ㅊ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
              'ㅋ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ'],
              'ㅌ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ']}

    result = []
    # Jamo example for = decompose_syllable('미') = ('ㅁ', 'ㅣ', None)
    # Test input validity
    if len(inputStr) == 1:
        if is_syllable(inputStr):
            jamo = decompose_syllable(inputStr)
            # if exist in dict
            for a in fuzzyChoseongDicts.get(jamo[0]) or jamo[0]: # Handle when not exist in Choseong Dict (e.g. '미' , since Choseong Dict has no 'ㅁ')
                for b in fuzzyJungseongDicts.get(jamo[1]) or jamo[1]:
                    # Handle Jongseongdict. Since many Jamo has no  Jongseong i.e. '미' (a.k.a. jamo[2] returns None)
                    if jamo[2]:  #if Jamo even has Jongseong ending
                        for c in fuzzyJongseongDicts.get(jamo[2]) or jamo[2]:
                            result.append(compose_jamo_characters(a, b, c))
                    else: #if No Jongseong ending
                            result.append(compose_jamo_characters(a, b))

    if result == []:
        result.append(inputStr)
    return result

def bold_HTML(input):
    return '<b>'+input+'</b>'
    

def Optional_Generate_AllHanzi_Homophone_List_As_HTML(Master_Vocab_Dicts):
    print ("Optional_Generate_AllHanzi_Homophone_List_As_HTML")
    HtmlOutput = ''
    for mKey in Master_Vocab_Dicts:
        HtmlOutput = HtmlOutput + mKey + ' : '
        for mVal in Master_Vocab_Dicts[mKey]:
            HtmlOutput = HtmlOutput + mVal
        HtmlOutput = HtmlOutput + '<br />'
    #for XY in get_all_chinese_tone('chìfanX'):
    #    TextOutput = TextOutput + XY + ", "
    #print(TextOutput)
    #Debug_Quick_Save_info_to_Note(nids,TextOutput)
    return HtmlOutput
def BulkGenerateSimilarHanziVocabList(nids):
    mw.checkpoint("Bulk-Generate TotalWordCount")
    reload_config()
    warning_counter = 0
    warning_ModelNotFound = 0
    warning_Vocab_SrcField_NotFound = 0
    warning_Meaning_SrcField_NotFound = 0
    warning_Pinyin_SrcField_NotFound = 0
    warning_Output_SrcField_NotFound = 0
    Master_Vocab_Dicts = {'first':'string value'}
    Master_CompositeJongseong_Dicts = {'first':'string value'}
    Pattern_Cache_Dicts = {'first':'string value'} #fnmatch with wild cards can be costly, so we cache the searched pattern results to optimise time
    #before using Cache takes around 3 minutes for 5200 cards. now around 1minutes10secs
    ran_fnmatchregex_count = 0
    fnmatchregex_time = 0
    filteredCache_used_count = 0
    warning_Output_SrcField_NotFound = 0
    notincache_but_already_inmasterdict_count = 0
    
    HanziFreqList = []
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, "HanziFrequencyList.txt"), "r", encoding="utf-8") as f:
        HanziFreqList = [line.split('\t') for line in f]
    info_Slave_Hanzi_not_in_Hanzi_Frequency_List = 0
    HanziOfHanziFreqList = [hanzi[1] for hanzi in HanziFreqList]
    HanziOfHanziFreqList += [hanzi[2] for hanzi in HanziFreqList]

    print ("Beginning with the following config:\n modelName: %s \n Vocab_SrcField: %s \n Meaning_SrcField: %s \n Output_SrcField: %s \n OVERWRITE_DST_FIELD: %s \n Fuzzy_Character_Mode_Enabled: %s " %(str(modelName),Vocab_SrcField,Meaning_SrcField,Output_SrcField,OVERWRITE_DST_FIELD,Fuzzy_Character_Mode_Enabled ))

    for nid in nids:
        #print ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if isinstance(modelName, str):
            if modelName not in note.model()['name']:
                if warning_ModelNotFound == 0:
                      print ("--> Model mismatch Str type: %s not in  %s" %( modelName, note.model()['name']))
                warning_counter += 1
                warning_ModelNotFound += 1
                continue
        elif isinstance(modelName, list):
            if not set(modelName).isdisjoint(note.model()['name']):
                if warning_ModelNotFound == 0:
                      print ("--> Model mismatch List type: %s not in %s" %( str(modelName), note.model()['name']))
                warning_counter += 1
                warning_ModelNotFound += 1
                continue

        src1 = None
        src_Meaning = None
        src_Pinyin = None
        if Vocab_SrcField in note:
            src1 = Vocab_SrcField
        if not src1:
            # no src1 field

            if warning_Vocab_SrcField_NotFound == 0:
                  print ("--> Field %s not found." % (Vocab_SrcField))
            warning_counter += 1
            warning_Vocab_SrcField_NotFound += 1
            continue
        if Pinyin_SrcField in note:
            src_Pinyin = Pinyin_SrcField
        if not src_Pinyin:
            # no src_Pinyin field
            warning_Pinyin_SrcField_NotFound += 1
            continue
        if Meaning_SrcField in note:
            src_Meaning = Meaning_SrcField
        if not src_Meaning:
            # no src_Meaning field
            if warning_Meaning_SrcField_NotFound == 0:
                  print ("--> Field %s not found." % (Meaning_SrcField))
            warning_counter += 1
            warning_Meaning_SrcField_NotFound += 1
            continue
        dst = None
        if Output_SrcField in note:
            dst = Output_SrcField
        if not dst:
            # no dst field
            if warning_Output_SrcField_NotFound == 0:
                  print ("--> Field %s not found." % (Output_SrcField))
            warning_counter += 1
            warning_Output_SrcField_NotFound += 1
            continue
        if note[dst] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            #print ("--> %s not empty. Skipping!" % (Output_SrcField))
            continue
        try:
            for x in note[src1]:
                if x in HanziOfHanziFreqList:
                    if x not in Master_Vocab_Dicts:
                        Master_Vocab_Dicts[x] = [[note[src1], note[src_Pinyin], note[src_Meaning]]]
                    else:
                        Master_Vocab_Dicts[x].append([note[src1], note[src_Pinyin], note[src_Meaning]])
                else:
                    info_Slave_Hanzi_not_in_Hanzi_Frequency_List += 1
            # print ("--> Everything should have worked. Trying Regex")

            #Test Composite Jongseong Dict
            """
            tempCompositeList = []
            if len(note[src1]) <=3 and len(note[src1]) >0:
                for ch in note[src1]:
                    t = hasComposite_jongseong(ch)
                    if t and not(t in tempCompositeList):
                        tempCompositeList.append(t)
            for tempComposite in tempCompositeList:
                if tempComposite not in Master_CompositeJongseong_Dicts:
                     Master_CompositeJongseong_Dicts[tempComposite] = [note[src1] + ": " + note[src_Meaning]]
                else:
                    Master_CompositeJongseong_Dicts[tempComposite].append(note[src1] + ": " + note[src_Meaning])
            """
            #END Test Composite Jongseong Dict
            #print (Master_Vocab_Dicts[note[src1]][0])
            #TextOutput = note[src1]
            #note[dst]= str(TotalWordCount)
        except Exception as e:
            raise
        note.flush()
    ##ROUND two. this one assign compiled list to appropriate notes.
    print ("--> Now on final part. Binding final output to dst !")
    mw.progress.start()
    debugcount = 0
    refreshGuiTimer = time.perf_counter()
    totalRunTime = time.perf_counter()
    maxloop = max(len(nids),1)
    for  loopno, nid in enumerate(nids):
        #print ("Found note: %s" % (nid))
        #print(str((currentloop/maxLoop)*100 %2))
        #if ((currentloop/maxLoop)*100 %2 ==0): THIS WON'T WORK, sometimes result is 2.000000000245 and that's not valid

        if ( time.perf_counter() - refreshGuiTimer >= 2.5):
            refreshGuiTimer = time.perf_counter()
            #update timer every 2.5 seconds
            #update every 2.5 percent
            #updateProgressDialog(widget,(currentloop/maxLoop)*100)
            tooltip("Progress : %d %%" % ( (loopno/maxloop)*100),    period=300    )
            # refresh GUI during loop
            time.sleep(0.1)
            #print('hi')
            mw.app.processEvents()


        debugcount += 1
        note = mw.col.getNote(nid)
        if isinstance(modelName, str):
            if modelName not in note.model()['name']:
                if warning_ModelNotFound == 0:
                      print ("--> Model mismatch: %s vs %s" %( modelName, note.model()['name']))
                warning_counter += 1
                warning_ModelNotFound += 1
                continue
        elif isinstance(modelName, list):
            if not set(modelName).isdisjoint(note.model()['name']):
                if warning_ModelNotFound == 0:
                      print ("--> Model mismatch: %s vs %s" %( str(modelName), note.model()['name']))
                warning_counter += 1
                warning_ModelNotFound += 1
                continue
        src1 = None
        if Pinyin_SrcField in note:
            src_Pinyin = Pinyin_SrcField
        if not src_Pinyin:
            # no src_Pinyin field
            warning_Pinyin_SrcField_NotFound += 1
            continue
        src_Meaning = None
        if Vocab_SrcField in note:
            src1 = Vocab_SrcField
        if not src1:
            # no src1 field
            #print ("--> Field %s not found." % (Vocab_SrcField))
            continue
        if Meaning_SrcField in note:
            src_Meaning = Meaning_SrcField
        if not src_Meaning:
            # no src_Meaning field
            #print ("--> Field %s not found." % (Meaning_SrcField))
            continue
        dst = None
        if Output_SrcField in note:
            dst = Output_SrcField
        if not dst:
            #print ("--> Field %s not found!" % (Output_SrcField))
            # no dst field
            continue
        if note[dst] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            #print ("--> %s not empty. Skipping!" % (Vocab_SrcField))
            continue
        try:
            #dct = {'this':1,'is':2,'just':3,'tazvikst':4,'test':5,'tzxct':6,'test':7}
            #filtered = fnmatch.filter(dct, 't*t')
            # (result =)filtered => ['tazvikst', 'test', 'tzxct']
            #  a = Master_Vocab_Dicts.get(note[master_Hanzi_SrcField])
            
            cur_TextOutput = ''
            
            for cur_Char in note[src1]:
                if cur_Char in HanziOfHanziFreqList:
                    if (cur_Char in Master_Vocab_Dicts):
                        pass
                    filteredLst = Master_Vocab_Dicts.get(cur_Char)
                    if (len(filteredLst)>0 and len(filteredLst)<40 ):
                         #Skips null result . e.g skips 먹하다 (match nothing) , also if len exceed 40 it's too common, don't want
                         cur_TextOutput = cur_TextOutput + bold_HTML('&emsp;*' +cur_Char + '* ('+str(len(filteredLst))+')<br />')+  '<ol>' #i.e  *먹다* (4)
                         #only the first 7 is taken
                         for filtered in filteredLst[:20]:
                            #filtered[0] == HanziVocab, filtered[1] = Pinyin
                            HanziVocab = filtered[0].replace("<div>","").replace("</div>","")
                            Pinyin = filtered[1].replace("<div>","").replace("</div>","")  #won't work with  e.g. <div style="background-color:lightblue"> . this sufficient enough for me. will regex later
                            Meaning = filtered[2].replace("<div>","").replace("</div>","")
                            cur_TextOutput = cur_TextOutput + "<li>"+ HanziVocab + ": "+Pinyin+": "+Meaning[:15]+"</li>" # max meaning 15 char
                         cur_TextOutput += '</ol>'
                else:
                    pass
                


            #Now to deal with composite JongSeongDict

            tempCompositeList = []
            if len(note[src1]) <=3 and len(note[src1]) >0:
                for ch in note[src1]:
                    t = hasComposite_jongseong(ch)
                    if t and not(t in tempCompositeList):
                        tempCompositeList.append(t)

            for tempComposite in tempCompositeList:
                #print(str(tempComposite))
                if tempComposite in Master_CompositeJongseong_Dicts:
                    #print(str(tempComposite) + str(Master_CompositeJongseong_Dicts[tempComposite]))
                    cur_TextOutput += "<br />" + bold_HTML('&emsp;' +tempComposite + '<br />') +  '<ol>'
                    for x in Master_CompositeJongseong_Dicts[tempComposite]:
                         cur_TextOutput += '<li>' + x + '</li>'
                    cur_TextOutput += '</ol>'




            if (Fuzzy_Character_Mode_Enabled == True):
                if len(note[src1]) > 0:
                    # only get first char from korean vocab . e.g. '썩'  from '썩이다'
                    mFuzz_List = get_fuzzyJamoList(note[src1][0])

                    FuzzyHeaderMade = False
                    for cur_Fuzz in mFuzz_List:
                        mAllFuzzyToneInput_List = get_singleChar_da_hada_Patterns(cur_Fuzz)
                        mAllFuzzyToneInput_List = list(dict.fromkeys(mAllFuzzyToneInput_List)) #remove duplicate

                        for x in mAllFuzzyToneInput_List:
                             if x in Master_Vocab_Dicts:
                                if not FuzzyHeaderMade:
                                    # Make header for fuzzy list The first time only.
                                    cur_TextOutput += "<br />" + bold_HTML('&emsp;' +'Fuzzy' + '<br />') +  '<ol>'
                                    FuzzyHeaderMade = True

                                #for filtered in filteredLst[:7]:
                                y = Master_Vocab_Dicts[x][0] #need the [0] because dict result is stored in list e.g. ['to suffer a big loss, be cheated']. this will convert it to string
                                y = y.replace("<div>","").replace("</div>","")  #won't work with  e.g. <div style="background-color:lightblue"> . this sufficient enough for me. will regex later
                                cur_TextOutput = cur_TextOutput + '<li>' + x + ": "+str(y)+"</li>"

                    if FuzzyHeaderMade:
                        cur_TextOutput += '</ol>'
            note[dst]= cur_TextOutput
            #print (Master_Vocab_Dicts[note[src1]][0])
            #TextOutput = note[src1]
            #note[dst]= str(TotalWordCount)
        except Exception as e:
            raise
        note.flush()
    mw.progress.finish()
    totalRunTime  = time.perf_counter() -totalRunTime
    showInfo ("--> Everything should have worked.\n warning_counter = %d \n warning_ModelNotFound = %d \n warning_Vocab_SrcField_NotFound = %d \n warning_Meaning_SrcField_NotFound = %d \n warning_Output_SrcField_NotFound = %d" %(warning_counter,warning_ModelNotFound,warning_Vocab_SrcField_NotFound,warning_Meaning_SrcField_NotFound,warning_Output_SrcField_NotFound))
    if (debugMode):
        showInfo(str(Master_Vocab_Dicts.get('将')))
        showInfo(str('将' in HanziOfHanziFreqList))
        showInfo(str(HanziOfHanziFreqList[0:10]))
        showInfo ("len(Pattern_Cache_Dicts): %d \n filteredCache_used_count: %d \n  ran_fnmatchregex_count: %d \n fnmatchregex_time: %d \n notincache_but_already_inmasterdict_count: %d \n totalRunTime: %d" %(len(Pattern_Cache_Dicts),filteredCache_used_count,ran_fnmatchregex_count,fnmatchregex_time, notincache_but_already_inmasterdict_count, totalRunTime))
    # for 5200 cards, len(Pattern_Cache_Dicts):14632,filteredCache_used_count:52027,ran_fnmatchregex_count:14631,fnmatchregex_time:71
    #print (TextOutput)
    
    mw.reset()


def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('CN Find_Hanzi_Vocabs_With_Similar_Sound')
    a.triggered.connect(lambda _, b=browser: onBulkGenerateSimilarHanziVocabList(b))


def onBulkGenerateSimilarHanziVocabList(browser):
    BulkGenerateSimilarHanziVocabList(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
