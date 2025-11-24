from flask import Flask, render_template, request, jsonify

# 원소 데이터 (전자 껍질 배치 정보 추가 - 보어 모델 기준)
# 껍질 순서: K, L, M, N, O, P, Q (1, 2, 3, 4, 5, 6, 7 주기)
elements_dict = {
    # 1주기
    "H": {"name": "수소", "group": 1, "period": 1, "type": "nonmetal", "electron_shells": [1]},
    "He": {"name": "헬륨", "group": 18, "period": 1, "type": "noble-gas", "electron_shells": [2]},
    # 2주기
    "Li": {"name": "리튬", "group": 1, "period": 2, "type": "alkali-metal", "electron_shells": [2, 1]},
    "Be": {"name": "베릴륨", "group": 2, "period": 2, "type": "alkaline-earth-metal", "electron_shells": [2, 2]},
    "B": {"name": "붕소", "group": 13, "period": 2, "type": "metalloid", "electron_shells": [2, 3]},
    "C": {"name": "탄소", "group": 14, "period": 2, "type": "nonmetal", "electron_shells": [2, 4]},
    "N": {"name": "질소", "group": 15, "period": 2, "type": "nonmetal", "electron_shells": [2, 5]},
    "O": {"name": "산소", "group": 16, "period": 2, "type": "nonmetal", "electron_shells": [2, 6]},
    "F": {"name": "플루오린", "group": 17, "period": 2, "type": "halogen", "electron_shells": [2, 7]},
    "Ne": {"name": "네온", "group": 18, "period": 2, "type": "noble-gas", "electron_shells": [2, 8]},
    # 3주기
    "Na": {"name": "나트륨", "group": 1, "period": 3, "type": "alkali-metal", "electron_shells": [2, 8, 1]},
    "Mg": {"name": "마그네슘", "group": 2, "period": 3, "type": "alkaline-earth-metal", "electron_shells": [2, 8, 2]},
    "Al": {"name": "알루미늄", "group": 13, "period": 3, "type": "post-transition-metal", "electron_shells": [2, 8, 3]},
    "Si": {"name": "규소", "group": 14, "period": 3, "type": "metalloid", "electron_shells": [2, 8, 4]},
    "P": {"name": "인", "group": 15, "period": 3, "type": "nonmetal", "electron_shells": [2, 8, 5]},
    "S": {"name": "황", "group": 16, "period": 3, "type": "nonmetal", "electron_shells": [2, 8, 6]},
    "Cl": {"name": "염소", "group": 17, "period": 3, "type": "halogen", "electron_shells": [2, 8, 7]},
    "Ar": {"name": "아르곤", "group": 18, "period": 3, "type": "noble-gas", "electron_shells": [2, 8, 8]},
    # 4주기 (전이 금속 구간은 단순 보어 모형을 위해 최외각 전자만 고려하여 단순화함)
    "K": {"name": "칼륨", "group": 1, "period": 4, "type": "alkali-metal", "electron_shells": [2, 8, 8, 1]},
    "Ca": {"name": "칼슘", "group": 2, "period": 4, "type": "alkaline-earth-metal", "electron_shells": [2, 8, 8, 2]},
    "Sc": {"name": "스칸듐", "group": 3, "period": 4, "type": "transition-metal", "electron_shells": [2, 8, 9, 2]},
    "Ti": {"name": "타이타늄", "group": 4, "period": 4, "type": "transition-metal", "electron_shells": [2, 8, 10, 2]},
    "V": {"name": "바나듐", "group": 5, "period": 4, "type": "transition-metal", "electron_shells": [2, 8, 11, 2]},
    "Cr": {"name": "크로뮴", "group": 6, "period": 4, "type": "transition-metal", "electron_shells": [2, 8, 13, 1]},
    "Mn": {"name": "망가니즈", "group": 7, "period": 4, "type": "transition-metal", "electron_shells": [2, 8, 13, 2]},
    "Fe": {"name": "철", "group": 8, "period": 4, "type": "transition-metal", "electron_shells": [2, 8, 14, 2]},
    "Co": {"name": "코발트", "group": 9, "period": 4, "type": "transition-metal", "electron_shells": [2, 8, 15, 2]},
    "Ni": {"name": "니켈", "group": 10, "period": 4, "type": "transition-metal", "electron_shells": [2, 8, 16, 2]},
    "Cu": {"name": "구리", "group": 11, "period": 4, "type": "transition-metal", "electron_shells": [2, 8, 18, 1]},
    "Zn": {"name": "아연", "group": 12, "period": 4, "type": "transition-metal", "electron_shells": [2, 8, 18, 2]},
    "Ga": {"name": "갈륨", "group": 13, "period": 4, "type": "post-transition-metal", "electron_shells": [2, 8, 18, 3]},
    "Ge": {"name": "저마늄", "group": 14, "period": 4, "type": "metalloid", "electron_shells": [2, 8, 18, 4]},
    "As": {"name": "비소", "group": 15, "period": 4, "type": "metalloid", "electron_shells": [2, 8, 18, 5]},
    "Se": {"name": "셀레늄", "group": 16, "period": 4, "type": "nonmetal", "electron_shells": [2, 8, 18, 6]},
    "Br": {"name": "브로민", "group": 17, "period": 4, "type": "halogen", "electron_shells": [2, 8, 18, 7]},
    "Kr": {"name": "크립톤", "group": 18, "period": 4, "type": "noble-gas", "electron_shells": [2, 8, 18, 8]},
    # 5~7주기 (HTML에 포함된 원소만 일부 추가)
    "Rb": {"name": "루비듐", "group": 1, "period": 5, "type": "alkali-metal", "electron_shells": [2, 8, 18, 8, 1]},
    "Sr": {"name": "스트론튬", "group": 2, "period": 5, "type": "alkaline-earth-metal", "electron_shells": [2, 8, 18, 8, 2]},
    "Cs": {"name": "세슘", "group": 1, "period": 6, "type": "alkali-metal", "electron_shells": [2, 8, 18, 18, 8, 1]},
    "Ba": {"name": "바륨", "group": 2, "period": 6, "type": "alkaline-earth-metal", "electron_shells": [2, 8, 18, 18, 8, 2]},
    "La": {"name": "란타넘", "group": 3, "period": 6, "type": "lanthanide", "electron_shells": [2, 8, 18, 18, 9, 2]},
    "Fr": {"name": "프랑슘", "group": 1, "period": 7, "type": "alkali-metal", "electron_shells": [2, 8, 18, 32, 18, 8, 1]},
    "Ra": {"name": "라듐", "group": 2, "period": 7, "type": "alkaline-earth-metal", "electron_shells": [2, 8, 18, 32, 18, 8, 2]},
    "Ac": {"name": "악티늄", "group": 3, "period": 7, "type": "actinide", "electron_shells": [2, 8, 18, 32, 18, 9, 2]},
    "Og": {"name": "오가네손", "group": 18, "period": 7, "type": "noble-gas", "electron_shells": [2, 8, 18, 32, 32, 18, 8]}
}

# 원소 기호 목록을 기반으로 원자 번호를 할당합니다.
# 원소 기호 순서대로 원자 번호가 증가한다고 가정합니다.
all_symbols = list(elements_dict.keys())
for i, symbol in enumerate(all_symbols, 1):
    elements_dict[symbol]['number'] = i

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    # 템플릿 폴더에 index.html을 저장해야 합니다.
    return render_template("index.html")

# 특정 원소 기호에 대한 상세 정보를 반환하는 API 엔드포인트
@app.route("/api/element/<symbol>")
def get_element_data(symbol):
    symbol_upper = symbol.capitalize()
    
    if symbol_upper in elements_dict:
        # 전이 금속 등은 실제 복잡한 전자 배치 규칙을 따르지만, 
        # 여기서는 시뮬레이션에 필요한 껍질별 개수만 반환합니다.
        data = elements_dict[symbol_upper]
        
        # 원소의 총 전자 개수 (원자 번호)를 계산
        total_electrons = sum(data['electron_shells'])
        
        return jsonify({
            "symbol": symbol_upper,
            "name": data["name"],
            "group": data["group"],
            "period": data["period"],
            "electron_shells": data["electron_shells"],
            "total_electrons": total_electrons # 핵의 양성자 수로 사용됨
        })
    else:
        return jsonify({"error": f"'{symbol}'에 대한 데이터가 없습니다."}), 404

# 검색 기능 API는 이전과 동일하게 유지합니다.
@app.route("/api/search")
def search_element():
    symbol = request.args.get("symbol", "").strip()
    group = request.args.get("group", "").strip()
    period = request.args.get("period", "").strip()

    results = []
    
    # 1️⃣ 원소 기호 검색
    if symbol:
        symbol = symbol.capitalize()
        if symbol in elements_dict:
            info = elements_dict[symbol]
            results.append({
                "symbol": symbol,
                "name": info["name"],
                "group": info["group"],
                "period": info["period"]
            })
            return jsonify(results)
        else:
            return jsonify({"error": f"'{symbol}'은(는) 알 수 없는 원소입니다."}), 404

    # 2️⃣ 족/주기 검색
    for s, info in elements_dict.items():
        if (not group or str(info["group"]) == group) and (not period or str(info["period"]) == period):
            # 'type' 속성을 추가하여 검색 결과를 하이라이트할 때 사용할 수 있도록 합니다.
            results.append({
                "symbol": s,
                "name": info["name"],
                "group": info["group"],
                "period": info["period"],
                "type": info.get("type", "unknown")
            })

    if results:
        return jsonify(results)
    else:
        return jsonify({"error": "조건에 맞는 원소가 없습니다."}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)
