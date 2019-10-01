import requests

class crickbuz():
    def __init__(self):
        pass
    def getjson(self,url):
        self.url=url
        try:
            res=requests.get(url).json()
            return res
        except Exception:
            raise

    def livescore(self):
        url = "http://mapps.cricbuzz.com/cbzios/match/livematches"
        try:
            result=self.getjson(url)
            retstr=[]
            for i in range(len(result['matches'])):
                if (result['matches'][i]['header']['state'])=='inprogress':
                    retstr.append(result['matches'][i]['series_name']+"  "+result['matches'][i]['header']['status'])
            if len(retstr)!=0:
                return retstr
        except:
            return retstr.append("No live matches ")
a=crickbuz()
print(a.livescore())