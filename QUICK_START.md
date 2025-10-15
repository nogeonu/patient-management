# 🚀 빠른 시작 가이드

## 5분 안에 시작하기

### 1️⃣ 사전 준비

먼저 다음 프로그램들이 설치되어 있는지 확인하세요:

```bash
# Python 버전 확인 (3.9 이상 필요)
python3 --version

# MySQL 설치 확인
mysql --version

# pip 확인
pip3 --version
```

### 2️⃣ 프로젝트 설정

```bash
# 1. 저장소 클론
git clone https://github.com/YOUR_USERNAME/konyang-patient-management.git
cd konyang-patient-management

# 2. 가상환경 생성 및 활성화
python3 -m venv flask_env
source flask_env/bin/activate  # macOS/Linux
# flask_env\Scripts\activate   # Windows

# 3. 패키지 설치
pip install -r requirements.txt
```

### 3️⃣ 데이터베이스 설정

```bash
# 1. MySQL 서버 시작
# macOS: brew services start mysql
# Linux: sudo systemctl start mysql
# Windows: MySQL Workbench에서 시작

# 2. 데이터베이스 생성
mysql -u root -p

# MySQL 프롬프트에서:
CREATE DATABASE konyang CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'konyang_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON konyang.* TO 'konyang_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 3. 초기 데이터 및 스키마 로드
mysql -u konyang_user -p konyang < gcp_mysql_setup.sql
```

### 4️⃣ 환경변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일을 열어서 데이터베이스 정보 수정
# nano .env 또는 원하는 에디터 사용
```

`.env` 파일 내용:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=konyang_user
DB_PASSWORD=your_password
DB_NAME=konyang
APP_PORT=5004
```

### 5️⃣ 애플리케이션 실행

```bash
# 방법 1: Python으로 직접 실행
python patient_management_app.py

# 방법 2: 실행 스크립트 사용 (Unix 계열)
chmod +x run.sh
./run.sh

# 방법 3: Flask CLI 사용
export FLASK_APP=patient_management_app.py
flask run --host=0.0.0.0 --port=5004
```

### 6️⃣ 브라우저에서 확인

웹 브라우저를 열고 다음 주소로 접속:

```
http://localhost:5004
```

🎉 **축하합니다!** 환자 관리 시스템이 실행되었습니다.

---

## 📋 초기 테스트 데이터

시스템을 테스트하려면 다음 예제 환자를 등록해보세요:

| 이름 | 나이 | 성별 | 질병 | 중증도 | 전화번호 |
|------|------|------|------|--------|----------|
| 김철수 | 75 | 남성 | 고혈압 | 중등도(2) | 010-1234-5678 |
| 이영희 | 35 | 여성 | 감기 | 경증(1) | 010-2345-6789 |
| 박민수 | 82 | 남성 | 폐렴 | 중증(3) | 010-3456-7890 |

---

## 🔍 문제 해결

### 포트가 이미 사용 중인 경우

```bash
# 포트 사용 중인 프로세스 확인 및 종료
# macOS/Linux:
lsof -ti:5004 | xargs kill -9

# Windows:
netstat -ano | findstr :5004
taskkill /PID <PID번호> /F
```

### MySQL 연결 오류

```bash
# MySQL 서비스 상태 확인
# macOS:
brew services list

# Linux:
sudo systemctl status mysql

# MySQL 로그 확인
# macOS: /usr/local/var/mysql/*.err
# Linux: /var/log/mysql/error.log
```

### 패키지 설치 오류

```bash
# pip 업그레이드
pip install --upgrade pip

# 개별 패키지 재설치
pip install --force-reinstall Flask mysql-connector-python
```

### 가상환경 활성화 안 될 때

```bash
# 실행 권한 부여 (macOS/Linux)
chmod +x flask_env/bin/activate

# PowerShell 정책 변경 (Windows)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎯 다음 단계

시스템이 정상 작동하면:

1. ✅ 대시보드에서 통계 확인
2. ✅ 환자 등록 테스트
3. ✅ 검색 기능 테스트
4. ✅ 우선순위 업데이트 테스트
5. ✅ 병원 현황 확인

---

## 📚 추가 자료

- 📖 [전체 README](README.md) - 상세한 프로젝트 문서
- 🔧 [GCP 배포 가이드](gcp_deploy/gcp_setup_guide.md) - 클라우드 배포 방법
- 🐛 [Issues](https://github.com/YOUR_USERNAME/konyang-patient-management/issues) - 버그 리포트 및 질문

---

**도움이 필요하신가요?** GitHub Issues에 질문을 올려주세요! 💬

