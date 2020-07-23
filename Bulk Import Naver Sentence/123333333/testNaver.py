import requests
from bs4 import BeautifulSoup
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("hi")
debugMode= True
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
                    print("input: %s \n sentence , type: %s  , value : %s \n meaning, type: %s  , value : %s \n x, type: %s value: %s " %(para,type(sentence),str(sentence),type(officialExamp_Meaning[idx]),str(officialExamp_Meaning[idx]),type(x),str(x)))
                x += sentence + "<br>" + officialExamp_Meaning[idx] + "<br>"
                result["Sentence"] += sentence + "<br>"
                result["Meaning"] += officialExamp_Meaning[idx] + "<br>"

            result["Merged"] = x
            #print (result)

    else:
        print("url not found")

    time.sleep(0.3)

    return result

start = time.perf_counter()
for i in range(1):
    getNaverSentenceExample("예매하다")

print("Took %d seconds" %(time.perf_counter()-start) )
