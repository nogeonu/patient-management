#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
건양대학교병원 환자관리시스템 - Flask 웹 애플리케이션
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from typing import List, Optional, Dict, Any
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'konyang_hospital_secret_key_2024'

class Patient:
    """개별 환자 데이터 모델"""
    
    def __init__(self, id: Optional[int] = None, name: str = "", 
                 age: int = 0, disease: str = "", severity: int = 1,
                 gender: str = "", phone: str = ""):
        self.id = id
        self.name = name
        self.age = age
        self.disease = disease
        self.severity = severity
        self.gender = gender  # 성별 추가
        self.phone = phone    # 전화번호 추가
        self.treatment_cost = 0
        self.total_cost = 0.0
        self.priority = "낮음"
        self.rank = 0
        self.hospital_name = ""
        self.admission_date = None
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Patient':
        """딕셔너리에서 Patient 객체 생성"""
        patient = cls(
            id=data.get('id'),
            name=data.get('name', '') or '',
            age=data.get('age', 0) or 0,
            disease=data.get('disease', '') or '',
            severity=data.get('severity', 1) or 1,
            gender=data.get('gender', '') or '',
            phone=data.get('phone', '') or ''
        )
        patient.treatment_cost = data.get('treatment_cost', 0) or 0
        patient.total_cost = float(data.get('total_cost', 0.0) or 0.0)
        patient.priority = data.get('priority', '낮음') or '낮음'
        patient.rank = data.get('rank', 0) or 0
        patient.hospital_name = data.get('hospital_name', '') or ''
        patient.admission_date = data.get('admission_date')
        return patient

class WebDatabaseManager:
    """웹용 데이터베이스 매니저"""
    
    def __init__(self):
        self.host = "104.197.185.10"
        self.user = "acorn"
        self.password = "acorn1234"
        self.db_name = "konyang"
        self.default_hospital_code = "KY00000001"
    
    def get_connection(self):
        """데이터베이스 연결 반환"""
        return mysql.connector.connect(
            host=self.host,
            port=3306,
            user=self.user,
            password=self.password,
            database=self.db_name
        )
    
    def _calculate_treatment_cost(self, disease: str, severity: int) -> int:
        """질병별 기본 진료비 계산 (중증도 배수 적용)"""
        base_costs = {
            '감기': 30000,
            '독감': 50000,
            '폐렴': 200000,
            '고혈압': 80000,
            '당뇨': 120000,
            '심장병': 500000,
            '암': 1000000,
            '골절': 300000
        }
        
        base_cost = base_costs.get(disease, 50000)  # 기타 질병은 50000
        
        # 중증도 배수 적용
        multiplier = {1: 1.0, 2: 1.5, 3: 2.5}.get(severity, 1.0)
        
        return int(base_cost * multiplier)
    
    def _calculate_priority(self, severity: int, age: int) -> str:
        """우선순위 계산 (중증도와 나이 고려)"""
        if severity == 3 or age >= 80:
            return '높음'
        elif severity == 2 or age >= 65:
            return '중간'
        else:
            return '낮음'
    
    def insert_patient_proc(self, patient: Patient, hospital_code: str = None) -> bool:
        """환자 데이터 삽입 (gender, phone 포함)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            code = hospital_code or self.default_hospital_code
            
            # 질병별 기본 진료비 계산
            treatment_cost_calc = self._calculate_treatment_cost(patient.disease, patient.severity)
            
            # 나이에 따른 총 비용 계산 (65세 이상 20% 할인)
            total_cost_calc = treatment_cost_calc * 0.8 if patient.age >= 65 else treatment_cost_calc
            
            # 우선순위 계산
            priority_calc = self._calculate_priority(patient.severity, patient.age)
            
            # 환자 데이터 삽입 (gender, phone 포함)
            insert_query = """
            INSERT INTO patient (name, age, disease, severity, treatment_cost, total_cost, 
                               priority, hospitalcode, gender, phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                patient.name, patient.age, patient.disease, patient.severity,
                treatment_cost_calc, total_cost_calc, priority_calc, code,
                patient.gender, patient.phone
            ))
            
            # 병원별 환자수 업데이트
            cursor.callproc('update_hospital_patient_count')
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"[ERROR] 환자 추가 실패: {e}")
            return False
    
    def update_patient_proc(self, patient: Patient) -> bool:
        """환자 정보 수정 (gender, phone 포함)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 환자가 존재하는지 확인
            cursor.execute("SELECT COUNT(*) FROM patient WHERE patient_id = %s", (patient.id,))
            if cursor.fetchone()[0] == 0:
                return False
            
            # 비용 재계산
            treatment_cost_calc = self._calculate_treatment_cost(patient.disease, patient.severity)
            total_cost_calc = treatment_cost_calc * 0.8 if patient.age >= 65 else treatment_cost_calc
            priority_calc = self._calculate_priority(patient.severity, patient.age)
            
            # 환자 정보 업데이트 (gender, phone 포함)
            update_query = """
            UPDATE patient 
            SET name = %s, age = %s, disease = %s, severity = %s,
                treatment_cost = %s, total_cost = %s, priority = %s,
                gender = %s, phone = %s
            WHERE patient_id = %s
            """
            
            cursor.execute(update_query, (
                patient.name, patient.age, patient.disease, patient.severity,
                treatment_cost_calc, total_cost_calc, priority_calc,
                patient.gender, patient.phone, patient.id
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"[ERROR] 환자 수정 실패: {e}")
            return False
    
    def delete_patient_proc(self, patient_id: int) -> bool:
        """저장 프로시저를 사용한 환자 삭제"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            args = [patient_id, 0]
            result = cursor.callproc('patient_delete_by_id', args)
            
            result_code = result[1]
            conn.commit()
            cursor.close()
            conn.close()
            
            return result_code == 1
        except Exception as e:
            print(f"[ERROR] 환자 삭제 실패: {e}")
            return False
    
    def update_ranks_proc(self) -> bool:
        """저장 프로시저를 사용한 우선순위별 순위 업데이트"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.callproc('update_patient_ranks')
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"[ERROR] 우선순위 업데이트 실패: {e}")
            return False
    
    def select_all_patients(self) -> List[Dict[str, Any]]:
        """모든 환자 데이터 조회"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            sql = """SELECT p.patient_id, p.name, p.age, p.disease, p.severity, p.treatment_cost, 
                            p.total_cost, p.priority, p.ranks, p.admission_date, h.hospitalname,
                            p.gender, p.phone
                     FROM patient p 
                     LEFT JOIN hospital h ON p.hospitalcode = h.hospitalcode
                     ORDER BY p.ranks"""
            cursor.execute(sql)
            
            columns = ["id", "name", "age", "disease", "severity", "treatment_cost", 
                      "total_cost", "priority", "rank", "admission_date", "hospital_name",
                      "gender", "phone"]
            
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            
            return results
        except Exception as e:
            print(f"[ERROR] 환자 데이터 조회 실패: {e}")
            return []
    
    def search_patients_by_name(self, search_name: str) -> List[Dict[str, Any]]:
        """이름으로 환자 검색 (같은 이름+전화번호 환자의 모든 기록 포함)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 1단계: 검색된 이름과 일치하는 환자들의 전화번호 목록 조회
            phone_query = """
            SELECT DISTINCT phone 
            FROM patient 
            WHERE name LIKE %s AND phone IS NOT NULL AND phone != ''
            """
            cursor.execute(phone_query, (f"%{search_name}%",))
            phone_results = cursor.fetchall()
            phone_numbers = [row[0] for row in phone_results if row[0]]
            
            # 2단계: 같은 이름 또는 같은 전화번호를 가진 모든 환자 조회
            if phone_numbers:
                # 전화번호가 있는 경우: 이름이 일치하거나 전화번호가 일치하는 모든 환자
                placeholders = ','.join(['%s'] * len(phone_numbers))
                sql = f"""
                SELECT p.patient_id, p.name, p.age, p.disease, p.severity, p.treatment_cost, 
                       p.total_cost, p.priority, p.ranks, p.admission_date, h.hospitalname,
                       p.gender, p.phone
                FROM patient p 
                LEFT JOIN hospital h ON p.hospitalcode = h.hospitalcode
                WHERE (p.name LIKE %s) OR (p.phone IN ({placeholders}) AND p.phone IS NOT NULL AND p.phone != '')
                ORDER BY p.name, p.ranks
                """
                params = [f"%{search_name}%"] + phone_numbers
            else:
                # 전화번호가 없는 경우: 이름만으로 검색
                sql = """
                SELECT p.patient_id, p.name, p.age, p.disease, p.severity, p.treatment_cost, 
                       p.total_cost, p.priority, p.ranks, p.admission_date, h.hospitalname,
                       p.gender, p.phone
                FROM patient p 
                LEFT JOIN hospital h ON p.hospitalcode = h.hospitalcode
                WHERE p.name LIKE %s
                ORDER BY p.name, p.ranks
                """
            
            cursor.execute(sql, params)
            
            columns = ["id", "name", "age", "disease", "severity", "treatment_cost", 
                      "total_cost", "priority", "rank", "admission_date", "hospital_name",
                      "gender", "phone"]
            
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            
            return results
        except Exception as e:
            print(f"[ERROR] 환자 검색 실패: {e}")
            return []
    
    def select_all_hospitals(self) -> List[Dict[str, Any]]:
        """모든 병원 데이터 조회"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT hospitalname, address, hospitalcode, patientcount, speciality FROM hospital ORDER BY hospitalname"
            cursor.execute(sql)
            
            columns = ["name", "address", "code", "patient_count", "speciality"]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            
            return results
        except Exception as e:
            print(f"[ERROR] 병원 데이터 조회 실패: {e}")
            return []
    
    def get_hospital_severity_stats(self) -> List[Dict[str, Any]]:
        """병원별 중증도별 환자 수 조회"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
            SELECT 
                h.hospitalname,
                h.address,
                h.hospitalcode,
                h.speciality,
                COUNT(CASE WHEN p.severity = 1 THEN 1 END) as mild_count,
                COUNT(CASE WHEN p.severity = 2 THEN 1 END) as moderate_count,
                COUNT(CASE WHEN p.severity = 3 THEN 1 END) as severe_count,
                COUNT(p.patient_id) as total_count
            FROM hospital h
            LEFT JOIN patient p ON h.hospitalcode = p.hospitalcode
            GROUP BY h.hospitalcode, h.hospitalname, h.address, h.speciality
            ORDER BY total_count DESC, h.hospitalname
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            hospitals = []
            for row in results:
                hospitals.append({
                    'name': row[0],
                    'address': row[1],
                    'code': row[2],
                    'speciality': row[3],
                    'mild_count': row[4],      # 경증
                    'moderate_count': row[5],  # 중등도
                    'severe_count': row[6],    # 중증
                    'total_count': row[7]      # 총합
                })
            
            cursor.close()
            conn.close()
            
            return hospitals
            
        except Exception as e:
            print(f"[ERROR] 병원별 중증도 통계 조회 실패: {e}")
            return []
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """대시보드용 통계 데이터"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 전체 환자 수
            cursor.execute("SELECT COUNT(*) FROM patient")
            total_patients = cursor.fetchone()[0]
            
            # 높은 우선순위 환자 수
            cursor.execute("SELECT COUNT(*) FROM patient WHERE priority = '높음'")
            high_priority = cursor.fetchone()[0]
            
            # 총 진료비
            cursor.execute("SELECT SUM(total_cost) FROM patient")
            total_cost = cursor.fetchone()[0] or 0
            
            # 병원 수
            cursor.execute("SELECT COUNT(*) FROM hospital")
            hospital_count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return {
                'total_patients': total_patients,
                'high_priority': high_priority,
                'total_cost': int(total_cost),
                'hospital_count': hospital_count
            }
        except Exception as e:
            print(f"[ERROR] 대시보드 통계 조회 실패: {e}")
            return {
                'total_patients': 0,
                'high_priority': 0,
                'total_cost': 0,
                'hospital_count': 0
            }
    
    def get_hospital_stats_for_dashboard(self) -> List[Dict[str, Any]]:
        """대시보드용 병원별 통계 (Top 10 환자 기준)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Top 10 환자들의 병원별 분포
            sql = """
            SELECT h.hospitalname, h.address, h.speciality, COUNT(p.patient_id) as patient_count
            FROM hospital h
            LEFT JOIN patient p ON h.hospitalcode = p.hospitalcode AND p.ranks <= 10
            GROUP BY h.hospitalcode, h.hospitalname, h.address, h.speciality
            HAVING COUNT(p.patient_id) > 0
            ORDER BY patient_count DESC
            """
            cursor.execute(sql)
            
            columns = ["name", "address", "speciality", "patient_count"]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            
            return results
        except Exception as e:
            print(f"[ERROR] 병원 통계 조회 실패: {e}")
            return []

# 전역 데이터베이스 매니저
db_manager = WebDatabaseManager()

@app.route('/')
def dashboard():
    """메인 대시보드"""
    try:
        stats = db_manager.get_dashboard_stats()
        patients = db_manager.select_all_patients()[:10]  # 상위 10명만
        hospital_stats = db_manager.get_hospital_stats_for_dashboard()  # 병원별 통계
        
        return render_template('dashboard.html', 
                             stats=stats, 
                             patients=patients,
                             hospital_stats=hospital_stats,
                             current_time=datetime.now().strftime('%Y. %m. %d. %H:%M:%S'))
    except Exception as e:
        flash(f'대시보드 로드 중 오류가 발생했습니다: {e}', 'error')
        return render_template('dashboard.html', 
                             stats={'total_patients': 0, 'high_priority': 0, 'total_cost': 0, 'hospital_count': 0},
                             patients=[],
                             hospital_stats=[])

@app.route('/patients')
def list_patients():
    """환자 목록 페이지 (검색 기능 포함)"""
    try:
        search_name = request.args.get('search_name', '').strip()
        
        if search_name:
            # 검색어가 있는 경우: 이름으로 검색
            patients = db_manager.search_patients_by_name(search_name)
            if not patients:
                flash(f'"{search_name}"에 대한 검색 결과가 없습니다.', 'info')
        else:
            # 검색어가 없는 경우: 전체 목록
            patients = db_manager.select_all_patients()
        
        return render_template('patients.html', patients=patients)
    except Exception as e:
        flash(f'환자 목록 조회 중 오류가 발생했습니다: {e}', 'error')
        return render_template('patients.html', patients=[])

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    """환자 등록"""
    if request.method == 'GET':
        hospitals = db_manager.select_all_hospitals()
        diseases = ["감기", "독감", "폐렴", "고혈압", "당뇨", "심장병", "암", "골절", "기타"]
        return render_template('add_patient.html', hospitals=hospitals, diseases=diseases)
    
    try:
        name = request.form['name'].strip()
        age = int(request.form['age'])
        disease = request.form['disease']
        severity = int(request.form['severity'])
        gender = request.form.get('gender', '')
        phone = request.form.get('phone', '').strip()
        hospital_code = request.form.get('hospital_code')
        
        if not name:
            flash('환자 이름을 입력해주세요.', 'error')
            return redirect(url_for('add_patient'))
        
        if age < 0 or age > 150:
            flash('올바른 나이를 입력해주세요.', 'error')
            return redirect(url_for('add_patient'))
        
        patient = Patient(name=name, age=age, disease=disease, severity=severity, 
                         gender=gender, phone=phone)
        
        if db_manager.insert_patient_proc(patient, hospital_code):
            db_manager.update_ranks_proc()  # 우선순위 업데이트
            flash(f'{name} 환자가 성공적으로 등록되었습니다!', 'success')
        else:
            flash('환자 등록에 실패했습니다.', 'error')
        
        return redirect(url_for('list_patients'))
        
    except ValueError:
        flash('입력 형식이 올바르지 않습니다.', 'error')
        return redirect(url_for('add_patient'))
    except Exception as e:
        flash(f'환자 등록 중 오류가 발생했습니다: {e}', 'error')
        return redirect(url_for('add_patient'))

@app.route('/patients/<int:patient_id>/edit', methods=['GET', 'POST'])
def edit_patient(patient_id):
    """환자 수정"""
    if request.method == 'GET':
        patients = db_manager.select_all_patients()
        patient_data = next((p for p in patients if p['id'] == patient_id), None)
        
        if not patient_data:
            flash('환자를 찾을 수 없습니다.', 'error')
            return redirect(url_for('list_patients'))
        
        hospitals = db_manager.select_all_hospitals()
        diseases = ["감기", "독감", "폐렴", "고혈압", "당뇨", "심장병", "암", "골절", "기타"]
        return render_template('edit_patient.html', 
                             patient=patient_data, 
                             hospitals=hospitals, 
                             diseases=diseases)
    
    try:
        name = request.form['name'].strip()
        age = int(request.form['age'])
        disease = request.form['disease']
        severity = int(request.form['severity'])
        gender = request.form.get('gender', '')
        phone = request.form.get('phone', '').strip()
        
        patient = Patient(id=patient_id, name=name, age=age, disease=disease, 
                         severity=severity, gender=gender, phone=phone)
        
        if db_manager.update_patient_proc(patient):
            db_manager.update_ranks_proc()  # 우선순위 업데이트
            flash(f'{name} 환자 정보가 성공적으로 수정되었습니다!', 'success')
        else:
            flash('환자 정보 수정에 실패했습니다.', 'error')
        
        return redirect(url_for('list_patients'))
        
    except ValueError:
        flash('입력 형식이 올바르지 않습니다.', 'error')
        return redirect(url_for('edit_patient', patient_id=patient_id))
    except Exception as e:
        flash(f'환자 수정 중 오류가 발생했습니다: {e}', 'error')
        return redirect(url_for('edit_patient', patient_id=patient_id))

@app.route('/patients/<int:patient_id>/delete', methods=['POST'])
def delete_patient(patient_id):
    """환자 삭제"""
    try:
        if db_manager.delete_patient_proc(patient_id):
            db_manager.update_ranks_proc()  # 우선순위 업데이트
            flash('환자가 성공적으로 삭제되었습니다.', 'success')
        else:
            flash('환자 삭제에 실패했습니다.', 'error')
    except Exception as e:
        flash(f'환자 삭제 중 오류가 발생했습니다: {e}', 'error')
    
    return redirect(url_for('list_patients'))

@app.route('/hospitals')
def list_hospitals():
    """병원 현황 (중증도별 환자 수 포함)"""
    try:
        hospitals = db_manager.get_hospital_severity_stats()
        return render_template('hospitals.html', hospitals=hospitals)
    except Exception as e:
        flash(f'병원 목록 조회 중 오류가 발생했습니다: {e}', 'error')
        return render_template('hospitals.html', hospitals=[])

@app.route('/api/update_ranks', methods=['POST'])
def update_ranks():
    """우선순위 업데이트 API"""
    try:
        if db_manager.update_ranks_proc():
            return jsonify({'success': True, 'message': '우선순위가 성공적으로 업데이트되었습니다.'})
        else:
            return jsonify({'success': False, 'message': '우선순위 업데이트에 실패했습니다.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {e}'})

@app.route('/api/dashboard_stats')
def api_dashboard_stats():
    """대시보드 통계 API"""
    try:
        stats = db_manager.get_dashboard_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/db-info')
def db_info():
    """데이터베이스 정보 페이지"""
    try:
        db_info_data = {
            'host': db_manager.host,
            'port': 3306,
            'user': db_manager.user,
            'password': db_manager.password,
            'database': db_manager.db_name
        }
        
        return render_template('db_info.html', 
                             db_info=db_info_data,
                             current_time=datetime.now().strftime('%Y. %m. %d. %H:%M:%S'))
    except Exception as e:
        flash(f'데이터베이스 정보 로드 중 오류가 발생했습니다: {e}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/api/test_db_connection', methods=['POST'])
def test_db_connection():
    """데이터베이스 연결 테스트 API"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'message': '데이터베이스 연결이 성공적으로 확인되었습니다.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'연결 실패: {str(e)}'})

@app.route('/api/table_data/<table_name>')
def get_table_data(table_name):
    """테이블 데이터 조회 API"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # 허용된 테이블만 조회
        allowed_tables = ['patient', 'hospital', 'items', 'students']
        if table_name not in allowed_tables:
            return jsonify({'success': False, 'message': '허용되지 않은 테이블입니다.'})
        
        # 테이블 데이터 조회
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        rows = cursor.fetchall()
        
        # 컬럼 정보 가져오기
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [row[0] for row in cursor.fetchall()]
        
        # 데이터를 딕셔너리 형태로 변환
        data = []
        for row in rows:
            row_dict = {}
            for i, col in enumerate(columns):
                value = row[i]
                if value is None:
                    row_dict[col] = ""
                else:
                    row_dict[col] = str(value)
            data.append(row_dict)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': data,
            'columns': columns,
            'count': len(data)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'데이터 조회 실패: {str(e)}'})

@app.route('/api/table_stats')
def get_table_stats():
    """테이블별 레코드 수 조회 API"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        tables = ['patient', 'hospital', 'items', 'students']
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                stats[table] = count
            except:
                stats[table] = 0
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'통계 조회 실패: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
