# -*- coding: utf-8 -*-
#
# Entry point for the add-on into Anki
# Please do not edit this if you do not know what you are doing.
#
# Copyright: mo  <paradoxez919@gmail.com>
# License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
from anki.hooks import addHook
from .CN_01_Add_Example_Vocabs_To_Vocab_Deck import CN_01_Add_Example_Vocabs_To_Vocab_Deck
from .CN_02_Generate_Dynamic_Hanzi_Deck import CN_02_Generate_Dynamic_Hanzi_Deck
from .CN_03_Add_Example_Vocabs_To_Hanzi_Deck import CN_03_Add_Example_Vocabs_To_Hanzi_Deck
from .CN_04_Find_Hanzi_Homophone import CN_04_Find_Hanzi_Homophone
#from . import CN_04_Find_Hanzi_Homophone


def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    q = menu.addAction('CN_00_(QUERY ALL Function)')
    q.triggered.connect(lambda _, b=browser: onQueryAllFunction(b))


def onQueryAllFunction(b):
    CN_01_Add_Example_Vocabs_To_Vocab_Deck.onBulkGenerateSimilarHanziVocabList(b,"QUERY")
    CN_02_Generate_Dynamic_Hanzi_Deck.onBulkGenerateLearned_Hanzi_Cross_Indexing(b,"QUERY")
    CN_03_Add_Example_Vocabs_To_Hanzi_Deck.onBulkGenerateSimilarHanziVocabList(b,"QUERY")
    CN_04_Find_Hanzi_Homophone.onBulkGenerateHanziHomophoneList(b,"QUERY")


addHook("browser.setupMenus", setupMenu)