# 🎈 Blank app template

A simple Streamlit app template for collecting YouTube video stats.

## 준비 파일

- `streamlit_app.py` — 실행할 Streamlit 앱 코드
- `requirements.txt` — 필요한 Python 패키지 목록
- `run.sh` — 리눅스/맥에서 가상환경을 만들고 앱을 실행하는 스크립트
- `run.bat` — Windows에서 가상환경을 만들고 앱을 실행하는 배치 스크립트

## 빠른 실행 방법

1. 프로젝트 루트로 이동
   ```bash
   cd /workspaces/blank-app
   ```

2. `run.sh` 실행
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

3. 브라우저에서 표시된 `Local URL`을 열기

## 수동 실행 방법

1. 가상환경 생성 및 활성화
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. 의존성 설치
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. 앱 실행
   ```bash
   ./.venv/bin/python -m streamlit run streamlit_app.py --server.port 8502
   ```

## YouTube API 키 사용

앱 실행 후 화면에서 `YouTube API Key` 입력란에 키를 넣거나, 환경 변수를 설정할 수 있습니다:

```bash
export YOUTUBE_API_KEY="your_api_key_here"
```

## 자동 번역 기능

앱에서 `자동 한국어 번역 (일본어 → 한국어)` 체크박스를 켜면 `제목(원본 제목)`을 한국어로 번역한 결과를 `제목(한국어 번역)` 열에 표시합니다.

## 다른 컴퓨터에서 복사해서 사용하기

이 저장소 전체를 다른 컴퓨터로 옮기거나 GitHub에서 클론한 뒤, 아래 파일들이 있어야 합니다:

- `streamlit_app.py`
- `requirements.txt`
- `run.sh` 또는 `run.bat`
- `Dockerfile` / `Procfile` (원할 경우 배포에 사용)

### 복사 후 실행 방법

1. 저장소 루트로 이동
   ```bash
   cd /path/to/blank-app
   ```

2. Linux/macOS에서 실행
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

3. Windows에서 실행
   ```bat
   run.bat
   ```

4. 설치된 가상환경이 없으면 `run.sh`/`run.bat`가 자동으로 만듭니다.

5. 앱이 실행되면 터미널에 표시되는 URL을 웹 브라우저에서 엽니다.

## 다른 컴퓨터에서 접속하기

현재 이 앱은 로컬에서 실행 중인 웹 서버이므로 다른 컴퓨터에서 접근하려면 앱을 공개 호스팅 또는 포트 포워딩이 필요합니다.

### 1. Streamlit Cloud에 배포하기(가장 쉬움)

1. 이 저장소를 GitHub에 푸시합니다.
2. Streamlit Cloud에서 새 앱을 만들고 이 저장소를 연결합니다.
3. `requirements.txt`와 `streamlit_app.py`가 자동으로 설치/실행됩니다.

이 저장소에는 Streamlit Cloud용 `Procfile`이 포함되어 있어 자동 배포에 도움이 됩니다.

### 2. Docker로 배포하기

1. `Dockerfile`이 추가되어 있으므로 다음 명령으로 이미지 빌드 후 실행할 수 있습니다.
   ```bash
   docker build -t blank-app .
   docker run -p 8501:8501 blank-app
   ```
2. 그 후 브라우저에서 `http://서버주소:8501`에 접속합니다.

### 3. 로컬 네트워크에서 접근하기

1. 서버에서 앱을 실행합니다.
   ```bash
   ./.venv/bin/python -m streamlit run streamlit_app.py --server.port 8502 --server.address 0.0.0.0
   ```
2. 같은 네트워크의 다른 컴퓨터에서 `http://<호스트IP>:8502`로 접속합니다.
3. 방화벽이나 보안 그룹에서 포트 8502가 열려 있어야 합니다.

## 주의

- 로컬 서버는 서버가 켜져 있는 동안에만 외부에서 접근 가능합니다.
- 컴퓨터를 종료하거나 터미널을 닫으면 연결이 끊깁니다.
- 공개로 서비스를 운영하려면 Streamlit Cloud, VPS, 또는 Docker 서버 등 별도 호스팅이 필요합니다.
