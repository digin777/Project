import wikipedia as wiki
import pyttsx3 as pts
import requests, json
api_key = "5db169c97645b8c606bcbc686e51fda7"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
#elsa Iniating
elsa=pts.init()
elsa.setProperty('rate',140)
####################
def elsay(cmd):
    elsa.say(cmd),elsa.runAndWait()

#########Whether Forcasing#########
def wether(city):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        elsay( "the  Wether in {0} is {1} and cureent teparature is {2} and atmospheric pressure is {3} and humidity is {4}".format(city_name,weather_description,current_temperature,current_pressure,current_humidiy)),elsa.runAndWait()
    else:
       elsay(" City Not Found ")
def tellme(cmd):
    res=wiki.search(cmd,10)
    if len(res)!=0:
        print(res)
        #res.sort()
        ms=list()
        for i in res:
            finded_items=str(i)
            finded_items.lower()
            if finded_items.__contains__(cmd):
                ms.append(i)
        sas=""
        try:
            print(ms)
            sas=wiki.summary(res[0],sentences=2)
            sas = str(sas[:sas.index('('):] + sas[sas.index(')') + 2:])
            wks={"data":sas}
            try:
                file=open("../cached/wdat.mint","w")
                json.dump(wks,file)
                file.close()
            except FileNotFoundError as es:
                print("Some Internal Error")
            finally:
                file.close()
            print(sas)
        except Exception:
            elsay("Oh oh I could not load the item")

        for words in sas:
            if words==" ":
                sas.replace(" ",3*" ")
        elsay(sas)
def anal(cmd):
    if "what is the wheter in" in cmd:
        a=cmd.lstrip("what is the wheter in")
        print(a)
        wether(a)
    else:
        for i in ["who is","what is","tell me about"]:
            if i in cmd:
                print(type(cmd))
                a=cmd.replace(i,"")
                print(a)
                tellme(a)
while True:
    elsa.say("say something   "),elsa.runAndWait()
    inp=str(input())
    anal(inp)
