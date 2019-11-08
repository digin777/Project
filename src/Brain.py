import threading
#
import pyttsx3 as pts
import sys,re
sys.path.append("/home/pi/git/project/Project/src/libs/")
import socket,time
from libs.recipe.recipe import *
from libs.Alaram.alarm import *
from libs.weather.Weather import *
from libs.News import news
from libs.IoT.IOT import *
from libs.MsgPass.msgpass import *
from libs.wolfram.Wolfram import *
from libs.CricketScore.cricket import crickbuz
import wikipedia as wiki
import logging
elsa=pts.init()
connectives=['in', 'at', 'is','a','an','and','the','are','with','for','on','was','of']
connectives_IOT=['in', 'at', 'is','a','an','and','the','are','with','for']
days=['today','yesterday','tomorrow',"yesterday's","today's","tomarrows","tomorrow's"]
qust=['what','where','when','why','who','how','whats',"hows","how's","whos","what's","where's","wheres","whys","why's","who's"]
info=['my','you','your','i','you’s','mine','yours','me']
commamds=['alarm','timer','headline','headlines','news','remind','weather','livescore','score','recipe','bible','nearby','reminder','turn','switch','your','yours',"your's",'you','recipes']
HOST = '127.0.0.1'
PORT=6373

class Parser():
    def __init__(self):
        self.x=0
    def wearher_checking(self,inp_arry,sinp):
        stripped_array=inp_arry[inp_arry.index('weather')+1:]
        print("weather")
        for conective in connectives:
            if conective in stripped_array:
                stripped_array.remove(conective)
        if stripped_array[0] in days:
            weather_detials=get16daysweather(stripped_array[1])
        else:
            weather_detials=getwether(stripped_array.pop())
        print(weather_detials)
        
        #CODE FOR SENDING WEATHER DATA  TO SOCKET
        Msgpass(weather_detials)
        



    def alaram(self,inp_arry):
        stripped_array=inp_arry[inp_arry.index('alarm')+1:]
        a_hour=a_minute=None
        for conective in connectives:
            if conective in stripped_array:
                stripped_array.remove(conective)
        if len(stripped_array)==0:
            print("Canot set an alaram")
        elif len(stripped_array)==1:
            if stripped_array[0].isdigit():
                a_hour=stripped_array[0]
                a_minute=0
            elif len(stripped_array[0].split(':'))!=0:
                a_hour=stripped_array[0].split(':')[0]
                a_minute=stripped_array[0].split(':')[1]
        elif len(stripped_array)==2:
            if stripped_array[0].isdigit():
                a_hour=stripped_array[0]
                a_minute=0
            elif len(stripped_array[0].split(':'))!=0:
                a_hour=stripped_array[0].split(':')[0]
                a_minute=stripped_array[0].split(':')[1]
            if stripped_array[1]=='p.m.':
                a_hour=int(a_hour)
                if a_hour<12:
                    a_hour+=12
        if a_hour and a_minute is not None:
            a_hour,a_minute=int(a_hour),int(a_minute)
            if a_hour>24 or a_minute>59:
                print("Please Provide valid Time")
            else:
                setalaram(int(a_hour),int(a_minute))
                
                
                
                
    def IoT(self,inp_arry,command):
        port_map={'lbed':10,'fbed':12,'lmain':16,'fmain':18}
        stripped_array=inp_arry[inp_arry.index(command):]
        index_of_command=stripped_array.index(command)
        for connective in connectives_IOT:
            if connective in stripped_array:
                while stripped_array.count(connective)>0:
                    stripped_array.remove(connective)
        try:
            state=None
            state=stripped_array[index_of_command+1]
            if state=='off' or state=='of':
                state='off'
            elif state=='on':
                state='on'
            room_id=None
            print(stripped_array)
            if (stripped_array[index_of_command+2]=='light' or stripped_array[index_of_command+2]=='lights') and ((stripped_array[index_of_command+3]=='bed' and stripped_array[index_of_command+4]=='room') or (stripped_array[index_of_command+3]=='bedroom')):
                room_id='lbed'
            elif (stripped_array[index_of_command+2]=='light' or stripped_array[index_of_command+2]=='lights') and ((stripped_array[index_of_command+3]=='main' and stripped_array[index_of_command+4]=='room')or (stripped_array[index_of_command+3]=='mainroom')):
                room_id='lmain'
            elif (stripped_array[index_of_command+2]=='fan' or stripped_array[index_of_command+2]=='fans') and ((stripped_array[index_of_command+3]=='main' and stripped_array[index_of_command+4]=='room')or (stripped_array[index_of_command+3]=='mainroom')):
                room_id='fmain'
            elif (stripped_array[index_of_command+2]=='fan' or stripped_array[index_of_command+2]=='fans') and ((stripped_array[index_of_command+3]=='bed' and stripped_array[index_of_command+4]=='room')or (stripped_array[index_of_command+3]=='bedroom')):
                room_id='fbed'
            
            if state is not None and room_id is not None:
                pin_No=port_map[room_id]
                result=performIOT(pin_No,state.upper())
            else:
                result='Unknown command'
        except:
            result='Unknown command'
            
        
        
        
    def news(self,inp_arry,sinp,command):
        news_catagory=news_from_country=None
        news_from_country='india'
        index_of_command=inp_arry.index(command) #index of command in the input array
        for conective in connectives: #Removing Connectives from input array
            if conective in inp_arry:
                inp_arry.remove(conective)
        try:
            if inp_arry[index_of_command+1]=='about':#checking weather any specific catagory of news is specified in the speech
                news_catagory=inp_arry[index_of_command+2]
        except IndexError:
            pass
        try:
            if inp_arry[index_of_command+3]=='from': #checking weather any specific country is specified
                news_from_country=inp_arry[index_of_command+4]
        except IndexError:
            pass
        ISOCOEDS={'afghanistan': 'af', 'aland islands': 'ax', 'albania': 'al', 'algeria': 'dz', 'american samoa': 'as', 'andorra': 'ad', 'angola': 'ao', 'anguilla': 'ai', 'antarctica': 'aq', 'antigua and barbuda': 'ag', 'argentina': 'ar', 'armenia': 'am', 'aruba': 'aw', 'australia': 'au', 'austria': 'at', 'azerbaijan': 'az', 'bahamas': 'bs', 'bahrain': 'bh', 'bangladesh': 'bd', 'barbados': 'bb', 'belarus': 'by', 'belgium': 'be', 'belize': 'bz', 'benin': 'bj', 'bermuda': 'bm', 'bhutan': 'bt', 'bolivia': 'bo', 'bosnia and herzegovina': 'ba', 'botswana': 'bw', 'bouvet island': 'bv', 'brazil': 'br', 'british indian ocean territory': 'io', 'brunei darussalam': 'bn', 'bulgaria': 'bg', 'burkina faso': 'bf', 'burundi': 'bi', 'cambodia': 'kh', 'cameroon': 'cm', 'canada': 'ca', 'cape verde': 'cv', 'cayman islands': 'ky', 'central african republic': 'cf', 'chad': 'td', 'chile': 'cl', 'china': 'cn', 'christmas island': 'cx', 'cocos (keeling) islands': 'cc', 'colombia': 'co', 'comoros': 'km', 'congo': 'cg', 'congo, democratic republic': 'cd', 'cook islands': 'ck', 'costa rica': 'cr', 'cote d"ivoire': 'ci', 'croatia': 'hr', 'cuba': 'cu', 'cyprus': 'cy', 'czech republic': 'cz', 'denmark': 'dk', 'djibouti': 'dj', 'dominica': 'dm', 'dominican republic': 'do', 'ecuador': 'ec', 'egypt': 'eg', 'el salvador': 'sv', 'equatorial guinea': 'gq', 'eritrea': 'er', 'estonia': 'ee', 'ethiopia': 'et', 'falkland islands (malvinas)': 'fk', 'faroe islands': 'fo', 'fiji': 'fj', 'finland': 'fi', 'france': 'fr', 'french guiana': 'gf', 'french polynesia': 'pf', 'french southern territories': 'tf', 'gabon': 'ga', 'gambia': 'gm', 'georgia': 'ge', 'germany': 'de', 'ghana': 'gh', 'gibraltar': 'gi', 'greece': 'gr', 'greenland': 'gl', 'grenada': 'gd', 'guadeloupe': 'gp', 'guam': 'gu', 'guatemala': 'gt', 'guernsey': 'gg', 'guinea': 'gn', 'guinea-bissau': 'gw', 'guyana': 'gy', 'haiti': 'ht', 'heard island & mcdonald islands': 'hm', 'holy see (vatican city state)': 'va', 'honduras': 'hn', 'hong kong': 'hk', 'hungary': 'hu', 'iceland': 'is', 'india': 'in', 'indonesia': 'id', 'iran, islamic republic of': 'ir', 'iraq': 'iq', 'ireland': 'ie', 'isle of man': 'im', 'israel': 'il', 'italy': 'it', 'jamaica': 'jm', 'japan': 'jp', 'jersey': 'je', 'jordan': 'jo', 'kazakhstan': 'kz', 'kenya': 'ke', 'kiribati': 'ki', 'korea': 'kr', 'kuwait': 'kw', 'kyrgyzstan': 'kg', 'lao people"s democratic republic': 'la', 'latvia': 'lv', 'lebanon': 'lb', 'lesotho': 'ls', 'liberia': 'lr', 'libyan arab jamahiriya': 'ly', 'liechtenstein': 'li', 'lithuania': 'lt', 'luxembourg': 'lu', 'macao': 'mo', 'macedonia': 'mk', 'madagascar': 'mg', 'malawi': 'mw', 'malaysia': 'my', 'maldives': 'mv', 'mali': 'ml', 'malta': 'mt', 'marshall islands': 'mh', 'martinique': 'mq', 'mauritania': 'mr', 'mauritius': 'mu', 'mayotte': 'yt', 'mexico': 'mx', 'micronesia, federated states of': 'fm', 'moldova': 'md', 'monaco': 'mc', 'mongolia': 'mn', 'montenegro': 'me', 'montserrat': 'ms', 'morocco': 'ma', 'mozambique': 'mz', 'myanmar': 'mm', 'namibia': 'na', 'nauru': 'nr', 'nepal': 'np', 'netherlands': 'nl', 'netherlands antilles': 'an', 'new caledonia': 'nc', 'new zealand': 'nz', 'nicaragua': 'ni', 'niger': 'ne', 'nigeria': 'ng', 'niue': 'nu', 'norfolk island': 'nf', 'northern mariana islands': 'mp', 'norway': 'no', 'oman': 'om', 'pakistan': 'pk', 'palau': 'pw', 'palestinian territory, occupied': 'ps', 'panama': 'pa', 'papua new guinea': 'pg', 'paraguay': 'py', 'peru': 'pe', 'philippines': 'ph', 'pitcairn': 'pn', 'poland': 'pl', 'portugal': 'pt', 'puerto rico': 'pr', 'qatar': 'qa', 'reunion': 're', 'romania': 'ro', 'russian federation': 'ru', 'rwanda': 'rw', 'saint barthelemy': 'bl', 'saint helena': 'sh', 'saint kitts and nevis': 'kn', 'saint lucia': 'lc', 'saint martin': 'mf', 'saint pierre and miquelon': 'pm', 'saint vincent and grenadines': 'vc', 'samoa': 'ws', 'san marino': 'sm', 'sao tome and principe': 'st', 'saudi arabia': 'sa', 'senegal': 'sn', 'serbia': 'rs', 'seychelles': 'sc', 'sierra leone': 'sl', 'singapore': 'sg', 'slovakia': 'sk', 'slovenia': 'si', 'solomon islands': 'sb', 'somalia': 'so', 'south africa': 'za', 'south georgia and sandwich isl.': 'gs', 'spain': 'es', 'sri lanka': 'lk', 'sudan': 'sd', 'suriname': 'sr', 'svalbard and jan mayen': 'sj', 'swaziland': 'sz', 'sweden': 'se', 'switzerland': 'ch', 'syrian arab republic': 'sy', 'taiwan': 'tw', 'tajikistan': 'tj', 'tanzania': 'tz', 'thailand': 'th', 'timor-leste': 'tl', 'togo': 'tg', 'tokelau': 'tk', 'tonga': 'to', 'trinidad and tobago': 'tt', 'tunisia': 'tn', 'turkey': 'tr', 'turkmenistan': 'tm', 'turks and caicos islands': 'tc', 'tuvalu': 'tv', 'uganda': 'ug', 'ukraine': 'ua', 'united arab emirates': 'ae', 'united kingdom': 'gb', 'united states': 'us', 'united states outlying islands': 'um', 'uruguay': 'uy', 'uzbekistan': 'uz', 'vanuatu': 'vu', 'venezuela': 've', 'viet nam': 'vn', 'virgin islands, british': 'vg', 'virgin islands, u.s.': 'vi', 'wallis and futuna': 'wf', 'western sahara': 'eh', 'yemen': 'ye', 'zambia': 'zm', 'zimbabwe': 'zw', 'af': 'afghanistan'}
        #iso country codes
        
        if news_from_country is not None and news_from_country in ISOCOEDS.keys():
            news_from_country=ISOCOEDS[news_from_country] #assign country codes

        headlines=news.getNews(country=news_from_country,category=news_catagory,page=2)
        if type(headlines)==list: #check werather list of head line is returened
            headlines=headlines[:4]
            result=''
            for headline in headlines:
                result+=headline+(2*'\n')
            headlines=result
            print(headlines)
        else:
            print(headlines) #error so error message is returend
        Msgpass(headlines)
        
        
        
    def relation(self,inp_arr,command):
        relations=['family','father','mother','brother','sister','husbend','wife','son','doughter']
        try:
            if inp_arr[inp_arr.index(command)+1] in relations:
                Msgpass(f'I dont have a {inp_arr[inp_arr.index(command)+1]} i am an AI based virtual assitant developed by DSP software foundations ')
        except:
            Msgpass('Unknown command')
    def wikiprocess(self,inp_arr,sinp):
        collection=[connectives,days,qust]
        for item in collection:
            for connective in item:
                if connective in inp_arr:
                    while inp_arr.count(connective)>0:
                        inp_arr.remove(connective)
        query=''
        for i in inp_arr:
            query+=(' '+i)
        if query is not '':
            try:
                print(query)
                res=wiki.search(query,10)
                summary=wiki.summary(res[0],sentences=3)
                if '(' in summary:
                    summary = str(summary[:summary.index('('):] + summary[summary.index(')') + 2:])
                return summary
            except:
                return "Could not find data"
                
                
    def reminder(self,inp_arr,sinp,command):
        index_of_command=inp_arr.index(command)
        striped_arry=inp_arr[index_of_command:]
        index_of_about=index_of_to =index_of_item= None
        if 'to' in striped_arry:
            index_of_to=striped_arry.index('to')
           
        if 'about' in striped_arry:
            index_of_about=striped_arry.index('about')
        
        if index_of_about is not None and index_of_to is not None:
            if index_of_to<index_of_about:
                index_of_item=index_of_to
            else:
                index_of_item=index_of_about
        elif index_of_about is not None and index_of_to is None:
            index_of_item=index_of_about
        elif index_of_to is not None and index_of_about is None:
            index_of_item=index_of_to
        striped_arry=striped_arry[index_of_item+1:]
        r_time=re.findall(r'\d{1,2}(?:(?:a.m|p.m)|(?::\d{1,2})(?:a.m|p.m)?)', sinp)
        if len(r_time) is not 0:
            r_time=r_time.pop(0)
            r_h=r_time.split(':').pop(0)
            r_min=r_time.split(':').pop(1)
            
            state=None
            try:
                state=inp_arr[inp_arr.index(r_time)+1]
                
                if r_time in striped_arry:
                    striped_arry.pop(striped_arry.index(r_time)+1)
                    striped_arry.pop(striped_arry.index(r_time))
            except IndexError as e:
                state='a.m'
            if state == 'p.m.':
                r_h=int(r_h)+12
            message=''
            for words in striped_arry:
                message+=words+' '
            
            if message is not '':
                setreminder(int(r_h),int(r_min),message)
            else:
                Msgpass('Unable to set your reminder')
            
    def livescore(self):
        crikz=crickbuz()
        scorelist=crikz.livescore()
        res=''
        if type(scorelist)==list:
            for score in scorelist:
                res+=score+5*' \n'
        else:
            res=scorelist
        Msgpass(res)
                
    def recipe(self,inp_arr,sinp,command):
        index_of_command=inp_arr.index(command)
        stripped_array=inp_arr[index_of_command+1:]
        for connective in connectives:
            if connective in stripped_array:
                while stripped_array.count(connective)>0:
                    stripped_array.remove(connective)
        query=''
        for word in stripped_array:
            query+=word+' '
        reci=recipypuppy()
        resdict=reci.search(query)
        res=''
        for k,v in resdict.items():
            res+=k+' ingredients are '+v
            Msgpass(res)
    def getInfo(self,inp):
        cmdflag=0
        inp=str(inp).lower()
        inp_arry=inp.split(' ')
        print(inp_arry)
        main_list=[commamds,qust,info,days,connectives]
        for command in commamds:
            if command in inp_arry:
                cmdflag=1
                if command is 'weather':
                    self.wearher_checking(inp_arry,inp)
                    break
                elif command is 'alarm':
                    self.alaram(inp_arry)
                    break
                elif command is 'switch' or command is 'turn':
                    self.IoT(inp_arry,command)
                    break
                elif command is 'headlines' or command is 'news' or command is 'headline':
                    self.news(inp_arry,inp,command)
                    break
                elif command is 'your' or command is 'yours' or command is "your's":
                    self.relation(inp_arry,command)
                elif command is 'remind' or command is 'reminder':
                    self.reminder(inp_arry,inp,command)
                elif command is 'recipe' or command is 'recipes':
                    self.recipe(inp_arry,inp,command)
                elif command is 'score' or command is 'livescore':
                    self.livescore()
            else :
                pass
        if inp.startswith(tuple(qust)) and len(inp)>5 and cmdflag==0:
                try:
                    res=getwolfram(inp)
                    print('x=',res)
                    if '(' in res:
                        res =res[:res.index('(')]+res[res.index(')')+1:]
                    print('y=',res)
                except:
                    res='could not get the results'
                    res=self.wikiprocess(inp_arry,inp)
                Msgpass(res)
                
        
        
try:
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        while 1:
            s.listen()
            conn,addr=s.accept()
            print("Connected to ",addr)
            while 1:
                data = conn.recv(1024).decode()
                time.sleep(1)
                if not data:
                    break
                parser = Parser()
                threading.Thread(target=parser.getInfo, args=(data,), daemon=True).start()
except Exception as e:
    print("Output is Not allowed",e.args)
