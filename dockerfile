# 베이스 이미지 설정
FROM python:3.9-alpine

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 다운로드
RUN wget https://github.com/GeonDDing/Test-Automation/archive/refs/heads/main.zip \
    && unzip main.zip \
    && mv Test-Automation-main Test-Automation
    && rm main.zip

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r ./Test-Automation/requirements.txt

# 테스트 실행
CMD ["sh", "-c", "pytest ./Tests --capture=tee-sys --tb=no --alluredir=allure-results && pytest ./Backend/Tests --capture=tee-sys --tb=no --alluredir=allure-results"]
