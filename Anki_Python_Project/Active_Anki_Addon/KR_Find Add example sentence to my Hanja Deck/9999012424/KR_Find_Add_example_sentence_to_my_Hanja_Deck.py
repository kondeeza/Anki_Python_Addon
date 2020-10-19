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

##########################################################################


##########################################################################
from aqt.qt import *
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning, showInfo, tooltip
import re
import platform
import time
import os
import json
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
# if data exists in Output_SrcField, should we overwrite it?
OVERWRITE_DST_FIELD = ''

KanjiDict = {}


slave_Model_Sentence_SPinyin_SMeaning_SAudio_List = []
#ConfigDict = {" ": " "}

## Initiate Kanji Dict {}
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "kanjidic2.json"), "r", encoding="utf-8") as obj:
    data = json.load(obj)

for i in range(len(data["kanjidic2"]["character"])):
    KanjiDict[data["kanjidic2"]["character"][i]["literal"]] = data["kanjidic2"]["character"][i]
## End Initiate Kanji Dict

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

        names = ['Hanja Deck Name', 'Hanja Field', 'Meaning_E', 'Reading_E','Reading_K','Reading_K_FullList','On_Yomi','Kun_Yomi','Pinyin',
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
                for i in range(0, 8):
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
            showInfo("Saving master_modelName & master_deckName: %s" % mode)
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
    config['01_master_modelName'] = master_modelName
    config['10_master_deckName'] = master_deckName

    config['02_master_Hanzi_SrcField'] = master_Hanzi_SrcField
    config['21_master_Traditional_Field'] = master_Traditional_Field
    config['22_master_Freq_Field'] = master_Freq_Field
    config['23_master_Pinyin_Field'] = master_Pinyin_Field
    config['24_master_Pinyin2_Field'] = master_Pinyin2_Field
    config['25_master_meaning_Field'] = master_meaning_Field
    config['26_master_CardCreate_Other1_field'] = master_CardCreate_Other1_field
    config['27_master_CardCreate_Other2_field'] = master_CardCreate_Other2_field

    config['03_master_Auto_Sentence_SrcField'] = master_Auto_Sentence_SrcField
    config['04_master_Auto_SR_SrcField'] = master_Auto_SR_SrcField
    config['05_master_Auto_ST_SrcField'] = master_Auto_ST_SrcField
    config['06_master_Auto_SA_SrcField'] = master_Auto_SA_SrcField
    config['11_master_Auto_Synced_Hint_SrcField'] = master_Auto_Synced_Hint_SrcField
    config['07_master_other1_Field'] = master_other1_Field
    config['08_master_other2_Field'] = master_other2_Field
    config['09_master_other3_Field'] = master_other3_Field

    config['16_slave_Model_Sentence_SPinyin_SMeaning_SAudio_List'] = slave_Model_Sentence_SPinyin_SMeaning_SAudio_List

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

    config = mw.addonManager.getConfig(__name__)
    master_modelName = config['01_master_modelName']
    master_Hanzi_SrcField = config['02_master_Hanzi_SrcField']
    master_Auto_Sentence_SrcField = config['03_master_Auto_Sentence_SrcField']
    master_Auto_SR_SrcField = config['04_master_Auto_SR_SrcField']
    master_Auto_ST_SrcField = config['05_master_Auto_ST_SrcField']
    master_Auto_SA_SrcField = config['06_master_Auto_SA_SrcField']
    #master_Auto_SentenceF_SrcField = config['07_master_Auto_SentenceF_SrcField']
    #master_Auto_SR_F_SrcField = config['08_master_Auto_SR_F_SrcField']
    #master_Auto_ST_F_SrcField = config['09_master_Auto_ST_F_SrcField']
    OVERWRITE_DST_FIELD = config['15_OVERWRITE_DST_FIELD']
    master_deckName = config['10_master_deckName']
    master_Auto_Synced_Hint_SrcField = config['11_master_Auto_Synced_Hint_SrcField']
    slave_Model_Sentence_SPinyin_SMeaning_SAudio_List = config['16_slave_Model_Sentence_SPinyin_SMeaning_SAudio_List']
    Enable_Optional_Custom_MasterSlaveSyncFieldList = config['13_Enable_Optional_Custom_MasterSlaveSyncFieldList']

    master_Traditional_Field = config['21_master_Traditional_Field']
    master_Freq_Field = config['22_master_Freq_Field']
    master_Pinyin_Field = config['23_master_Pinyin_Field']
    master_Pinyin2_Field = config['24_master_Pinyin2_Field']
    master_meaning_Field = config['25_master_meaning_Field']
    master_CardCreate_Other1_field = config['26_master_CardCreate_Other1_field']
    master_CardCreate_Other2_field = config['27_master_CardCreate_Other2_field']

    master_other1_Field = config['07_master_other1_Field']
    master_other2_Field = config['08_master_other2_Field']
    master_other3_Field = config['09_master_other3_Field']




def validateFieldList(nids):
    # TODO: 1. validate Master & Slave Note exist, Deck exist 2. validate master and slave fields exist 3. also validate correct field list syntax input
    # TODO: if validate did not pass (i.e field not exist), prompt user and abort program. else, return true and proceed. This is for simplifying Hanzi and kanji validation compatability process
    return True


def createAnkiNote(hanziToAddNoteList):
    mw.checkpoint("Manual Create Note")
    mw.progress.start()

    tooltip("Card creation is slow. It would take about 15 seconds per 100 cards creation")
    # Get desired deck name from input box
    deckName = master_deckName
    if not deckName:
        return
    # deckName = deckName.replace('"', "")

    # Create new deck with name from input box
    deck = mw.col.decks.get(mw.col.decks.id(deckName))
    #tooltip("Kanji Deck Info is: %s" %str(deck))
    # Copy notes
    showinfocounter = 0
    for hanziNote in hanziToAddNoteList:
        if showinfocounter <=10:
            showInfo("Found note: %s" % (str(hanziNote)))

        if showinfocounter%100==0:
            # period means to only show for x /1000 second. i.e. 1000 = 1 sec. though it doesn't seem to work
            tooltip("card created counter is : %s" % (str(showinfocounter)), period=1000)
            # refresh GUI during loop
            mw.app.processEvents()


        showinfocounter = showinfocounter + 1
        # note = mw.col.getNote(nid)
        model = mw.col.models.byName(master_modelName)

        # Assign model to deck
        mw.col.decks.select(deck['id'])
        #showInfo("Model file is %s " %str(model))
        mw.col.decks.get(deck)['mid'] = model['id']
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


        note_toAdd[master_Hanzi_SrcField] = hanziNote[0]["character"]
        if master_Traditional_Field:
            note_toAdd[master_Traditional_Field] = str(hanziNote[0]["meaning"])
        if master_Freq_Field:
            note_toAdd[master_Freq_Field] = str(hanziNote[0]["Korean_reading1"])
        if master_Pinyin_Field:
            note_toAdd[master_Pinyin_Field] = str(hanziNote[0]["Korean_hangul1"])
        if master_Pinyin2_Field:
            note_toAdd[master_Pinyin2_Field] = str(hanziNote[0]["Korean_hangul_Full"])
        if master_meaning_Field:
            note_toAdd[master_meaning_Field] = str(hanziNote[0]["Reading_On"])
        if master_CardCreate_Other1_field:
            note_toAdd[master_CardCreate_Other1_field] = str(hanziNote[0]["Reading_Kun"])
        if master_CardCreate_Other2_field:
            note_toAdd[master_CardCreate_Other2_field] = str(hanziNote[0]["Pinyin"])

        if hanziNote[1][0]:
            note_toAdd[master_Auto_Sentence_SrcField] = hanziNote[1][0]
        if hanziNote[1][1] and master_Auto_SR_SrcField:
            note_toAdd[master_Auto_SR_SrcField] = hanziNote[1][1]
        if hanziNote[1][2] and master_Auto_ST_SrcField:
            note_toAdd[master_Auto_ST_SrcField] = hanziNote[1][2]
        if hanziNote[1][3] and master_Auto_SA_SrcField:
            note_toAdd[master_Auto_SA_SrcField] = hanziNote[1][3]
        if hanziNote[1][4] and master_Auto_Synced_Hint_SrcField:
            note_toAdd[master_Auto_Synced_Hint_SrcField] = hanziNote[1][4]
        if hanziNote[1][5] and master_other1_Field:
            note_toAdd[master_other1_Field] = hanziNote[1][5]
        if hanziNote[1][6] and master_other2_Field:
            note_toAdd[master_other2_Field] = hanziNote[1][6]
        if hanziNote[1][7] and master_other3_Field:
            note_toAdd[master_other3_Field] = hanziNote[1][7]

        """
        if len(hanziNote[8]) >= 6 and Enable_Optional_Custom_MasterSlaveSyncFieldList == True:
            note_toAdd[hanziNote[8][5][0]] = hanziNote[8][5][1]
        """
        # Refresh note and add to database
        note_toAdd.flush()
        mw.col.addNote(note_toAdd)

    # Reset collection and main window

    showInfo("Resetting Collection")
    mw.col.reset()
    showInfo("collection has been reset")
    mw.progress.finish()
    mw.reset()
    showInfo("All done !")


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


def getKanjiDefinition_v2(kanjiInput):
    """Significantly faster than v1"""
    #print(KanjiDict.get(kanjiInput))

    KanjiResultDict = {}
    KanjiDefition_Result = KanjiDict.get(kanjiInput)
    KanjiDefition_character = ''
    KanjiDef_stroke_count = ''
    KanjiDef_freq = ''
    KanjiDef_jlpt = ''
    KanjiDef_grade = ''
    KanjiDef_nelson_n = ''
    KanjiDef_heisig = ''
    KanjiDef_meaning = ''
    KanjiDef_Pinyin = ''
    KanjiDef_Korean_reading1 = ''
    KanjiDef_Korean_hangul1 = ''
    KanjiDef_Korean_reading_Full = ''
    KanjiDef_Korean_hangul_Full = ''
    KanjiDef_Reading_On = ''
    KanjiDef_Reading_Kun = ''

    if KanjiDefition_Result:
        # only run if result not None i.e input is actually kanji
        if 'literal' in KanjiDefition_Result:
            KanjiDefition_character = KanjiDefition_Result['literal']
        if 'stroke_count' in KanjiDefition_Result['misc']:
            KanjiDef_stroke_count = KanjiDefition_Result['misc']['stroke_count']
        if 'freq' in KanjiDefition_Result['misc']:
            KanjiDef_freq = KanjiDefition_Result['misc']['freq']
        if 'jlpt' in KanjiDefition_Result['misc']:
            KanjiDef_jlpt = KanjiDefition_Result['misc']['jlpt']
        if 'grade' in KanjiDefition_Result['misc']:
            KanjiDef_grade = KanjiDefition_Result['misc']['grade']
        if 'dic_number' in KanjiDefition_Result:
            if 'dic_ref' in KanjiDefition_Result['dic_number']:
                # nelson_n = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if elem["-dr_type"] == 'nelson_n']
                if isinstance(KanjiDefition_Result['dic_number']['dic_ref'], list):
                    KanjiDef_nelson_n_tem = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if
                                         elem['-dr_type'] == 'nelson_n']
                    if bool(KanjiDef_nelson_n_tem):
                        KanjiDef_nelson_n = KanjiDef_nelson_n_tem[0]
                    # KanjiDef_heisig = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if elem['-dr_type'] == 'heisig'][0]  . Old version that gave error if 'heisig' dict did not exist because you are trying to read 'heisig'][0]
                    KanjiDef_heisig_tem = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if
                                       elem['-dr_type'] == 'heisig']
                    if bool(KanjiDef_heisig_tem):
                        KanjiDef_heisig = KanjiDef_heisig_tem[0]


        if 'rmgroup' in KanjiDefition_Result['reading_meaning']:
            if 'meaning' in KanjiDefition_Result['reading_meaning']['rmgroup']:
                for mList in KanjiDefition_Result['reading_meaning']['rmgroup']['meaning']:
                    # english meaning is in str type whereas other meaning is in list type
                    if isinstance(mList, str):
                        KanjiDef_meaning = KanjiDef_meaning + mList + ', '
            if 'reading' in KanjiDefition_Result['reading_meaning']['rmgroup']:
                for readingList in KanjiDefition_Result['reading_meaning']['rmgroup']['reading']:
                    if isinstance(readingList, str):
                        # showInfo(str(KanjiDefition_Result))
                        # there's likely a typo in kanjidic json. This is a hotfix to prevent an error message
                        continue

                    if readingList.get('-r_type') == 'pinyin':
                        KanjiDef_Pinyin = KanjiDef_Pinyin + readingList.get('#text') + ', '
                    elif readingList.get('-r_type') == 'ja_on':
                        KanjiDef_Reading_On = KanjiDef_Reading_On + readingList.get('#text') + ', '
                    elif readingList.get('-r_type') == 'ja_kun':
                        KanjiDef_Reading_Kun = KanjiDef_Reading_Kun + readingList.get('#text') + ', '
                    elif readingList.get('-r_type') == 'korean_r':
                        KanjiDef_Korean_reading_Full = KanjiDef_Korean_reading_Full + readingList.get('#text') + ', '
                        if not KanjiDef_Korean_reading1:
                            KanjiDef_Korean_reading1 = readingList.get('#text')
                    elif readingList.get('-r_type') == 'korean_h':
                        KanjiDef_Korean_hangul_Full = KanjiDef_Korean_hangul_Full + readingList.get('#text') + ', '
                        if not KanjiDef_Korean_hangul1:
                            KanjiDef_Korean_hangul1 = readingList.get('#text')

    #remove the unneeded extra ", " at the end of variable
    if KanjiDef_Korean_reading_Full:
        KanjiDef_Korean_reading_Full = KanjiDef_Korean_reading_Full[:-2]
    if KanjiDef_Korean_hangul_Full:
        KanjiDef_Korean_hangul_Full = KanjiDef_Korean_hangul_Full[:-2]

    KanjiResultDict["character"] = KanjiDefition_character
    KanjiResultDict["stroke_count"] = KanjiDef_stroke_count
    KanjiResultDict["freq"] = KanjiDef_freq
    KanjiResultDict["jlpt"] = KanjiDef_jlpt
    KanjiResultDict["grade"] = KanjiDef_grade
    KanjiResultDict["nelson_n"] = KanjiDef_nelson_n
    KanjiResultDict["heisig"] = KanjiDef_heisig
    KanjiResultDict["meaning"] = KanjiDef_meaning
    KanjiResultDict["Pinyin"] = KanjiDef_Pinyin
    KanjiResultDict["Reading_On"] = KanjiDef_Reading_On
    KanjiResultDict["Reading_Kun"] = KanjiDef_Reading_Kun
    KanjiResultDict["Korean_reading1"] = KanjiDef_Korean_reading1
    KanjiResultDict["Korean_hangul1"] = KanjiDef_Korean_hangul1
    KanjiResultDict["Korean_reading_Full"] = KanjiDef_Korean_reading_Full
    KanjiResultDict["Korean_hangul_Full"] = KanjiDef_Korean_hangul_Full

    if not KanjiResultDict["character"]:
        KanjiResultDict = ''

    #print(KanjiDefition_Result.keys())
    #print("")
    #print(KanjiDefition_Result)
    #print(KanjiResultDict)
    return KanjiResultDict

def Generate_Slave_Hanzi_Index(nids):
    mw.checkpoint("Bulk-Generate Generate_Slave_Kanji_Index")
    mw.progress.start()

    Slave_Hanzi_Dict = {}



    warning_counter = 0
    warning_slaveModelNotFound = 0
    warning_slaveSentence_NotFound = 0
    info_Slave_Hanzi_indexed = 0
    info_Slave_Hanzi_not_in_Hanzi_Frequency_List = 0

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
                if getKanjiDefinition_v2(x) != "":
                    # if x character from vocab sentence deck is found in dictionary
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
    showInfo(
        "--> Generate_Slave_Hanzi_Index.\n warning_counter = %d \n warning_slaveModelNotFound = %d \n warning_slaveSentence_NotFound = %d \n info_Slave_Hanzi_indexed = %d \n info_Slave_Hanzi_not_in_Hanzi_Frequency_List = %d" % (
        warning_counter, warning_slaveModelNotFound, warning_slaveSentence_NotFound, info_Slave_Hanzi_indexed,
        info_Slave_Hanzi_not_in_Hanzi_Frequency_List))
    mw.progress.finish()
    mw.reset()
    # Slave_Hanzi_Dict should be something like
    # Slave_Hanzi_Dict = { '我':[ ['我爱你','wo3 ai4 ni3,'i love you','very simple','２０'], ['你爱我',,,,'２０'] ] , etc}

    return Slave_Hanzi_Dict

def BulkGenerateLearned_Hanzi_Cross_Indexing(nids):
    mw.checkpoint("Bulk-Generate TotalWordCount")
    mw.progress.start()

    reload_config()
    # HanziFreqList contains the list of 10k Hanzi Frequency as: [freq,HanS,HanT,Index,PinY,Meaning,index2]
    HanziFreqDict = {}


    # showInfo ("Beginning BulkGenerateLearned_Hanzi_Cross_Indexing with this config:\n master_modelName: %s \n master_Hanzi_SrcField: %s \n master_Auto_Sentence_SrcField: %s \n master_Auto_SR_SrcField: %s \n master_Auto_ST_SrcField: %s \n master_Auto_SA_SrcField: %s \n master_Auto_SentenceF_SrcField: %s \n master_Auto_SR_F_SrcField: %s \n master_Auto_ST_F_SrcField: %s \n OVERWRITE_DST_FIELD: %s \n slave_Model_Sentence_SPinyin_SMeaning_SAudio_List: %s " %(master_modelName,master_Hanzi_SrcField,master_Auto_Sentence_SrcField,master_Auto_SR_SrcField,master_Auto_ST_SrcField,master_Auto_SA_SrcField,master_Auto_SentenceF_SrcField,master_Auto_SR_F_SrcField,master_Auto_ST_F_SrcField,OVERWRITE_DST_FIELD, str(slave_Model_Sentence_SPinyin_SMeaning_SAudio_List) ))
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
    showInfo("--> Now on final part. Binding final output to dst !")
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

    # Now to deal with slave hanzi that does not exist in master deck
    info_Hanzi_In_Slave_Card_but_Not_in_Master = len(Slave_Hanzi_Dict)
    showInfo(
        "--> Everything should have worked.\n info_Hanzi_In_Master_Card_but_Not_in_Slave = %d \n info_Total_Changes_Made_To_Master_Card = %d \n info_Distinct_Hanzi_In_Slave_Deck = %d \n info_Hanzi_In_Slave_Card_but_Not_in_Master = %d" % (
        info_Hanzi_In_Master_Card_but_Not_in_Slave, info_Total_Changes_Made_To_Master_Card,
        info_Distinct_Hanzi_In_Slave_Deck, info_Hanzi_In_Slave_Card_but_Not_in_Master))
    # convert frequency list to dict

    SlaveNoteToAdd = []
    for Slave_Hanzi_Not_in_Master in Slave_Hanzi_Dict:
          # grab the dict definition from HanziF and sentence example from Slave_Hanzi_Dict
          #showInfo("Slave_Hanzi_Not_in_Master to be appended: %s" % str(Slave_Hanzi_Not_in_Master))
          #showInfo("to be appended value: %s" % str([getKanjiDefinition_v2(Slave_Hanzi_Not_in_Master)] + Slave_Hanzi_Dict.get(Slave_Hanzi_Not_in_Master)))
          SlaveNoteToAdd.append( [getKanjiDefinition_v2(Slave_Hanzi_Not_in_Master)] + Slave_Hanzi_Dict.get(Slave_Hanzi_Not_in_Master))

          #showInfo("SlaveNoteToAdd appended: %s" % str(SlaveNoteToAdd))
          #[0]['DictKey'] for kanjidefinition ,  [1][0-7] for slave fields value


    showInfo("List of Hanzi_In_Slave_Card_but_Not_in_Master: %s" % str(Slave_Hanzi_Dict.keys()))
    tooltip("Now test add note")
    #showInfo("final slave note to add = %s " % str(SlaveNoteToAdd))
    # dummyNoteToAdd = [[6352,"糗","",99.98774599,"qiǔ","","(surname)/dryprovisions",36],[6353,"鸮","鴞",99.9877646,
    # "xiāo","","",36],[6354,"蕰","",99.9877832,"wēn","","",36],[6355,"坼","",99.9878018,"chè","","tocrack/split/break/tochap",36]]
    createAnkiNote(SlaveNoteToAdd)
    mw.progress.finish()
    mw.reset()


def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('KR_Find/Add example sentence to my Hanja Deck')
    a.triggered.connect(lambda _, b=browser: onBulkGenerateLearned_Hanzi_Cross_Indexing(b))


def onBulkGenerateLearned_Hanzi_Cross_Indexing(browser):
    nids = browser.selectedNotes()


    if not nids:
        tooltip("No cards selected.")
        return
    # BulkGenerateLearned_Hanzi_Cross_Indexing(browser.selectedNotes())
    dialog = HanziIndexDialog(browser, nids)
    dialog.exec_()


addHook("browser.setupMenus", setupMenu)
