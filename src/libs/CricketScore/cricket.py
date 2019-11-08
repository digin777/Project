import requests

class crickbuz():
    def __init__(self):
        self.url= "http://mapps.cricbuzz.com/cbzios/match/livematches"
    def getjson(self):
        try:
            res=requests.get(self.url).json()
            return res
        except Exception:
            raise Exception('Could not fetch Data')

    def livescore(self):
        try:
            result=self.getjson()
            retstr=[]
            for i in range(len(result['matches'])):
                #if (result['matches'][i]['header']['state'])=='inprogress':
                retstr.append(result['matches'][i]['series_name']+"  "+result['matches'][i]['header']['status'])
            if len(retstr)!=0:
                return retstr[:4]
        except:
            return retstr.append("No live matches ")
#a=crickbuz()
#print(a.livescore())