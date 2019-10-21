
import wolframalpha

def getwolfram(q):
    app_id='A8P348-5AHH27X94E'
    client = wolframalpha.Client(app_id)
    res=client.query(q)
    return (next(res.results).text)
if __name__ =='__main__':
    print(getwolfram(client,'python programing language'))