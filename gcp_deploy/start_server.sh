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
