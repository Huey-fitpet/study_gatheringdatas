
# 조달청 표준 정보 수집
import requests
from bs4 import BeautifulSoup as bs
#uri 소스에서 넣을 때 길이가 256자 이내로 
'''
b%2BuPtb%2FjY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN%2FkTdkwOEWeXW6F6H8V%2Fkcc78hvdg%3D%3D
url = f'https://apis.data.go.kr/1230000/PubDataOpnStdService/getDataSetOpnStdBidPblancInfo?
serviceKey=b%2BuPtb%2FjY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN%2FkTdkwOEWeXW6F6H8V%2Fkcc78hvdg%3D%3D&
pageNo=1&
numOfRows=10&
type=json&
bidNtceBgnDt=201712010000&
bidNtceEndDt=201712312359'
'''


'''
에러코드	에러메세지	          설명
1	        APPLICATION ERROR	어플리케이션 에러
4	        HTTP_ERROR	        HTTP 에러
12	        NO_OPENAPI_SERVICE_ERROR	해당 오픈 API 서비스가 없거나 폐기됨
20	        SERVICE_ACCESS_DENIED_ERROR	서비스 접근거부
22	        LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR	서비스 요청제한횟수 초과에러
30	        SERVICE_KEY_IS_NOT_REGISTERED_ERROR	등록되지 않은 서비스키
31	        DEADLINE_HAS_EXPIRED_ERROR	활용기간 만료
32	        UNREGISTERED_IP_ERROR	등록되지 않은 IP
99	        UNKNOWN_ERROR	    기타에러

'''

url = f'http://apis.data.go.kr/1230000/PubDataOpnStdService/getDataSetOpnStdBidPblancInfo'
params ={
    'serviceKey' : '+uPtb/jY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN/kTdkwOEWeXW6F6H8V/kcc78hvdg==', 
    'pageNo' : '1', 
    'numOfRows' : '10', 
    'type' : 'json', 
    'bidNtceBgnDt' : '201712010000', 
    'bidNtceEndDt' : '201712312359' 
    }

response = requests.get(url, params=params)
if response.status_code == 200 :
    '''
    <OpenAPI_ServiceResponse>\n\t<cmmMsgHeader>\n\t\t<errMsg>SERVICE ERROR</errMsg>\n\t\t<returnAuthMsg>SERVICE_KEY_IS_NOT_REGISTERED_ERROR</returnAuthMsg>\n\t\t<returnReasonCode>30</returnReasonCode>\n\t</cmmMsgHeader>\n</OpenAPI_ServiceResponse>
    '''
    soup = bs(markup=response.text, features='xml')
    print(soup.prettify())
    return_auth_msg = soup.find('returnAuthMsg')
    if return_auth_msg != None :
        print(return_auth_msg.text)
    pass
else :
    print(f'error : {response.status_code}')


pass

