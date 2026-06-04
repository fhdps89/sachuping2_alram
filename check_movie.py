import os
import re
import requests
from bs4 import BeautifulSoup

# 환경변수에서 텔레그램 봇 토큰 및 챗 ID 로드 (GitHub Secrets와 연동)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# KOBIS 영화 상세정보 호출 URL (사랑의 하츄핑: 고래보석의 전설, 코드: 20262381)
KOBIS_URL = "https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do"
PAYLOAD = {"code": "20262381"}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 스크린샷 기준의 기존 최종수정일자 (변경 감지 기준점)
TARGET_DATE = "2026-03-10 10:14:47"

def send_telegram_alert(new_date):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("텔레그램 환경변수가 설정되지 않았습니다.")
        return
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    message = (
        f"🚨 [사랑의 하츄핑: 고래보석의 전설] 정보가 업데이트 되었습니다!\n\n"
        f"▪ 기존: {TARGET_DATE}\n"
        f"▪ 변경: {new_date}\n\n"
        f"등급분류 및 개봉일이 특정되었을 수 있으니 KOBIS를 확인해 보세요."
    )
    try:
        response = requests.post(api_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        response.raise_for_status()
        result = response.json()
        if result.get('ok'):
            print("텔레그램 메시지 전송 성공")
        else:
            print(f"텔레그램 API 오류: {result.get('description')}")
    except Exception as e:
        print(f"텔레그램 메시지 전송 실패: {e}")

def check_movie_update():
    try:
        # 상세정보 페이지 요청 (KOBIS는 일반적으로 POST 방식으로 영화 코드를 전달)
        response = requests.post(KOBIS_URL, data=PAYLOAD, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()
        
        # '최종수정: 2026-03-10 10:14:47' 패턴 탐색
        match = re.search(r'최종수정:\s*([\d\-:\s]+)', page_text)
        if match:
            current_date = match.group(1).strip()
            print(f"현재 KOBIS 최종수정일자: {current_date}")
            
            # 파싱한 날짜가 기준점과 다르면 텔레그램 알림 전송
            if current_date != TARGET_DATE:
                send_telegram_alert(current_date)
                print("업데이트 알림을 전송했습니다.")
            else:
                print("수정일자가 변경되지 않았습니다. 대기 중...")
        else:
            print("최종수정 텍스트를 찾을 수 없습니다. (페이지 구조 변경 또는 IP 차단 가능성)")
            
    except Exception as e:
        print(f"스크래핑 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    check_movie_update()
