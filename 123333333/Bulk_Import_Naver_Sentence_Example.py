# -*- coding: utf-8 -*-
'''
Created on 09/12/2014

@author: Myxoma
'''

# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, showWarning,tooltip
# import all of the Qt GUI library
from aqt.qt import *
from anki.hooks import addHook
import requests
from bs4 import BeautifulSoup
import time


##########################################################################
# Model name must contain this.
# each field name must be exact!
#Model name of the note type
modelName = 'Korean Vocab'
# The Field containing Japanese Vocab which you want to know the frequency ranking
Vocab_SrcField = 'Korean'
# Field to hold  the Freuency Ranking Goes here
dstField_Merged = 'Example_Merged' #Optional as long as either dstField_Merged or dstField_Sentence field is not empty
dstField_Sentence = 'Example_Sentence'
dstField_Meaning = 'Example_Meaning'
debugMode = False
# if data exists in dstField, should we overwrite it?
OVERWRITE_DST_FIELD=True
##########################################################################


def getNaverSentenceExample(para):

    """ To disable unverified request warning :
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    """
    url = 'https://endic.naver.com/search_example.nhn?sLn=en&query='
    # para  = '부족하다'
    r = requests.get(url+para, stream=True, verify=False)
    x = ""
    result = {"Merged":x, "Sentence":"", "Meaning":""}
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        officialExamp = soup.find("div", id="exampleAjaxArea")
        if (officialExamp):
            officialExamp_Meaning = [ a.get('value') for a in officialExamp.find_all("input", attrs={"name":"", "type":"hidden"})]

            # N=a:xml.detail only, not something like class="btn_detail2 detail_url_link N=a:xml.detail"
            officialExamp_Sentence = [a.text for a in officialExamp.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['N=a:xml.detail'])]

            vliveExamp= soup.find("div", id="vliveExamCollection")

            #print(officialExamp_Meaning[:2])
            #print(officialExamp_Sentence[:2])


            for idx, sentence in enumerate(officialExamp_Sentence[:2]):
                if (debugMode):
                    showInfo("input: %s \n sentence , type: %s  , value : %s \n meaning, type: %s  , value : %s \n x, type: %s value: %s " %(para,type(sentence),str(sentence),type(officialExamp_Meaning[idx]),str(officialExamp_Meaning[idx]),type(x),str(x)))
                x += sentence + "<br>" + officialExamp_Meaning[idx] + "<br>"
                result["Sentence"] += sentence + "<br>"
                result["Meaning"] += officialExamp_Meaning[idx] + "<br>"

            result["Merged"] = x
            #print (result)

    else:
        print("url not found")

    time.sleep(0.3)

    return result

def BulkImportNaverSentenceExample(nids):
    mw.checkpoint("BulkImportNaverSentenceExample")
    mw.progress.start()

    maxloop = max(len(nids),1)
    showInfo("Time required = ~1 second/query \n Estimated Time required for %d cards is %d seconds" %(maxloop, maxloop))
    refreshGuiTimer = time.perf_counter()
    totalRunTime = time.perf_counter()
    for  loopno, nid in enumerate(nids):

        if ( time.perf_counter() - refreshGuiTimer >= 10):
            refreshGuiTimer = time.perf_counter()
            #update timer every 10 seconds

            tooltip("loop no: %d Progress : %d %%" % (loopno, (loopno/maxloop)*100),    period=300)
            # refresh GUI during loop
            time.sleep(0.2)
            #showInfo('hi')
            mw.app.processEvents()
            time.sleep(0.1)

        note = mw.col.getNote(nid)
        if modelName not in note.model()['name']:
            #showInfo ("--> Model mismatch: %s vs %s" %( modelName, note.model()['name']))
            continue
        src1 = None
        if Vocab_SrcField in note:
            src1 = Vocab_SrcField
        if not src1:
            # no src1 field
            #showInfo ("--> Field %s not found." % (Vocab_SrcField))
            continue
        dst_mrged = None
        dst_st = None
        dst_mn = None
        if dstField_Merged in note:
            dst_mrged = dstField_Merged

        if dstField_Sentence in note:
            dst_st = dstField_Sentence

        if dstField_Meaning in note:
            dst_mn = dstField_Meaning

        if not (dst_st or dst_mrged or dst_mn):
            #showInfo ("--> No Output field found!")
            # no dst field
            continue
        """    
        if note[dst_st] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            #showInfo ("--> %s not empty. Skipping!" % (Vocab_SrcField))
            continue"""
        #srcTxt = mw.col.media.strip(note[src1])
        #if not srcTxt.strip():
        #    continue
        try:
            #showInfo ("--> Everything should have worked.")
            #vocabToQuery = "相当"
            vocabToQuery = note[src1]
            
            #showInfo (str(defobj["시내"]))
            #showInfo (str(defobj[''+vocabToQuery]))
            if (vocabToQuery != ""):

                    if (debugMode):
                        showInfo (str(vocabToQuery))

                    qResult = getNaverSentenceExample(vocabToQuery)
                    if (dst_mrged):
                        note[dst_mrged] = qResult["Merged"]
                    if (dst_st):
                        note[dst_st] = qResult["Sentence"]
                    if (dst_mn):
                        note[dst_mn] = qResult["Meaning"]




            
        except Exception as e:
            raise
        note.flush()

    totalRunTime  = time.perf_counter() -totalRunTime

    showInfo ("Everything should have worked. \n totalRunTime: %d" %(totalRunTime))

    mw.progress.finish()
    mw.reset()
    

def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Bulk-Import Naver Sentence Example')
    a.triggered.connect(lambda _, b=browser: onBulkImportNaverSentenceExample(b))

def onBulkImportNaverSentenceExample(browser):
    BulkImportNaverSentenceExample(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
