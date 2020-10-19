# -*- coding: utf-8 -*-
'''
Created on 30/12/2014

@author: Myxoma
'''

import re

def cleanBrFormat(pInput, deepClean = False):
    #tell the method that parameter is always unicode string
    pInput = unicode(pInput)
    pInput = re.sub(r'(<br>)', r"<br />", pInput)
    pInput = re.sub(r'(<br/>)', r"<br />", pInput)
    pInput = re.sub(r'(<br >)', r"<br />", pInput)
    if (deepClean == True):
        pInput = re.sub(r'(<Br>)', r"<br />", pInput)
        pInput = re.sub(r'(<Br/>)', r"<br />", pInput)
        pInput = re.sub(r'(<Br >)', r"<br />", pInput)
        
        insensitive_BrBrRE =  re.compile(re.escape('<br /><br />'), re.IGNORECASE)
        InitialpInput = pInput
        pInput = insensitive_BrBrRE.sub('<br />', pInput)
        while(InitialpInput != pInput):
            InitialpInput = pInput
            pInput = insensitive_BrBrRE.sub('<br />', pInput)
    return pInput

def IsBREndingOnFinalLine(pX):
    #tell the method that parameter is always unicode string
    pX = unicode(pX)
    pX = pX.lower()
    if (pX.endswith("<br />") == True or pX.endswith("<br>") == True or pX.endswith("<br >") == True):
        return True
    else:
        return False

def InsertBREndingOnFinalLine(pY):
    #tell the method that parameter is always unicode string
    pY = unicode(pY)
    pY_alreadyHasBrEnding = IsBREndingOnFinalLine(pY)
    if (pY_alreadyHasBrEnding == True):
        return pY
    else:
        pY = pY+ unicode(ur'<br />')
        return pY

def RemoveBREndingOnFinalLine(pY):    
    #tell the method that parameter is always unicode string
    pY = unicode(pY)
    pY = cleanBrFormat(pY)
    pY_alreadyHasBrEnding = IsBREndingOnFinalLine(pY)
    if (pY_alreadyHasBrEnding == True):
        return pY[:-6]
    else:
        return pY

def CleanNbsp(pInputUnicode):
    pInputUnicode = unicode(pInputUnicode)
    pInputUnicode = pInputUnicode.replace(ur"&nbsp", " ")
    return pInputUnicode


def CleanDivSyntaxToBR(pInputUnicode):
    #tell the method that parameter is always unicode string
    pInputUnicode = unicode(pInputUnicode)
    
   
    #Begin Re part 1
    insensitive_DivRE1 = re.compile(re.escape('<div>'), re.IGNORECASE)
    pInputUnicode = insensitive_DivRE1.sub('', pInputUnicode)
    
    #Begin Re part 2
    insensitive_DivRE2 = re.compile(re.escape('</div></div>'), re.IGNORECASE)
    InitialpInputUnicode = pInputUnicode
    pInputUnicode = insensitive_DivRE2.sub('</div>', pInputUnicode)
    while(InitialpInputUnicode != pInputUnicode):
        InitialpInputUnicode = pInputUnicode
        pInputUnicode = insensitive_DivRE2.sub('</div>', pInputUnicode)
    
    #Begin Re part 3
    insensitive_DivToBr = re.compile(re.escape('</div>'), re.IGNORECASE)
    pInputUnicode = insensitive_DivToBr.sub('<br />', pInputUnicode)
    
    #Begin Re part 4

    insensitive_BrBrRE =  re.compile(re.escape('<br /><br />'), re.IGNORECASE)
    InitialpInputUnicode = pInputUnicode
    pInputUnicode = insensitive_BrBrRE.sub('<br />', pInputUnicode)
    while(InitialpInputUnicode != pInputUnicode):
        InitialpInputUnicode = pInputUnicode
        pInputUnicode = insensitive_BrBrRE.sub('<br />', pInputUnicode)
    

    """
    #for debug  only, can delete
    print "before process: " + pInputUnicode
    my_list = pInputUnicode.split(ur"<br />")
    for i in my_list:
        print i
    #end of debug
    """
    return pInputUnicode

def AutoCleanField(pInputUnic, pInsertFinalLineBr= False, debugMode = False):
    pInputUnic = unicode(pInputUnic)
    pInputUnic = CleanNbsp(pInputUnic)
    pInputUnic = CleanDivSyntaxToBR(pInputUnic)
    if (pInsertFinalLineBr == True):
        pInputUnic = InsertBREndingOnFinalLine(pInputUnic)
    else:
        pInputUnic = RemoveBREndingOnFinalLine(pInputUnic)
    

    if (debugMode == True):
        print pInputUnic
        print
        my_list = pInputUnic.split(ur"<br />")
        for i in my_list:
            print i

    return pInputUnic