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