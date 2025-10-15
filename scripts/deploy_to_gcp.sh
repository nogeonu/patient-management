#!/bin/bash

echo "🚀 GCP 배포용 파일 준비 중..."

# 배포용 디렉토리 생성
mkdir -p gcp_deploy

# 필요한 파일들 복사
cp patient_management_app.py gcp_deploy/
cp requirements.txt gcp_deploy/
cp -r static gcp_deploy/
cp -r templates gcp_deploy/

# GCP용 실행 스크립트 생성
cat > gcp_deploy/start_server.sh << 'EOF'
#!/bin/bash

echo "🔧 Python 환경 설정 중..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv mysql-client

echo "📦 가상환경 생성 및 활성화..."
python3 -m venv flask_env
source flask_env/bin/activate

echo "📋 의존성 설치 중..."
pip install -r requirements.txt

echo "🌐 Flask 서버 시작..."
python3 patient_management_app.py
EOF

chmod +x gcp_deploy/start_server.sh

# 압축 파일 생성
tar -czf patient_management_gcp.tar.gz -C gcp_deploy .

echo "✅ 배포 파일 준비 완료!"
echo "📦 생성된 파일: patient_management_gcp.tar.gz"
echo ""
echo "🔥 다음 단계:"
echo "1. patient_management_gcp.tar.gz 파일을 GCP VM에 업로드"
echo "2. VM에서 압축 해제 및 실행"

