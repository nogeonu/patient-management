#!/bin/bash
# 건양대학교병원 환자관리시스템 실행 스크립트

echo "=== 건양대학교병원 환자관리시스템 시작 ==="

# 가상환경 활성화
source flask_env/bin/activate

# Flask 애플리케이션 실행
python3 patient_management_app.py
