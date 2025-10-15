-- GCP MySQL 데이터베이스 설정 스크립트
-- VM에서 MySQL 설치 후 실행하세요

-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS medical_db;
USE medical_db;

-- 병원 테이블 생성
CREATE TABLE IF NOT EXISTS hospital (
    hospitalcode INT AUTO_INCREMENT PRIMARY KEY,
    hospitalname VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    speciality VARCHAR(100)
);

-- 환자 테이블 생성
CREATE TABLE IF NOT EXISTS patient (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    disease VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    treatment_cost DECIMAL(10,2),
    total_cost DECIMAL(10,2),
    priority INT,
    ranks INT,
    hospitalcode INT,
    admission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    gender VARCHAR(10),
    phone VARCHAR(20),
    FOREIGN KEY (hospitalcode) REFERENCES hospital(hospitalcode)
);

-- 샘플 병원 데이터 삽입
INSERT INTO hospital (hospitalname, address, speciality) VALUES
('서울대학교병원', '서울특별시 종로구 대학로 101', '종합병원'),
('연세대학교 세브란스병원', '서울특별시 서대문구 연세로 50-1', '종합병원'),
('삼성서울병원', '서울특별시 강남구 일원로 81', '종합병원'),
('건양대학교병원', '대전광역시 서구 관저동로 158', '종합병원'),
('아산병원', '서울특별시 송파구 올림픽로43길 88', '종합병원');

-- 샘플 환자 데이터 삽입
INSERT INTO patient (name, age, disease, severity, treatment_cost, total_cost, priority, ranks, hospitalcode, gender, phone) VALUES
('김철수', 45, '고혈압', '중간', 150000, 150000, 5, 1, 1, '남성', '010-1234-5678'),
('이영희', 67, '당뇨병', '심각', 200000, 160000, 9, 2, 2, '여성', '010-2345-6789'),
('박민수', 34, '감기', '경미', 50000, 50000, 2, 3, 3, '남성', '010-3456-7890'),
('홍길동', 72, '심장병', '심각', 300000, 240000, 10, 4, 1, '남성', '010-4567-8901'),
('김영수', 28, '위염', '중간', 80000, 80000, 4, 5, 4, '남성', '010-5678-9012');

-- 사용자 권한 설정 (GCP MySQL 사용자)
CREATE USER IF NOT EXISTS 'flask_user'@'%' IDENTIFIED BY 'flask_password123!';
GRANT ALL PRIVILEGES ON medical_db.* TO 'flask_user'@'%';
FLUSH PRIVILEGES;

SELECT '✅ 데이터베이스 설정 완료!' as status;

