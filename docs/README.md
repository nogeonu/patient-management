# 📚 Documentation

이 폴더에는 프로젝트 관련 문서와 이미지가 포함되어 있습니다.

## 📁 폴더 구조

```
docs/
├── images/              # 스크린샷 및 다이어그램
│   ├── dashboard.png
│   ├── patients.png
│   ├── add_patient.png
│   ├── edit_patient.png
│   ├── hospitals.png
│   └── db_info.png
│
└── README.md           # 이 파일
```

## 📸 스크린샷 가이드

### 스크린샷 촬영 방법

1. **애플리케이션 실행**
```bash
python patient_management_app.py
```

2. **브라우저에서 각 페이지 접속**
- http://localhost:5004/ (대시보드)
- http://localhost:5004/patients (환자 목록)
- http://localhost:5004/patients/add (환자 등록)
- http://localhost:5004/hospitals (병원 현황)
- http://localhost:5004/db-info (DB 정보)

3. **스크린샷 촬영**
- macOS: `Cmd + Shift + 4`
- Windows: `Win + Shift + S`
- Linux: `Print Screen` 또는 `gnome-screenshot`

4. **이미지 저장**
- 파일명: 영문 소문자, 언더스코어 사용
- 형식: PNG (권장)
- 크기: 1920x1080 또는 1440x900

### 필요한 스크린샷 목록

#### 데스크톱 화면
- [ ] `dashboard.png` - 메인 대시보드
- [ ] `patients.png` - 환자 목록
- [ ] `add_patient.png` - 환자 등록 폼
- [ ] `edit_patient.png` - 환자 수정 폼
- [ ] `hospitals.png` - 병원 현황
- [ ] `db_info.png` - 데이터베이스 정보

#### 모바일 화면 (선택사항)
- [ ] `mobile_dashboard.png` - 모바일 대시보드
- [ ] `mobile_patients.png` - 모바일 환자 목록

#### 기능 화면
- [ ] `search_result.png` - 검색 결과
- [ ] `priority_update.png` - 우선순위 업데이트
- [ ] `statistics.png` - 통계 화면

## 🎨 스크린샷 최적화

### 이미지 최적화 도구

```bash
# ImageMagick으로 크기 조정
convert dashboard.png -resize 1920x1080 dashboard_optimized.png

# 용량 압축 (품질 85%)
convert dashboard.png -quality 85 dashboard_compressed.png
```

### 온라인 도구
- [TinyPNG](https://tinypng.com/) - PNG 압축
- [Squoosh](https://squoosh.app/) - 이미지 최적화
- [ImageOptim](https://imageoptim.com/) - macOS 전용

## 📝 다이어그램

### 추가 가능한 다이어그램

#### 1. 시스템 아키텍처
```
┌─────────┐     ┌─────────┐     ┌──────────┐
│ Client  │────▶│  Flask  │────▶│  MySQL   │
│ Browser │     │  App    │     │ Database │
└─────────┘     └─────────┘     └──────────┘
```

#### 2. 데이터 플로우
```
User Input → Validation → Business Logic → Database → Response
```

#### 3. ER 다이어그램
```
┌──────────┐       ┌──────────┐
│ Patient  │───────│ Hospital │
│          │  N:1  │          │
└──────────┘       └──────────┘
```

## 🖼️ 이미지 사용 가이드

### README.md에서 이미지 삽입

```markdown
![대시보드](docs/images/dashboard.png)
```

### 상대 경로 사용
```markdown
![환자 목록](./images/patients.png)
```

### HTML 이미지 태그
```html
<img src="docs/images/dashboard.png" alt="대시보드" width="800"/>
```

## 📐 권장 이미지 규격

| 용도 | 크기 | 형식 |
|-----|------|------|
| 메인 스크린샷 | 1920x1080 | PNG |
| 모바일 스크린샷 | 375x812 | PNG |
| 아이콘 | 512x512 | PNG |
| 로고 | SVG 또는 PNG | SVG/PNG |
| 다이어그램 | 가변 | SVG/PNG |

## 🎯 체크리스트

스크린샷 추가 전 확인사항:

- [ ] 테스트 데이터가 충분히 입력되어 있는가?
- [ ] 브라우저 창이 깔끔한가? (개발자 도구 닫기)
- [ ] 민감한 정보가 노출되지 않는가?
- [ ] 이미지가 선명한가?
- [ ] 파일 크기가 적절한가? (< 500KB)
- [ ] 파일명이 명확한가?

---

**문서 업데이트일**: 2025년 10월 15일

