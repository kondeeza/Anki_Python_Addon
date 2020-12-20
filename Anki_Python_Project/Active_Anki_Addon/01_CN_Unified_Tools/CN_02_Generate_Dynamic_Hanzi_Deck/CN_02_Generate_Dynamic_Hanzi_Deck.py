# -*- coding: utf-8 -*-
# Copyright: mo  <paradoxez919@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# Bulk copy data in one field to another.
# TODO: copy batch edit add on templete. first choose hanzi-kanji master deck & note type.
# TODO: field list should be automatically filled in
# TODO: then option to choose slave deck note type & choose which field to match
# Auto Sentence supplementary LIST
# Sync Hint field. maybe for all note that shared audio file, allowing user to mark field with ** or something to be the most recent update. or maybe just simply copy along the note field to master.
# GUI? nah
# Factorise , i.e. Move all pre validation of note field etc into prevalidate() or something. then make reporting info more informative
# Factorise , remove fuzzy shotgun coding, or maybe seperate into different python. test git commmit

# NOTE TO SELF, don't call showInfo  inside/after mw.progress.start() or you wouldn't be able to click the dialog
##########################################################################

# FIND AND ADD EXAMPLE SENTENCES FROM YOUR OTHER DECKS INTO YOUR HANZI DECK. BECAUSE HAVING SENTENCE EXAMPLE MAKE MEMORISING CHARACTERS THAT MUCH EASIER

##########################################################################
from aqt.qt import *
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning, showInfo, tooltip
import re
import platform
import re
import os
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE
import sys

# reload(sys) #apparently this doesn't work in python3...
# sys.setdefaultencoding('utf-8')
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE !!

master_modelName = ''
master_Hanzi_SrcField = ''
master_Auto_Sentence_SrcField = ''
master_Auto_SR_SrcField = ''
master_Auto_ST_SrcField = ''
master_Auto_SA_SrcField = ''
#master_Auto_SentenceF_SrcField = ''
#master_Auto_SR_F_SrcField = ''
#master_Auto_ST_F_SrcField = ''
master_Auto_Synced_Hint_SrcField = ''
master_deckName = ''
Enable_Optional_Custom_MasterSlaveSyncFieldList = ''
master_Traditional_Field = ''
master_Freq_Field = ''
master_Pinyin_Field = ''
master_Pinyin2_Field = ''
master_meaning_Field = ''
master_CardCreate_Other1_field = ''
master_CardCreate_Other2_field = ''
master_other1_Field = ''
master_other2_Field = ''
master_other3_Field = ''
tag_for_note_used_as_hanzi_sentence_example = 'used_as_hanzi_sentence_example'
# if data exists in Output_SrcField, should we overwrite it?
OVERWRITE_DST_FIELD = ''

slave_Model_Sentence_SPinyin_SMeaning_SAudio_List = []
#ConfigDict = {" ": " "}
debugMode = False
query_input= ''

def findNotes( query=None):
    if query is None:
        return []
    else:
        return list(map(int, mw.col.findNotes(query)))
        
class HanziIndexDialog(QDialog):
    """Main dialog"""

    def __init__(self, browser, nids):
        QDialog.__init__(self, parent=browser)
        self.browser = browser
        self.nids = nids
        self._setupUi()

    def _setupUi(self):
        reload_config()
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Kanji Deck Name', 'Kanji Hanzi', 'Kanji Traditional', 'Kanji Frequency','Kanji Pinyin','Kanji Pinyin2','Kanji Meaning','Kanji Other Field1','Kanji Other Field2',
                 ' ', '', '', '', '', '', '', '', '',
                 'Kanji Notetype','KanjiDeck Auto_Sentence', 'KanjiDeck Auto_Sentence Reading', 'KanjiDeck Auto_Sentence Translation', 'KanjiDeck Auto_Sentence Audio', 'KanjiDeck Auto_Hint', 'Others_1','Others_2','Others_3',
                 '', '', '', '', '', '', '', '', '',
                 'Vocab Notetype','VocabDeck Sentence', 'VocabDeck Sentence Reading', 'VocabDeck Sentence Translation', 'VocabDeck Sentence Audio', 'VocabDeck Hint', 'Others_1','Others_2','Others_3',
                 '', '', '', '', '', '', '', '', '',]



        positions = [(i, j) for i in range(6) for j in range(9)]

        for position, name in zip(positions, names):

            if name == '':
                continue
            label = QLabel(name)
            #showInfo("adding grid widget, button = %s , and position =  %s" % (name, str(position)))
            grid.addWidget(label, *position)

        save_button = QPushButton("Save Config")
        save_button.clicked.connect(lambda state, x="save": self.onConfirm(x))
        run_button = QPushButton("Run")
        run_button.clicked.connect(lambda state, x="run": self.onConfirm(x))
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        grid.addWidget(QLabel(" "), 16, 0)
        grid.addWidget(save_button, 17,6)
        grid.addWidget(run_button, 17,7)
        grid.addWidget(cancel_button, 17,8)

        "Deck Selection Box"
        self.dsel = QComboBox()
        decks = self._getDeckLists()
        self.dsel.addItems([master_deckName] + decks)
        grid.addWidget(self.dsel, 1, 0)


        self.kanjiNotebox = QComboBox()
        noteType = self._getNoteTypeLists()
        self.kanjiNotebox.addItems([master_modelName] + noteType)
        self.kanjiNotebox.currentIndexChanged.connect(
            lambda state, x="QComboBox_Note_Updated_KJ": self.onQBoxUpdate(x))
        grid.addWidget(self.kanjiNotebox, 3, 0)

        Global_KC_Var = [master_Hanzi_SrcField, master_Traditional_Field, master_Freq_Field, master_Pinyin_Field ,master_Pinyin2_Field, master_meaning_Field,master_CardCreate_Other1_field,master_CardCreate_Other2_field]

        self.kanjiNewCardFieldbox = [None] * len(Global_KC_Var)
        for i in range(0,8):
            "Kanji kanjiNewCardFieldbox"
            self.kanjiNewCardFieldbox[i] = QComboBox()
            fields = self._getFieldsFromNoteType(self.kanjiNotebox.currentText())
            self.kanjiNewCardFieldbox[i].addItems([Global_KC_Var[i]]+fields)
            grid.addWidget(self.kanjiNewCardFieldbox[i], 1, int(i+1))

        Global_KF_Var = [master_Auto_Sentence_SrcField,master_Auto_SR_SrcField,master_Auto_ST_SrcField,master_Auto_SA_SrcField,master_Auto_Synced_Hint_SrcField,master_other1_Field, master_other2_Field, master_other3_Field]
        self.kanjiFieldbox = [None] * len(Global_KF_Var)
        for i in range(0,8):
            "Kanji Field Selection Box"
            self.kanjiFieldbox[i] = QComboBox()
            fields = self._getFieldsFromNoteType(self.kanjiNotebox.currentText())
            #showInfo(str(Global_KF_Var[i]))
            #showInfo(Global_KF_Var[i])
            self.kanjiFieldbox[i].addItems([Global_KF_Var[i]] + fields)
            grid.addWidget(self.kanjiFieldbox[i], 3, int(i+1))


        self.vocabNoteBox = [None] * 10
        for i in range(0,10):

            self.vocabNoteBox[i] = QComboBox()
            noteType = self._getNoteTypeLists()
            if len(slave_Model_Sentence_SPinyin_SMeaning_SAudio_List)-1 >= i:
                # if not ran out of slave note type. else, just add ' '
                self.vocabNoteBox[i].addItems([slave_Model_Sentence_SPinyin_SMeaning_SAudio_List[i][0]] + noteType)
            else:
                self.vocabNoteBox[i].addItems([""] + noteType)
            self.vocabNoteBox[i].currentIndexChanged.connect(lambda state, x="QComboBox_Note_Updated_%d" % i: self.onQBoxUpdate(x))
            grid.addWidget(self.vocabNoteBox[i], int(i+5), 0)

        "Field Selection Box"
        self.vocabFieldBox_YX = [[None for x in range(8)] for y in range(10)]
        # self.vocabFieldBox = [None] * 10
        for y in range(0, 10):
            for x in range(0, 8):
                self.vocabFieldBox_YX[y][x] = QComboBox()
                fields = self._getFieldsFromNoteType(self.vocabNoteBox[y].currentText())
                if len(slave_Model_Sentence_SPinyin_SMeaning_SAudio_List) - 1 >= y:
                    if len(slave_Model_Sentence_SPinyin_SMeaning_SAudio_List[y]) - 2 >= x:
                        self.vocabFieldBox_YX[y][x].addItems([slave_Model_Sentence_SPinyin_SMeaning_SAudio_List[y][x+1]] + fields)
                    else:
                        self.vocabFieldBox_YX[y][x].addItems([""]+fields)
                else:
                    self.vocabFieldBox_YX[y][x].addItems([""]+fields)
                grid.addWidget(self.vocabFieldBox_YX[y][x], int(y+5), int(1+x))

        self.move(300, 150)


        self.setMinimumWidth(540)
        self.setMinimumHeight(400)
        self.setWindowTitle("Hanzi Index Dialog Configuration page")

    def _getFields(self):
        nid = self.nids[0]
        mw = self.browser.mw
        model = mw.col.getNote(nid).model()
        fields = mw.col.models.fieldNames(model)

        return fields

    def _getDeckLists(self):
        """Return All Deck List in Anki DB"""
        #showInfo(str(mw.col.decks.allNames()))
        return mw.col.decks.allNames()

    def _getNoteTypeLists(self):
        """Return All Notetype List in Anki DB"""
        #showInfo(str(mw.col.models.allNames()))
        result = mw.col.models.allNames()
        result.append("")
        return result

    def _getFieldsFromNoteType(self,NoteTypeName):
        model = mw.col.models.byName(NoteTypeName)
        if model is not None:
            fields = mw.col.models.fieldNames(model)
            fields.append("")
        else:
            fields = [""]
        return fields

    def onQBoxUpdate(self, mode):
            # if mode == "QComboBox_Note_Updated":
            #showInfo("Box updated, mode is %s" % mode)

            if mode == "QComboBox_Note_Updated_KJ":
                for i in range(0, 8):
                    self.kanjiFieldbox[i].clear()
                    fields = self._getFieldsFromNoteType(self.kanjiNotebox.currentText())
                    self.kanjiFieldbox[i].addItems(fields)
                for i in range(0, 6):
                    self.kanjiNewCardFieldbox[i].clear()
                    fields = self._getFieldsFromNoteType(self.kanjiNotebox.currentText())
                    self.kanjiNewCardFieldbox[i].addItems(fields)


            for y in range(0, 10):
                if mode == "QComboBox_Note_Updated_%d" % y:
                    for x in range(0, 8):
                        self.vocabFieldBox_YX[y][x].clear()
                        fields = self._getFieldsFromNoteType(self.vocabNoteBox[y].currentText())
                        self.vocabFieldBox_YX[y][x].addItems(fields)


    def onConfirm(self, mode):
            """Current save limitation is on the kanji(master) card creation field. The variable name is hard wired"""

            global master_modelName
            global master_Hanzi_SrcField
            global master_Auto_Sentence_SrcField
            global master_Auto_SR_SrcField
            global master_Auto_ST_SrcField
            global master_Auto_SA_SrcField
            # global master_Auto_SentenceF_SrcField
            # global master_Auto_SR_F_SrcField
            # global master_Auto_ST_F_SrcField
            global OVERWRITE_DST_FIELD
            global slave_Model_Sentence_SPinyin_SMeaning_SAudio_List
            global master_deckName
            global master_Auto_Synced_Hint_SrcField
            global Enable_Optional_Custom_MasterSlaveSyncFieldList
            global master_Traditional_Field
            global master_Freq_Field
            global master_Pinyin_Field
            global master_Pinyin2_Field
            global master_meaning_Field
            global master_CardCreate_Other1_field
            global master_CardCreate_Other2_field
            global master_other1_Field
            global master_other2_Field
            global master_other3_Field
            tooltip("Saving master_modelName & master_deckName: %s" % mode)
            master_deckName = self.dsel.currentText()
            master_modelName = self.kanjiNotebox.currentText()

            master_Hanzi_SrcField = self.kanjiNewCardFieldbox[0].currentText()
            master_Traditional_Field = self.kanjiNewCardFieldbox[1].currentText()
            master_Freq_Field = self.kanjiNewCardFieldbox[2].currentText()
            master_Pinyin_Field = self.kanjiNewCardFieldbox[3].currentText()
            master_Pinyin2_Field = self.kanjiNewCardFieldbox[4].currentText()
            master_meaning_Field = self.kanjiNewCardFieldbox[5].currentText()
            master_CardCreate_Other1_field = self.kanjiNewCardFieldbox[6].currentText()
            master_CardCreate_Other2_field = self.kanjiNewCardFieldbox[7].currentText()

            master_Auto_Sentence_SrcField = self.kanjiFieldbox[0].currentText()
            master_Auto_SR_SrcField = self.kanjiFieldbox[1].currentText()
            master_Auto_ST_SrcField = self.kanjiFieldbox[2].currentText()
            master_Auto_SA_SrcField = self.kanjiFieldbox[3].currentText()
            master_Auto_Synced_Hint_SrcField = self.kanjiFieldbox[4].currentText()
            master_other1_Field = self.kanjiFieldbox[5].currentText()
            master_other2_Field = self.kanjiFieldbox[6].currentText()
            master_other3_Field = self.kanjiFieldbox[7].currentText()

            # let's just make a new slave_Model_Sentence_SPinyin_SMeaning_SAudio_List from the beginning and clone it instead

            TempVocabFieldAndNote_NameList = [[None for zz in range(9)] for yy in range(10)]
            # that's [10][9] 10 for 10 row, and 1 note field + 8 note field. note field at [x][0]. vocab at [x][1-8]
            for y in range(0, 10):
                for x in range(0, 8):
                    #howInfo("TempVocabNameList[y][x + 1] y is %d  x is %d x+1 is %d" %(y,x,x+1))
                    TempVocabFieldAndNote_NameList[y][x + 1] = self.vocabFieldBox_YX[y][x].currentText()

            #showInfo(str(TempVocabFieldAndNote_NameList))

            for i in list(reversed(range(0,10))):
                # start in reversed order to avoid issue with popping out of range list
                if self.vocabNoteBox[i].currentText():
                    # if vocab model name not null, then save.
                    TempVocabFieldAndNote_NameList[i][0] = self.vocabNoteBox[i].currentText()
                else:
                    # otherwise, delete the whole row for that model+vocab field
                    TempVocabFieldAndNote_NameList.pop(i)

            #showInfo(str(TempVocabFieldAndNote_NameList))
            slave_Model_Sentence_SPinyin_SMeaning_SAudio_List = TempVocabFieldAndNote_NameList
            save_config()

            if mode == "run":
                BulkGenerateLearned_Hanzi_Cross_Indexing(self.browser.selectedNotes())


def save_config():
    global master_modelName
    global master_Hanzi_SrcField
    global master_Auto_Sentence_SrcField
    global master_Auto_SR_SrcField
    global master_Auto_ST_SrcField
    global master_Auto_SA_SrcField
    # global master_Auto_SentenceF_SrcField
    # global master_Auto_SR_F_SrcField
    # global master_Auto_ST_F_SrcField
    global OVERWRITE_DST_FIELD
    global slave_Model_Sentence_SPinyin_SMeaning_SAudio_List
    global master_deckName
    global master_Auto_Synced_Hint_SrcField
    global Enable_Optional_Custom_MasterSlaveSyncFieldList
    global master_Traditional_Field
    global master_Freq_Field
    global master_Pinyin_Field
    global master_Pinyin2_Field
    global master_meaning_Field
    global master_CardCreate_Other1_field
    global master_CardCreate_Other2_field
    global master_other1_Field
    global master_other2_Field
    global master_other3_Field

    # unused are OVERWRITE_DST_FIELD
    config = mw.addonManager.getConfig(__name__)
    config['02_01_master_modelName'] = master_modelName
    config['02_10_master_deckName'] = master_deckName

    config['02_02_master_Hanzi_SrcField'] = master_Hanzi_SrcField
    config['02_21_master_Traditional_Field'] = master_Traditional_Field
    config['02_22_master_Freq_Field'] = master_Freq_Field
    config['02_23_master_Pinyin_Field'] = master_Pinyin_Field
    config['02_24_master_Pinyin2_Field'] = master_Pinyin2_Field
    config['02_25_master_meaning_Field'] = master_meaning_Field
    config['02_26_master_CardCreate_Other1_field'] = master_CardCreate_Other1_field
    config['02_27_master_CardCreate_Other2_field'] = master_CardCreate_Other2_field

    config['02_03_master_Auto_Sentence_SrcField'] = master_Auto_Sentence_SrcField
    config['02_04_master_Auto_SR_SrcField'] = master_Auto_SR_SrcField
    config['02_05_master_Auto_ST_SrcField'] = master_Auto_ST_SrcField
    config['02_06_master_Auto_SA_SrcField'] = master_Auto_SA_SrcField
    config['02_11_master_Auto_Synced_Hint_SrcField'] = master_Auto_Synced_Hint_SrcField
    config['02_07_master_other1_Field'] = master_other1_Field
    config['02_08_master_other2_Field'] = master_other2_Field
    config['02_09_master_other3_Field'] = master_other3_Field

    config['02_16_slave_Model_Sentence_SPinyin_SMeaning_SAudio_List'] = slave_Model_Sentence_SPinyin_SMeaning_SAudio_List

    mw.addonManager.writeConfig(__name__, config)



def reload_config():
    global master_modelName
    global master_Hanzi_SrcField
    global master_Auto_Sentence_SrcField
    global master_Auto_SR_SrcField
    global master_Auto_ST_SrcField
    global master_Auto_SA_SrcField
    # global master_Auto_SentenceF_SrcField
    # global master_Auto_SR_F_SrcField
    # global master_Auto_ST_F_SrcField
    global OVERWRITE_DST_FIELD
    global slave_Model_Sentence_SPinyin_SMeaning_SAudio_List
    global master_deckName
    global master_Auto_Synced_Hint_SrcField
    global Enable_Optional_Custom_MasterSlaveSyncFieldList
    global master_Traditional_Field
    global master_Freq_Field
    global master_Pinyin_Field
    global master_Pinyin2_Field
    global master_meaning_Field
    global master_CardCreate_Other1_field
    global master_CardCreate_Other2_field
    global master_other1_Field
    global master_other2_Field
    global master_other3_Field
    global query_input
    config = mw.addonManager.getConfig(__name__)
    master_modelName = config['02_01_master_modelName']
    master_Hanzi_SrcField = config['02_02_master_Hanzi_SrcField']
    master_Auto_Sentence_SrcField = config['02_03_master_Auto_Sentence_SrcField']
    master_Auto_SR_SrcField = config['02_04_master_Auto_SR_SrcField']
    master_Auto_ST_SrcField = config['02_05_master_Auto_ST_SrcField']
    master_Auto_SA_SrcField = config['02_06_master_Auto_SA_SrcField']
    #master_Auto_SentenceF_SrcField = config['02_07_master_Auto_SentenceF_SrcField']
    #master_Auto_SR_F_SrcField = config['02_08_master_Auto_SR_F_SrcField']
    #master_Auto_ST_F_SrcField = config['02_09_master_Auto_ST_F_SrcField']
    OVERWRITE_DST_FIELD = config['02_15_OVERWRITE_DST_FIELD']
    master_deckName = config['02_10_master_deckName']
    master_Auto_Synced_Hint_SrcField = config['02_11_master_Auto_Synced_Hint_SrcField']
    slave_Model_Sentence_SPinyin_SMeaning_SAudio_List = config['02_16_slave_Model_Sentence_SPinyin_SMeaning_SAudio_List']
    Enable_Optional_Custom_MasterSlaveSyncFieldList = config['02_13_Enable_Optional_Custom_MasterSlaveSyncFieldList']

    master_Traditional_Field = config['02_21_master_Traditional_Field']
    master_Freq_Field = config['02_22_master_Freq_Field']
    master_Pinyin_Field = config['02_23_master_Pinyin_Field']
    master_Pinyin2_Field = config['02_24_master_Pinyin2_Field']
    master_meaning_Field = config['02_25_master_meaning_Field']
    master_CardCreate_Other1_field = config['02_26_master_CardCreate_Other1_field']
    master_CardCreate_Other2_field = config['02_27_master_CardCreate_Other2_field']

    master_other1_Field = config['02_07_master_other1_Field']
    master_other2_Field = config['02_08_master_other2_Field']
    master_other3_Field = config['02_09_master_other3_Field']
    query_input = config['02_30_query_input']




def validateFieldList(nids):
    # TODO: 1. validate Master & Slave Note exist, Deck exist 2. validate master and slave fields exist 3. also validate correct field list syntax input
    # TODO: if validate did not pass (i.e field not exist), prompt user and abort program. else, return true and proceed. This is for simplifying Hanzi and kanji validation compatability process
    return True


def createAnkiNote(hanziToAddNoteList):
    mw.checkpoint("Manual Create Note")


    # Get desired deck name from input box
    deckName = master_deckName
    if not deckName:
        return
    # deckName = deckName.replace('"', "")

    # Create new deck with name from input box
    deck = mw.col.decks.get(mw.col.decks.id(deckName))
    #showInfo(str(deck))
    # Copy notes
    for hanziNote in hanziToAddNoteList:
        tooltip("Found note: %s" % (str(hanziNote)))
        # note = mw.col.getNote(nid)
        model = mw.col.models.byName(master_modelName)

        # Assign model to deck
        mw.col.decks.select(deck['id'])
        #showInfo("Model file is %s " %str(model))
        #showInfo("deck is %s " %str(deck))
        #mw.col.decks.get(deck)['mid'] = model['id']  
        deck['mid'] = model['id']
        #showInfo("Creating card On Deck:%s with model name: %s"%( str(deck['name']), str(model['name'])))
        mw.col.decks.save(deck)

        # Assign deck to model
        mw.col.models.setCurrent(model)
        mw.col.models.current()['did'] = deck['id']
        mw.col.models.save(model)
        # Create new note
        note_toAdd = mw.col.newNote()
        # Copy tags and fields (all model fields) from original note
        # note_toAdd.tags = note.tags
        # note_toAdd.fields = note.fields
        note_toAdd[master_Hanzi_SrcField] = hanziNote[1]
        if master_Traditional_Field:
            note_toAdd[master_Traditional_Field] = hanziNote[2]
        if master_Freq_Field:
            note_toAdd[master_Freq_Field] = str(hanziNote[0])
        if master_Pinyin_Field:
            note_toAdd[master_Pinyin_Field] = hanziNote[4]
        if master_Pinyin2_Field:
            note_toAdd[master_Pinyin2_Field] = hanziNote[5]
        if master_meaning_Field:
            note_toAdd[master_meaning_Field] = hanziNote[6]

        if hanziNote[8][0]:
            note_toAdd[master_Auto_Sentence_SrcField] = hanziNote[8][0]
        if hanziNote[8][1] and master_Auto_SR_SrcField:
            note_toAdd[master_Auto_SR_SrcField] = hanziNote[8][1]
        if hanziNote[8][2] and master_Auto_ST_SrcField:
            note_toAdd[master_Auto_ST_SrcField] = hanziNote[8][2]
        if hanziNote[8][3] and master_Auto_SA_SrcField:
            note_toAdd[master_Auto_SA_SrcField] = hanziNote[8][3]
        if hanziNote[8][4] and master_Auto_Synced_Hint_SrcField:
            note_toAdd[master_Auto_Synced_Hint_SrcField] = hanziNote[8][4]
        if hanziNote[8][5] and master_other1_Field:
            note_toAdd[master_other1_Field] = hanziNote[8][5]
        if hanziNote[8][6] and master_other2_Field:
            note_toAdd[master_other2_Field] = hanziNote[8][6]
        if hanziNote[8][7] and master_other3_Field:
            note_toAdd[master_other3_Field] = hanziNote[8][7]

        """
        if len(hanziNote[8]) >= 6 and Enable_Optional_Custom_MasterSlaveSyncFieldList == True:
            note_toAdd[hanziNote[8][5][0]] = hanziNote[8][5][1]
        """
        # Refresh note and add to database
        #note_toAdd.flush() #This gives error for some reason. . . .
        mw.col.addNote(note_toAdd)

    # Reset collection and main window

    mw.col.reset()
    mw.progress.finish()
    mw.reset()
    tooltip("All done ! collection has been reset")


def get_Correct_Slave_Schema_List_For_Current_Note(note):
    # this will return the correct slave schema for current note input.
    # result would be from one of the list inside slave_Model_Sentence_SPinyin_SMeaning_SAudio_List
    # for example, result could be
    #  [
    #    "HSK",
    #    "SentenceSimplified",
    #    "SentencePinyinMarks",
    #    "SentenceMeaning",
    #    "SentenceAudio",
    #    "Note",
    #    "Key"
    #  ]
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
    # Slave_Hanzi_Dict = { '我':[ ['我爱你','wo3 ai4 ni3,'i love you','very simple','２０'],
    # ['你爱我',,,,'２０'] ] , etc}
    # Slave_Hanzi_Dict['我'] = [['我爱你','wo3 ai4 ni3,'i love you','very simple','２０'],  ['你爱我',,,,'２０'] ]

    HanziFreqList = []
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, "HanziFrequencyList.txt"), "r", encoding="utf-8") as f:
        HanziFreqList = [line.split('\t') for line in f]
    warning_counter = 0
    warning_slaveModelNotFound = 0
    warning_slaveSentence_NotFound = 0
    info_Slave_Hanzi_indexed = 0
    info_Slave_Hanzi_not_in_Hanzi_Frequency_List = 0
    HanziOfHanziFreqList = [hanzi[1] for hanzi in HanziFreqList]
    # HanziFreqList Example [x][0]= 21, [x][1] = 地, [x][2] =地(traditional), [x][3] 20.22369169, [x][4]= de,
    # [x][5] = dì [x][6] = earth / ground / field / place / land
    # [x][7] =  969349
    # HanziOfHanziFreqList = HanziFreqList[x][1] = 地, i.e. just hanzi list to be searched against
    for nid in nids:
        # showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        cSlaveSchema = get_Correct_Slave_Schema_List_For_Current_Note(note)
        #showInfo("cSlaveSchema is %s " %str(cSlaveSchema))
        if not cSlaveSchema:
            # showInfo ("no Model matched")
            warning_counter += 1
            warning_slaveModelNotFound += 1
            continue
        slave_sentence_FieldName = None
        # check to see if note indeed contain the field from cSlaveSchema. This should be moved to validation() later
        # cSlaveSchema[0] will always be its note type name e.g. "My Basic Note Type"
        # cSlaveSchema[1] will always be slave sentence schema e.g. "Vocab Sentence Field"
        if cSlaveSchema[1] in note:
            slave_sentence_FieldName = cSlaveSchema[1]
            #showInfo("slave_sentence_FieldName is %s " % str(slave_sentence_FieldName))
        if not slave_sentence_FieldName:
            # no slave_sentence_FieldName field
            # showInfo ("--> Field %s not found." % (slave_Sentence_SrcField))
            warning_counter += 1
            warning_slaveSentence_NotFound += 1
            continue

        try:

            # This code turn string from slave_Sentence Field into char, then check for each char
            # whether it is in HanziOfHanziFreqList or not, if it is then that char is Hanzi character
            # and it will be indexed in Slave_Hanzi_Dict[x] where x = Hanzi
            # Slave_Hanzi_Dict[x] will return
            for x in note[slave_sentence_FieldName]:
                if x in HanziOfHanziFreqList:
                    cSlave_ToIndex_Note = []
                    # currentoopCount is used to skip cSlaveSchema[0], a.k.a. Slave note name, from being added into Slave_Hanzi_Dict[x]
                    currentloopCount = 0
                    for i in cSlaveSchema:
                        if currentloopCount != 0:
                                #if isinstance(i, str):
                                # condition to catch the None type. i.e cSlave_ToIndex_Note.append(note.get(""))
                                # because using cSlave_ToIndex_Note.append(note[""]) will return error
                                if i is not None and i != "":
                                    cSlave_ToIndex_Note.append(note[i])
                                else:
                                    cSlave_ToIndex_Note.append("")

                        currentloopCount += 1
                    if x not in Slave_Hanzi_Dict:
                        Slave_Hanzi_Dict[x] = [cSlave_ToIndex_Note]
                        info_Slave_Hanzi_indexed += 1
                        if tag_for_note_used_as_hanzi_sentence_example:
                            note.addTag(tag_for_note_used_as_hanzi_sentence_example) # for adding tags to Note in vocab deck that is used as hanzi sentence example. Useful is user wants to prioritise their study vocab with new distinct Hanzi
                        else:
                            pass
                    else:
                        Slave_Hanzi_Dict[x].append(cSlave_ToIndex_Note)
                        info_Slave_Hanzi_indexed += 1
                else:
                    info_Slave_Hanzi_not_in_Hanzi_Frequency_List += 1
                    #showInfo("Slave_Hanzi_not_in_Hanzi_Frequency_List, note[slave_sentence_FieldName] is %s , x is %s" %(str(note[slave_sentence_FieldName]), str(x)))
                    # showInfo (str(Slave_Hanzi_Dict[x]))
                    # TextOutput = note[src1]
                    # note[dst]= str(TotalWordCount)
        except Exception as e:
            raise
        note.flush()
    # showInfo ("Completed Distinct Hanzi Count is %s" %str(len(Slave_Hanzi_List)))
    # showInfo (str(Slave_Hanzi_List))



    # showInfo (TextOutput)
    mw.progress.finish()
    mw.reset()
    if (debugMode):
        showInfo(
            "--> Generate_Slave_Hanzi_Index.\n warning_counter = %d \n warning_slaveModelNotFound = %d \n warning_slaveSentence_NotFound = %d \n info_Slave_Hanzi_indexed = %d \n info_Slave_Hanzi_not_in_Hanzi_Frequency_List = %d" % (
            warning_counter, warning_slaveModelNotFound, warning_slaveSentence_NotFound, info_Slave_Hanzi_indexed,
            info_Slave_Hanzi_not_in_Hanzi_Frequency_List))

    # Slave_Hanzi_Dict should be something like
    # Slave_Hanzi_Dict = { '我':[ ['我爱你','wo3 ai4 ni3,'i love you','very simple','２０'], ['你爱我',,,,'２０'] ] , etc}

    return Slave_Hanzi_Dict


def BulkGenerateLearned_Hanzi_Cross_Indexing(nids):
    mw.checkpoint("Bulk-Generate TotalWordCount")
    reload_config()
    # HanziFreqList contains the list of 10k Hanzi Frequency as: [freq,HanS,HanT,Index,PinY,Meaning,index2]
    HanziFreqList = []
    HanziFreqDict = {}
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, "HanziFrequencyList.txt"), "r", encoding="utf-8") as f:
        HanziFreqList = [line.split('\t') for line in f]

    # showInfo ("Beginning BulkGenerateLearned_Hanzi_Cross_Indexing with this config:\n master_modelName: %s \n master_Hanzi_SrcField: %s \n master_Auto_Sentence_SrcField: %s \n master_Auto_SR_SrcField: %s \n master_Auto_ST_SrcField: %s \n master_Auto_SA_SrcField: %s \n master_Auto_SentenceF_SrcField: %s \n master_Auto_SR_F_SrcField: %s \n master_Auto_ST_F_SrcField: %s \n OVERWRITE_DST_FIELD: %s \n slave_Model_Sentence_SPinyin_SMeaning_SAudio_List: %s " %(master_modelName,master_Hanzi_SrcField,master_Auto_Sentence_SrcField,master_Auto_SR_SrcField,master_Auto_ST_SrcField,master_Auto_SA_SrcField,master_Auto_SentenceF_SrcField,master_Auto_SR_F_SrcField,master_Auto_ST_F_SrcField,OVERWRITE_DST_FIELD, str(slave_Model_Sentence_SPinyin_SMeaning_SAudio_List) ))
    if (debugMode):
        showInfo(
            "Begins BulkGenerateLearned_Hanzi_Cross_Indexing with this config:\n master_modelName: %s \n master_Hanzi_SrcField: %s \n slave_Model_Sentence_SPinyin_SMeaning_SAudio_List %s \n OVERWRITE_DST_FIELD: %s" % (
            master_modelName, master_Hanzi_SrcField, str(slave_Model_Sentence_SPinyin_SMeaning_SAudio_List),
            OVERWRITE_DST_FIELD))
    validateFieldList(nids)
    # TODO: add abort clause if validate return false
    Master_Hanzi_Dict = {}
    Slave_Hanzi_Dict = Generate_Slave_Hanzi_Index(nids)
    # Sample of Slave_Hanzi_Dict, note that we only use the first result of multi list so far.
    # Slave_Hanzi_Dict = { '我':[ ['我爱你','wo3 ai4 ni3,'i love you','very simple','２０'],
    # ['你爱我',,,,'２０'] ] , etc}
    # Slave_Hanzi_Dict['我'] = [['我爱你','wo3 ai4 ni3,'i love you','very simple','２０'],  ['你爱我',,,,'２０'] ]

    info_Distinct_Hanzi_In_Slave_Deck = len(Slave_Hanzi_Dict)
    info_Hanzi_In_Master_Card_but_Not_in_Slave = 0
    info_Total_Changes_Made_To_Master_Card = 0
    if (debugMode):
        showInfo("--> Now on final part. Binding final output to dst !")
    mw.progress.start()
    ########################################
    # for Sla_H in Slave_Hanzi_Dict
    ###########################################
    for nid in nids:
        """For every note card that has the model name matching master/hanzi card:
                search if the hanzi field from master card has match in  slave hanzi dict:
                    if exist, then update master card using the field from slave hanzi dict (Unless overwrite set to false):
                        also delete hanzi entry from slave hanzi dict when the hanzi entry is found:
                            eventually slave hanzi dict will only have entry of hanzi not in master deck left: we then create 
                        """
        # showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if master_modelName not in note.model()['name']:
            continue
        # showInfo(str(note.model()))
        # showInfo(str(note._model))
        if master_Hanzi_SrcField in note:
            #showInfo ("No issue with master_Hanzi_SrcField")
            print("No issue with master_Hanzi_SrcField")
        else:
            # no master_Hanzi_SrcField field
            # showInfo ("--> Field %s not found." % (master_Hanzi_SrcField))
            continue
        if master_Auto_Sentence_SrcField in note:
            #showInfo ("--> Field %s is found!" % (master_Auto_Sentence_SrcField))
            print("--> Field %s is found!" % (master_Auto_Sentence_SrcField))
        else:
            # showInfo ("--> Field %s not found!" % (master_Auto_Sentence_SrcField))
            # no dst field
            continue
        if note[master_Auto_Sentence_SrcField] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            # showInfo ("--> %s not empty. Skipping!" % (master_Auto_Sentence_SrcField))
            continue
        try:
            a = Slave_Hanzi_Dict.get(note[master_Hanzi_SrcField])
            #showInfo("a is : %s" %str(a))
            # Search if the hanzi field from master card has match in  slave hanzi dict
            # Sample,  a = Slave_Hanzi_Dict.get('我')
            if not a:
                # showInfo ("--> cannot find cross ref for %s Skipping!" % note[master_Hanzi_SrcField])
                info_Hanzi_In_Master_Card_but_Not_in_Slave += 1
                continue
            del Slave_Hanzi_Dict[note[master_Hanzi_SrcField]]
            # showInfo ("for Hanzi" + note[master_Hanzi_SrcField] + "We will use" + str(a))
            # showInfo ("a[0] = %s" %str(a[0]))

            # always a to get the first occuring entry list for that hanzi

            # check if Slave_Hanzi_Dict entry field value not none. if not none then add
            if a[0][0]:
                note[master_Auto_Sentence_SrcField] = a[0][0]
            # check same as above, but also make sure master field also exist (i.e, not None)
            if a[0][1] and master_Auto_SR_SrcField:
                note[master_Auto_SR_SrcField] = a[0][1]
            if a[0][2] and master_Auto_ST_SrcField:
                note[master_Auto_ST_SrcField] = a[0][2]
            if a[0][3] and master_Auto_SA_SrcField:
                note[master_Auto_SA_SrcField] = a[0][3]
            if a[0][4] and master_Auto_Synced_Hint_SrcField:
                note[master_Auto_Synced_Hint_SrcField] = a[0][4]
            if a[0][5] and master_other1_Field:
                note[master_other1_Field] = a[0][5]
            if a[0][6] and master_other2_Field:
                note[master_other2_Field] = a[0][6]
            if a[0][7] and master_other3_Field:
                note[master_other3_Field] = a[0][7]




            """
            if len(a[0]) >= 6 and Enable_Optional_Custom_MasterSlaveSyncFieldList == True:
                note[a[0][5][0]] = a[0][5][1]
            """
            info_Total_Changes_Made_To_Master_Card += 1
            # note[master_Auto_SentenceF_SrcField] = 'Auto_SentenceF'
            # note[master_Auto_SR_F_SrcField] = 'Auto_SR_F'
            # note[master_Auto_ST_F_SrcField] = 'Auto_ST_F'
        except Exception as e:
            raise
        note.flush()
    mw.progress.finish()
    # Now to deal with slave hanzi that does not exist in master deck
    info_Hanzi_In_Slave_Card_but_Not_in_Master = len(Slave_Hanzi_Dict)
    showInfo(
        "--> Everything should have worked.\n info_Hanzi_In_Master_Card_but_Not_in_Slave = %d \n info_Total_Changes_Made_To_Master_Card = %d \n info_Distinct_Hanzi_In_Slave_Deck = %d \n info_Hanzi_In_Slave_Card_but_Not_in_Master = %d" % (
        info_Hanzi_In_Master_Card_but_Not_in_Slave, info_Total_Changes_Made_To_Master_Card,
        info_Distinct_Hanzi_In_Slave_Deck, info_Hanzi_In_Slave_Card_but_Not_in_Master))
    # convert frequency list to dict

    SlaveNoteToAdd = []
    for Slave_Hanzi_Not_in_Master in Slave_Hanzi_Dict:
        for HanziF in HanziFreqList:
            if HanziF[1] == Slave_Hanzi_Not_in_Master:
                # grab the dict definition from HanziF and sentence example from Slave_Hanzi_Dict
                SlaveNoteToAdd.append(HanziF + Slave_Hanzi_Dict.get(Slave_Hanzi_Not_in_Master))
                break
    if (debugMode):
        showInfo("List of Hanzi_In_Slave_Card_but_Not_in_Master: %s" % str(Slave_Hanzi_Dict.keys()))
        showInfo("Now test add note")
        showInfo("note to add = %s " % str(SlaveNoteToAdd))
    # dummyNoteToAdd = [[6352,"糗","",99.98774599,"qiǔ","","(surname)/dryprovisions",36],[6353,"鸮","鴞",99.9877646,
    # "xiāo","","",36],[6354,"蕰","",99.9877832,"wēn","","",36],[6355,"坼","",99.9878018,"chè","","tocrack/split/break/tochap",36]]
    createAnkiNote(SlaveNoteToAdd)
    
    mw.reset()


def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('CN_02_Generate_Dynamic_Hanzi_Deck')
    a.triggered.connect(lambda _, b=browser: onBulkGenerateLearned_Hanzi_Cross_Indexing(b,"manual"))
    q = menu.addAction('CN_02_Generate_Dynamic_Hanzi_Deck(QUERY)')
    q.triggered.connect(lambda _, b=browser: onBulkGenerateLearned_Hanzi_Cross_Indexing(b,"QUERY"))

def onBulkGenerateLearned_Hanzi_Cross_Indexing(browser,fieldmode):
    reload_config()
    
    if (fieldmode == "QUERY"):
        BulkGenerateLearned_Hanzi_Cross_Indexing(findNotes(query_input))
    else:
        nids = browser.selectedNotes()
        if not nids:
            tooltip("No cards selected.")
            return
        # BulkGenerateLearned_Hanzi_Cross_Indexing(browser.selectedNotes())
        dialog = HanziIndexDialog(browser, nids)
        dialog.exec_()


addHook("browser.setupMenus", setupMenu)
