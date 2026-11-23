"""모드 2: data.json 분석 - 필터와 패턴을 읽어 일괄 판정하고 expected와 비교한다."""

import os

from console import print_section
from labels import CROSS, UNDECIDED, X
from loader import load_filters, load_json, load_patterns
from mac import EPSILON, judge, mac

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
CATEGORIES = ("데이터/스키마", "로직", "수치 비교")  # 실패 원인 3분류


def run_json_mode(path=DATA_PATH):
    print_section("[1] 필터 로드")
    print(f"파일: {os.path.relpath(path)}")
    try:
        data = load_json(path)
    except ValueError as error:
        print(f"✗ data.json 로드 실패: {error}")
        return
    filters, logs = load_filters(data["filters"])
    for log in logs:
        print(log)

    print_section("[2] 패턴 분석 (라벨 정규화 적용)")
    results = []
    for case in load_patterns(data["patterns"]):
        result = evaluate_case(case, filters)
        print_case(result)
        results.append(result)

    print_section("[3] 결과 요약")
    print_summary(results)


def evaluate_case(case, filters):
    """케이스 1개를 판정한다. 문제가 있으면 멈추지 않고 실패 원인(분류+이유)을 담아 돌려준다."""
    result = {
        "id": case["id"], "cross": None, "x": None, "verdict": None,
        "expected": case["expected"], "passed": False, "category": None, "reason": None,
    }
    if case["error"]:
        return _fail(result, "데이터/스키마", case["error"])
    n = case["n"]
    pattern = case["pattern"]
    if n not in filters:
        return _fail(result, "데이터/스키마", f"size_{n} 필터가 없습니다.")
    if pattern.n != n:
        return _fail(
            result, "데이터/스키마", f"크기 불일치: 필터 {n}×{n}, 패턴 {pattern.n}×{pattern.n}"
        )

    result["cross"] = mac(pattern, filters[n][CROSS])
    result["x"] = mac(pattern, filters[n][X])
    result["verdict"] = judge(result["cross"], result["x"], CROSS, X, UNDECIDED)
    if result["verdict"] == result["expected"]:
        result["passed"] = True
        return result
    if result["verdict"] == UNDECIDED:
        diff = abs(result["cross"] - result["x"])
        return _fail(
            result, "수치 비교",
            f"|Cross-X| = {diff:.2e} < {EPSILON} → 동점(UNDECIDED) 처리 규칙에 따라 FAIL",
        )
    return _fail(
        result, "로직",
        f"판정 {result['verdict']}, expected {result['expected']} (필터 선택·라벨·MAC 점검 필요)",
    )


def _fail(result, category, reason):
    result["category"] = category
    result["reason"] = reason
    return result


def print_case(result):
    print(f"--- {result['id']} ---")
    if result["verdict"] is None:  # MAC 전에 걸러진 경우 (데이터/스키마 문제)
        print(f"FAIL: [{result['category']}] {result['reason']}")
        return
    print(f"Cross 점수: {result['cross']}")
    print(f"X 점수: {result['x']}")
    if result["passed"]:
        status = "PASS"
    elif result["verdict"] == UNDECIDED:
        status = "FAIL (동점 규칙)"
    else:
        status = "FAIL"
    print(f"판정: {result['verdict']} | expected: {result['expected']} | {status}")


def print_summary(results):
    failed = [result for result in results if not result["passed"]]
    print(f"총 테스트: {len(results)}개")
    print(f"통과: {len(results) - len(failed)}개")
    print(f"실패: {len(failed)}개")
    print()
    if not failed:
        print("실패 케이스: 없음")
        return
    counts = [f"{name} {sum(1 for r in failed if r['category'] == name)}개" for name in CATEGORIES]
    print("실패 원인 분류: " + " / ".join(counts))
    print()
    print("실패 케이스:")
    for result in failed:
        print(f"- {result['id']}: [{result['category']}] {result['reason']}")