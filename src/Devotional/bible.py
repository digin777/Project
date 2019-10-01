import requests
import json
class Bible():
    global api_key
    api_key = "73845cf3admsh59899f61530b896p1301e5jsnd85fc71ffe76"
    def __init__(self,api_key):
        self.api_key=api_key
    def getBooks():
        try:
            response = requests.get("https://ajith-holy-bible.p.rapidapi.com/GetBooks",
                                    headers={
                                        "X-RapidAPI-Host": "ajith-holy-bible.p.rapidapi.com",
                                        "X-RapidAPI-Key": api_key
                                            }
                                    )
            result=response.json()
            s1=str(result['The_Old_Testament'])
            s2=str(result['The_New_Testament'])
            s1=s1.split(' ')
            s2=s2.split(' ')
            for i in s1:
                if '.' in i:
                    s1.remove(i)
            for i in s1:
                if i.isdecimal():
                    s1[s1.index(i)]=s1[s1.index(i)]+" "+s1.pop(s1.index(i)+1)
            s1[21]=s1[21]+" "+s1.pop(22)+" "+s1.pop(22)
            for i in s2:
                if '.' in i:
                    s2.remove(i)
            for i in s2:
                if i.isdecimal():
                    s2[s2.index(i)]=s2[s2.index(i)]+" "+s2.pop(s2.index(i)+1)
            s2[4] = s2[4] + " " + s2.pop(5) + " " + s2.pop(5)+" "+s2.pop(5)
            return s1,s2
        except :
            pass
    def getChapter(book,chapter):
        try:
            response = requests.get("https://ajith-holy-bible.p.rapidapi.com/GetChapter?Book="+book+"&"+"chapter="+str(chapter),
                              headers={
                                  "X-RapidAPI-Host": "ajith-holy-bible.p.rapidapi.com",
                                  "X-RapidAPI-Key": api_key
                              }
                              )
            response=response.json()
            return response['Output']
        except:
            pass
    def getVerses(book,chapter,vfrom,vto):
        try:
            response = requests.get(
            "https://ajith-holy-bible.p.rapidapi.com/GetVerses?Book="+book+"&chapter="+str(chapter)+"&VerseFrom="+str(vfrom)+"&VerseTo="+str(vto),
            headers={
                "X-RapidAPI-Host": "ajith-holy-bible.p.rapidapi.com",
                "X-RapidAPI-Key":api_key
            }
            )
            response=response.json()
            return response['Output']
        except:
            pass
    def getVersusChapter(book,chapter,verse):
        try:
            response = requests.get(
                "https://ajith-holy-bible.p.rapidapi.com/GetVerseOfaChapter?Verse="+str(verse)+"&Book="+book+"&chapter="+str(chapter),
                headers={
                    "X-RapidAPI-Host": "ajith-holy-bible.p.rapidapi.com",
                    "X-RapidAPI-Key": api_key
                }
                )
            response=response.json()
            return response['Output']
        except:
            pass
