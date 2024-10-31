
# * 웹 크롤링 동작
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as ac

import time 

class ProductInfoScraper:

    def get_product_info(browser) :

        '''
        메인 페이지 검색창 #headerSearchId
        메인 페이지 검색버튼 #mainLayout > header > div > div.main.innerContent > div.searchAreaWrap > div > button
        검색어 p6000

        상품을 페이지 이동하며 정보 수집
        1페이지
        #s-search-app > div.srchResultProductArea > div.s-goods-layout.s-goods-layout__grid > div.srchPagination > span.srchPaginationActive
        2~6,13,srchPaginationNext 총 7개 
        #s-search-app > div.srchResultProductArea > div.s-goods-layout.s-goods-layout__grid > div.srchPagination > a
        srchPaginationNext stop 키워드 
        #s-search-app > div.srchResultProductArea > div.s-goods-layout.s-goods-layout__grid > div.srchPagination > a.srchPaginationNext

        상품 리스트 => url 가져오기
        #s-search-app > div.srchResultProductArea > div.s-goods-layout.s-goods-layout__grid > div.s-goods-grid.s-goods-grid--col-4 > ul > li > div
        
        #s-search-app > div.srchResultProductArea > div.s-goods-layout.s-goods-layout__grid > div.s-goods-grid.s-goods-grid--col-4 > ul > li > div > div.s-goods__thumbnail > a

        url 넘어가서 
        태그가 동적으로 생성? 되어서 셀레니움으로 가지고 와야함.
        section[data-v-06e72560].pd-widget1 

        상품명, 가격, 상품상세
        #stickyTopParent > div.productDetailTop > section.pd-widget1 > div.pd-widget1__info-box > h2
        상품명  #stickyTopParent > div.productDetailTop > section.pd-widget1 > div.pd-widget1__info-box > h2
        가격 더 봐야 되 #stickyTopParent > div.productDetailTop > section.pd-price > div > dl > dd > strong
        상품상세 
        #m2-prd-frame
        #m2root
        '''

        search_tag = f'#headerSearchId'
        btn_tag = f'#mainLayout > header > div > div.main.innerContent > div.searchAreaWrap > div > button'
        search_item_str = f'p6000'

        element_id = browser.find_element(by=By.CSS_SELECTOR, value=search_tag)
        time.sleep(1) 
        element_id.send_keys(search_item_str)

        
        element_btn = browser.find_element(by=By.CSS_SELECTOR, value=btn_tag)
        time.sleep(1) 
        element_btn.click()

        # -- 위까지 main page 

        time.sleep(1) # 시간 확인
        page_list_tag = f'#s-search-app > div.srchResultProductArea > div.s-goods-layout.s-goods-layout__grid > div.srchPagination > a,  #s-search-app > div.srchResultProductArea > div.s-goods-layout.s-goods-layout__grid > div.srchPagination > span.srchPaginationActive'
        goods_tag_list = f'#s-search-app > div.srchResultProductArea > div.s-goods-layout.s-goods-layout__grid > div.s-goods-grid.s-goods-grid--col-4 > ul > li > div > div.s-goods__thumbnail > a'
        goods_name_tag = f'#stickyTopParent > div.productDetailTop > section.pd-widget1 > div.pd-widget1__info-box > h2'
        # 'section[data-v-06e72560].pd-widget1' # '#stickyTopParent > div.productDetailTop > section.pd-widget1 > div.pd-widget1__info-box > h2'
        goods_price_tag = f'#stickyTopParent > div.productDetailTop > section.pd-price > div > dl > dd > strong'
        url_list = []
        while True :
            time.sleep(1)
            
            goods_url_list = browser.find_elements(by=By.CSS_SELECTOR, value=goods_tag_list)

            # 리스트를 전부 담았다가 한번에 상품정보 빼는 게 나음

            for num, news in enumerate(goods_url_list):
                target_link = news.get_attribute(f'href')
                # print(target_link)
                url_list.append(target_link)
                pass

            pagination_list = browser.find_elements(by=By.CSS_SELECTOR, value=page_list_tag)
            num = 0
            for index in range(len(pagination_list)):
                if pagination_list[index].text.startswith('현재 페이지'):
                    num = index+1
                    break
            
            if num == len(pagination_list) :
                print(f'end page')
                break

            pagination_tag = pagination_list[num]
            ac(browser).key_down(Keys.END).perform() # 안하면 에러남 
            time.sleep(1)
            pagination_tag.click()

            pass

        final_goods_list = []
        print(len(url_list))
        for index, url in enumerate(url_list[750:], start=750): # 시간이 너무 오래 걸려서 일부만 수행 
            browser.get(url)
            time.sleep(1)

            good_name = browser.find_elements(by=By.CSS_SELECTOR, value=goods_name_tag)
            good_price = browser.find_elements(by=By.CSS_SELECTOR, value=goods_price_tag)

            good_detail = {
                'product_name' : good_name[0].text,
                'product_price' : good_price[0].text,
            }
            final_goods_list.append(good_detail)

            pass
        pass

        return final_goods_list




