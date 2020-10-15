# -*- coding: utf-8 -*-
""" Python3

v1.0.3
Todo:
1. add html creation script with simple [content insert] in the middle

2a. move {image folder} directory to item/image/
2b. Load {image.tbl} , rename 0001 to  cover.jpg Etc.

21May2017 Task
1. find <A href> , if <FRAME> inside > look & save inside content into val TOC_data[0]
2. find <HSRT> , check if (TOC_data[0] in <HSRT> {content} </HSRT> , if yes, then replace <HSRT> with <HSRT id="TOC_data[0]">
3. go back to <A href> that contain TOC_data[0], replace <A href="#whatever" with <A href="#TOC_data[0]"

4. Now bomb every element except <A> , <br>, <HSRT>, <Frame>
5. Now split HTML for each chapter
5.5 Alternatively, split HTML for each images
5.75 Or even Easier, us PAGEPOS TAG to split
6. Now limit image width height



-- (<J .*?>) >>>> if match does not contain /> then ignore 

python27.exe "B:\Dropbox\my stuff\Vtask script\00_python\HontoDecryptedEpubXToHTML_v2.py" "B:\testground\LN_IsekaiTenseiSoudoikiV1\0001\Text\aText_3.xml" "IsekaiTenseiSoudouki_LN_Vol1_Formattedv2.html"

python27.exe -m pip install beautifulsoup4 


Bomb script

\<(?!IMG|BR|\/IMG|HSRT|\/HSRT|A |\/A|FRAME|\/FRAME).*?\>
Test Sample


<A href="#c5" id="1"><FRAME widthbefore="0.75pt" >序章</FRAME></A><BR />
転生した魂<BR />
<PAGEPOS align="center" /><HSRT>序章　転生した魂</HSRT>
<IMG src="item/image/005.jpg" viewmode="integration" fitmode="fullin" fitlarge="false"></IMG>
<KP newpage="even" />

<J size="100.0%" /><G okuri="1.6ji" okuri="1.6ji" align="eql" /><G indhead="0.0ji" indhead="0pt+0pt" indend="0.0ji" indend="0pt+0pt" indfirst="0.0ji" okuri="1.6ji" okuri="1.6ji" align="eql" /><G indhead="0.0ji" indhead="0pt+0pt" indend="0.0ji" indend="0pt+0pt" indfirst="0.0ji" okuri="1.6ji" okuri="1.6ji" align="eql" /><J f="20" size="130.0%" fweight="bold"><A href="#item/xhtml/p-tobira-004.xhtml_id-a003" id="1"><J f="20" fweight="bold" fstyle="normal"><FRAME widthbefore="0.75pt" colorbefore="#3366ff" stylebefore="1" spacebefore="0.037ji" spacebefore="0.375pt">第二章</FRAME></J></A></J><!-- br --><G okuri="1.6ji" okuri="1.6ji" align="eql" /><G indhead="0.0ji" indhead="0pt+0pt" indend="0.0ji" indend="0pt+0pt" indfirst="0.0ji" okuri="1.6ji" okuri="1.6ji" align="eql" /><BR />
<J size="100.0%" /><G okuri="1.6ji" okuri="1.6ji" align="eql" /><G indhead="0.0ji" indhead="0pt+0pt" indend="0.0ji" indend="0pt+0pt" indfirst="0.0ji" okuri="1.6ji" okuri="1.6ji" align="eql" /><G indhead="0.0ji" indhead="0pt+0pt" indend="0.0ji" indend="0pt+0pt" indfirst="0.0ji" okuri="1.6ji" okuri="1.6ji" align="eql" /><J f="20" size="110.0%" fweight="bold">東からの来訪者</J><!-- br --><G okuri="1.6ji" okuri="1.6ji" align="eql" /><G indhead="0.0ji" indhead="0pt+0pt" indend="0.0ji" indend="0pt+0pt" indfirst="0.0ji" okuri="1.6ji" okuri="1.6ji" align="eql" /><BR />
"""



# Decrypt DRM'd .epubx books from honto.jp
 
import zipfile
import struct
import os,errno
import sys
import re
from functools import reduce

def splitkeepdelimiter(data, delimiter):
   return reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == delimiter else acc + [elem], re.split("(%s)" % re.escape(delimiter), data), [])

def cleanhtml(raw_html):
  """
  #rubycleanr = re.compile('(<RT>).*?(</RT>)')   --this removes ruby all together (part1)
  #cleantext = re.sub(rubycleanr, '', raw_html)  --this removes ruby all together (part2)
  rubycleanr = re.compile('(<JRUBY>)')
  cleantext = re.sub(rubycleanr, '<RUBY>', raw_html)
  elementcleanr = re.compile('(</JRUBY>)')
  cleantext = re.sub(elementcleanr, '</RUBY>', cleantext)
  elementcleanr = re.compile('<(?!IMG|BR|\/IMG|HSRT|\/HSRT|A |\/A|FRAME|\/FRAME|PAGEPOS|RUBY|\/RUBY|RT|\/RT|KP \/).*?\>')
  cleantext = re.sub(elementcleanr, '', cleantext)
  elementcleanr = re.compile('(<HSRT><\/HSRT>)')
  cleantext = re.sub(elementcleanr, '', cleantext)
  
  #print "cleantext: %s" % cleantext
  """
  return raw_html

def HontoHtmlOutBasicCssTemplate():
  template = """
  
body{
  margin-left: 5%; line-height: 200%; padding: 0.5em;
  background-color:#F6F3E9;
  font-size:21px;
  font-family:Arial, Helvetica, sans-serif;
}

p{
  width:70%;
  float:left;
  clear: both;
}

button{
clear: both;
 float:left;
}

img {
  max-width:100%
}

@media only screen and (orientation : portrait) {
	/* Styles for mobile devices on portrait mode */
  body {
    margin-left: 2%;
    font-size:28px;
  }
 p{
  width:97%;
 }
}

.calibreMeta{
  background-color:#39322B;
  color:white;
  padding:10px;
}

.KR{
  color:black;
}

.JP{
  color:purple;
}

.CN{
  color:darkred;
}

.calibreMeta a, .calibreEbNav a, .calibreEbNavTop a, .calibreToc a{
  color:white;
}

.calibreMeta h1{
  margin:0px;
  font-size:18px;
  background-color:#39322B;
}

.calibreEbookContent{
  padding:20px;
}

.calibreEbNav, .calibreEbNavTop{
  clear:both;
  background-color:#39322B;
  color:white;
  padding:10px;
  text-align:center;
}

.dontDisplay {
        display: none;
}

.hidden {
        visibility: hidden;
}

.calibreToc{
  float:left;
  margin:20px;
  width:60%;
  color:black;
  background-color:black;
  padding:10px;
}
.calibreEbookContent{
  width:70%;
  float:left;
  clear: both;
}
  """
  return template


fontSizeAndThemeButtonTemplate = """
<br><button onclick='toggledoublefontsize(21)' > 21px</button>
<br><button onclick='toggledoublefontsize(28)' > 28px</button>
<br><button onclick='toggledoublefontsize(33)' > 33px</button>
<br><button onclick='toggledoublefontsize(37)' > 37px</button><br>
<br><button onclick='toggleblacktheme()' > Black Theme</button>
<br><button onclick='togglenormaltheme()' > Normal Theme</button><br>
<br><button onclick='toggleDisplayShowClass("KR")' > Toggle Display/Hide KR</button>
<br><button onclick='toggleHiddenShowClass("KR")' > Toggle Visible/Invisible KR</button><br>
<br><button onclick='toggleDisplayShowClass("JP")' > Toggle Display/Hide JP</button>
<br><button onclick='toggleHiddenShowClass("JP")' > Toggle Visible/Invisible JP</button><br>
<br><button onclick='toggleDisplayShowClass("CN")' > Toggle Display/Hide CN</button>
<br><button onclick='toggleHiddenShowClass("CN")' > Toggle Visible/Invisible CN</button><br>
<script>function toggledoublefontsize(myvalue){document.body.style.fontSize =  myvalue +"px";}</script>
<script>function toggleblacktheme(){
    document.body.style.color =  "white";document.body.style.backgroundColor =  "black";
    let all = document.getElementsByClassName('KR');
    for (let i = 0; i < all.length; i++) {
      all[i].style.color = 'white';
    }
    all = document.getElementsByClassName('JP');
    for (let i = 0; i < all.length; i++) {
      all[i].style.color = 'violet';
    }
    all = document.getElementsByClassName('CN');
    for (let i = 0; i < all.length; i++) {
      all[i].style.color = 'darkorange';
    }
}
</script>
<script>function togglenormaltheme(){
    document.body.style.color =  "black";document.body.style.backgroundColor =  "#F6F3E9";
    let all = document.getElementsByClassName('KR');
    for (let i = 0; i < all.length; i++) {
      all[i].style.color = '';
    }
    all = document.getElementsByClassName('JP');
    for (let i = 0; i < all.length; i++) {
      all[i].style.color = '';
    }
    all = document.getElementsByClassName('CN');
    for (let i = 0; i < all.length; i++) {
      all[i].style.color = '';
    }
}
</script>
<script>function toggleDisplayShowClass(className) {
    let all = document.getElementsByClassName(className);
    for (let i = 0; i < all.length; i++) {
        all[i].classList.toggle('dontDisplay');
    }
}</script>
<script>function toggleHiddenShowClass(className) {
    let all = document.getElementsByClassName(className);
    for (let i = 0; i < all.length; i++) {
        all[i].classList.toggle('hidden');
    }
}</script>

"""


def splitHTML(raw_html, delimitertype, delimitervalue):
   #splittedHTML = splitkeepdelimiter(raw_html,'<PAGEPOS align="center" />')
   if (delimitertype == '1'):
      splittedHTML  = splitkeepdelimiter(raw_html, delimitervalue)
   elif (delimitertype == '2'):
      splittedHTML = raw_html
      print("splittedHTML len = " + str(len(raw_html.splitlines())))
   elif (delimitertype == '3'):
      splittedHTML = []
      splittedHTML.append("")
      index = 0
      lines = raw_html.splitlines()
      print("@ for line in lines:")
      for line in lines:
        if (str(index) == str(delimitervalue)):
            index = 0
            splittedHTML.append(""+line+ "\n")
        else:
            splittedHTML[-1] += line + "\n"
            index += 1
   else:
      print("unexpected delimitertype: " + delimitertype + " at splitHTML function")
      splittedHTML = raw_html
   
   #print len(splittedHTML)
   #print splittedHTML
   print("Finished splitHTML()")
   return splittedHTML
 
def process_text_ToHtml(filename, output_path, output_name, delimitertype ,delimitervalue):
   fulloutputfilepath = os.path.join(output_path, output_name)
   IS_SPLIT_HTML = 1
   print("fulloutputfilepath %s" % fulloutputfilepath)
   print("processing")
   
   if not os.path.exists(os.path.dirname(fulloutputfilepath)):
    try:
        os.makedirs(os.path.dirname(fulloutputfilepath))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
         
   with open (filename, "r", encoding="utf8") as mTextFile:
      #print mTextFile.read()
      #Now create HontoHtmlOutBasicCss.css file
      open(os.path.join(output_path, "HontoHtmlOutBasicCss.css"), "w", encoding="utf8").write(HontoHtmlOutBasicCssTemplate())
      
      with open(fulloutputfilepath, "w", encoding="utf8") as mOutputTextFile:
         #mOutputTextFile.write("hahahaha1")
         cleaned_html = cleanhtml(mTextFile.read())
         Html_Template_header =  """<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>""" + output_name+ """</title><link href="HontoHtmlOutBasicCss.css" type="text/css" rel="stylesheet" /></head><body>""" + "\r\n"
         Html_Template_closing =  "\r\n"+ "</body></html> " + "\r\n"
         mOutputTextFile.write(Html_Template_header + cleaned_html + Html_Template_closing)
         if IS_SPLIT_HTML == 1:
            SplittedHTML_LIST = splitHTML(cleaned_html, delimitertype, delimitervalue)
            i = 1
            Html_Template_TOC_Toggle = " <button onclick='toggleTOC()'>Toggle TOC</button> <script>function toggleTOC() {  var x = document.getElementById('myTOC');  if (x.style.display === 'none') {    x.style.display = 'block';  } else {    x.style.display = 'none';  }}</script><br>"
            Html_Template_TOC = "<ol id='myTOC' class='calibreToc'><H>TOC</H>\r\n"
            for SplittedHTML in SplittedHTML_LIST:
              TOC_templink = output_name.split(".")[0] + '_Splitted_%s.html' %'{:02d}'.format(i)
              Html_Template_TOC += '<li> <a href="' + TOC_templink + '">' + TOC_templink + '</a></li>\r\n' 
              i += 1
            Html_Template_TOC += "</ol>\r\n"
            i = 1
            for SplittedHTML in SplittedHTML_LIST:

               Dir_And_FN_splitted = os.path.join(output_path, output_name.split(".")[0] +"_Splitted_%s.html" % '{:02d}'.format(i))
               #print "Dir_And_FN_splitted: %s" % Dir_And_FN_splitted
               missing_closing_element = ""

               if SplittedHTML.count('\n')>=2:
                    #  Ensure final line does not miss closing element.   i.e. <p class="calibre1">「うん」  >>  <p class="calibre1">「うん」</p>
                    lastline = SplittedHTML.split('\n')[-1]
                    if lastline.startswith('<') and not lastline.endswith('>') and lastline.index(' ') != -1:
                        missing_closing_element = "</%s>" %lastline[1:lastline.index(' ')]
                        print("last line missing closing element. Appending. . . %s" %missing_closing_element)
               open(Dir_And_FN_splitted, "w", encoding="utf8").write(Html_Template_header + Html_Template_TOC_Toggle + Html_Template_TOC + fontSizeAndThemeButtonTemplate + SplittedHTML + missing_closing_element + Html_Template_TOC + Html_Template_closing)
               i += 1
              

      
if __name__ == "__main__":
   print(len(sys.argv))
   delimitertype = '1'
   delimitervalue = '&gt; 끝</p>'
   
   if len(sys.argv) <= 1:
     print("usage: %s $Input(e.g. C:\input.html), $output (optional: e.g. C:\output.html)" % (sys.argv[0]))
     print(os.getcwd())
     userin = input("Enter Interactive Mode? (y/n) : ")
     if not(userin == 'y' or userin == 'Y'):
        exit(1)
     print("Welcome to interactive mode\n File to Spilt : \n")
     for file in os.listdir(os.getcwd()):
        if file.endswith(".html") or file.endswith(".txt"):
            print(os.path.join(os.getcwd(), file))
            filename = os.path.join(os.getcwd(), file)
            output_path = os.getcwd()
            output_name = file
            break
     userin = input("\nChoose spliting option (1/2/3/n/leave blank for default): \n 1. Split file with input delimiter text \n 2. split into 'x' amount of files \n 3. split after 'x' paragragh lines \n n. Exit \n (Leave blank and Press Enter for default setting)\n\n Input(1/2/3/n/leave blank for default) : ")
     if (userin == '1'):
        delimitertype = '1'
        delimitervalue = input("1. Split file with input delimiter text \n Please type delimiter text (Without Quotation'') (Fav pattern is ##!!## ):")
     elif (userin == '2'):
        delimitertype = '2'
        delimitervalue = input("2. split into 'x' amount of files \n how many files would you like ? :")
     elif (userin == '3'):
        delimitertype = '3'
        delimitervalue = input("3. split after 'x' paragragh lines. \n (Recommended value = 300) input: ")
        if (delimitervalue == '0'):
            input("0 is not a valid value, existing . .  .")
            exit(1)
     elif (userin == ''):
        input("Default mode Choosen. . .")
     else:
        input("Exiting. . . \n Press enter to Exit")
        exit(1)
   elif len(sys.argv) == 2:
     #output_name = "output.html"
     output_name = os.path.basename(sys.argv[1])
     filename = sys.argv[1]
   else:
     output_name = sys.argv[2]
     print("sys.argv[2]:%s" %sys.argv[2])
     filename = sys.argv[1]
   print("inputfilename: %s" % filename)
   print("output_name:%s" % output_name)
   
   output_path = os.path.splitext(filename)[0]
   print("Output path: %s" % output_path)
   

   
   print("delimitertype = " + delimitertype + " delimitervalue = " + delimitervalue)
   process_text_ToHtml(filename, output_path, output_name, delimitertype, delimitervalue)
   input("Completed !")
