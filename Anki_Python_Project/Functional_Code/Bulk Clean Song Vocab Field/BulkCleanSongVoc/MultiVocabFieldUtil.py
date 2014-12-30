# -*- coding: utf-8 -*-
'''
Created on 30/12/2014

@author: Myxoma
'''

import re

def CountBrInString():
    #assumed Text Input from Words field and has no <br> at the very last line
    TextInput = "万(ばん): many, all<br />万人(ばんじん): all people, everybody, 10000 people<br />万能(ばんのう): all-purpose, almighty, omnipotent<br />万歳(ばんざい): strolling comic dancer<br />万一(まんいち): by some chance, by some possibility, if by any chance, 10,000:1 odds<br />万(まん): 10,000, ten thousand, myriad(s), all, everything<br />万年筆(まんねんひつ): fountain pen"
    brformat1count = TextInput.count("<br />")
    brformat2count = TextInput.count("<br/>")
    brformat3count = TextInput.count("<br>")
    TotalWordCount = brformat1count + brformat2count + brformat3count
    if (TotalWordCount !=0):
        TotalWordCount = TotalWordCount+1
    print "TotalWordCount :", TotalWordCount




"""
def AssertBREndingOnFinalLine():

def InsertBREndingOnFinalLine():
def RemoveBREndingOnFinalLine():    

"""
def CleaNnbsp(pInputUnicode):
    pInputUnicode = unicode(pInputUnicode)
    pInputUnicode = pInputUnicode.replace(ur"&nbsp", " ")
    return pInputUnicode

def CleanDivSyntaxToBR(pInputUnicode):
    print "You Have Accessed CleanDivSyntaxToBR file"
    #tell the method that parameter is always unicode string
    pInputUnicode = unicode(pInputUnicode)
    #pInputUnicode.replace("<div>", "")
    print pInputUnicode
    print 
    print 
    insensitive_DivRE1 = re.compile(re.escape('<div>'), re.IGNORECASE)
    insensitive_DivRE2 = re.compile(re.escape('</div></div>'), re.IGNORECASE)
    pInputUnicode = insensitive_DivRE1.sub('', pInputUnicode)
    
    InitialpInputUnicode = pInputUnicode
    pInputUnicode = insensitive_DivRE2.sub('</div>', pInputUnicode)
    while(InitialpInputUnicode != pInputUnicode):
        InitialpInputUnicode = pInputUnicode
        pInputUnicode = insensitive_DivRE2.sub('</div>', pInputUnicode)
        
    insensitive_DivToBr = re.compile(re.escape('</div>'), re.IGNORECASE)
    pInputUnicode = insensitive_DivToBr.sub('<br />', pInputUnicode)
    
    #for debug  only, can delete
    my_list = pInputUnicode.split(ur"<br />")
    for i in my_list:
        print i
    #end of debug
    return pInputUnicode
    
