from bs4 import BeautifulSoup # html 해석기

import requests # url 주소

# naver 검색어에 따른 타이틀 수집
# https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EA%B8%88%EC%9C%B5
# span.lnk_tit

'''
title count : 4
title : 연금저축 보험
sub title count : 4
sub title : 연금저축보험이율
sub title : 연금저축보험 가입
sub title : 개인연금저축 보험
sub title : 우체국연금저축보험
title : 은행 연금저축
sub title count : 4
sub title : 은행 개인연금저축
sub title : 신한 은행 연금저축
sub title : 국민은행 연금저축
sub title : 하나 은행 연금저축
title : 연금저축펀드계좌
sub title count : 0 
title : 연금저축 세액 공제
sub title count : 4
sub title : 연금저축IRP세액공제
sub title : IRP 연금저축세액공제한도
sub title : 연말정산연금저축세액공제
sub title : 연금저축세액공제한도 변경
'''
# 중간에 인기주제가 없는 경우도 있음 

def search_naver(keyword) :
    # 검색어 받기
    #keyword = '연금저축'#input('input search word : ')

    # 브라우저 주소창
    html_str = f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={keyword}'
    response = requests.get(html_str)

    #Dom 구조화
    soup = BeautifulSoup(markup=response.text, features='html.parser')


    # titles = soup.select(
    # 'span.BqZGMHlcQKUqdI_4Wl43'  # 첫 번째 클래스
    # '.fds-comps-keyword-chip-text'  # 두 번째 클래스
    # '.xWYCPbd1ikavaw8UZRF0'  # 세 번째 클래스
    # )

    titles = soup.select(
    'a.Z9iTuchDIS2CJfxW3wSy'  # 첫 번째 클래스
    '.gS6qOJs_g9rbnshlqOzE'  # 두 번째 클래스
    '.fds-comps-keyword-chip'  # 세 번째 클래스
    '.fds-modules-keyword-chip'  # 세 번째 클래스
    )

    return titles


def main():
    reault_list = search_naver('연금저축')

    print(f'title count : {len(reault_list)}')
    for title in reault_list :
        print(f'title : {title.text}')
        sub_list = search_naver(title.text)
        print(f'sub title count : {len(sub_list)}')
        for sub_title in sub_list:
            print(f'sub title : {sub_title.text}')


if __name__ == '__main__':
    main()
