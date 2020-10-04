# -*- coding: utf-8 -*-
import itertools
import os
import csv
import re
"""
list1 = ['f', 'o', 'o']
list2 = ['hello', 'world','yeah','man','a','b','c']

print ([x for x in itertools.chain.from_iterable(itertools.zip_longest(list1,list2)) if x])

TODO: 

Sometimes text has full-stop . typoed as " 
See below

"카일의 의문에, 카라는 마리에의 기분을 대변한다."

하지만――복수의 남성이 자신을 두고 경쟁한다, 라는 건 여자로서는 조금 기

분이 좋을지도"

Fix idea. if line ends with " > check if total comma count so far is even. > if total comma count is odd then it's a typo
"""

"""
OCR common quote typo

‘미카도네 누나… 인가7


if really ends one line with single quote then turn to bracket:
    ‘어이어이… 이게 무슨 수라장이야.’ >> (어이어이… 이게 무슨 수라장이야.)
"""
#Config
debugmode = True
replaceDoubleQuote = True
formatOption1 = False
completeFormatWithQuoteSub = False
replaceSingleLineSingleQuoteWithBracket = True
OCR_quickFix_replace_single_quote_with_double_quote = True
OCR_quickFix_regex_sub_common_quote_typos = True
OCR_quickFix_use_simple_newline_identifier = True
#Ends config
out_f = open('outputfile.txt', 'w', encoding="utf-8")
toOpenFile = 'file.txt'



temp_f = open('temp_f.txt', 'w', encoding="utf-8")


def convert_to_standard_quote(input_string):
    input_string = input_string.replace('“','"')
    input_string = input_string.replace('”','"')
    input_string = input_string.replace('’',"'")
    input_string = input_string.replace('‘',"'")
    # input_string = input_string.replace('〝','"')   Too rare
    # input_string = input_string.replace('〟','"')   Too rare
    return input_string


def convert_to_standard_parentheses(input_string):
    input_string = input_string.replace('（', '(')  # Korean & Japanese parentheses changed to standard ones
    input_string = input_string.replace('）', ')')  # Korean & Japanese parentheses changed to standard ones
    return input_string


def OCR_quick_fix_replace_single_quote_with_double_quote(input_string):
    """
    can be useful for when OCR is too inaccurate and incorrectly detects " as ' and vice versa. So we simply converts them all to doublequote
    ‘*미안，" >> "*미안，"     (From Hikaru 1)

    Note: Make sure to convert all none standard quotes (i.e. ’‘  to the standard quote first)
    """
    input_string = input_string.replace('’','"')
    input_string = input_string.replace('‘','"')
    input_string = input_string.replace("'",'"')
    return input_string

def OCR_quick_fix_regex_sub_common_quote_typos(input_string):
    """
    """
    input_string = input_string.replace("''",'"')  # ''다른 부타악?'    >> converts 2x single quotes '' to "

    input_string = re.sub("^'([^']*)[17\*•]$", r"'\1'", input_string, flags=re.MULTILINE)
    input_string = re.sub("^'([^']*)[17\*•]'$" , r'"\1"', input_string, flags=re.MULTILINE)
    input_string = re.sub("^'([^']*)'[17\*•]$",r'"\1"' , input_string, flags=re.MULTILINE)
    pattern = '''^"([^']*)[17\*•]'$'''
    input_string = re.sub(pattern, r'"\1"' , input_string, flags=re.MULTILINE)
    pattern = '''^"([^']*)'[17\*•]$'''
    input_string = re.sub(pattern,r'"\1"' , input_string, flags=re.MULTILINE)
    pattern = '''^"([^']*)[17\*•]$'''
    input_string = re.sub(pattern,r'"\1"' , input_string, flags=re.MULTILINE)
    pattern = '''^[17\*•]([^']*)'$'''
    input_string = re.sub(pattern,r"'\1'" , input_string, flags=re.MULTILINE)
    pattern = '''^[17\*•]([^']*)"$'''
    input_string = re.sub(pattern,r'"\1"' , input_string, flags=re.MULTILINE)
    pattern = '''(?:^[17\*•]'|^'[17\*•])([^']*)(?:"|')$'''
    input_string = re.sub(pattern,r'"\1"' , input_string, flags=re.MULTILINE)

    start_or_end_patterns_doubleQ = ["44", "17", "71"]

    for p in start_or_end_patterns_doubleQ:
        startswith = "^" + p + "(.*?)$"
        endswith = "^(.*?)" + p + "$"
        input_string = re.sub(startswith, r'"\1', input_string, flags=re.MULTILINE)   # /^44(.*?)$/    , 44네 목적은 도대체 뭐였지?’ >> "네 목적은 도대체 뭐였지?’
        input_string = re.sub(endswith, r'\1"', input_string, flags=re.MULTILINE)    #  /^(.*?)44$/    , '네 목적은 도대체 뭐였지?44 >> '네 목적은 도대체 뭐였지?"

    start_or_end_patterns_singleQ = ["4", "7", "T"]  # handle "•••야，설마 귀여운 꽃이란 건 네 얘기냐?T

    for p in start_or_end_patterns_singleQ:
        startswith = "^" + p + "(.*?)$"
        endswith = "^(.*?)" + p + "$"
        input_string = re.sub(startswith, r"'\1", input_string, flags=re.MULTILINE)
        input_string = re.sub(endswith, r"\1'", input_string, flags=re.MULTILINE)

    """
    input_string_lines = [line for line in input_string.splitlines()]
    input_string = ""
    for start_or_end_pattern in start_or_end_patterns:
        for i_line in input_string_lines:
            if i_line.startswith(start_or_end_pattern):
                input_string = input_string + '\n' + ('"'+i)"""

    pattern = '''^"(.*?)(?:'$|'.{1}$)'''
    input_string = re.sub(pattern, r'"\1"', input_string, flags=re.MULTILINE)
    # match if starts with "  and ends with str[-1] = ' or str[-2] = '
    # "네 목적은 도대체 뭐였지?'
    # "네 목적은 도대체 뭐였지'7
    pattern = '''^(?:'|.{1}')(.*?)"$'''
    input_string = re.sub(pattern, r'"\1"', input_string, flags=re.MULTILINE)
    # match if first index or second index contains ' and the line  and ends with "
    # ?'네 목적은 도대체 뭐였지?"
    # '1네 목적은 도대체 뭐였지"


    input_string = re.sub(endswith, r'\1"', input_string, flags=re.MULTILINE)    #  /^(.*?)44$/    , '네 목적은 도대체 뭐였지?44 >> '네 목적은 도대체 뭐였지?"
    return input_string

def OCR_quick_fix_use_simple_newline_identifier(input_f):

    contain_line_ender = False
    for line in input_f:

        if line not in ['\n', '\r\n']:  # if line not empty

            if line.strip()[-1] in ['.', '•', '。', '…', '一', '，', ',', '、', 'O', '◊', '◇', '』', '」', '）', ')', '〟', '’', '”', '"', '!', '！', '?', '？']:
                    if line.strip()[0] in ['.', '•', '。', '…', '一', '，', ',', '、', 'O', '◊', '◇', '』', '」', '）', ')', '〟', '’', '”', '"', '!', '！', '?', '？'] + ['“', '‘', '（', '〝', '『', '「']:
                        if not contain_line_ender:
                            """  if 1. current line starts and end with quote and 2.previous line doesn't contain \n then add \n before that. For example:
                                젠장, 안에서 문을 잠갔아
                                "안 돼，나는 히카루의 마음을 네게 전할 사명이 있어!”
                                Would be 2 separate lines.
                            """
                            out_f.write('\n')
                    out_f.write('%s' % line.strip())
                    contain_line_ender = True
                    out_f.write('\n')
            else:
                out_f.write('%s' % line.strip())
                contain_line_ender = False
            if debugmode:
                    print("line[-1] contain_line_ender:%s  Txt: %s" % (contain_line_ender,line.strip()))







if replaceDoubleQuote:
    with open(toOpenFile, mode="r", encoding="utf-8") as f:
        # This will replace the front  " with 「 and the back " with  」. Because excel doesn't like quotation
        # e.g. "마리에 님, 모처럼 여름방학인데 기쁘지 않으세요?" >>>  「마리에 님, 모처럼 여름방학인데 기쁘지 않으세요?」
        formatted_f = f.read()

        #also replaces Korean doublequote with normal ASCII doublequote because sometimes they typoed like this “너무하네. 난 정직함이 장점인데"
        # ( From otomege_v5_ch2) The front doublequote is kr style but the back is ascii

        formatted_f = convert_to_standard_quote(formatted_f)
        formatted_f = convert_to_standard_parentheses(formatted_f)

        if OCR_quickFix_regex_sub_common_quote_typos:
            formatted_f = OCR_quick_fix_regex_sub_common_quote_typos(formatted_f)
        if replaceSingleLineSingleQuoteWithBracket:
            """
            useful for OCR, only when a single line contains a  complete set of single quote at the beginning and end of line then convert to bracket
            probably the most OCR detection error-free conversion compared to quote spanning over multiple lines
            '있잖아, 이카기.' >> (있잖아, 이카기.)
            """
            formatted_f = re.sub("^'([^']*)'$", r'(\1)', formatted_f, flags=re.MULTILINE)  # flags=re.MULTILINE required to use anchor ^ and $ operators

        if OCR_quickFix_replace_single_quote_with_double_quote:
            formatted_f = OCR_quick_fix_replace_single_quote_with_double_quote(formatted_f)

        """Dealing with bad OCR
        1.  if line ends with .’OR !’  but there were no preceding incomplete ‘   then  the OCR likely missed the ‘   so simply add  ‘ at the beginning of the same line.
        2. if line ends with ’ but there were no preceding incomplete ‘ then OCR probably mistook the . for '     so simply convert ' to .
        
        """
        # x = [line.splitlines() for line in formatted_f]
        x = [line for line in formatted_f.splitlines()]
        print(len(x))
        print(len(formatted_f.splitlines()))
        print(formatted_f.count('\n'))
        outtxt = ""

        if formatOption1:
            #old version
            formatted_f = re.sub('"([^"]*)"', r'「\1」', formatted_f)
            """ 
            The "([^"]*)" regex captures a ", followed by 0 or more things that aren't another ", and a closing ". 
            The replacement uses $1 as a reference for the things that were wrapped in quotes.
            see https://stackoverflow.com/questions/53901717/string-replace-double-quotes-into-curly-brackets
            """
        else:

            commaCount = 0
            for i in x:
                commaCount = i.count('"') + commaCount
                if (i.endswith('."') or i.endswith('!"')) and not i.startswith('"'):
                    if (commaCount % 2) != 0:  # if odd
                        outtxt = outtxt + '\n' + ('"'+i)
                        commaCount += 1
                        print("type1odd " + ('"'+i))
                    else:  # if even, still do the same thing
                        outtxt = outtxt + '\n' + ('"'+i)
                        print("type1even " + ('"'+i))


                elif( not(i.endswith('."') or i.endswith('!"')) and i.endswith('"') and not i.startswith('"')):
                    if (commaCount % 2) != 0:  # if odd
                        outtxt = outtxt + '\n' + ('"'+i)
                        commaCount += 1
                        print("type2odd " + ('"'+i))
                    else:
                        outtxt = outtxt + '\n' + (i[:-1] + ".")
                        print("type2even " + (i[:-1] + "."))
                else:
                    outtxt = outtxt + '\n' + i

            if completeFormatWithQuoteSub:
                formatted_f = re.sub('"([^"]*)"', r'「\1」', outtxt)
            else:
                formatted_f = outtxt



        temp_f.write(formatted_f)
        toOpenFile = 'temp_f.txt'
        temp_f.close()
        f.close()


with open(toOpenFile, mode="r", encoding="utf-8") as f:
    incomplete_quote = False
    incomplete_quote2 = False
    incomplete_quote3 = False
    incomplete_quote4 = False
    incomplete_quote5 = False

    def check_char(c1):
        global incomplete_quote
        global incomplete_quote2
        global incomplete_quote3
        global incomplete_quote4
        global incomplete_quote5
        start_with_complete_quote = incomplete_quote is False and incomplete_quote2 is False and incomplete_quote3 is False and incomplete_quote4 is False and incomplete_quote5 is False

        if incomplete_quote is True:
            if c1 in ['」']:
                incomplete_quote = False
        if incomplete_quote2 is True:
            if c1 in ['』']:
                incomplete_quote2 = False
        if incomplete_quote3 is True:
            if c1 in ['）']:
                incomplete_quote3 = False
        if incomplete_quote4 is True:
            if c1 in ['”']:
                incomplete_quote4 = False
        if incomplete_quote5 is True:
            if c1 in [')']:
                incomplete_quote5 = False
        end_with_complete_quote = incomplete_quote is False and incomplete_quote2 is False and incomplete_quote3 is False and incomplete_quote4 is False and incomplete_quote5 is False
        if start_with_complete_quote:
            if c1 in ['.', '◇', '」', '』', '?', '!!', '!', '）', '”', ')', ',']:
                out_f.write('\n')
        elif start_with_complete_quote is False and end_with_complete_quote is True:
            out_f.write('\n')
        return c1

    if OCR_quickFix_use_simple_newline_identifier:
        OCR_quick_fix_use_simple_newline_identifier(f)
    else:
        for line in f:
            if line not in ['\n', '\r\n']:  # if line not empty
                #print(line.strip())
                if '「' in line and not '」' in line and incomplete_quote is False:
                   incomplete_quote = True
                if '『' in line and not '』' in line and incomplete_quote2 is False:
                    incomplete_quote2 = True
                if '（' in line and not '）' in line and incomplete_quote3 is False:
                    incomplete_quote3 = True
                if '“' in line and not '”' in line and incomplete_quote4 is False:
                    incomplete_quote4 = True
                if '(' in line and not ')' in line and incomplete_quote5 is False: #This got me big time. So many bracket unicode. '（' isn't the same is '('
                    incomplete_quote5 = True

                if incomplete_quote is False and incomplete_quote2 is False and incomplete_quote3 is False and incomplete_quote4 is False and incomplete_quote5 is False:
                    out_f.write('%s' % line.strip())

                    if incomplete_quote is False and incomplete_quote2 is False and incomplete_quote3 is False and incomplete_quote4 is False and incomplete_quote5 is False:
                        if line.strip()[-1] in ['.', '◇', '」', '』', '?', '!!', '!', '）', '”', ')', ',', '"', 'O', '◊']:
                            out_f.write('\n')
                    if incomplete_quote is True:
                        if line.strip()[-1] in ['」']:
                            out_f.write('\n')
                            incomplete_quote = False
                    if incomplete_quote2 is True:
                        if line.strip()[-1] in ['』']:
                            out_f.write('\n')
                            incomplete_quote2 = False
                    if incomplete_quote3 is True:
                        if line.strip()[-1] in ['）']:
                            out_f.write('\n')
                            incomplete_quote3 = False
                    if incomplete_quote4 is True:
                        if line.strip()[-1] in ['”']:
                            out_f.write('\n')
                            incomplete_quote4 = False
                    if incomplete_quote5 is True:
                        if line.strip()[-1] in [')']:
                            out_f.write('\n')
                            incomplete_quote5 = False
                else:
                    linestr = line.strip()
                    for c in linestr:
                        out_f.write(c)
                        check_char(c)

                #TODO:  Deal with faulty bracket
                """
                
                     incomplete_qte:0 incomplete_qte2:0 incomplete_qte3:0 incomplete_qte4:0 incomplete_quote5:0 line[-1] in[. ◇ 」 』 ? !! ! ）)”,]:1 line[-1] contains 」:0 txt: 레리아도 그 시절을 기억하고 있다.
                     incomplete_qte:0 incomplete_qte2:0 incomplete_qte3:0 incomplete_qte4:0 incomplete_quote5:1 line[-1] in[. ◇ 」 』 ? !! ! ）)”,]:0 line[-1] contains 」:0 txt: (그리고, 2편의 주인공은 학원에서 공략 대상과 사랑을 나누고, 최종적으로 좋
                     incomplete_qte:0 incomplete_qte2:0 incomplete_qte3:0 incomplete_qte4:0 incomplete_quote5:1 line[-1] in[. ◇ 」 』 ? !! ! ）)”,]:1 line[-1] contains 」:0 txt: 아하는 상대를 수호자로 선택해. 하지만, 이대로면 선택받은 건 리온이 돼) 레리아로서는 곤혹스러울 수밖에 없었다.
                     incomplete_qte:0 incomplete_qte2:0 incomplete_qte3:0 incomplete_qte4:0 incomplete_quote5:1 line[-1] in[. ◇ 」 』 ? !! ! ）)”,]:1 line[-1] contains 」:0 txt: 설마, 자신의 언니가 리온을 선택할 거라고는 생각하지 않은 것이다.
                """



                if debugmode:
                    print("incomplete_qte:%i incomplete_qte2:%i incomplete_qte3:%i incomplete_qte4:%i incomplete_quote5:%i line[-1] in[. ◇ 」 』 ? !! ! ）)”,]:%i line[-1] contains 」:%i txt: %s" % (incomplete_quote, incomplete_quote2,incomplete_quote3,incomplete_quote4,incomplete_quote5,  line.strip()[-1] in ['.', '◇', '」', '』', '?', '!!', '!', '）', '”', ')', ','],line.strip()[-1] in ['」'],line.strip() ))
    out_f.close()
    f.close()




csvLocation = ""+os.path.dirname(__file__) + "\\list2.csv"
def csvToRoundrobinList(fileName):
    L1 = []
    L2 = []
    with open(fileName, "r", encoding="utf-8")as tsvfile:
        reader = csv.DictReader(tsvfile,delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            L1.append(row["KR"])
            L2.append(row["JP"])
    finalL = makeRoundRobinList(L1,L2)


    #now make file
    with open('SSS Class Suicide Hunter_KR_JP_1-50.txt', 'w', encoding="utf-8") as f:
        for item in finalL:
            #f.write('<p class="calibre1">%s </p>\n' % item)
            f.write('%s\n' % item)


def makeRoundRobinList(L1,L2):
    return ([x for x in itertools.chain.from_iterable(itertools.zip_longest(L1,L2)) if x])


"""
csvToRoundrobinList(csvLocation)

"""
