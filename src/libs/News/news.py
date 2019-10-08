import requests

def getNews(**kwrgs):
    '''
    country
        Possible options: ae ar at au be bg br ca ch cn co cu cz de eg fr gb gr hk hu id ie il
        in it jp kr lt lv ma mx my ng nl no nz ph pl pt ro rs ru sa se sg si sk th tr tw ua us ve za .
    category
        Possible options: business entertainment general health science sports technology .
    sources

    q
        Keywords or a phrase to search for.
    pageSize(int)
        The number of results to return per page (request). 20 is the default, 100 is the maximum.
    page(int)
        Use this to page through the results if the total results found is greater than the page size.
    '''
    apiKey='apiKey=40209bb595314fa4ad188518b041dd59'
    url='https://newsapi.org/v2/top-headlines?'
    for k,v in kwrgs.items():
        if v is not None:
            url+=str(k)+'='+str(v)+'&'
    url+=apiKey
    print(url)
    try:
        response = requests.get(url)
        if response.status_code==200:
            response=response.json()
            titles=[]
            for i in range(0,len(response['articles'])):
                titles.append(response['articles'][i]['title'])
            return(titles)
        else:
            return("Canot Get News")
    except:
        return("Canot Get the News")
'''if __name__=='__main__':
    x=getNews(category='entertainment',country='in',page=2)
    print(x)
'''