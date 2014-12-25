# -*- coding: utf-8 -*-
'''
Created on 25/12/2014

@author: Myxoma
'''

import os.path


temp = unicode(u"[sound:ahashdhasdあすｇｄ　-さ語.mp3")
temp = temp.replace("[sound:", "")
print temp
FileToSearch = unicode(ur"D:\03-Japanese raw manga + Anime subs + Novel\more jap\SUper Jdic audio pack\JDIC_Audio_All_09April2010\extracted output\ティ - ティ.mp3")
if os.path.isfile(FileToSearch):
     print True
else:
    print False
