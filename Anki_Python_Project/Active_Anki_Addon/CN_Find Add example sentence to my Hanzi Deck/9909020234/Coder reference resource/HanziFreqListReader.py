HanziFreqList = []

with open("C:/Users/Myxoma/AppData/Roaming/Anki2/addons21/999999996/HanziFrequencyList.txt", "r", encoding="utf-8") as f:
    HanziFreqList = [line.split('\t') for line in f]

for x in range(10):
    print(HanziFreqList[x])


    
    
########## Now to write it back

with open('C:/Users/Myxoma/AppData/Roaming/Anki2/addons21/999999996/ReWrited_HanziFrequencyList_mini.txt', 'w', encoding="utf-8") as f:
    for item in HanziFreqList:
    
        f.write("%s\n" % item)
        
############### actual code

HanziFreqList = []

with open("C:/Users/Myxoma/AppData/Roaming/Anki2/addons21/999999996/HanziFrequencyList.txt", "r", encoding="utf-8") as f:
    HanziFreqList = [line.split('\t') for line in f]
    
for HFreq in HanziFreqList:
    if not HFreq[4]:
        HFreq[4] = ''
    else:
        HFreq[4] = decode_pinyin(HFreq[4])

with open('C:/Users/Myxoma/AppData/Roaming/Anki2/addons21/999999996/ReWrited_HanziFrequencyList_mini.txt', 'w', encoding="utf-8") as f:
    for item in HanziFreqList:
    
        f.write("%s\n" % item[4])

        
        
#for HFreq in HanziFreqList:
#    print(HFreq[4])
############### actual code final part

HanziFreqList = []

with open("C:/Users/Myxoma/AppData/Roaming/Anki2/addons21/999999996/HanziFrequencyList.txt", "r", encoding="utf-8") as f:
    HanziFreqList = [line.split('\t') for line in f]
    
for HFreq in HanziFreqList:
    #print(str(HFreq))
    if not HFreq[5]:
        HFreq[5] = ''
    else:
        temp = []
        for x in HFreq[5].split(','):
            temp.append(decode_pinyin(x))
        HFreq[5] = ", ".join(temp)

        #HFreq[5] = decode_pinyin(HFreq[5])

with open('C:/Users/Myxoma/AppData/Roaming/Anki2/addons21/999999996/ReWrited_HanziFrequencyList_mini.txt', 'w', encoding="utf-8") as f:
    for item in HanziFreqList:
    
        f.write("%s\n" % item[5])

        
        
#for HFreq in HanziFreqList:
#    print(HFreq[4])
for HFreq in HanziFreqList:
	if len(HFreq) !=7:
		print(str(HFreq))