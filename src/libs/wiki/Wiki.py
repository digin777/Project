import wikipedia as wiki
import requests, json
def tellme(cmd):
    res=wiki.search(cmd,10)
    print(res)
    sas=""
    symbols={'(':')' ,'{':'}','[':']'}
    try:
        sas = wiki.summary(res[0],sentences=3)
        print(sas)
        for k,v in symbols.items():
            if k in sas:
                sas = str(sas[:sas.index(k):] + sas[sas.index(v) + 2:])
        return sas
    except Exception as e:
        return("Oh oh I could not load the item ")
print(tellme('taj mahal'))