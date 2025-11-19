// Canvas context 및 애니메이션 변수 설정
const canvas = document.getElementById('atomCanvas');
const ctx = canvas.getContext('2d');
// 캔버스 중앙 위치를 계산합니다.
const center = { x: canvas.width / 2, y: canvas.height / 2 };
const atomInfoDiv = document.getElementById('atom-info');

let currentAtom = null;
let animationFrameId = null;
let electronAngles = []; // 각 껍질의 전자가 현재 위치한 각도를 저장

// 껍질별 반지름 설정 (시각적 균형을 위해 임의로 설정)
const SHELL_RADII = [
    50,  // K (1)
    100, // L (2)
    150, // M (3)
    200, // N (4)
    250, // O (5)
    300, // P (6)
    350  // Q (7)
];

// 1. 원자 모형 그리기 함수
function drawAtom(shellsData, symbol, name) {
    if (!shellsData || shellsData.length === 0) return;

    // 애니메이션 초기화 (이전 애니메이션 중지)
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
    }
    
    // 캔버스 초기화
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 전자의 초기 각도 설정 (시뮬레이션 재시작 시 필요)
    electronAngles = shellsData.map(numElectrons => {
        const angles = [];
        for (let i = 0; i < numElectrons; i++) {
            angles.push(i * (360 / numElectrons)); // 균등하게 초기 배치
        }
        return angles;
    });

    currentAtom = { shellsData, symbol, name };
    
    // 정보 표시 업데이트
    const totalElectrons = shellsData.reduce((sum, count) => sum + count, 0);
    atomInfoDiv.innerHTML = `
        <strong>${symbol} - ${name}</strong><br>
        원자 번호(전자/양성자 수): ${totalElectrons}<br>
        전자 껍질 배치: ${shellsData.join(', ')}
    `;

    // 애니메이션 시작
    animate();
}

// 2. 애니메이션 루프
function animate() {
    // 캔버스 초기화 (이전 프레임 지우기)
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (currentAtom) {
        const { shellsData, symbol } = currentAtom;
        const totalElectrons = shellsData.reduce((sum, count) => sum + count, 0);

        // A. 원자핵 그리기 (양성자 수를 대략적으로 표현)
        const nucleusRadius = 15 + Math.log(totalElectrons + 1) * 2;
        ctx.fillStyle = '#C0392B'; // 핵 색상 (붉은색 계열)
        ctx.beginPath();
        ctx.arc(center.x, center.y, nucleusRadius, 0, Math.PI * 2);
        ctx.fill();
        
        // 핵 내부 텍스트 (원소 기호)
        ctx.fillStyle = 'white';
        ctx.font = 'bold 16px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(symbol, center.x, center.y - 8);
        ctx.font = '12px Arial';
        ctx.fillText(totalElectrons, center.x, center.y + 10); // 원자 번호

        // B. 껍질 및 전자 그리기
        shellsData.forEach((numElectrons, shellIndex) => {
            const radius = SHELL_RADII[shellIndex];
            
            // 껍질 궤도 그리기
            ctx.strokeStyle = '#2980B9'; // 껍질 색상 (푸른색 계열)
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.arc(center.x, center.y, radius, 0, Math.PI * 2);
            ctx.stroke();

            // 전자 그리기 및 각도 업데이트
            if (numElectrons > 0) {
                // 안쪽 껍질이 더 빠르게 회전하도록 속도 조정
                const speed = 1.0 - (shellIndex * 0.1); 

                for (let i = 0; i < numElectrons; i++) {
                    // 각도 업데이트 (회전)
                    electronAngles[shellIndex][i] = (electronAngles[shellIndex][i] + speed) % 360;
                    const angleRad = (electronAngles[shellIndex][i] * Math.PI) / 180;

                    // 전자의 새로운 (x, y) 위치 계산
                    const x = center.x + radius * Math.cos(angleRad);
                    const y = center.y + radius * Math.sin(angleRad);

                    // 전자 그리기
                    ctx.fillStyle = '#27AE60'; // 전자 색상 (초록색 계열)
                    ctx.beginPath();
                    ctx.arc(x, y, 5, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
        });
    }

    // 다음 프레임 요청
    animationFrameId = requestAnimationFrame(animate);
}

// 3. 주기율표 하이라이트 기능 (검색 결과에 따라)
function highlightTable(searchResults) {
    // 기존 하이라이트 제거
    document.querySelectorAll('td').forEach(cell => {
        cell.classList.remove('highlighted');
    });

    if (searchResults.error) return;

    // 검색된 원소 기호 추출
    const resultsArray = Array.isArray(searchResults) ? searchResults : [searchResults];
    const foundSymbols = resultsArray.map(e => e.symbol);

    // 해당하는 셀에 하이라이트 추가
    document.querySelectorAll('td[data-symbol]').forEach(cell => {
        const cellSymbol = cell.getAttribute('data-symbol');
        if (foundSymbols.includes(cellSymbol)) {
            cell.classList.add('highlighted');
        }
    });
}

// 4. 검색 기능
function searchElement() {
    const symbol = document.getElementById("symbolInput").value.trim();
    const group = document.getElementById("groupInput").value.trim();
    const period = document.getElementById("periodInput").value.trim();
    
    // 입력 값 중 하나라도 있어야 검색을 시도합니다.
    if (!symbol && !group && !period) {
        document.getElementById("result").textContent = "❌ 검색 조건을 입력해주세요.";
        return;
    }

    const query = new URLSearchParams({ symbol, group, period });
    const resultBox = document.getElementById("result");

    fetch(`/api/search?${query}`)
        .then(res => {
            if (!res.ok) {
                // 404 에러 등 HTTP 오류 처리
                return res.json().then(data => { throw new Error(data.error || "알 수 없는 오류"); });
            }
            return res.json();
        })
        .then(data => {
            highlightTable(data); // 검색 결과를 주기율표에 하이라이트

            if (data.error) {
                resultBox.textContent = "❌ " + data.error;
                return;
            } 
            
            // 검색 결과 출력
            if (Array.isArray(data)) {
                resultBox.textContent = data
                    .map(e => `${e.symbol} (${e.name}) - ${e.group}족, ${e.period}주기`)
                    .join("\n");
                
                // 다중 검색 결과는 시뮬레이션 대신 메시지 표시
                if (data.length > 1) {
                    if (animationFrameId) cancelAnimationFrame(animationFrameId);
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    atomInfoDiv.textContent = "여러 원소가 검색되었습니다. 단일 원소를 클릭하세요.";
                } else if (data.length === 1) {
                    // 단일 원소 검색 결과일 경우 시뮬레이션 실행
                    const singleSymbol = data[0].symbol;
                    fetch(`/api/element/${singleSymbol}`)
                        .then(resp => resp.json())
                        .then(atomData => {
                            drawAtom(atomData.electron_shells, atomData.symbol, atomData.name);
                        });
                }
            } else {
                // 원소 기호 단일 검색 결과 (app.py의 1️⃣ 검색 로직)
                resultBox.textContent = `${data.symbol} (${data.name}) - ${data.group}족, ${data.period}주기`;
                
                // 단일 원소 상세 정보를 다시 가져와 시뮬레이션 실행
                fetch(`/api/element/${data.symbol}`)
                    .then(resp => resp.json())
                    .then(atomData => {
                         drawAtom(atomData.electron_shells, atomData.symbol, atomData.name);
                    });
            }
        })
        .catch(err => {
            resultBox.textContent = `⚠️ 검색 중 오류가 발생했습니다: ${err.message}`;
            console.error('Fetch Error:', err);
        });
}


// 5. 툴팁 위치 조정 함수
function moveTooltip(e) {
    const tooltip = document.getElementById("tooltip");
    tooltip.style.left = e.clientX + window.scrollX + 10 + "px";
    tooltip.style.top = e.clientY + window.scrollY + 10 + "px";
}

// 6. Canvas 크기 조정 및 초기화 함수
function resizeCanvas() {
    const container = document.querySelector('.simulation-container');
    canvas.width = container.clientWidth;
    canvas.height = container.clientWidth; // 정사각형 유지
    center.x = canvas.width / 2;
    center.y = canvas.height / 2;
    
    // 크기 조정 후 현재 원자 모형을 다시 그립니다.
    if (currentAtom) {
        // drawAtom이 내부에서 animate를 호출하므로 재호출합니다.
        drawAtom(currentAtom.shellsData, currentAtom.symbol, currentAtom.name);
    }
}


document.addEventListener("DOMContentLoaded", () => {
    const tableCells = document.querySelectorAll('td[data-symbol]');
    const searchBtn = document.getElementById("searchBtn");
    const symbolInput = document.getElementById("symbolInput");
    const groupInput = document.getElementById("groupInput");
    const periodInput = document.getElementById("periodInput");
    const tooltip = document.getElementById("tooltip");

    // A. 검색 버튼 및 Enter 키 연결 (사용자 제공 로직)
    if (searchBtn) {
        searchBtn.addEventListener("click", searchElement);
    }
    [symbolInput, groupInput, periodInput].forEach(input => {
        if (input) {
            input.addEventListener("keypress", (e) => {
                if (e.key === "Enter") {
                    searchElement();
                }
            });
        }
    });
    
    // B. 주기율표 셀 클릭 처리 (원자 시뮬레이션 트리거)
    tableCells.forEach(cell => {
        cell.addEventListener('click', function() {
            const symbol = this.getAttribute('data-symbol');
            if (!symbol) return;

            // API 호출: 클릭한 원소의 상세 정보(전자 껍질) 가져오기
            fetch(`/api/element/${symbol}`)
                .then(response => {
                    if (!response.ok) throw new Error('API Error');
                    return response.json();
                })
                .then(data => {
                    // API에서 받은 전자 껍질 배열로 시뮬레이션 시작
                    drawAtom(data.electron_shells, data.symbol, data.name);
                    
                    // 검색 결과 창 클리어 및 하이라이트 제거
                    document.getElementById("result").textContent = '';
                    highlightTable([]);
                })
                .catch(error => {
                    atomInfoDiv.textContent = `오류: ${symbol}의 데이터를 불러올 수 없습니다.`;
                    console.error('Fetch Error:', error);
                });
        });
    });

    // C. 툴팁 기능 (사용자 제공 로직)
    document.querySelectorAll("td").forEach(cell => {
        const symbol = cell.getAttribute('data-symbol');
        if (!symbol) return;

        cell.addEventListener("mouseenter", async (e) => {
            try {
                // API 호출: 단일 원소 정보를 가져와 툴팁에 표시
                const res = await fetch(`/api/element/${symbol}`);
                if (!res.ok) throw new Error();
                const data = await res.json();
                
                if (data.symbol) {
                    tooltip.textContent = `${data.symbol} (${data.name}) - ${data.group}족, ${data.period}주기`;
                } else {
                    tooltip.textContent = "정보 없음";
                }
            } catch {
                tooltip.textContent = "정보 없음";
            }

            tooltip.style.visibility = "visible";
            tooltip.style.opacity = "1";
            moveTooltip(e);
        });

        cell.addEventListener("mousemove", moveTooltip);

        cell.addEventListener("mouseleave", () => {
            tooltip.style.visibility = "hidden";
            tooltip.style.opacity = "0";
        });
    });

    // D. 초기화: Canvas 크기 설정 및 수소(H) 원자 그리기
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas(); // 초기 로드 시 크기 설정
    
    // 초기 화면 로드 시 수소 원자 그리기
    fetch('/api/element/H')
        .then(response => response.json())
        .then(data => {
            drawAtom(data.electron_shells, data.symbol, data.name);
        })
        .catch(e => console.error("Initial H drawing failed:", e));
});