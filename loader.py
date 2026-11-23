"""Mini NPU Simulator - data.json 로드와 스키마(구조) 검증.

잘못된 항목이 있어도 프로그램을 멈추지 않고, 그 항목만 실패로 표시한다.
"""

import json

from labels import CROSS, X, normalize_label
from matrix import Matrix


def load_json(path):
    """data.json을 읽어 dict로 돌려준다. 문제가 있으면 ValueError(안내 문구)를 발생시킨다."""
    try:
        with open(path, encoding="utf-8-sig") as file:  # utf-8-sig: BOM이 있어도 읽힘
            data = json.load(file)
    except FileNotFoundError:
        raise ValueError(f"파일을 찾을 수 없습니다: {path}") from None
    except UnicodeDecodeError:
        raise ValueError("UTF-8 형식의 파일이 아닙니다.") from None
    except json.JSONDecodeError as error:
        raise ValueError(f"JSON 문법 오류 ({error.lineno}번째 줄): {error.msg}") from None
    except OSError as error:
        raise ValueError(f"파일을 읽을 수 없습니다: {error}") from None

    if not isinstance(data, dict):
        raise ValueError("최상위 구조가 객체({ })가 아닙니다.")
    for key in ("filters", "patterns"):
        if not isinstance(data.get(key), dict):
            raise ValueError(f"'{key}' 항목이 없거나 객체({{ }})가 아닙니다.")
    return data


def size_from_key(key, part_count):
    """'size_13'(part_count=2) 또는 'size_13_2'(part_count=3) 키에서 크기 N=13을 꺼낸다."""
    parts = str(key).split("_")
    if len(parts) != part_count or parts[0] != "size" or not parts[1].isdecimal():
        form = "size_{N}" if part_count == 2 else "size_{N}_{idx}"
        raise ValueError(f"키 형식 오류: '{key}' ({form} 형태여야 합니다)")
    return int(parts[1])


def load_filters(raw_filters):
    """filters 항목을 읽는다.

    반환: ({N: {"Cross": Matrix, "X": Matrix}}, 화면에 보여 줄 로그 목록)
    """
    filters = {}
    logs = []
    for key, group in raw_filters.items():
        try:
            n = size_from_key(key, 2)
            if not isinstance(group, dict):
                raise ValueError("필터 묶음이 객체({ })가 아닙니다.")
            pair = {}
            for raw_label, rows in group.items():
                label = normalize_label(raw_label)  # 'cross' → Cross, 'x' → X
                if label is None:
                    raise ValueError(f"알 수 없는 필터 키: {raw_label!r}")
                if label in pair:
                    raise ValueError(f"{label} 필터가 중복되었습니다.")
                matrix = Matrix.from_rows(rows)
                if matrix.n != n:
                    raise ValueError(
                        f"{label} 필터 크기 불일치: 키는 {n}×{n}, 실제는 {matrix.n}×{matrix.n}"
                    )
                pair[label] = matrix
            for label in (CROSS, X):
                if label not in pair:
                    raise ValueError(f"{label} 필터가 없습니다.")
        except ValueError as error:
            logs.append(f"✗ {key:<7} 필터 로드 실패: {error}")
            continue
        filters[n] = pair
        logs.append(f"✓ {key:<7} 필터 로드 완료 (Cross, X)")
    return filters, logs


def load_patterns(raw_patterns):
    """patterns 항목을 케이스 목록으로 바꾼다.

    형식이 잘못된 케이스는 멈추지 않고 error에 이유를 담아 둔다(케이스 단위 FAIL).
    """
    cases = []
    for key, item in raw_patterns.items():
        case = {"id": key, "n": None, "pattern": None, "expected": None, "error": None}
        try:
            case["n"] = size_from_key(key, 3)
            if not isinstance(item, dict):
                raise ValueError("케이스 값이 객체({ })가 아닙니다.")
            for field in ("input", "expected"):
                if field not in item:
                    raise ValueError(f"'{field}' 항목이 없습니다.")
            case["expected"] = normalize_label(item["expected"])  # '+' → Cross, 'x' → X
            if case["expected"] is None:
                raise ValueError(f"expected 라벨을 해석할 수 없습니다: {item['expected']!r}")
            case["pattern"] = Matrix.from_rows(item["input"])
        except ValueError as error:
            case["error"] = str(error)
        cases.append(case)
    return cases