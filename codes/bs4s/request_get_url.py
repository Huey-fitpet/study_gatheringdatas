from bs4 import BeautifulSoup # html 해석기

import requests # url 주소

# 브라우저 주소창
response = requests.get('http://192.168.0.7:5500/codes/target_samples.html')

print(response.text)

pass
