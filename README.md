# 🏥 Patient Management System

> Flask 기반의 현대적인 환자 관리 웹 애플리케이션

[![Flask](https://img.shields.io/badge/Flask-3.1.1-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 프로젝트 소개

기존 콘솔 기반 환자관리시스템을 현대적인 웹 인터페이스로 전환한 Flask 애플리케이션입니다. 
실시간 환자 정보 관리, 우선순위 시스템, 병원별 통계 등을 제공하여 효율적인 병원 운영을 지원합니다.

### ✨ 주요 기능

- **📊 실시간 대시보드**
  - 환자 수, 우선순위, 진료비 실시간 통계
  - Top 10 우선순위 환자 목록
  - 병원별 현황 요약

- **👥 환자 관리**
  - 환자 등록, 수정, 삭제
  - 이름 및 전화번호 기반 검색
  - 자동 우선순위 계산 (중증도 + 나이)
  - 진료비 자동 산정 (65세 이상 20% 할인)

- **🏥 병원 현황**
  - 병원별 환자 분포
  - 중증도별 통계 (경증/중등도/중증)
  - 전문분야별 분류

- **📱 반응형 디자인**
  - 모바일, 태블릿, 데스크톱 지원
  - Bootstrap 5 기반 현대적인 UI
  - 직관적인 사용자 경험

## 🚀 빠른 시작

### 필수 요구사항

- Python 3.9 이상
- MySQL 8.0 이상
- pip (Python 패키지 관리자)

### 설치 방법

1. **저장소 클론**
```bash
git clone https://github.com/nogeonu/patient-management.git
cd patient-management
```

2. **가상환경 생성 및 활성화**
```bash
python3 -m venv flask_env
source flask_env/bin/activate  # macOS/Linux
# 또는
flask_env\Scripts\activate     # Windows
```

3. **의존성 패키지 설치**
```bash
pip install -r requirements.txt
```

4. **데이터베이스 설정**
```bash
# MySQL 서버에 접속하여 데이터베이스 생성
mysql -u root -p < database/gcp_mysql_setup.sql
```

5. **환경변수 설정**
```bash
# 환경변수 파일 생성
cp env.example .env
# .env 파일을 열어서 데이터베이스 정보 수정
```

6. **애플리케이션 실행**
```bash
python patient_management_app.py
# 또는
./scripts/run.sh
```

7. **브라우저에서 접속**
```
http://localhost:5004
```

## 📁 프로젝트 구조

```
patient-management/
├── 📄 patient_management_app.py    # 메인 Flask 애플리케이션
├── 📄 requirements.txt              # Python 패키지 의존성
├── 📄 env.example                  # 환경변수 설정 예제
├── 📄 README.md                     # 프로젝트 문서
├── 📄 LICENSE                       # MIT 라이센스
├── 📄 .gitignore                    # Git 제외 파일 목록
│
├── 📁 templates/                    # HTML 템플릿
│   ├── base.html                   # 기본 레이아웃
│   ├── dashboard.html              # 대시보드
│   ├── patients.html               # 환자 목록
│   ├── add_patient.html            # 환자 등록
│   ├── edit_patient.html           # 환자 수정
│   └── hospitals.html              # 병원 현황
│
├── 📁 static/                       # 정적 파일
│   ├── css/
│   │   └── style.css              # 커스텀 스타일시트
│   ├── js/
│   │   └── app.js                 # JavaScript 기능
│   └── images/                    # 이미지 파일
│
├── 📁 database/                     # 데이터베이스 관련
│   └── gcp_mysql_setup.sql        # 초기화 스크립트
│
├── 📁 scripts/                      # 실행 스크립트
│   ├── run.sh                     # 애플리케이션 실행
│   └── deploy_to_gcp.sh           # GCP 배포 스크립트
│
├── 📁 docs/                         # 문서
│   ├── README.md                  # 문서 가이드
│   ├── guides/                    # 상세 가이드들
│   │   ├── QUICK_START.md         # 빠른 시작
│   │   ├── DEPLOY.md              # 배포 가이드
│   │   ├── CONTRIBUTING.md        # 기여 가이드
│   │   └── ...                    # 기타 가이드들
│   └── images/                    # 스크린샷
│
├── 📁 gcp_deploy/                   # GCP 배포 설정
│   ├── gcp_setup_guide.md
│   ├── patient_management_app.py
│   ├── requirements.txt
│   ├── start_server.sh
│   ├── static/ → templates/
│
└── 📁 .github/                      # GitHub 설정
    └── workflows/
        └── ci.yml                 # CI/CD 파이프라인
```

## 🔧 기술 스택

### Backend
- **Flask 3.1.1** - Python 웹 프레임워크
- **MySQL Connector 9.4.0** - 데이터베이스 연동
- **Python 3.9+** - 프로그래밍 언어

### Frontend
- **Bootstrap 5** - UI 프레임워크
- **Bootstrap Icons** - 아이콘
- **JavaScript (Vanilla)** - 클라이언트 로직
- **HTML5 / CSS3** - 마크업 & 스타일링

### Database
- **MySQL 8.0+** - 관계형 데이터베이스
- **저장 프로시저** - 비즈니스 로직 처리

### Deployment
- **Google Cloud Platform (GCP)** - 클라우드 호스팅
- **Cloud SQL** - 관리형 MySQL

## 📊 API 엔드포인트

### 웹 페이지
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/` | 대시보드 |
| GET | `/patients` | 환자 목록 |
| GET | `/patients/add` | 환자 등록 페이지 |
| POST | `/patients/add` | 환자 등록 처리 |
| GET | `/patients/<id>/edit` | 환자 수정 페이지 |
| POST | `/patients/<id>/edit` | 환자 수정 처리 |
| POST | `/patients/<id>/delete` | 환자 삭제 |
| GET | `/hospitals` | 병원 현황 |

### REST API
| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/update_ranks` | 우선순위 업데이트 |
| GET | `/api/dashboard_stats` | 대시보드 통계 |
| POST | `/api/test_db_connection` | DB 연결 테스트 |
| GET | `/api/table_data/<table_name>` | 테이블 데이터 조회 |
| GET | `/api/table_stats` | 테이블 통계 |

## 🎯 핵심 특징

### 1. 자동 우선순위 시스템
- 중증도(1-3)와 나이를 기반으로 우선순위 자동 계산
- 중증(3) 또는 80세 이상 → 높음
- 중등도(2) 또는 65세 이상 → 중간
- 경증(1) → 낮음

### 2. 진료비 자동 산정
- 질병별 기본 진료비 테이블
- 중증도에 따른 배수 적용 (경증 1.0x, 중등도 1.5x, 중증 2.5x)
- 65세 이상 환자 20% 자동 할인

### 3. 통합 환자 검색
- 이름으로 검색 시 같은 전화번호를 가진 모든 기록 조회
- 재방문 환자 관리 용이

### 4. 실시간 통계
- 대시보드 실시간 업데이트
- AJAX 기반 비동기 데이터 갱신

## 🔒 보안 기능

- ✅ CSRF 보호 (Flask secret key)
- ✅ SQL Injection 방지 (저장 프로시저 사용)
- ✅ XSS 방지 (Jinja2 템플릿 자동 이스케이프)
- ✅ 입력 유효성 검사
- ✅ 안전한 비밀번호 관리 (환경변수 권장)

## 🌐 배포

### 로컬 개발
```bash
python patient_management_app.py
```

### GCP 배포
```bash
./scripts/deploy_to_gcp.sh
```

### Docker 배포
```bash
docker-compose up -d
```

자세한 배포 방법은 [`docs/guides/DEPLOY.md`](docs/guides/DEPLOY.md)를 참고하세요.

## 📚 문서

- 📖 [빠른 시작 가이드](docs/guides/QUICK_START.md)
- 📖 [배포 가이드](docs/guides/DEPLOY.md)
- 📖 [기여 가이드](docs/guides/CONTRIBUTING.md)
- 📖 [Git 사용법](docs/guides/GIT_GUIDE.md)
- 📖 [프로젝트 요약](docs/guides/PROJECT_SUMMARY.md)
- 📖 [변경 이력](docs/guides/CHANGELOG.md)

## 🚨 문제 해결

### 데이터베이스 연결 오류
```
[ERROR] DB 연결 실패
```
**해결방법:**
- MySQL 서버 상태 확인
- 연결 정보 (host, user, password) 확인
- 방화벽 규칙 확인

### 포트 충돌
```
Address already in use
```
**해결방법:**
- 다른 포트 사용: `app.run(port=5001)`
- 기존 프로세스 종료

### 템플릿 오류
**해결방법:**
- `templates/` 폴더 경로 확인
- 템플릿 파일 존재 여부 확인

## 📈 향후 개선 계획

- [ ] 사용자 인증 시스템 추가 (로그인/로그아웃)
- [ ] 환자 진료 기록 관리
- [ ] 차트 및 시각화 개선 (Chart.js)
- [ ] PDF 리포트 생성 기능
- [ ] 이메일 알림 시스템
- [ ] 백업/복구 자동화
- [ ] REST API 문서화 (Swagger)
- [ ] Docker 컨테이너화

## 🤝 기여하기

프로젝트 개선에 기여하고 싶으시다면 [`docs/guides/CONTRIBUTING.md`](docs/guides/CONTRIBUTING.md)를 참고하세요.

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

## 👨‍💻 개발자

건양대학교 바이오메디컬팀

## 📞 문의

프로젝트 관련 문의사항이나 버그 리포트는 [GitHub Issues](https://github.com/nogeonu/patient-management/issues)를 통해 등록해주세요.

---

**Patient Management System v1.3**  
*최종 업데이트: 2025년 10월*

Made with ❤️ by 건양대학교 바이오메디컬팀