# 🚀 GCP VM 배포 가이드

## 1단계: GCP VM 인스턴스 설정

### VM 사양 권장사항:
- **머신 유형**: e2-medium (2 vCPU, 4GB 메모리)
- **부팅 디스크**: Ubuntu 20.04 LTS
- **방화벽**: HTTP, HTTPS 트래픽 허용 체크

## 2단계: 방화벽 규칙 생성

```bash
# GCP Console에서 또는 gcloud CLI로:
gcloud compute firewall-rules create allow-flask-5004 \
    --allow tcp:5004 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow Flask app on port 5004"
```

## 3단계: VM에 파일 업로드

### 방법 1: gcloud SCP 사용
```bash
gcloud compute scp patient_management_gcp.tar.gz [VM_INSTANCE_NAME]:~/
```

### 방법 2: SSH 접속 후 wget 사용
```bash
# 로컬에서 파일을 웹서버에 업로드한 후
wget [파일_URL]
```

## 4단계: VM에서 실행

### SSH로 VM 접속:
```bash
gcloud compute ssh [VM_INSTANCE_NAME]
```

### 파일 압축 해제 및 설정:
```bash
# 압축 해제
tar -xzf patient_management_gcp.tar.gz

# 실행 권한 부여
chmod +x start_server.sh

# 서버 시작
./start_server.sh
```

## 5단계: 백그라운드 실행 (선택사항)

```bash
# nohup으로 백그라운드 실행
nohup python3 patient_management_app.py > app.log 2>&1 &

# 또는 screen 사용
screen -S flask_app
python3 patient_management_app.py
# Ctrl+A, D로 detach
```

## 6단계: 접속 확인

브라우저에서 접속:
```
http://104.197.185.10:5004
```

## 🔧 트러블슈팅

### MySQL 연결 오류 시:
```bash
# MySQL 서버 상태 확인
sudo systemctl status mysql

# MySQL 재시작
sudo systemctl restart mysql
```

### 포트 확인:
```bash
# 포트 5004가 열려있는지 확인
netstat -tlnp | grep 5004
```

### 로그 확인:
```bash
# Flask 앱 로그 확인
tail -f app.log
```

## 🔒 보안 설정 (운영환경)

### 1. 방화벽을 특정 IP만 허용하도록 변경:
```bash
gcloud compute firewall-rules update allow-flask-5004 \
    --source-ranges [허용할_IP_대역]
```

### 2. HTTPS 설정 (Let's Encrypt):
```bash
sudo apt install certbot
sudo certbot certonly --standalone -d [도메인명]
```

### 3. 환경변수로 DB 정보 분리:
```bash
export DB_HOST="104.197.185.10"
export DB_USER="acorn"
export DB_PASSWORD="acorn1234"
export DB_NAME="konyang"
```
