# 사랑의 하츄핑: 고래보석의 전설 - 영화정보 업데이트 감시 시스템

KOBIS 영화 상세정보에서 **1시간마다** 자동으로 영화 정보 변경을 감지하고, 변경되면 **텔레그램으로 알림**을 보내는 자동화 시스템입니다.

## 📋 주요 기능

- ✅ **1시간마다 자동 체크** (GitHub Actions 스케줄)
- ✅ **변경 감지** (최종수정 일자 비교)
- ✅ **텔레그램 자동 알림** (변경 시 즉시 알림)
- ✅ **에러 처리** (IP 차단, 페이지 구조 변경 등)

## 🔧 설정 방법

### 1️⃣ 텔레그램 설정

#### 텔레그램 봇 토큰 얻기
1. 텔레그램에서 `@BotFather`를 검색하고 시작
2. `/newbot` 명령어로 새 봇 생성
3. 봇 이름과 username 설정
4. 받은 **토큰** 저장

#### 텔레그램 Chat ID 얻기
1. 생성한 봇과 1:1 채팅 시작
2. 아래 링크 방문 (토큰 입력):
   ```
   https://api.telegram.org/bot{YOUR_TOKEN}/getUpdates
   ```
3. `"id"` 필드의 숫자가 Chat ID (예: `123456789`)

### 2️⃣ GitHub Secrets 설정

1. **리포지토리 Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** 클릭
3. 두 개 추가:
   - **Name**: `TELEGRAM_TOKEN` / **Value**: 위에서 받은 토큰
   - **Name**: `TELEGRAM_CHAT_ID` / **Value**: 위에서 받은 Chat ID

### 3️⃣ 완료! 🎉

워크플로우가 자동으로 실행됩니다:
- **매시간 정각**에 자동 실행
- **Actions** 탭에서 실행 기록 확인 가능
- 변경 감지 시 텔레그램으로 알림 수신

## 📝 커스터마이징

### 스케줄 변경
`.github/workflows/hourly-check.yml`의 `cron` 값 수정:
```yaml
schedule:
  - cron: '0 * * * *'   # 매시간 정각
  - cron: '0 0 * * *'   # 매일 자정
  - cron: '*/30 * * * *' # 30분마다
```

### 감시 대상 영화 변경
`check_movie.py`에서 수정:
```python
PAYLOAD = {"code": "원하는_영화_코드"}
TARGET_DATE = "기준_날짜"
```

## 📊 GitHub Actions 모니터링

리포지토리의 **Actions** 탭에서:
- ✅ 성공/실패 상태 확인
- 📜 각 실행의 상세 로그 확인
- ⏱️ 실행 시간 및 이력 조회

## 🚀 수동 실행

GitHub Actions의 "Run workflow" 버튼으로 언제든 수동 실행 가능

---

**Made with ❤️ for Sachuping fans**
