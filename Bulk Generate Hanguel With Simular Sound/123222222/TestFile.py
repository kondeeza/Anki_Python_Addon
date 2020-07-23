# -*- coding: utf-8 -*-
from hangul_jamo import is_syllable, is_jamo_character, compose_jamo_characters, decompose_syllable, compose, decompose




fuzzyChoseongDicts = {'ㄱ': ['ㄱ', 'ㅋ', 'ㄲ'],
              'ㅋ': ['ㄱ', 'ㅋ', 'ㄲ'],
              'ㄲ': ['ㄱ', 'ㅋ', 'ㄲ'],
              'ㄷ': ['ㄷ', 'ㅌ', 'ㄸ'],
              'ㅌ': ['ㄷ', 'ㅌ', 'ㄸ'],
              'ㄸ': ['ㄷ', 'ㅌ', 'ㄸ'],
              'ㅂ': ['ㅂ', 'ㅍ', 'ㅃ'],
              'ㅍ': ['ㅂ', 'ㅍ', 'ㅃ'],
              'ㅃ': ['ㅂ', 'ㅍ', 'ㅃ'],
              'ㅅ': ['ㅅ', 'ㅈ', 'ㅆ', 'ㅉ'],
              'ㅈ': ['ㅅ', 'ㅈ', 'ㅆ', 'ㅉ'],
              'ㅆ': ['ㅅ', 'ㅈ', 'ㅆ', 'ㅉ'],
              'ㅉ': ['ㅅ', 'ㅈ', 'ㅆ', 'ㅉ'],
              'ㅇ': ['ㅇ', 'ㅎ'],
              'ㅎ': ['ㅇ', 'ㅎ']}

fuzzyJungseongDicts = {'ㅏ': ['ㅏ', 'ㅑ', 'ㅘ'],
              'ㅑ':  ['ㅏ', 'ㅑ', 'ㅘ'],
              'ㅘ':  ['ㅏ', 'ㅑ', 'ㅘ'],
              'ㅓ': ['ㅓ', 'ㅕ', 'ㅝ'],
              'ㅕ': ['ㅓ', 'ㅕ', 'ㅝ'],
              'ㅝ': ['ㅓ', 'ㅕ', 'ㅝ'],
              'ㅗ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅛ'],
              'ㅛ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅛ'],
              'ㅜ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅛ'],
              'ㅠ': ['ㅗ', 'ㅛ', 'ㅜ', 'ㅛ'],
              'ㅔ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ','ㅚ'],
              'ㅐ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ','ㅚ'],
              'ㅖ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ','ㅚ'],
              'ㅒ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ','ㅚ'],
              'ㅞ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ','ㅚ'],
              'ㅙ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ','ㅚ'],
              'ㅚ': ['ㅔ', 'ㅐ', 'ㅖ', 'ㅒ', 'ㅞ', 'ㅙ','ㅚ'],
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
                  'ㅆ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ']}

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
                  'ㅆ': ['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ','ㅋ','ㅌ']}
    result = False
    if len(input) == 1:
        if is_syllable(input):
            if decompose_syllable(input)[2] in Composite_jamo_Dicts:
                result = decompose_syllable(input)[2]
    return result


#fuzzyJongseongDicts = 'nothing   ng   n   g  b  r  m'

input = '가'

result = []

# Test input validity

if len(input) == 1:
    if is_syllable(input):
        jamo = decompose_syllable(input)
        if fuzzyChoseongDicts.get(jamo[0]):
            for a in fuzzyChoseongDicts.get(jamo[0]):
                result.append(compose_jamo_characters(a, jamo[1], jamo[2]))

if result == []:
    print("result is null")
    result.append(input)

print(result)


###
result = []

# Test input validity
if len(input) == 1:
    if is_syllable(input):
        print("Pass validity")
        x = decompose_syllable(input)
        if fuzzyJungseongDicts.get(x[1]):
            for a in fuzzyJungseongDicts.get(x[1]):
                 result.append(compose_jamo_characters(x[0], a, x[2]))


if result == []:
    print("result is null")
    result.append(input)

print(result)



mjamo = decompose_syllable('혋')
print ('ㅄ' == mjamo[2])
print ( not set([decompose_syllable('중')[2],decompose_syllable('함')[2],decompose_syllable('혋')[2],decompose_syllable('새')[2]]).isdisjoint(Composite_jamo_Dicts)  )
print (hasComposite_jongseong('혋'))
print (hasComposite_jongseong('혋'))

"""
inputstr = '재미있다'
result = false
for ch in inputstr:
    if is_syllable(ch):
        decompose_syllable(ch)[2] in Composite_jamo_Dicts"""
print("begin fuzzy test")
mInput = '썩이다'
mFuzz_List = []
for x1 in mInput:
    #print(get_fuzzyChoseongList(x1))
    #print(get_fuzzyJungseongList(x1))
    #print(get_fuzzyJongseongList(x1))
    mFuzz_List.append(get_fuzzyChoseongList(x1))
    mFuzz_List.append(get_fuzzyJungseongList(x1))
    mFuzz_List.append(get_fuzzyJongseongList(x1))
    print(mFuzz_List)

print("begin fuzzy test2")
m_fuzzyJamo = get_fuzzyJamoList('쌓')
print(m_fuzzyJamo)
print(len(m_fuzzyJamo))
