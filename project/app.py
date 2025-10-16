from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder="static")

# 원소 데이터 (일부 예시, 실제로는 전체 주기율표를 넣을 수 있음)
elements_dict = {
    "H": {"name": "수소", "group": 1, "period": 1},
    "He": {"name": "헬륨", "group": 18, "period": 1},
    "Li": {"name": "리튬", "group": 1, "period": 2},
    "Be": {"name": "베릴륨", "group": 2, "period": 2},
    "B": {"name": "붕소", "group": 13, "period": 2},
    "C": {"name": "탄소", "group": 14, "period": 2},
    "N": {"name": "질소", "group": 15, "period": 2},
    "O": {"name": "산소", "group": 16, "period": 2},
    "F": {"name": "플루오린", "group": 17, "period": 2},
    "Ne": {"name": "네온", "group": 18, "period": 2},
    "Na": {"name": "나트륨", "group": 1, "period": 3},
    "Mg": {"name": "마그네슘", "group": 2, "period": 3},
    "Al": {"name": "알루미늄", "group": 13, "period": 3},
    "Si": {"name": "규소", "group": 14, "period": 3},
    "P": {"name": "인", "group": 15, "period": 3},
    "S": {"name": "황", "group": 16, "period": 3},
    "Cl": {"name": "염소", "group": 17, "period": 3},
    "Ar": {"name": "아르곤", "group": 18, "period": 3},
    "K": {"name": "칼륨", "group": 1, "period": 4},
    "Ca": {"name": "칼슘", "group": 2, "period": 4},
    "Sc": {"name": "스칸듐", "group": 3, "period": 4},
    "Ti": {"name": "타이타늄", "group": 4, "period": 4},
    "V": {"name": "바나듐", "group": 5, "period": 4},
    "Cr": {"name": "크로뮴", "group": 6, "period": 4},
    "Mn": {"name": "망가니즈", "group": 7, "period": 4},
    "Fe": {"name": "철", "group": 8, "period": 4},
    "Co": {"name": "코발트", "group": 9, "period": 4},
    "Ni": {"name": "니켈", "group": 10, "period": 4},
    "Cu": {"name": "구리", "group": 11, "period": 4},
    "Zn": {"name": "아연", "group": 12, "period": 4},
    "Ga": {"name": "갈륨", "group": 13, "period": 4},
    "Ge": {"name": "저마늄", "group": 14, "period": 4},
    "As": {"name": "비소", "group": 15, "period": 4},
    "Se": {"name": "셀레늄", "group": 16, "period": 4},
    "Br": {"name": "브로민", "group": 17, "period": 4},
    "Kr": {"name": "크립톤", "group": 18, "period": 4},
    "Rb": {"name": "루비듐", "group": 1, "period": 5},
    "Sr": {"name": "스트론튬", "group": 2, "period": 5},
    "Y": {"name": "이트륨", "group": 3, "period": 5},
    "Zr": {"name": "지르코늄", "group": 4, "period": 5},
    "Nb": {"name": "나이오븀", "group": 5, "period": 5},
    "Mo": {"name": "몰리브데넘", "group": 6, "period": 5},
    "Tc": {"name": "테크네튬", "group": 7, "period": 5},
    "Ru": {"name": "루테늄", "group": 8, "period": 5},
    "Rh": {"name": "로듐", "group": 9, "period": 5},
    "Pd": {"name": "팔라듐", "group": 10, "period": 5},
    "Ag": {"name": "은", "group": 11, "period": 5},
    "Cd": {"name": "카드뮴", "group": 12, "period": 5},
    "In": {"name": "인듐", "group": 13, "period": 5},
    "Sn": {"name": "주석", "group": 14, "period": 5},
    "Sb": {"name": "안티모니", "group": 15, "period": 5},
    "Te": {"name": "텔루륨", "group": 16, "period": 5},
    "I": {"name": "아이오딘", "group": 17, "period": 5},
    "Xe": {"name": "제논", "group": 18, "period": 5},
    "Cs": {"name": "세슘", "group": 1, "period": 6},
    "Ba": {"name": "바륨", "group": 2, "period": 6},
    "La": {"name": "란타넘", "group": 3, "period": 6},
    "Ce": {"name": "세륨", "group": 3, "period": 6},
    "Pr": {"name": "프라세오디뮴", "group": 3, "period": 6},
    "Nd": {"name": "네오디뮴", "group": 3, "period": 6},
    "Pm": {"name": "프로메튬", "group": 3, "period": 6},
    "Sm": {"name": "사마륨", "group": 3, "period": 6},
    "Eu": {"name": "유로퓸", "group": 3, "period": 6},
    "Gd": {"name": "가돌리늄", "group": 3, "period": 6},
    "Tb": {"name": "터븀", "group": 3, "period": 6},
    "Dy": {"name": "디스프로슘", "group": 3, "period": 6},
    "Ho": {"name": "홀뮴", "group": 3, "period": 6},
    "Er": {"name": "어븀", "group": 3, "period": 6},
    "Tm": {"name": "툴륨", "group": 3, "period": 6},
    "Yb": {"name": "이터븀", "group": 3, "period": 6},
    "Lu": {"name": "루테튬", "group": 3, "period": 6},
    "Hf": {"name": "하프늄", "group": 4, "period": 6},
    "Ta": {"name": "탄탈럼", "group": 5, "period": 6},
    "W": {"name": "텅스텐", "group": 6, "period": 6},
    "Re": {"name": "레늄", "group": 7, "period": 6},
    "Os": {"name": "오스뮴", "group": 8, "period": 6},
    "Ir": {"name": "이리듐", "group": 9, "period": 6},
    "Pt": {"name": "백금", "group": 10, "period": 6},
    "Au": {"name": "금", "group": 11, "period": 6},
    "Hg": {"name": "수은", "group": 12, "period": 6},
    "Tl": {"name": "탈륨", "group": 13, "period": 6},
    "Pb": {"name": "납", "group": 14, "period": 6},
    "Bi": {"name": "비스무트", "group": 15, "period": 6},
    "Po": {"name": "폴로늄", "group": 16, "period": 6},
    "At": {"name": "아스타틴", "group": 17, "period": 6},
    "Rn": {"name": "라돈", "group": 18, "period": 6},
    "Fr": {"name": "프랑슘", "group": 1, "period": 7},
    "Ra": {"name": "라듐", "group": 2, "period": 7},
    "Ac": {"name": "악티늄", "group": 3, "period": 7},
    "Th": {"name": "토륨", "group": 3, "period": 7},
    "Pa": {"name": "프로트악티늄", "group": 3, "period": 7},
    "U": {"name": "우라늄", "group": 3, "period": 7},
    "Np": {"name": "넵투늄", "group": 3, "period": 7},
    "Pu": {"name": "플루토늄", "group": 3, "period": 7},
    "Am": {"name": "아메리슘", "group": 3, "period": 7},
    "Cm": {"name": "퀴륨", "group": 3, "period": 7},
    "Bk": {"name": "버클륨", "group": 3, "period": 7},
    "Cf": {"name": "캘리포늄", "group": 3, "period": 7},
    "Es": {"name": "아인슈타이늄", "group": 3, "period": 7},
    "Fm": {"name": "페르뮴", "group": 3, "period": 7},
    "Md": {"name": "멘델레븀", "group": 3, "period": 7},
    "No": {"name": "노벨륨", "group": 3, "period": 7},
    "Lr": {"name": "로렌슘", "group": 3, "period": 7},
    "Rf": {"name": "러더포듐", "group": 4, "period": 7},
    "Db": {"name": "더브늄", "group": 5, "period": 7},
    "Sg": {"name": "시보귬", "group": 6, "period": 7},
    "Bh": {"name": "보륨", "group": 7, "period": 7},
    "Hs": {"name": "하슘", "group": 8, "period": 7},
    "Mt": {"name": "마이트너륨", "group": 9, "period": 7},
    "Ds": {"name": "다름슈타튬", "group": 10, "period": 7},
    "Rg": {"name": "뢴트게늄", "group": 11, "period": 7},
    "Cn": {"name": "코페르니슘", "group": 12, "period": 7},
    "Nh": {"name": "니호늄", "group": 13, "period": 7},
    "Fl": {"name": "플레로븀", "group": 14, "period": 7},
    "Mc": {"name": "모스코븀", "group": 15, "period": 7},
    "Lv": {"name": "리버모륨", "group": 16, "period": 7},
    "Ts": {"name": "테네신", "group": 17, "period": 7},
    "Og": {"name": "오가네손", "group": 18, "period": 7}
}



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search")
def search_element():
    symbol = request.args.get("symbol", "").strip()
    group = request.args.get("group", "").strip()
    period = request.args.get("period", "").strip()

    results = []

    # 1️⃣ 원소 기호 검색
    if symbol:
        symbol = symbol.capitalize()  # 예: 'fe' -> 'Fe'
        if symbol in elements_dict:
            info = elements_dict[symbol]
            return jsonify({
                "symbol": symbol,
                "name": info["name"],
                "group": info["group"],
                "period": info["period"]
            })
        else:
            return jsonify({"error": f"'{symbol}'은(는) 알 수 없는 원소입니다."}), 404

    # 2️⃣ 족/주기 검색
    for s, info in elements_dict.items():
        if (not group or str(info["group"]) == group) and (not period or str(info["period"]) == period):
            results.append({
                "symbol": s,
                "name": info["name"],
                "group": info["group"],
                "period": info["period"]
            })

    if results:
        return jsonify(results)
    else:
        return jsonify({"error": "조건에 맞는 원소가 없습니다."}), 404


if __name__ == "__main__":
    app.run(debug=True)