# -*- coding: utf-8 -*-
'''
Created on 06/12/2014

@author: Myxoma
'''
import re


#assumed Text Input from Words field and has no <br> at the very last line
TextInput = "万(ばん): many, all<br />万人(ばんじん): all people, everybody, 10000 people<br />万能(ばんのう): all-purpose, almighty, omnipotent<br />万歳(ばんざい): strolling comic dancer<br />万一(まんいち): by some chance, by some possibility, if by any chance, 10,000:1 odds<br />万(まん): 10,000, ten thousand, myriad(s), all, everything<br />万年筆(まんねんひつ): fountain pen"
brformat1count = TextInput.count("<br />")
brformat2count = TextInput.count("<br/>")
brformat3count = TextInput.count("<br>")
TotalWordCount = brformat1count + brformat2count + brformat3count
if (TotalWordCount !=0):
    TotalWordCount = TotalWordCount+1
print "TotalWordCount :", TotalWordCount
