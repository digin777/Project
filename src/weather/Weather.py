import requests, json
import pyowm
api_key1 = "5db169c97645b8c606bcbc686e51fda7"
api_key2="532d313d6a9ec4ea93eb89696983e369"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
# city is not found
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