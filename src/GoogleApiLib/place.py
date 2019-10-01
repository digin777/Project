import requests
import json
api_key="AIzaSyAc7DVEVWX3PQbMoXQwYD6VsXmGrS9i2O4"
class place():
    def getNearby(key,lattitude,longitude,radius,type,nof,**kwargs):
        keywords=['keyword','language','name','opennow','rankby',]
        strn=""
        #rq="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=1500&type=restaurant&keyword=cruise&key="+api_key
        req="https://maps.googleapis.com/maps/api/place/nearbysearch/json?key="+key+"&location="+str(longitude)+","+str(lattitude)+"&radius="+str(radius)+"&type="+type
        if len(kwargs.keys())>0:
           for i in kwargs.keys():
               if i in keywords:
                  strn+="&"+i+"="+kwargs.get(i)
        req+=(strn)
        try:
            response = requests.post(req)
            my_results=response.json()
            print(my_results)
            result=""
            print(my_result)
            for i in range(nof):
                try:
                    #result+=my_results.get('results')[i].get('name')+"\n"
                    print(my_results.get('results'))
                except IndexError:
                    pass
            print(result)
            print(my_results)
        except:
            pass
a=place
a.getNearby(api_key, 76.307034,9.782923,1500,"restaurant",5)