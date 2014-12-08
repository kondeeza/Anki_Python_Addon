# -*- coding: utf-8 -*-
'''
Created on 06/12/2014

@author: Myxoma
'''
import re



TextInput = "悪口(あっこう): abuse, insult, slander, evil speaking<br />悪口(わるくち): abuse, insult, slander, evil speaking<br />甘口(あまくち): sweet flavour, mildness, flattery, stupidity<br />口ずさむ(くちずさむ): to hum something, to sing to oneself #humming song zusa<br />口述(こうじゅつ): verbal statement<br />口頭(こうとう): oral<br />出入り口(でいりぐち): exit and entrance<br />閉口(へいこう): shut mouth<br />無口(むくち): reticence<br />裏口(うらぐち): back door, rear entrance<br />火口(ひぐち): crater<br />口紅(くちべに): lipstick<br />口実(こうじつ): excuse #truth from mouth is only an excuse<br />蛇口(じゃぐち): faucet, tap #JYAK!! snake came out of the faucet!!<br />早口(はやくち): fast-talking<br />窓口(まどぐち): ticket window<br />利口(りこう): clever, shrewd, bright, sharp, wise, intelligent #shrewd mouth is profitfulmouth<br />人口(じんこう): population<br />入口(いりぐち): entrance, gate, approach, mouth<br />口(くち): mouth, orifice, opening<br />出口(でぐち): exit, gateway, way out, outlet, leak, vent"

# Delete Python-style comments
TextOutput = re.sub('\((.*?)\)[:](.*?)(<br />)', "<br />", TextInput)
TextOutput = re.sub('\((.*?)\)[:](.*)', "<br />", TextOutput)
print "Input :", TextInput
print "Output :", TextOutput
