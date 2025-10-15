// 건양대학교병원 환자관리시스템 - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 페이지 로드 애니메이션
    document.body.classList.add('fade-in');
    
    // 현재 시간 업데이트
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
    
    // 툴팁 초기화
    initializeTooltips();
    
    // 폼 유효성 검사
    initializeFormValidation();
    
    // 테이블 정렬 기능
    initializeTableSorting();
    
    // 검색 기능
    initializeSearch();
    
    // 알림 자동 숨김
    initializeAlerts();
    
    console.log('건양대학교병원 환자관리시스템 초기화 완료');
});

// 현재 시간 업데이트
function updateCurrentTime() {
    const timeElements = document.querySelectorAll('.current-time');
    const now = new Date();
    const timeString = now.toLocaleString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    timeElements.forEach(element => {
        element.textContent = timeString;
    });
}

// 툴팁 초기화
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// 폼 유효성 검사
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// 테이블 정렬 기능
function initializeTableSorting() {
    const tables = document.querySelectorAll('table.sortable');
    
    tables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sort]');
        
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.innerHTML += ' <i class="bi bi-arrow-down-up ms-1"></i>';
            
            header.addEventListener('click', function() {
                const column = this.dataset.sort;
                const isNumeric = this.dataset.type === 'number';
                sortTable(table, column, isNumeric);
            });
        });
    });
}

// 테이블 정렬 실행
function sortTable(table, column, isNumeric = false) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aValue = a.querySelector(`td:nth-child(${getColumnIndex(table, column)})`).textContent.trim();
        const bValue = b.querySelector(`td:nth-child(${getColumnIndex(table, column)})`).textContent.trim();
        
        if (isNumeric) {
            return parseFloat(aValue) - parseFloat(bValue);
        } else {
            return aValue.localeCompare(bValue, 'ko-KR');
        }
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// 컬럼 인덱스 찾기
function getColumnIndex(table, column) {
    const headers = table.querySelectorAll('th');
    for (let i = 0; i < headers.length; i++) {
        if (headers[i].dataset.sort === column) {
            return i + 1;
        }
    }
    return 1;
}

// 검색 기능
function initializeSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const targetTable = document.querySelector(this.dataset.target);
            
            if (targetTable) {
                filterTable(targetTable, searchTerm);
            }
        });
    });
}

// 테이블 필터링
function filterTable(table, searchTerm) {
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// 알림 자동 숨김
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // 5초 후 자동 숨김
    });
}

// 우선순위 업데이트 (대시보드용)
function updateRanks() {
    const button = event.target;
    const originalText = button.innerHTML;
    
    // 로딩 상태 표시
    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> 업데이트 중...';
    
    fetch('/api/update_ranks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('우선순위가 성공적으로 업데이트되었습니다.', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification('우선순위 업데이트에 실패했습니다: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('오류가 발생했습니다.', 'error');
    })
    .finally(() => {
        // 로딩 상태 해제
        button.disabled = false;
        button.innerHTML = originalText;
    });
}

// 알림 표시
function showNotification(message, type = 'info') {
    const alertClass = type === 'error' ? 'alert-danger' : 
                      type === 'success' ? 'alert-success' : 
                      'alert-info';
    
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="bi bi-${type === 'error' ? 'exclamation-triangle' : 'check-circle'}"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('.container-fluid');
    container.insertAdjacentHTML('afterbegin', alertHtml);
    
    // 5초 후 자동 제거
    setTimeout(() => {
        const alert = container.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

// 환자 삭제 확인
function confirmDelete(patientId, patientName) {
    return confirm(`${patientName} 환자를 정말 삭제하시겠습니까?\n\n이 작업은 되돌릴 수 없습니다.`);
}

// 숫자 포맷팅 (천 단위 구분)
function formatNumber(num) {
    return new Intl.NumberFormat('ko-KR').format(num);
}

// 날짜 포맷팅
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

// 중증도별 색상 반환
function getSeverityColor(severity) {
    switch(severity) {
        case 1: return 'success';
        case 2: return 'warning';
        case 3: return 'danger';
        default: return 'secondary';
    }
}

// 우선순위별 색상 반환
function getPriorityColor(priority) {
    switch(priority) {
        case '높음': return 'danger';
        case '중간': return 'warning';
        case '낮음': return 'success';
        default: return 'secondary';
    }
}

// 로컬 스토리지 관리
const Storage = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch(e) {
            console.error('로컬 스토리지 저장 실패:', e);
        }
    },
    
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch(e) {
            console.error('로컬 스토리지 읽기 실패:', e);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
        } catch(e) {
            console.error('로컬 스토리지 삭제 실패:', e);
        }
    }
};

// 페이지 성능 모니터링
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log(`페이지 로드 시간: ${Math.round(loadTime)}ms`);
    
    // 성능 정보 저장 (선택사항)
    Storage.set('lastLoadTime', {
        time: loadTime,
        timestamp: Date.now(),
        page: window.location.pathname
    });
});

// 오류 처리
window.addEventListener('error', function(event) {
    console.error('JavaScript 오류:', event.error);
    
    // 사용자에게 친화적인 오류 메시지 표시
    showNotification('일시적인 오류가 발생했습니다. 페이지를 새로고침해주세요.', 'error');
});

// 네트워크 상태 모니터링
window.addEventListener('online', function() {
    showNotification('네트워크 연결이 복구되었습니다.', 'success');
});

window.addEventListener('offline', function() {
    showNotification('네트워크 연결이 끊어졌습니다.', 'error');
});

// 유틸리티 함수들
const Utils = {
    // 디바운스 함수
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // 쓰로틀 함수
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    },
    
    // 요소가 뷰포트에 있는지 확인
    isInViewport: function(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
};

// 전역 함수로 내보내기 (필요한 경우)
window.KonyangHospital = {
    updateRanks,
    confirmDelete,
    formatNumber,
    formatDate,
    getSeverityColor,
    getPriorityColor,
    showNotification,
    Storage,
    Utils
};
