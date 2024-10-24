
import requests
from bs4 import BeautifulSoup
import os
import urllib.request as req
'''
이미지 다운로드
target tag : div.box-image > a > span > img

저장 위치 

'''

def main() :

    folder_name = f'./downloads'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    url = f'http://www.cgv.co.kr/movies/?lt=1&ft=0'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    target_tag = f'div.box-image > a > span > img'
    img_link_list = soup.select(target_tag)
    
    for num, img_link in enumerate(img_link_list, start=1):
        img_url = img_link.attrs["src"]
        req.urlretrieve(img_url,f'{folder_name}/{num}.jpg')
    return

if __name__ == '__main__':
    main()
    pass