
import requests

#uri 소스에서 넣을 때 길이가 256자 이내로 
'''
url = f'https://apis.data.go.kr/1230000/PubDataOpnStdService/getDataSetOpnStdBidPblancInfo?
serviceKey=b%2BuPtb%2FjY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN%2FkTdkwOEWeXW6F6H8V%2Fkcc78hvdg%3D%3D&
pageNo=1&
numOfRows=10&
type=json&
bidNtceBgnDt=201712010000&
bidNtceEndDt=201712312359'

'''

url = 'http://apis.data.go.kr/1230000/PubDataOpnStdService/getDataSetOpnStdBidPblancInfo'
params ={
    'serviceKey' : 'b+uPtb/jY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN/kTdkwOEWeXW6F6H8V/kcc78hvdg==', 
    'pageNo' : '1', 
    'numOfRows' : '10', 
    'type' : 'json', 
    'bidNtceBgnDt' : '201712010000', 
    'bidNtceEndDt' : '201712312359' 
    }

response = requests.get(url, params=params)
print(response.content)

pass

