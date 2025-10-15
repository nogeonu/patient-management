# 🤝 기여 가이드

환자관리시스템 프로젝트에 기여해주셔서 감사합니다! 

## 📋 기여 방법

### 1. 이슈 제기
버그를 발견하거나 새로운 기능을 제안하고 싶다면:
- GitHub Issues에 새로운 이슈 생성
- 명확한 제목과 설명 작성
- 가능하면 스크린샷 첨부

### 2. 풀 리퀘스트 (Pull Request)

#### 준비 단계
```bash
# 1. Fork this repository
# GitHub에서 'Fork' 버튼 클릭

# 2. 로컬에 클론
git clone https://github.com/YOUR_USERNAME/konyang-patient-management.git
cd konyang-patient-management

# 3. 원본 저장소를 upstream으로 추가
git remote add upstream https://github.com/ORIGINAL_OWNER/konyang-patient-management.git

# 4. 새 브랜치 생성
git checkout -b feature/your-feature-name
# 또는
git checkout -b bugfix/your-bugfix-name
```

#### 개발 단계
```bash
# 1. 변경사항 작성

# 2. 코드 스타일 확인 (선택사항)
# flake8이 설치되어 있다면:
flake8 patient_management_app.py

# 3. 변경사항 커밋
git add .
git commit -m "feat: add new feature description"
# 또는
git commit -m "fix: fix bug description"

# 4. Push to your fork
git push origin feature/your-feature-name
```

#### PR 생성
1. GitHub에서 'New Pull Request' 클릭
2. 변경사항 설명 작성
3. 리뷰어 대기

### 3. 커밋 메시지 규칙

다음 형식을 따라주세요:

```
<타입>: <제목>

<본문 (선택사항)>

<푸터 (선택사항)>
```

**타입:**
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅 (기능 변경 없음)
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드
- `chore`: 빌드 및 설정 변경

**예시:**
```bash
git commit -m "feat: add patient search by phone number"
git commit -m "fix: resolve database connection timeout issue"
git commit -m "docs: update README with new API endpoints"
```

## 🎨 코드 스타일

### Python (PEP 8)
- 들여쓰기: 4 spaces
- 최대 라인 길이: 100자
- 함수/메서드 사이: 2줄 공백
- 클래스 사이: 2줄 공백

```python
# 좋은 예
def calculate_priority(severity: int, age: int) -> str:
    """우선순위 계산 함수"""
    if severity == 3 or age >= 80:
        return '높음'
    return '낮음'

# 나쁜 예
def calculate_priority(severity,age):
    if severity==3 or age>=80:return '높음'
    return '낮음'
```

### HTML/CSS
- 들여쓰기: 2 spaces
- 클래스명: kebab-case (`patient-card`)
- ID: camelCase (`patientList`)

### JavaScript
- 들여쓰기: 2 spaces
- 세미콜론 사용
- 함수명: camelCase
- 상수: UPPER_SNAKE_CASE

## 🧪 테스트

변경사항이 있다면 테스트를 진행해주세요:

```bash
# 1. 개발 서버 실행
python patient_management_app.py

# 2. 브라우저에서 수동 테스트
# - 환자 등록/수정/삭제
# - 검색 기능
# - 통계 업데이트

# 3. 데이터베이스 연결 확인
# - /db-info 페이지 접속
```

## 📝 문서화

새로운 기능을 추가했다면:
- README.md 업데이트
- 함수/클래스에 docstring 추가
- 필요시 별도 문서 작성

## 🐛 버그 리포트

버그 리포트 시 다음 정보를 포함해주세요:

1. **재현 방법**: 버그를 재현하는 단계
2. **예상 동작**: 어떻게 동작해야 하는지
3. **실제 동작**: 실제로 어떻게 동작하는지
4. **환경 정보**:
   - OS: macOS / Windows / Linux
   - Python 버전
   - MySQL 버전
   - 브라우저 (Chrome / Firefox / Safari)
5. **스크린샷**: 가능하면 첨부

## ✨ 기능 제안

새로운 기능을 제안하려면:

1. **목적**: 왜 이 기능이 필요한가?
2. **설명**: 어떤 기능인가?
3. **예상 동작**: 어떻게 동작해야 하는가?
4. **대안**: 다른 방법은 없는가?

## 🎯 개선 우선순위

현재 진행 중이거나 환영하는 개선사항:

### High Priority
- [ ] 사용자 인증 시스템 (로그인/로그아웃)
- [ ] 환자 진료 기록 관리
- [ ] 단위 테스트 추가
- [ ] API 문서화 (Swagger)

### Medium Priority  
- [ ] 차트 및 시각화 개선
- [ ] PDF 리포트 생성
- [ ] 이메일 알림 시스템
- [ ] 백업/복구 기능

### Low Priority
- [ ] 다국어 지원 (i18n)
- [ ] 다크모드 지원
- [ ] 모바일 앱 개발
- [ ] Docker 컨테이너화

## 📞 연락처

질문이나 제안사항이 있다면:
- GitHub Issues
- Pull Request 코멘트
- Discussions (활성화 시)

---

**모든 기여자분들께 감사드립니다!** 🙏

여러분의 기여가 이 프로젝트를 더 나은 방향으로 발전시킵니다.

