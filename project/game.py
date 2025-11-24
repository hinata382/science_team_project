import random
import sys

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 주기율표 퀴즈 (간단 버전) — 주기(period)와 족(group)을 랜덤으로 제시하고 해당 위치의 원소를 맞추는 게임
# 현재는 첫 20개 원소(주기 1~4 일부)만 포함되어 있습니다. 전체 표로 확장하려면 elements 딕셔너리를 추가하세요.


# (period, group) -> {symbol, name_en, name_ko}
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

def normalize(s):
    return s.strip().lower()

def is_correct(answer, entry, symbol=None):
    a = normalize(answer)
    # check symbol (provided or inferred)
    sym = (symbol or entry.get("symbol") or "").lower()
    if a == sym:
        return True
    # check Korean name (some entries use 'name')
    name_ko = (entry.get("name_ko") or entry.get("name") or "").lower()
    if a == name_ko:
        return True
def play(rounds=None):
    keys = list(elements_dict.keys())
    score = 0
    asked = 0

    print("주기(period)와 족(group)을 보고 원소를 맞추세요.")
    print("입력: 원소 기호 또는 영어/한국어 이름 (종료: q, 힌트: hint)\n")

    while True:
        if rounds is not None and asked >= rounds:
            break

        # pick by symbol key (elements_dict uses symbols as keys)
        symbol = random.choice(keys)
        entry = elements_dict[symbol]
        period = entry.get("period")
        group = entry.get("group")

        prompt = f"[문제 {asked+1}] 주기: {period}, 족: {group} -> 원소는? "
        answer = input(prompt).strip()
        if not answer:
            continue
        if answer.lower() == 'q':
            break
        if answer.lower() == 'hint':
            # 힌트: 기호와 한국어/영어 이름 첫 글자 (가능하면)
            sym = symbol
            name_ko = entry.get("name") or entry.get("name_ko") or ""
            name_en = entry.get("name_en") or ""
            ko_first = name_ko[0] if name_ko else "?"
            en_first = name_en[0] if name_en else "?"
            hint = f"기호: {sym[0]}..., 한국어명 첫글자: {ko_first}, 영어명 첫글자: {en_first}"
            print("힌트:", hint)
            # allow retry without counting as asked
            answer = input("정답을 입력하세요 (종료 q): ").strip()
            if not answer:
                continue
            if answer.lower() == 'q':
                break

        asked += 1
        if is_correct(answer, entry, symbol):
            score += 1
            print("정답!\n")
        else:
            name_ko = entry.get("name") or entry.get("name_ko") or ""
            name_en = entry.get("name_en")
            if name_en:
                print("오답. 정답: {sym} - {ko} ({en})\n".format(
                sym=symbol, ko=name_ko, en=name_en
            ))
            else:
                print("오답. 정답: {sym} - {ko}\n".format(
                    sym=symbol, ko=name_ko
                ))

    print(f"\n게임 종료. 총 {asked}문제 중 {score}문제 정답.")

def main():
    print("간단한 주기율표 퀴즈입니다.")
    try:
        n = input("문제 수를 지정하세요 (엔터=무한, 예: 10): ").strip()
        if n == "":
            rounds = None
        else:
            rounds = int(n)
    except Exception:
        rounds = None

    try:
        play(rounds)
    except KeyboardInterrupt:
        print("\n중단됨.")
        sys.exit(0)

if __name__ == "__main__":
    main()