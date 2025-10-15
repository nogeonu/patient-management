# 🌳 Git & GitHub 가이드

## 📦 첫 번째 GitHub 업로드

### 1단계: Git 초기화

```bash
# 프로젝트 폴더로 이동
cd "/Users/nogeon-u/Desktop/건양대_바이오메디컬 /frountend/project/환자관리_대시보드"

# Git 저장소 초기화
git init

# 기본 브랜치를 main으로 설정
git branch -M main
```

### 2단계: 사용자 정보 설정 (최초 1회)

```bash
# 사용자 이름 설정
git config --global user.name "Your Name"

# 이메일 설정
git config --global user.email "your.email@example.com"

# 설정 확인
git config --list
```

### 3단계: 파일 추가 및 커밋

```bash
# 모든 파일 스테이징
git add .

# 첫 커밋
git commit -m "🎉 Initial commit: Konyang Hospital Patient Management System v1.3

- Flask 기반 환자 관리 웹 애플리케이션
- 실시간 대시보드 및 통계
- 환자 CRUD 기능
- 우선순위 자동 계산 시스템
- 반응형 디자인 (Bootstrap 5)
- GCP 배포 지원
- 완전한 문서화"
```

### 4단계: GitHub 저장소 생성

1. **GitHub 웹사이트 접속**
   - https://github.com 로그인

2. **New Repository 클릭**
   - Repository name: `konyang-patient-management`
   - Description: `🏥 Modern patient management web application for Konyang University Hospital built with Flask, MySQL, and Bootstrap 5`
   - Public 또는 Private 선택
   - **❌ README, .gitignore, license 추가하지 않기** (이미 있음)

3. **Create repository 클릭**

### 5단계: 원격 저장소 연결 및 푸시

```bash
# 원격 저장소 추가 (YOUR_USERNAME을 본인 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/konyang-patient-management.git

# 원격 저장소 확인
git remote -v

# 첫 푸시
git push -u origin main
```

### 6단계: GitHub에서 확인

브라우저에서 저장소 확인:
```
https://github.com/YOUR_USERNAME/konyang-patient-management
```

---

## 🔖 Topics 추가

GitHub 저장소 페이지에서:

1. **About** 옆의 ⚙️ 아이콘 클릭
2. **Topics** 추가:
```
flask, python, mysql, healthcare, patient-management, 
hospital-management, web-application, bootstrap, 
medical, dashboard, gcp, cloud-sql, korean
```
3. **Save changes** 클릭

---

## 📝 일상적인 Git 작업

### 변경사항 확인

```bash
# 변경된 파일 확인
git status

# 변경 내용 상세 확인
git diff
```

### 파일 추가 및 커밋

```bash
# 특정 파일만 추가
git add patient_management_app.py

# 모든 변경사항 추가
git add .

# 커밋 (간단한 메시지)
git commit -m "fix: resolve database connection issue"

# 커밋 (상세한 메시지)
git commit -m "feat: add patient search by phone number

- Implement phone number search functionality
- Update database query to include phone field
- Add search UI component
- Update tests"
```

### 푸시 및 풀

```bash
# 원격 저장소로 푸시
git push origin main

# 원격 저장소에서 풀
git pull origin main
```

---

## 🌿 브랜치 관리

### 새 기능 개발

```bash
# 새 브랜치 생성 및 이동
git checkout -b feature/user-authentication

# 브랜치 목록 확인
git branch

# 작업 후 커밋
git add .
git commit -m "feat: implement user login system"

# 원격에 푸시
git push origin feature/user-authentication
```

### 브랜치 병합

```bash
# main 브랜치로 이동
git checkout main

# 원격 최신 상태로 업데이트
git pull origin main

# feature 브랜치 병합
git merge feature/user-authentication

# 푸시
git push origin main

# feature 브랜치 삭제 (선택사항)
git branch -d feature/user-authentication
```

---

## 🔍 유용한 Git 명령어

### 로그 확인

```bash
# 커밋 히스토리 확인 (간단)
git log --oneline

# 커밋 히스토리 확인 (상세)
git log --graph --decorate --all

# 특정 파일 히스토리
git log -- patient_management_app.py
```

### 되돌리기

```bash
# 마지막 커밋 수정 (푸시 전)
git commit --amend -m "new commit message"

# 스테이징 취소
git reset HEAD patient_management_app.py

# 파일 변경 취소
git checkout -- patient_management_app.py

# 커밋 되돌리기 (안전한 방법)
git revert <commit-hash>

# 커밋 되돌리기 (강제, 주의!)
git reset --hard <commit-hash>
```

### 태그 관리

```bash
# 버전 태그 생성
git tag -a v1.3.0 -m "Release version 1.3.0"

# 태그 푸시
git push origin v1.3.0

# 모든 태그 푸시
git push origin --tags

# 태그 목록 확인
git tag -l
```

---

## 🤝 협업 워크플로우

### Fork & Pull Request 방식

1. **Fork**: GitHub에서 저장소 Fork
2. **Clone**: 본인 계정의 저장소 클론
```bash
git clone https://github.com/YOUR_USERNAME/konyang-patient-management.git
```

3. **Upstream 설정**: 원본 저장소 추가
```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/konyang-patient-management.git
```

4. **브랜치 생성**: 새 기능용 브랜치
```bash
git checkout -b feature/new-feature
```

5. **작업 후 커밋 및 푸시**
```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

6. **Pull Request**: GitHub에서 PR 생성

7. **Upstream 동기화**
```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## 🛠️ .gitignore 패턴

현재 프로젝트의 `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
flask_env/

# IDE
.vscode/
.idea/
.DS_Store

# Environment
.env
*.log

# Compressed
*.tar.gz
*.zip

# Database
*.sql.backup
```

---

## 📊 Git 통계

### 프로젝트 통계 확인

```bash
# 커밋 수 확인
git rev-list --count main

# 기여자 확인
git shortlog -sn

# 코드 변경 통계
git diff --stat

# 파일별 변경 이력
git log --follow -- patient_management_app.py
```

---

## 🚨 주의사항

### 절대 커밋하면 안 되는 것들

- ❌ `.env` 파일 (환경변수, 비밀번호)
- ❌ `flask_env/` 폴더 (가상환경)
- ❌ 데이터베이스 백업 파일
- ❌ API 키, 비밀 키
- ❌ 개인정보가 포함된 파일
- ❌ 대용량 바이너리 파일

### 실수로 커밋한 경우

```bash
# 파일을 Git에서 제거 (로컬 파일은 유지)
git rm --cached .env

# .gitignore에 추가
echo ".env" >> .gitignore

# 커밋
git commit -m "chore: remove .env from git"

# 강제 푸시 (이미 푸시한 경우, 주의!)
git push origin main --force
```

---

## 💡 Git 팁

### 1. 커밋 메시지 규칙
```
<type>: <subject>

<body>

<footer>
```

**Type:**
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅
- `refactor`: 리팩토링
- `test`: 테스트 추가
- `chore`: 빌드/설정 변경

### 2. 유용한 별칭 (Aliases)

```bash
# Git 별칭 설정
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph --decorate"

# 사용
git st
git lg
```

### 3. SSH 키 설정 (HTTPS 대신 SSH 사용)

```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your.email@example.com"

# 공개키 복사
cat ~/.ssh/id_ed25519.pub

# GitHub에 SSH 키 추가 (Settings > SSH and GPG keys)

# 원격 저장소 URL 변경
git remote set-url origin git@github.com:YOUR_USERNAME/konyang-patient-management.git
```

---

## 📚 더 배우기

- [Pro Git Book (한국어)](https://git-scm.com/book/ko/v2)
- [GitHub Docs](https://docs.github.com/ko)
- [GitHub Skills](https://skills.github.com/)
- [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials)

---

**Happy Git-ing! 🚀**

