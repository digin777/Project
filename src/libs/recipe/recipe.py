#the recipy calcluator scripted by Digin Antony copy right DSP softwares
import requests
import json
#recipy puppy  recipy finder
class recipypuppy():
    def search(self,item,pages=1):
        url = "https://recipe-puppy.p.rapidapi.com/"
        querystring = {"p":str(pages),"q":str(item)}
        headers = {
            'x-rapidapi-host': "recipe-puppy.p.rapidapi.com",
            'x-rapidapi-key': "73845cf3admsh59899f61530b896p1301e5jsnd85fc71ffe76"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code!=200:
            print ("unable to get results")
        else:
            response=response.json()
            string=""
            recipi_dict={}
            '''if len(response.get('results'))<5:
                for i in range(len(response.get('results'))):
                    recipi_dict[response.get('results')[i].get('title')]=response.get('results')[i].get('ingredients')
            else:
                for i in range(3):
                    recipi_dict[response.get('results')[i].get('title')]=response.get('results')[i].get('ingredients')'''
            recipi_dict[response.get('results')[0].get('title')]=response.get('results')[0].get('ingredients')
            return  recipi_dict

#nutrionix calori calculator
class nutritonix():
    def search(apikey,item):
        response = requests.get(
            "https://nutritionix-api.p.rapidapi.com/v1_1/search/"+item+"?fields=item_name%2Cnf_calories%2Cnf_total_fat",
            headers={
                "X-RapidAPI-Host": "nutritionix-api.p.rapidapi.com",
                "X-RapidAPI-Key": apikey
            }
            )
        if response.status_code!=200:
            print ("unable to get results")
        else:
            response=response.json()
            string=""
            a=response.get('hits')
            for i in range(len(response.get('hits'))):
               string+=response.get('hits')[i].get('fields').get('item_name')+" contains "+str(response.get('hits')[i].get('fields').get('nf_calories'))+" calories and "+str(response.get('hits')[i].get('fields').get('nf_total_fat'))+" fat \n"
            return (string)

#News Agragator
class newsagregator():
    def getCNN(apikey,section,count):
        """section can have any valule like
         top ,world ,us ,business ,politics ,crime ,technology ,health ,entertainment ,travel ,living ,video ,studentNews ,latest
         """

        response = requests.post(
            "https://api2ninja-api2-ninja-news-aggregator-and-weather-data-v1.p.rapidapi.com/api2ninja/news/cnn",
            headers={
                "X-RapidAPI-Host": "api2ninja-api2-ninja-news-aggregator-and-weather-data-v1.p.rapidapi.com",
                "X-RapidAPI-Key": apikey,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            params={
                "section": section
            }
            )
        if response.status_code!=200:
            print("Could not fetch results")
        else:
            response=response.json()
            print(response)
            if len(response['results'])<count:
                count=len(response['results'])
                news=[]
            for i in range(count):
                news.append(response['results'].get(i).get('description'))

#a=recipypuppy()
#print(a.search("omelet"))