import requests

def get_sec_filings(cik):
    # SEC EDGAR API URL
    url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    
    # API 요청
    headers = {
        'User-Agent': 'SangHoon Lee (demonic0319@gmail.com)'  # SEC의 요청 규정에 따라 User-Agent를 설정해야 합니다.
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # 최근 제출된 보고서 필터링
        filings = data.get('filings', {}).get('recent', {})
        
        # SC 13D 보고서 출력
        for index in range(len(filings.get('form', []))):
            if filings['form'][index] == 'SC 13D':
                print(f"SC 13D Report:")
                print(f"Date: {filings['filingDate'][index]}")
                print(f"Link: {filings['primaryDocument'][index]}")
                print(f"Description: {filings['primaryDocDescription'][index]}")
                print()
        
        # SC 13G/A 보고서 요청
        for index in range(len(filings.get('form', []))):
            if filings['form'][index] == 'SC 13G/A':
                print(f"SC 13G/A Report:")
                print(f"Date: {filings['filingDate'][index]}")
                print(f"Link: {filings['primaryDocument'][index]}")
                print(f"Description: {filings['primaryDocDescription'][index]}")
                
                # SC 13G/A 보고서의 링크를 사용하여 다시 API 요청
                report_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{filings['accessionNumber'][index].replace('-', '')}/{filings['primaryDocument'][index]}"
                report_response = requests.get(report_url, headers=headers)
                
                if report_response.status_code == 200:
                    # 보고서 파일 저장
                    report_filename = filings['primaryDocument'][index]  # 파일 이름
                    with open(report_filename, 'wb') as file:
                        file.write(report_response.content)  # 파일에 내용 저장
                    print(f"Successfully fetched and saved SC 13G/A report as: {report_filename}")
                else:
                    print(f"Error fetching SC 13G/A report: {report_response.status_code}")
                print()
    else:
        print(f"Error: {response.status_code}")

# CIK (Central Index Key) 번호를 사용하여 보고서 가져오기
cik_number = '0000320193'  # 예: Apple Inc.의 CIK 번호
get_sec_filings(cik_number)