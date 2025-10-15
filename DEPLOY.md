# 🚀 배포 가이드

## 배포 옵션

이 애플리케이션은 다양한 환경에 배포할 수 있습니다:

1. [로컬 서버](#1-로컬-서버-배포)
2. [Google Cloud Platform (GCP)](#2-gcp-배포)
3. [AWS EC2](#3-aws-ec2-배포)
4. [Heroku](#4-heroku-배포)
5. [Docker](#5-docker-배포)

---

## 1. 로컬 서버 배포

### 개발 환경
```bash
# 가상환경 활성화
source flask_env/bin/activate

# 개발 서버 실행
python patient_management_app.py
```

### 프로덕션 환경 (Gunicorn 사용)
```bash
# Gunicorn 설치
pip install gunicorn

# Gunicorn으로 실행 (4개 워커)
gunicorn -w 4 -b 0.0.0.0:5004 patient_management_app:app

# 백그라운드 실행
nohup gunicorn -w 4 -b 0.0.0.0:5004 patient_management_app:app &
```

---

## 2. GCP 배포

자세한 내용은 [`gcp_deploy/gcp_setup_guide.md`](gcp_deploy/gcp_setup_guide.md)를 참고하세요.

### 빠른 단계

1. **GCP 프로젝트 생성**
```bash
gcloud projects create konyang-patient-mgmt
gcloud config set project konyang-patient-mgmt
```

2. **Cloud SQL 인스턴스 생성**
```bash
gcloud sql instances create konyang-mysql \
  --tier=db-f1-micro \
  --region=asia-northeast3 \
  --database-version=MYSQL_8_0
```

3. **Compute Engine VM 생성**
```bash
gcloud compute instances create patient-mgmt-vm \
  --zone=asia-northeast3-a \
  --machine-type=e2-micro \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud
```

4. **애플리케이션 배포**
```bash
# VM에 SSH 접속
gcloud compute ssh patient-mgmt-vm

# 저장소 클론
git clone https://github.com/YOUR_USERNAME/konyang-patient-management.git
cd konyang-patient-management

# 설치 및 실행
./gcp_deploy/start_server.sh
```

---

## 3. AWS EC2 배포

### 단계별 가이드

1. **EC2 인스턴스 생성**
   - AMI: Ubuntu 20.04 LTS
   - 인스턴스 타입: t2.micro (프리티어)
   - 보안 그룹: HTTP (80), HTTPS (443), Custom TCP (5004)

2. **SSH 접속 및 설정**
```bash
# SSH 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 및 MySQL 설치
sudo apt install python3-pip python3-venv mysql-server -y

# 저장소 클론
git clone https://github.com/YOUR_USERNAME/konyang-patient-management.git
cd konyang-patient-management

# 가상환경 설정
python3 -m venv flask_env
source flask_env/bin/activate
pip install -r requirements.txt

# 데이터베이스 설정
sudo mysql < gcp_mysql_setup.sql

# Gunicorn으로 실행
gunicorn -w 4 -b 0.0.0.0:5004 patient_management_app:app
```

3. **Nginx 리버스 프록시 설정 (선택사항)**
```bash
# Nginx 설치
sudo apt install nginx -y

# 설정 파일 생성
sudo nano /etc/nginx/sites-available/patient-mgmt

# 다음 내용 추가:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 심볼릭 링크 생성
sudo ln -s /etc/nginx/sites-available/patient-mgmt /etc/nginx/sites-enabled/

# Nginx 재시작
sudo systemctl restart nginx
```

---

## 4. Heroku 배포

### 준비 파일

1. **Procfile 생성**
```bash
echo "web: gunicorn patient_management_app:app" > Procfile
```

2. **runtime.txt 생성**
```bash
echo "python-3.9.18" > runtime.txt
```

### 배포 단계
```bash
# Heroku CLI 설치 (macOS)
brew install heroku/brew/heroku

# 로그인
heroku login

# 앱 생성
heroku create konyang-patient-mgmt

# MySQL 애드온 추가
heroku addons:create cleardb:ignite

# 환경변수 설정
heroku config:set SECRET_KEY=your-secret-key

# 배포
git push heroku main

# 데이터베이스 초기화
heroku run bash
mysql -h your-cleardb-host < gcp_mysql_setup.sql
```

---

## 5. Docker 배포

### Dockerfile 생성
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 복사
COPY . .

# 포트 노출
EXPOSE 5004

# 실행
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5004", "patient_management_app:app"]
```

### docker-compose.yml 생성
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5004:5004"
    environment:
      - DB_HOST=db
      - DB_USER=konyang
      - DB_PASSWORD=konyang1234
      - DB_NAME=konyang
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root1234
      - MYSQL_DATABASE=konyang
      - MYSQL_USER=konyang
      - MYSQL_PASSWORD=konyang1234
    volumes:
      - mysql_data:/var/lib/mysql
      - ./gcp_mysql_setup.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  mysql_data:
```

### Docker 실행
```bash
# 빌드 및 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

---

## 🔒 프로덕션 체크리스트

배포 전 확인사항:

- [ ] `DEBUG = False` 설정
- [ ] 강력한 `SECRET_KEY` 사용
- [ ] 데이터베이스 비밀번호 변경
- [ ] HTTPS 설정 (SSL 인증서)
- [ ] 방화벽 규칙 설정
- [ ] 백업 시스템 구축
- [ ] 모니터링 설정
- [ ] 로그 관리 시스템
- [ ] 에러 추적 (Sentry 등)
- [ ] 성능 최적화
- [ ] 보안 헤더 설정
- [ ] CORS 설정 (필요시)

---

## 📊 모니터링

### 애플리케이션 로그
```bash
# 로그 파일 위치
tail -f /var/log/patient-mgmt/app.log

# Gunicorn 로그
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log
```

### 시스템 모니터링
```bash
# CPU/메모리 사용량
htop

# 디스크 사용량
df -h

# 네트워크 연결
netstat -tulpn | grep 5004
```

---

## 🔄 업데이트 및 롤백

### 코드 업데이트
```bash
# 최신 코드 가져오기
git pull origin main

# 의존성 업데이트
pip install -r requirements.txt --upgrade

# 서비스 재시작
sudo systemctl restart patient-mgmt
```

### 롤백
```bash
# 이전 커밋으로 되돌리기
git log --oneline  # 커밋 해시 확인
git checkout <commit-hash>

# 서비스 재시작
sudo systemctl restart patient-mgmt
```

---

## 📞 지원

배포 관련 문제가 발생하면 GitHub Issues에 문의해주세요.

