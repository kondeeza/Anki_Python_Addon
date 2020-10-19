# -*- coding: utf-8 -*-
# Copyright: mo  <paradoxez919@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# Bulk copy data in one field to another.

##########################################################################


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
#reload(sys) #apparently this doesn't work in python3... 
#sys.setdefaultencoding('utf-8')
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE !!

master_modelName = ''
master_Hanzi_SrcField = ''
master_Auto_Sentence_SrcField = ''
master_Auto_SR_SrcField = ''
master_Auto_ST_SrcField = ''
master_Auto_SA_SrcField = ''
master_Auto_SentenceF_SrcField = ''
master_Auto_SR_F_SrcField = ''
master_Auto_ST_F_SrcField = ''
master_deckName = ''
# if data exists in Output_SrcField, should we overwrite it?
OVERWRITE_DST_FIELD= ''

slave_Model_Sentence_SPinyin_SMeaning_SAudio_List = []


def reload_config():
    global master_modelName
    global master_Hanzi_SrcField
    global master_Auto_Sentence_SrcField
    global master_Auto_SR_SrcField
    global master_Auto_ST_SrcField
    global master_Auto_SA_SrcField
    global master_Auto_SentenceF_SrcField
    global master_Auto_SR_F_SrcField
    global master_Auto_ST_F_SrcField
    global OVERWRITE_DST_FIELD
    global slave_Model_Sentence_SPinyin_SMeaning_SAudio_List
    global master_deckName

    config = mw.addonManager.getConfig(__name__)
    master_modelName = config['01_master_modelName']
    master_Hanzi_SrcField = config['02_master_Hanzi_SrcField']
    master_Auto_Sentence_SrcField = config['03_master_Auto_Sentence_SrcField']
    master_Auto_SR_SrcField = config['04_master_Auto_SR_SrcField']
    master_Auto_ST_SrcField = config['05_master_Auto_ST_SrcField']
    master_Auto_SA_SrcField = config['06_master_Auto_SA_SrcField']
    master_Auto_SentenceF_SrcField = config['07_master_Auto_SentenceF_SrcField']
    master_Auto_SR_F_SrcField = config['08_master_Auto_SR_F_SrcField']
    master_Auto_ST_F_SrcField = config['09_master_Auto_ST_F_SrcField']
    OVERWRITE_DST_FIELD = config['15_OVERWRITE_DST_FIELD']
    master_deckName = config['10_master_deckName']
    slave_Model_Sentence_SPinyin_SMeaning_SAudio_List = config['16_slave_Model_Sentence_SPinyin_SMeaning_SAudio_List']

def createAnkiNote(hanziToAddNoteList,masterNoteModelFile):
    mw.checkpoint("Manual Create Note")
    mw.progress.start()
    
    # Get desired deck name from input box
    deckName = master_deckName
    if not deckName:
        return
    #deckName = deckName.replace('"', "")
    
    # Create new deck with name from input box
    deck = mw.col.decks.get(mw.col.decks.id(deckName))
    
    # Copy notes
    for hanziNote in hanziToAddNoteList:
        showInfo( "Found note: %s" % (str(hanziNote)))
        #note = mw.col.getNote(nid)
        model = masterNoteModelFile
        
        # Assign model to deck
        mw.col.decks.select(deck['id'])
        mw.col.decks.get(deck)['mid'] = model['id']
        mw.col.decks.save(deck)

        # Assign deck to model
        mw.col.models.setCurrent(model)
        mw.col.models.current()['did'] = deck['id']
        mw.col.models.save(model)
        
        # Create new note
        note_toAdd = mw.col.newNote()
        # Copy tags and fields (all model fields) from original note
        #note_toAdd.tags = note.tags
        #note_toAdd.fields = note.fields
        note_toAdd[master_Hanzi_SrcField]= hanziNote[1]
        note_toAdd['Traditional'] = hanziNote[2]
        note_toAdd['FrequencyRank'] = str(hanziNote[0])
        note_toAdd['Pinyin'] = hanziNote[4]
        note_toAdd['Pinyin 2'] = hanziNote[5]
        note_toAdd['Meaning'] = hanziNote[6]
        note_toAdd[master_Auto_Sentence_SrcField]= hanziNote[8][0]
        note_toAdd[master_Auto_SR_SrcField] = hanziNote[8][1]
        note_toAdd[master_Auto_ST_SrcField] = hanziNote[8][2]
        note_toAdd[master_Auto_SA_SrcField] = hanziNote[8][3]
        # Refresh note and add to database
        note_toAdd.flush()
        mw.col.addNote(note_toAdd)
        
    # Reset collection and main window
    
    mw.col.reset()
    showInfo( "collection has been reset")
    mw.progress.finish()
    mw.reset()
    showInfo( "All done !")

def get_Correct_Slave_List_For_Current_Note(note):
        result = []
        for k in slave_Model_Sentence_SPinyin_SMeaning_SAudio_List:
            if k[0] in note.model()['name']:
                result = k
        return result

def Generate_Slave_Hanzi_Index(nids):
    mw.checkpoint("Bulk-Generate Generate_Slave_Hanzi_Index")
    mw.progress.start()
    reload_config()
    Slave_Hanzi_Dict = {}
    HanziFreqList = []
    with open("C:/Users/Myxoma/AppData/Roaming/Anki2/addons21/999999996/HanziFrequencyList.txt", "r", encoding="utf-8") as f:
       HanziFreqList = [line.split('\t') for line in f]
    warning_counter = 0
    warning_slaveModelNotFound = 0
    warning_slaveSentence_NotFound = 0
    info_Slave_Hanzi_indexed = 0
    info_Slave_Hanzi_not_in_Hanzi_Frequency_List = 0
    HanziOfHanziFreqList = [hanzi[1] for hanzi in HanziFreqList]
    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        mSlaveList = get_Correct_Slave_List_For_Current_Note(note)
        if not mSlaveList:
            #showInfo ("no Note field matched")
            warning_counter += 1
            warning_slaveModelNotFound += 1
            continue
        src_slave_Sentence = None
        if mSlaveList[1] in note:
            src_slave_Sentence = mSlaveList[1]
        if not src_slave_Sentence:
            # no src_slave_Sentence field
            #showInfo ("--> Field %s not found." % (slave_Sentence_SrcField))
            warning_counter += 1
            warning_slaveSentence_NotFound += 1
            continue

        try:
            
            # showInfo ("--> Everything should have worked. Trying Regex")
            for x in note[src_slave_Sentence]:
               if x in HanziOfHanziFreqList:
                    if x not in Slave_Hanzi_Dict:
                        Slave_Hanzi_Dict[x] = [[note[src_slave_Sentence],note[mSlaveList[2]],note[mSlaveList[3]],note[mSlaveList[4]]]]
                        info_Slave_Hanzi_indexed += 1
                    else: 
                        Slave_Hanzi_Dict[x].append([note[src_slave_Sentence],note[mSlaveList[2]],note[mSlaveList[3]],note[mSlaveList[4]]])
                        info_Slave_Hanzi_indexed += 1
               else:
                    info_Slave_Hanzi_not_in_Hanzi_Frequency_List += 1
               #showInfo (str(Slave_Hanzi_Dict[x]))
               #TextOutput = note[src1]
               #note[dst]= str(TotalWordCount)
        except Exception as e:
            raise
        note.flush()
    #showInfo ("Completed Distinct Hanzi Count is %s" %str(len(Slave_Hanzi_List)))
    #showInfo (str(Slave_Hanzi_List))

    
    
    #showInfo (TextOutput)
    showInfo ("--> Generate_Slave_Hanzi_Index.\n warning_counter = %d \n warning_slaveModelNotFound = %d \n warning_slaveSentence_NotFound = %d \n info_Slave_Hanzi_indexed = %d \n info_Slave_Hanzi_not_in_Hanzi_Frequency_List = %d" %(warning_counter,warning_slaveModelNotFound,warning_slaveSentence_NotFound,info_Slave_Hanzi_indexed,info_Slave_Hanzi_not_in_Hanzi_Frequency_List))
    mw.progress.finish()
    mw.reset()
    return Slave_Hanzi_Dict


def BulkGenerateLearned_Hanzi_Cross_Indexing(nids):
    mw.checkpoint("Bulk-Generate TotalWordCount")
    mw.progress.start()
    reload_config()
    HanziFreqList = []
    HanziFreqDict = {}
    with open("C:/Users/Myxoma/AppData/Roaming/Anki2/addons21/999999996/HanziFrequencyList.txt", "r", encoding="utf-8") as f:
       HanziFreqList = [line.split('\t') for line in f]

    showInfo ("Beginning BulkGenerateLearned_Hanzi_Cross_Indexing with this config:\n master_modelName: %s \n master_Hanzi_SrcField: %s \n master_Auto_Sentence_SrcField: %s \n master_Auto_SR_SrcField: %s \n master_Auto_ST_SrcField: %s \n master_Auto_SA_SrcField: %s \n master_Auto_SentenceF_SrcField: %s \n master_Auto_SR_F_SrcField: %s \n master_Auto_ST_F_SrcField: %s \n OVERWRITE_DST_FIELD: %s \n slave_Model_Sentence_SPinyin_SMeaning_SAudio_List: %s " %(master_modelName,master_Hanzi_SrcField,master_Auto_Sentence_SrcField,master_Auto_SR_SrcField,master_Auto_ST_SrcField,master_Auto_SA_SrcField,master_Auto_SentenceF_SrcField,master_Auto_SR_F_SrcField,master_Auto_ST_F_SrcField,OVERWRITE_DST_FIELD, str(slave_Model_Sentence_SPinyin_SMeaning_SAudio_List) ))
    Master_Hanzi_Dict = {}
    Slave_Hanzi_Dict = Generate_Slave_Hanzi_Index(nids)
    info_Distinct_Hanzi_In_Slave_Deck = len(Slave_Hanzi_Dict)
    info_Hanzi_In_Master_Card_but_Not_in_Slave = 0
    info_Total_Changes_Made_To_Master_Card = 0
    masterNoteModelFile = ''
    showInfo ("--> Now on final part. Binding final output to dst !")
    ########################################
    #for Sla_H in Slave_Hanzi_Dict
    ###########################################
    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if master_modelName not in note.model()['name']:
            continue
        #showInfo(str(note.model()))
        #showInfo(str(note._model))
        if not masterNoteModelFile:
            masterNoteModelFile = note._model
        if master_Hanzi_SrcField in note:
            #showInfo ("No issue with master_Hanzi_SrcField")
            print("No issue with master_Hanzi_SrcField")
        else:
            # no master_Hanzi_SrcField field
            #showInfo ("--> Field %s not found." % (master_Hanzi_SrcField))
            continue
        if master_Auto_Sentence_SrcField in note:
            #showInfo ("--> Field %s is found!" % (master_Auto_Sentence_SrcField))
            print("--> Field %s is found!" % (master_Auto_Sentence_SrcField))
        else:
            #showInfo ("--> Field %s not found!" % (master_Auto_Sentence_SrcField))
            # no dst field
            continue
        if note[master_Auto_Sentence_SrcField] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            #showInfo ("--> %s not empty. Skipping!" % (master_Auto_Sentence_SrcField))
            continue
        try:
            a = Slave_Hanzi_Dict.get(note[master_Hanzi_SrcField])
            if not a:
                 #showInfo ("--> cannot find cross ref for %s Skipping!" % note[master_Hanzi_SrcField])
                 info_Hanzi_In_Master_Card_but_Not_in_Slave += 1
                 continue
            del Slave_Hanzi_Dict[note[master_Hanzi_SrcField]]
            #showInfo ("for Hanzi" + note[master_Hanzi_SrcField] + "We will use" + str(a))
            #showInfo ("a[0] = %s" %str(a[0]))
            note[master_Auto_Sentence_SrcField]= a[0][0]
            note[master_Auto_SR_SrcField] = a[0][1]
            note[master_Auto_ST_SrcField] = a[0][2]
            note[master_Auto_SA_SrcField] = a[0][3]
            info_Total_Changes_Made_To_Master_Card += 1
            #note[master_Auto_SentenceF_SrcField] = 'Auto_SentenceF'
            #note[master_Auto_SR_F_SrcField] = 'Auto_SR_F'
            #note[master_Auto_ST_F_SrcField] = 'Auto_ST_F'
        except Exception as e:
            raise
        note.flush()

    ## Now to deal with slave hanzi that does not exist in master deck
    info_Hanzi_In_Slave_Card_but_Not_in_Master = len(Slave_Hanzi_Dict)
    showInfo ("--> Everything should have worked.\n info_Hanzi_In_Master_Card_but_Not_in_Slave = %d \n info_Total_Changes_Made_To_Master_Card = %d \n info_Distinct_Hanzi_In_Slave_Deck = %d \n info_Hanzi_In_Slave_Card_but_Not_in_Master = %d" %(info_Hanzi_In_Master_Card_but_Not_in_Slave,info_Total_Changes_Made_To_Master_Card,info_Distinct_Hanzi_In_Slave_Deck,info_Hanzi_In_Slave_Card_but_Not_in_Master))
    #convert frequency list to dict

    SlaveNoteToAdd = []
    for Slave_Hanzi_Not_in_Master in Slave_Hanzi_Dict:
        for HanziF in HanziFreqList:
            if (HanziF[1] == Slave_Hanzi_Not_in_Master):
                SlaveNoteToAdd.append(HanziF + Slave_Hanzi_Dict.get(Slave_Hanzi_Not_in_Master))
                break

    showInfo ("List of Hanzi_In_Slave_Card_but_Not_in_Master: %s" %str(Slave_Hanzi_Dict.keys()))
    showInfo ("Now test add note")
    showInfo ("note to add = %s " %str(SlaveNoteToAdd))
    #dummyNoteToAdd = [[6352,"糗","",99.98774599,"qiǔ","","(surname)/dryprovisions",36],[6353,"鸮","鴞",99.9877646,"xiāo","","",36],[6354,"蕰","",99.9877832,"wēn","","",36],[6355,"坼","",99.9878018,"chè","","tocrack/split/break/tochap",36]]
    createAnkiNote(SlaveNoteToAdd,masterNoteModelFile)
    mw.progress.finish()
    mw.reset()

def BulkGenerateLearned_Hanzi_Cross_Indexing_OLD_BACKUP(nids):
    mw.checkpoint("Bulk-Generate TotalWordCount")
    mw.progress.start()
    reload_config()
    showInfo ("Beginning BulkGenerateLearned_Hanzi_Cross_Indexing with this config:\n master_modelName: %s \n master_Hanzi_SrcField: %s \n master_Auto_Sentence_SrcField: %s \n master_Auto_SR_SrcField: %s \n master_Auto_ST_SrcField: %s \n master_Auto_SA_SrcField: %s \n master_Auto_SentenceF_SrcField: %s \n master_Auto_SR_F_SrcField: %s \n master_Auto_ST_F_SrcField: %s \n OVERWRITE_DST_FIELD: %s \n slave_Model_Sentence_SPinyin_SMeaning_SAudio_List: %s " %(master_modelName,master_Hanzi_SrcField,master_Auto_Sentence_SrcField,master_Auto_SR_SrcField,master_Auto_ST_SrcField,master_Auto_SA_SrcField,master_Auto_SentenceF_SrcField,master_Auto_SR_F_SrcField,master_Auto_ST_F_SrcField,OVERWRITE_DST_FIELD, str(slave_Model_Sentence_SPinyin_SMeaning_SAudio_List) ))
    Master_Hanzi_Dict = {}
    Slave_Hanzi_Dict = Generate_Slave_Hanzi_Index(nids)
    info_Hanzi_In_Master_Card_but_Not_in_Slave = 0
    info_Total_Changes_Made_To_Master_Card = 0
    masterNoteModelFile = ''
    showInfo ("--> Now on final part. Binding final output to dst !")
    ########################################
    #for Sla_H in Slave_Hanzi_Dict
    ###########################################
    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if master_modelName not in note.model()['name']:
            continue
        #showInfo(str(note.model()))
        #showInfo(str(note._model))
        if not masterNoteModelFile:
            masterNoteModelFile = note._model
        if master_Hanzi_SrcField in note:
            #showInfo ("No issue with master_Hanzi_SrcField")
            print("No issue with master_Hanzi_SrcField")
        else:
            # no master_Hanzi_SrcField field
            #showInfo ("--> Field %s not found." % (master_Hanzi_SrcField))
            continue
        if master_Auto_Sentence_SrcField in note:
            #showInfo ("--> Field %s is found!" % (master_Auto_Sentence_SrcField))
            print("--> Field %s is found!" % (master_Auto_Sentence_SrcField))
        else:
            #showInfo ("--> Field %s not found!" % (master_Auto_Sentence_SrcField))
            # no dst field
            continue
        if note[master_Auto_Sentence_SrcField] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            #showInfo ("--> %s not empty. Skipping!" % (master_Auto_Sentence_SrcField))
            continue
        try:
            a = Slave_Hanzi_Dict.get(note[master_Hanzi_SrcField])
            if not a:
                 #showInfo ("--> cannot find cross ref for %s Skipping!" % note[master_Hanzi_SrcField])
                 info_Hanzi_In_Master_Card_but_Not_in_Slave += 1
                 continue
            #showInfo ("for Hanzi" + note[master_Hanzi_SrcField] + "We will use" + str(a))
            #showInfo ("a[0] = %s" %str(a[0]))
            note[master_Auto_Sentence_SrcField]= a[0][0]
            note[master_Auto_SR_SrcField] = a[0][1]
            note[master_Auto_ST_SrcField] = a[0][2]
            note[master_Auto_SA_SrcField] = a[0][3]
            info_Total_Changes_Made_To_Master_Card += 1
            #note[master_Auto_SentenceF_SrcField] = 'Auto_SentenceF'
            #note[master_Auto_SR_F_SrcField] = 'Auto_SR_F'
            #note[master_Auto_ST_F_SrcField] = 'Auto_ST_F'
        except Exception as e:
            raise
        note.flush()

    
    showInfo ("--> Everything should have worked.\n info_Hanzi_In_Master_Card_but_Not_in_Slave = %d \n info_Total_Changes_Made_To_Master_Card = %d " %(info_Hanzi_In_Master_Card_but_Not_in_Slave,info_Total_Changes_Made_To_Master_Card))
    showInfo ("Now test add note")
    dummyNoteToAdd = [[6352,"糗","",99.98774599,"qiǔ","","(surname)/dryprovisions",36],[6353,"鸮","鴞",99.9877646,"xiāo","","",36],[6354,"蕰","",99.9877832,"wēn","","",36],[6355,"坼","",99.9878018,"chè","","tocrack/split/break/tochap",36]]
    createAnkiNote(dummyNoteToAdd,masterNoteModelFile)
    mw.progress.finish()
    mw.reset()
    
def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Bulk_Generate_learned_Hanzi_Cross_Indexing')
    a.triggered.connect(lambda _, b=browser: onBulkGenerateLearned_Hanzi_Cross_Indexing(b))

def onBulkGenerateLearned_Hanzi_Cross_Indexing(browser):
    BulkGenerateLearned_Hanzi_Cross_Indexing(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
