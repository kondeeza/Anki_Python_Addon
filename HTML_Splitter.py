# -*- coding: utf-8 -*-
""" Python3

v1.0.4 12-NOV-2020
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
import shutil
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

def s2t_JS_Template():
    template = """
    !function(t){var c=new String("万与丑专业丛东丝丢两严丧个丬丰临为丽举么义乌乐乔习乡书买乱争于亏云亘亚产亩亲亵亸亿仅从仑仓仪们价众优伙会伛伞伟传伤伥伦伧伪伫体余佣佥侠侣侥侦侧侨侩侪侬俣俦俨俩俪俭债倾偬偻偾偿傥傧储傩儿兑兖党兰关兴兹养兽冁内冈册写军农冢冯冲决况冻净凄凉凌减凑凛几凤凫凭凯击凼凿刍划刘则刚创删别刬刭刽刿剀剂剐剑剥剧劝办务劢动励劲劳势勋勐勚匀匦匮区医华协单卖卢卤卧卫却卺厂厅历厉压厌厍厕厢厣厦厨厩厮县参叆叇双发变叙叠叶号叹叽吁后吓吕吗吣吨听启吴呒呓呕呖呗员呙呛呜咏咔咙咛咝咤咴咸哌响哑哒哓哔哕哗哙哜哝哟唛唝唠唡唢唣唤唿啧啬啭啮啰啴啸喷喽喾嗫呵嗳嘘嘤嘱噜噼嚣嚯团园囱围囵国图圆圣圹场坂坏块坚坛坜坝坞坟坠垄垅垆垒垦垧垩垫垭垯垱垲垴埘埙埚埝埯堑堕塆墙壮声壳壶壸处备复够头夸夹夺奁奂奋奖奥妆妇妈妩妪妫姗姜娄娅娆娇娈娱娲娴婳婴婵婶媪嫒嫔嫱嬷孙学孪宁宝实宠审宪宫宽宾寝对寻导寿将尔尘尧尴尸尽层屃屉届属屡屦屿岁岂岖岗岘岙岚岛岭岳岽岿峃峄峡峣峤峥峦崂崃崄崭嵘嵚嵛嵝嵴巅巩巯币帅师帏帐帘帜带帧帮帱帻帼幂幞干并广庄庆庐庑库应庙庞废庼廪开异弃张弥弪弯弹强归当录彟彦彻径徕御忆忏忧忾怀态怂怃怄怅怆怜总怼怿恋恳恶恸恹恺恻恼恽悦悫悬悭悯惊惧惨惩惫惬惭惮惯愍愠愤愦愿慑慭憷懑懒懔戆戋戏戗战戬户扎扑扦执扩扪扫扬扰抚抛抟抠抡抢护报担拟拢拣拥拦拧拨择挂挚挛挜挝挞挟挠挡挢挣挤挥挦捞损捡换捣据捻掳掴掷掸掺掼揸揽揿搀搁搂搅携摄摅摆摇摈摊撄撑撵撷撸撺擞攒敌敛数斋斓斗斩断无旧时旷旸昙昼昽显晋晒晓晔晕晖暂暧札术朴机杀杂权条来杨杩杰极构枞枢枣枥枧枨枪枫枭柜柠柽栀栅标栈栉栊栋栌栎栏树栖样栾桊桠桡桢档桤桥桦桧桨桩梦梼梾检棂椁椟椠椤椭楼榄榇榈榉槚槛槟槠横樯樱橥橱橹橼檐檩欢欤欧歼殁殇残殒殓殚殡殴毁毂毕毙毡毵氇气氢氩氲汇汉污汤汹沓沟没沣沤沥沦沧沨沩沪沵泞泪泶泷泸泺泻泼泽泾洁洒洼浃浅浆浇浈浉浊测浍济浏浐浑浒浓浔浕涂涌涛涝涞涟涠涡涢涣涤润涧涨涩淀渊渌渍渎渐渑渔渖渗温游湾湿溃溅溆溇滗滚滞滟滠满滢滤滥滦滨滩滪漤潆潇潋潍潜潴澜濑濒灏灭灯灵灾灿炀炉炖炜炝点炼炽烁烂烃烛烟烦烧烨烩烫烬热焕焖焘煅煳熘爱爷牍牦牵牺犊犟状犷犸犹狈狍狝狞独狭狮狯狰狱狲猃猎猕猡猪猫猬献獭玑玙玚玛玮环现玱玺珉珏珐珑珰珲琎琏琐琼瑶瑷璇璎瓒瓮瓯电画畅畲畴疖疗疟疠疡疬疮疯疱疴痈痉痒痖痨痪痫痴瘅瘆瘗瘘瘪瘫瘾瘿癞癣癫癯皑皱皲盏盐监盖盗盘眍眦眬着睁睐睑瞒瞩矫矶矾矿砀码砖砗砚砜砺砻砾础硁硅硕硖硗硙硚确硷碍碛碜碱碹磙礼祎祢祯祷祸禀禄禅离秃秆种积称秽秾稆税稣稳穑穷窃窍窑窜窝窥窦窭竖竞笃笋笔笕笺笼笾筑筚筛筜筝筹签简箓箦箧箨箩箪箫篑篓篮篱簖籁籴类籼粜粝粤粪粮糁糇紧絷纟纠纡红纣纤纥约级纨纩纪纫纬纭纮纯纰纱纲纳纴纵纶纷纸纹纺纻纼纽纾线绀绁绂练组绅细织终绉绊绋绌绍绎经绐绑绒结绔绕绖绗绘给绚绛络绝绞统绠绡绢绣绤绥绦继绨绩绪绫绬续绮绯绰绱绲绳维绵绶绷绸绹绺绻综绽绾绿缀缁缂缃缄缅缆缇缈缉缊缋缌缍缎缏缐缑缒缓缔缕编缗缘缙缚缛缜缝缞缟缠缡缢缣缤缥缦缧缨缩缪缫缬缭缮缯缰缱缲缳缴缵罂网罗罚罢罴羁羟羡翘翙翚耢耧耸耻聂聋职聍联聩聪肃肠肤肷肾肿胀胁胆胜胧胨胪胫胶脉脍脏脐脑脓脔脚脱脶脸腊腌腘腭腻腼腽腾膑臜舆舣舰舱舻艰艳艹艺节芈芗芜芦苁苇苈苋苌苍苎苏苘苹茎茏茑茔茕茧荆荐荙荚荛荜荞荟荠荡荣荤荥荦荧荨荩荪荫荬荭荮药莅莜莱莲莳莴莶获莸莹莺莼萚萝萤营萦萧萨葱蒇蒉蒋蒌蓝蓟蓠蓣蓥蓦蔷蔹蔺蔼蕲蕴薮藁藓虏虑虚虫虬虮虽虾虿蚀蚁蚂蚕蚝蚬蛊蛎蛏蛮蛰蛱蛲蛳蛴蜕蜗蜡蝇蝈蝉蝎蝼蝾螀螨蟏衅衔补衬衮袄袅袆袜袭袯装裆裈裢裣裤裥褛褴襁襕见观觃规觅视觇览觉觊觋觌觍觎觏觐觑觞触觯詟誉誊讠计订讣认讥讦讧讨让讪讫训议讯记讱讲讳讴讵讶讷许讹论讻讼讽设访诀证诂诃评诅识诇诈诉诊诋诌词诎诏诐译诒诓诔试诖诗诘诙诚诛诜话诞诟诠诡询诣诤该详诧诨诩诪诫诬语诮误诰诱诲诳说诵诶请诸诹诺读诼诽课诿谀谁谂调谄谅谆谇谈谊谋谌谍谎谏谐谑谒谓谔谕谖谗谘谙谚谛谜谝谞谟谠谡谢谣谤谥谦谧谨谩谪谫谬谭谮谯谰谱谲谳谴谵谶谷豮贝贞负贠贡财责贤败账货质贩贪贫贬购贮贯贰贱贲贳贴贵贶贷贸费贺贻贼贽贾贿赀赁赂赃资赅赆赇赈赉赊赋赌赍赎赏赐赑赒赓赔赕赖赗赘赙赚赛赜赝赞赟赠赡赢赣赪赵赶趋趱趸跃跄跖跞践跶跷跸跹跻踊踌踪踬踯蹑蹒蹰蹿躏躜躯车轧轨轩轪轫转轭轮软轰轱轲轳轴轵轶轷轸轹轺轻轼载轾轿辀辁辂较辄辅辆辇辈辉辊辋辌辍辎辏辐辑辒输辔辕辖辗辘辙辚辞辩辫边辽达迁过迈运还这进远违连迟迩迳迹适选逊递逦逻遗遥邓邝邬邮邹邺邻郁郄郏郐郑郓郦郧郸酝酦酱酽酾酿释里鉅鉴銮錾钆钇针钉钊钋钌钍钎钏钐钑钒钓钔钕钖钗钘钙钚钛钝钞钟钠钡钢钣钤钥钦钧钨钩钪钫钬钭钮钯钰钱钲钳钴钵钶钷钸钹钺钻钼钽钾钿铀铁铂铃铄铅铆铈铉铊铋铍铎铏铐铑铒铕铗铘铙铚铛铜铝铞铟铠铡铢铣铤铥铦铧铨铪铫铬铭铮铯铰铱铲铳铴铵银铷铸铹铺铻铼铽链铿销锁锂锃锄锅锆锇锈锉锊锋锌锍锎锏锐锑锒锓锔锕锖锗错锚锜锞锟锠锡锢锣锤锥锦锨锩锫锬锭键锯锰锱锲锳锴锵锶锷锸锹锺锻锼锽锾锿镀镁镂镃镆镇镈镉镊镌镍镎镏镐镑镒镕镖镗镙镚镛镜镝镞镟镠镡镢镣镤镥镦镧镨镩镪镫镬镭镮镯镰镱镲镳镴镶长门闩闪闫闬闭问闯闰闱闲闳间闵闶闷闸闹闺闻闼闽闾闿阀阁阂阃阄阅阆阇阈阉阊阋阌阍阎阏阐阑阒阓阔阕阖阗阘阙阚阛队阳阴阵阶际陆陇陈陉陕陧陨险随隐隶隽难雏雠雳雾霁霉霭靓静靥鞑鞒鞯鞴韦韧韨韩韪韫韬韵页顶顷顸项顺须顼顽顾顿颀颁颂颃预颅领颇颈颉颊颋颌颍颎颏颐频颒颓颔颕颖颗题颙颚颛颜额颞颟颠颡颢颣颤颥颦颧风飏飐飑飒飓飔飕飖飗飘飙飚飞飨餍饤饥饦饧饨饩饪饫饬饭饮饯饰饱饲饳饴饵饶饷饸饹饺饻饼饽饾饿馀馁馂馃馄馅馆馇馈馉馊馋馌馍馎馏馐馑馒馓馔馕马驭驮驯驰驱驲驳驴驵驶驷驸驹驺驻驼驽驾驿骀骁骂骃骄骅骆骇骈骉骊骋验骍骎骏骐骑骒骓骔骕骖骗骘骙骚骛骜骝骞骟骠骡骢骣骤骥骦骧髅髋髌鬓魇魉鱼鱽鱾鱿鲀鲁鲂鲄鲅鲆鲇鲈鲉鲊鲋鲌鲍鲎鲏鲐鲑鲒鲓鲔鲕鲖鲗鲘鲙鲚鲛鲜鲝鲞鲟鲠鲡鲢鲣鲤鲥鲦鲧鲨鲩鲪鲫鲬鲭鲮鲯鲰鲱鲲鲳鲴鲵鲶鲷鲸鲹鲺鲻鲼鲽鲾鲿鳀鳁鳂鳃鳄鳅鳆鳇鳈鳉鳊鳋鳌鳍鳎鳏鳐鳑鳒鳓鳔鳕鳖鳗鳘鳙鳛鳜鳝鳞鳟鳠鳡鳢鳣鸟鸠鸡鸢鸣鸤鸥鸦鸧鸨鸩鸪鸫鸬鸭鸮鸯鸰鸱鸲鸳鸴鸵鸶鸷鸸鸹鸺鸻鸼鸽鸾鸿鹀鹁鹂鹃鹄鹅鹆鹇鹈鹉鹊鹋鹌鹍鹎鹏鹐鹑鹒鹓鹔鹕鹖鹗鹘鹚鹛鹜鹝鹞鹟鹠鹡鹢鹣鹤鹥鹦鹧鹨鹩鹪鹫鹬鹭鹯鹰鹱鹲鹳鹴鹾麦麸黄黉黡黩黪黾鼋鼌鼍鼗鼹齄齐齑齿龀龁龂龃龄龅龆龇龈龉龊龋龌龙龚龛龟志制咨只里系范松没尝尝闹面准钟别闲干尽脏拼"),l=new String("萬與醜專業叢東絲丟兩嚴喪個爿豐臨為麗舉麼義烏樂喬習鄉書買亂爭於虧雲亙亞產畝親褻嚲億僅從侖倉儀們價眾優夥會傴傘偉傳傷倀倫傖偽佇體餘傭僉俠侶僥偵側僑儈儕儂俁儔儼倆儷儉債傾傯僂僨償儻儐儲儺兒兌兗黨蘭關興茲養獸囅內岡冊寫軍農塚馮衝決況凍淨淒涼淩減湊凜幾鳳鳧憑凱擊氹鑿芻劃劉則剛創刪別剗剄劊劌剴劑剮劍剝劇勸辦務勱動勵勁勞勢勳猛勩勻匭匱區醫華協單賣盧鹵臥衛卻巹廠廳曆厲壓厭厙廁廂厴廈廚廄廝縣參靉靆雙發變敘疊葉號歎嘰籲後嚇呂嗎唚噸聽啟吳嘸囈嘔嚦唄員咼嗆嗚詠哢嚨嚀噝吒噅鹹呱響啞噠嘵嗶噦嘩噲嚌噥喲嘜嗊嘮啢嗩唕喚呼嘖嗇囀齧囉嘽嘯噴嘍嚳囁嗬噯噓嚶囑嚕劈囂謔團園囪圍圇國圖圓聖壙場阪壞塊堅壇壢壩塢墳墜壟壟壚壘墾坰堊墊埡墶壋塏堖塒塤堝墊垵塹墮壪牆壯聲殼壺壼處備複夠頭誇夾奪奩奐奮獎奧妝婦媽嫵嫗媯姍薑婁婭嬈嬌孌娛媧嫻嫿嬰嬋嬸媼嬡嬪嬙嬤孫學孿寧寶實寵審憲宮寬賓寢對尋導壽將爾塵堯尷屍盡層屭屜屆屬屢屨嶼歲豈嶇崗峴嶴嵐島嶺嶽崠巋嶨嶧峽嶢嶠崢巒嶗崍嶮嶄嶸嶔崳嶁脊巔鞏巰幣帥師幃帳簾幟帶幀幫幬幘幗冪襆幹並廣莊慶廬廡庫應廟龐廢廎廩開異棄張彌弳彎彈強歸當錄彠彥徹徑徠禦憶懺憂愾懷態慫憮慪悵愴憐總懟懌戀懇惡慟懨愷惻惱惲悅愨懸慳憫驚懼慘懲憊愜慚憚慣湣慍憤憒願懾憖怵懣懶懍戇戔戲戧戰戩戶紮撲扡執擴捫掃揚擾撫拋摶摳掄搶護報擔擬攏揀擁攔擰撥擇掛摯攣掗撾撻挾撓擋撟掙擠揮撏撈損撿換搗據撚擄摑擲撣摻摜摣攬撳攙擱摟攪攜攝攄擺搖擯攤攖撐攆擷擼攛擻攢敵斂數齋斕鬥斬斷無舊時曠暘曇晝曨顯晉曬曉曄暈暉暫曖劄術樸機殺雜權條來楊榪傑極構樅樞棗櫪梘棖槍楓梟櫃檸檉梔柵標棧櫛櫳棟櫨櫟欄樹棲樣欒棬椏橈楨檔榿橋樺檜槳樁夢檮棶檢欞槨櫝槧欏橢樓欖櫬櫚櫸檟檻檳櫧橫檣櫻櫫櫥櫓櫞簷檁歡歟歐殲歿殤殘殞殮殫殯毆毀轂畢斃氈毿氌氣氫氬氳彙漢汙湯洶遝溝沒灃漚瀝淪滄渢溈滬濔濘淚澩瀧瀘濼瀉潑澤涇潔灑窪浹淺漿澆湞溮濁測澮濟瀏滻渾滸濃潯濜塗湧濤澇淶漣潿渦溳渙滌潤澗漲澀澱淵淥漬瀆漸澠漁瀋滲溫遊灣濕潰濺漵漊潷滾滯灩灄滿瀅濾濫灤濱灘澦濫瀠瀟瀲濰潛瀦瀾瀨瀕灝滅燈靈災燦煬爐燉煒熗點煉熾爍爛烴燭煙煩燒燁燴燙燼熱煥燜燾煆糊溜愛爺牘犛牽犧犢強狀獷獁猶狽麅獮獰獨狹獅獪猙獄猻獫獵獼玀豬貓蝟獻獺璣璵瑒瑪瑋環現瑲璽瑉玨琺瓏璫琿璡璉瑣瓊瑤璦璿瓔瓚甕甌電畫暢佘疇癤療瘧癘瘍鬁瘡瘋皰屙癰痙癢瘂癆瘓癇癡癉瘮瘞瘺癟癱癮癭癩癬癲臒皚皺皸盞鹽監蓋盜盤瞘眥矓著睜睞瞼瞞矚矯磯礬礦碭碼磚硨硯碸礪礱礫礎硜矽碩硤磽磑礄確鹼礙磧磣堿镟滾禮禕禰禎禱禍稟祿禪離禿稈種積稱穢穠穭稅穌穩穡窮竊竅窯竄窩窺竇窶豎競篤筍筆筧箋籠籩築篳篩簹箏籌簽簡籙簀篋籜籮簞簫簣簍籃籬籪籟糴類秈糶糲粵糞糧糝餱緊縶糸糾紆紅紂纖紇約級紈纊紀紉緯紜紘純紕紗綱納紝縱綸紛紙紋紡紵紖紐紓線紺絏紱練組紳細織終縐絆紼絀紹繹經紿綁絨結絝繞絰絎繪給絢絳絡絕絞統綆綃絹繡綌綏絛繼綈績緒綾緓續綺緋綽緔緄繩維綿綬繃綢綯綹綣綜綻綰綠綴緇緙緗緘緬纜緹緲緝縕繢緦綞緞緶線緱縋緩締縷編緡緣縉縛縟縝縫縗縞纏縭縊縑繽縹縵縲纓縮繆繅纈繚繕繒韁繾繰繯繳纘罌網羅罰罷羆羈羥羨翹翽翬耮耬聳恥聶聾職聹聯聵聰肅腸膚膁腎腫脹脅膽勝朧腖臚脛膠脈膾髒臍腦膿臠腳脫腡臉臘醃膕齶膩靦膃騰臏臢輿艤艦艙艫艱豔艸藝節羋薌蕪蘆蓯葦藶莧萇蒼苧蘇檾蘋莖蘢蔦塋煢繭荊薦薘莢蕘蓽蕎薈薺蕩榮葷滎犖熒蕁藎蓀蔭蕒葒葤藥蒞蓧萊蓮蒔萵薟獲蕕瑩鶯蓴蘀蘿螢營縈蕭薩蔥蕆蕢蔣蔞藍薊蘺蕷鎣驀薔蘞藺藹蘄蘊藪槁蘚虜慮虛蟲虯蟣雖蝦蠆蝕蟻螞蠶蠔蜆蠱蠣蟶蠻蟄蛺蟯螄蠐蛻蝸蠟蠅蟈蟬蠍螻蠑螿蟎蠨釁銜補襯袞襖嫋褘襪襲襏裝襠褌褳襝褲襇褸襤繈襴見觀覎規覓視覘覽覺覬覡覿覥覦覯覲覷觴觸觶讋譽謄訁計訂訃認譏訐訌討讓訕訖訓議訊記訒講諱謳詎訝訥許訛論訩訟諷設訪訣證詁訶評詛識詗詐訴診詆謅詞詘詔詖譯詒誆誄試詿詩詰詼誠誅詵話誕詬詮詭詢詣諍該詳詫諢詡譸誡誣語誚誤誥誘誨誑說誦誒請諸諏諾讀諑誹課諉諛誰諗調諂諒諄誶談誼謀諶諜謊諫諧謔謁謂諤諭諼讒諮諳諺諦謎諞諝謨讜謖謝謠謗諡謙謐謹謾謫譾謬譚譖譙讕譜譎讞譴譫讖穀豶貝貞負貟貢財責賢敗賬貨質販貪貧貶購貯貫貳賤賁貰貼貴貺貸貿費賀貽賊贄賈賄貲賃賂贓資賅贐賕賑賚賒賦賭齎贖賞賜贔賙賡賠賧賴賵贅賻賺賽賾贗讚贇贈贍贏贛赬趙趕趨趲躉躍蹌蹠躒踐躂蹺蹕躚躋踴躊蹤躓躑躡蹣躕躥躪躦軀車軋軌軒軑軔轉軛輪軟轟軲軻轤軸軹軼軤軫轢軺輕軾載輊轎輈輇輅較輒輔輛輦輩輝輥輞輬輟輜輳輻輯轀輸轡轅轄輾轆轍轔辭辯辮邊遼達遷過邁運還這進遠違連遲邇逕跡適選遜遞邐邏遺遙鄧鄺鄔郵鄒鄴鄰鬱郤郟鄶鄭鄆酈鄖鄲醞醱醬釅釃釀釋裏钜鑒鑾鏨釓釔針釘釗釙釕釷釺釧釤鈒釩釣鍆釹鍚釵鈃鈣鈈鈦鈍鈔鍾鈉鋇鋼鈑鈐鑰欽鈞鎢鉤鈧鈁鈥鈄鈕鈀鈺錢鉦鉗鈷缽鈳鉕鈽鈸鉞鑽鉬鉭鉀鈿鈾鐵鉑鈴鑠鉛鉚鈰鉉鉈鉍鈹鐸鉶銬銠鉺銪鋏鋣鐃銍鐺銅鋁銱銦鎧鍘銖銑鋌銩銛鏵銓鉿銚鉻銘錚銫鉸銥鏟銃鐋銨銀銣鑄鐒鋪鋙錸鋱鏈鏗銷鎖鋰鋥鋤鍋鋯鋨鏽銼鋝鋒鋅鋶鐦鐧銳銻鋃鋟鋦錒錆鍺錯錨錡錁錕錩錫錮鑼錘錐錦鍁錈錇錟錠鍵鋸錳錙鍥鍈鍇鏘鍶鍔鍤鍬鍾鍛鎪鍠鍰鎄鍍鎂鏤鎡鏌鎮鎛鎘鑷鐫鎳鎿鎦鎬鎊鎰鎔鏢鏜鏍鏰鏞鏡鏑鏃鏇鏐鐔钁鐐鏷鑥鐓鑭鐠鑹鏹鐙鑊鐳鐶鐲鐮鐿鑔鑣鑞鑲長門閂閃閆閈閉問闖閏闈閑閎間閔閌悶閘鬧閨聞闥閩閭闓閥閣閡閫鬮閱閬闍閾閹閶鬩閿閽閻閼闡闌闃闠闊闋闔闐闒闕闞闤隊陽陰陣階際陸隴陳陘陝隉隕險隨隱隸雋難雛讎靂霧霽黴靄靚靜靨韃鞽韉韝韋韌韍韓韙韞韜韻頁頂頃頇項順須頊頑顧頓頎頒頌頏預顱領頗頸頡頰頲頜潁熲頦頤頻頮頹頷頴穎顆題顒顎顓顏額顳顢顛顙顥纇顫顬顰顴風颺颭颮颯颶颸颼颻飀飄飆飆飛饗饜飣饑飥餳飩餼飪飫飭飯飲餞飾飽飼飿飴餌饒餉餄餎餃餏餅餑餖餓餘餒餕餜餛餡館餷饋餶餿饞饁饃餺餾饈饉饅饊饌饢馬馭馱馴馳驅馹駁驢駔駛駟駙駒騶駐駝駑駕驛駘驍罵駰驕驊駱駭駢驫驪騁驗騂駸駿騏騎騍騅騌驌驂騙騭騤騷騖驁騮騫騸驃騾驄驏驟驥驦驤髏髖髕鬢魘魎魚魛魢魷魨魯魴魺鮁鮃鯰鱸鮋鮓鮒鮊鮑鱟鮍鮐鮭鮚鮳鮪鮞鮦鰂鮜鱠鱭鮫鮮鮺鯗鱘鯁鱺鰱鰹鯉鰣鰷鯀鯊鯇鮶鯽鯒鯖鯪鯕鯫鯡鯤鯧鯝鯢鯰鯛鯨鯵鯴鯔鱝鰈鰏鱨鯷鰮鰃鰓鱷鰍鰒鰉鰁鱂鯿鰠鼇鰭鰨鰥鰩鰟鰜鰳鰾鱈鱉鰻鰵鱅鰼鱖鱔鱗鱒鱯鱤鱧鱣鳥鳩雞鳶鳴鳲鷗鴉鶬鴇鴆鴣鶇鸕鴨鴞鴦鴒鴟鴝鴛鴬鴕鷥鷙鴯鴰鵂鴴鵃鴿鸞鴻鵐鵓鸝鵑鵠鵝鵒鷳鵜鵡鵲鶓鵪鶤鵯鵬鵮鶉鶊鵷鷫鶘鶡鶚鶻鶿鶥鶩鷊鷂鶲鶹鶺鷁鶼鶴鷖鸚鷓鷚鷯鷦鷲鷸鷺鸇鷹鸌鸏鸛鸘鹺麥麩黃黌黶黷黲黽黿鼂鼉鞀鼴齇齊齏齒齔齕齗齟齡齙齠齜齦齬齪齲齷龍龔龕龜誌製谘隻裡係範鬆冇嚐嘗鬨麵準鐘彆閒乾儘臟拚");function u(t,e){var n,i,r,a,u,f="",o=e?(u=c,l):(u=l,c);if("string"!=typeof t)return t;for(n=0;n<t.length;n++)i=t.charAt(n),13312<(r=t.charCodeAt(n))&&r<40899||63744<r&&r<64106?f+=-1!==(a=u.indexOf(i))?o.charAt(a):i:f+=i;return f}function a(t,e){var n,i;if(1===t.nodeType)for(i=t.childNodes,n=0;n<i.length;n++){var r=i.item(n);if(1===r.nodeType){if(-1!=="|BR|HR|TEXTAREA|SCRIPT|OBJECT|EMBED|".indexOf("|"+r.tagName+"|"))continue;!function t(e,n,i){var r,a;if(n instanceof Array)for(r=0;r<n.length;r++)t(e,n[r],i);else""!==(a=e.getAttribute(n))&&null!==a&&e.setAttribute(n,u(a,i))}(r,["title","data-original-title","alt","placeholder"],e),"INPUT"===r.tagName&&""!==r.value&&"text"!==r.type&&"hidden"!==r.type&&(r.value=u(r.value,e)),a(r,e)}else 3===r.nodeType&&(r.data=u(r.data,e))}}t.extend({s2t:function(t){return u(t,!0)},t2s:function(t){return u(t,!1)}}),t.fn.extend({s2t:function(){return this.each(function(){a(this,!0)})},t2s:function(){return this.each(function(){a(this,!1)})}})}(jQuery);
    """
    return template
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
<!-- <br><button onclick='toggleHiddenShowClass("KR")' > Toggle Visible/Invisible KR</button><br>-->
<br><button onclick='toggleDisplayShowClass("JP")' > Toggle Display/Hide JP</button>
<!-- <br><button onclick='toggleHiddenShowClass("JP")' > Toggle Visible/Invisible JP</button><br>-->
<br><button onclick='toggleDisplayShowClass("CN")' > Toggle Display/Hide CN</button>
<!-- <br><button onclick='toggleHiddenShowClass("CN")' > Toggle Visible/Invisible CN</button><br>-->
<br><button onclick='(function(){$(".CN").s2t();})();' > Convert to Traditional</button><br>
<br><button onclick='(function(){$(".CN").t2s();})();' > Convert to Simplified</button><br>
<script type='text/javascript' src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script type='text/javascript' src="jquery.s2t.js"></script>
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
      open(os.path.join(output_path, "jquery.s2t.js"), "w", encoding="utf8").write(s2t_JS_Template())

      #shutil.copy("jquery.s2t.js", output_path)
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
