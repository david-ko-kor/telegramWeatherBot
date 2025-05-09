import requests
import telegram,asyncio
import schedule
import time
import httpx
import os
from dotenv import load_dotenv
load_dotenv()
apikey=os.getenv("apikey")
token=os.getenv("token")
id=os.getenv("id")
lat=37.3514
lon=127.9453
url=f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&lang=kr&appid={apikey}"

result=requests.get(url)
response=result.json()
if os.path.isfile('wether.csv'):
    os.remove('weather.csv')
list=[]
i=response['list'][0]
print(i)
bot=telegram.Bot(token=token)
def get_current_weather():
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&lang=kr&appid={apikey}&units=metric"
    result = requests.get(url)
    response = result.json()
    return response['list'][0]


# 동기식 텔레그램 메시지 전송 함수 (순수 HTTP 요청 사용)
def send_telegram_message(text):
    telegram_api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": id,
        "text": text
    }

    # httpx를 사용한 동기식 HTTP 요청
    with httpx.Client() as client:
        response = client.post(telegram_api_url, json=payload)

    # 응답 확인
    if response.status_code == 200:
        print(f"메시지 전송 완료: {text}")
        return True
    else:
        print(f"메시지 전송 실패: {response.status_code}, {response.text}")
        return False


# 스케줄러에서 호출될 함수
def send_weather_update():
    try:
        # 최신 날씨 데이터 가져오기
        weather_data = get_current_weather()

        # 메시지 준비
        message = f"{weather_data['dt_txt']}, 온도: {weather_data['main']['temp']}°C, 날씨: {weather_data['weather'][0]['description']}"

        # 텔레그램 메시지 전송
        send_telegram_message(message)

    except Exception as e:
        print(f"처리 중 오류 발생: {e}")


# 1분마다 실행 예약
schedule.every(1).minutes.do(send_weather_update)

# 시작 메시지
print("Bot started. Sending weather updates every minute...")

# 첫 메시지 즉시 전송
send_weather_update()

# 메인 루프
while True:
    schedule.run_pending()
    time.sleep(1)