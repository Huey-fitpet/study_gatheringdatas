import requests

def get_sec_13d(cik):
    # SEC EDGAR API URL
    url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    
    # API 요청
    headers = {
        'User-Agent': 'SangHoon Lee (demonic0319@gmail.com)'  # SEC의 요청 규정에 따라 User-Agent를 설정해야 합니다.
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # 13D 보고서 필터링
        filings = data.get('filings', {}).get('recent', {})
        for index in range(len(filings.get('form', []))):
            if filings['form'][index] == 'SC 13D':
                print(f"Date: {filings['date'][index]}")
                print(f"Link: {filings['filingHref'][index]}")
                print(f"Description: {filings['description'][index]}")
                print()
    else:
        print(f"Error: {response.status_code}")

# CIK (Central Index Key) 번호를 사용하여 13D 보고서 가져오기
cik_number = '0000320193'  # 예: Apple Inc.의 CIK 번호
get_sec_13d(cik_number)