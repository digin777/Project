import threading
#
import pyttsx3 as pts
import sys
sys.path.append("/home/pi/git/project/Project/src/libs/")
import socket,time
from libs.Alaram.alarm import *
from libs.weather.Weather import *
from libs.News import news
import logging
elsa=pts.init()
connectives=['in', 'at', 'is','a','an','and','the','are','with','for','on']
days=['today','yesterday','tomorrow',"yesterday's","today's","tomarrows","tomorrow's"]
qust=['what','where','when','why','who','how','whats',"hows","how's","whos","what's","where's","wheres","whys","why's","who's"]
info=['my','you','your','i','you’s','mine','yours',]
commamds=['alarm','timer','headline','headlines','news','remind','weather','score','recipe','bible','nearby','reminder','trun','switch']
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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, 6687))
                s.sendall(weather_detials.encode())
            except (socket.gaierror, ConnectionRefusedError) as e:
                print("Unable Open the Socket")
            else:
                print("The Message is successfully sent")





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
                #pass
                setalaram(int(a_hour),int(a_minute))
                
                
                
                
    def IoT(self,inp_arry,command):
        stripped_array=inp_arry[inp_arry.index(command)+1:]
        print(stripped_array)
        for connective in connectives:
            if connective in stripped_array:
                while stripped_array.count(connective)>0:
                    stripped_array.remove(connective)
        print(stripped_array)
        
        
        
        
        
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
        '''if news_from_country is not None:
            parameters['country']=news_from_country
        if news_catagory is not None:
            prameters['category']=news_catagory'''
        
     #paramlist=[]
        #for k,v in parameters.items():
            #paramlist.append(k+'='+v)
        #print(paramlist)
        headlines=news.getNews(country=news_from_country,category=news_catagory,page=2)
        if type(headlines)==list: #check werather list of head line is returened
            headlines=headlines[:6]
            result=''
            for headline in headlines:
                result+=headline+(5*'\n')
            headlines=result
            print(headlines)
        else:
            print(headlines) #error so error message is returend
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, 6687))
                s.sendall(headlines.encode())
            except (socket.gaierror, ConnectionRefusedError) as e:
                print("Unable Open the Socket")
            else:
                print("The Message is successfully sent")


        
      
      
        
    def getInfo(self,inp):
        inp=str(inp).lower()
        inp_arry=inp.split(' ')
        print(inp_arry)
        main_list=[commamds,qust,info,days,connectives]
        for command in commamds:
            if command in inp_arry:
                if command is 'weather':
                    self.wearher_checking(inp_arry,inp)
                elif command is 'alarm':
                    self.alaram(inp_arry)
                elif command is 'switch' or command is 'turn':
                    self.IoT(inp_arry,command)
                elif command is 'headlines' or command is 'news' or command is 'headline':
                    print(command)
                    self.news(inp_arry,inp,command)
                    

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
