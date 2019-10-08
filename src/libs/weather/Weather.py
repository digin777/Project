api_key1 = "5db169c97645b8c606bcbc686e51fda7"
api_key2="532d313d6a9ec4ea93eb89696983e369"
import requests, json
import pyowm
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def getwether(city):
    try:
        owm=pyowm.OWM(api_key1)
        place=owm.weather_at_place(city)
        wethers = place.get_weather()
        temparature=wethers.get_temperature('celsius')
        wind=wethers.get_wind()
        wether_stat="the weather at "+city+" is "+wethers.get_detailed_status()+" with teparature "+str(temparature['temp'])+" with speed "+str(wind['speed'])
        wdata={"data":wether_stat}
        return wether_stat
    except Exception as e:
        return "Sorry Could not Fetch the data"
    try:
        file=open("../cached/wetherdat.mint","w")
        json.dump(wdata,file)
        return wether_stat
    except Exception:
        print("Internal Error")
        
def get16daysweather(city,country='in',cnt='2'):
    query=f'http://api.openweathermap.org/data/2.5/forecast/daily?q={city}&cnt={cnt}&appid={api_key2}&units=metric'
    res=requests.get(query)
    if res.status_code==200:
        try:
            res=res.json()
            resposnestr='the Weather at {} is {} with speed  {} and temparature {} degree celsius and pressure is {} '.format(res['city']['name'],res['list'][1]['weather'][0]['main'],res['list'][1]['speed'],res['list'][1]['temp']['day'],res['list'][1]['pressure'])
            return(resposnestr)
        except:
            return("Canot get the Data")
    else:
        return("Canot get the Data")

if __name__=='__main__':
    print(get16daysweather('kochi'))
    print(getwether('kochi'))
