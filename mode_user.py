"""모드 1: 사용자 입력(3×3) - 필터 A, B와 패턴을 입력받아 MAC 점수로 판정한다."""

from benchmark import REPEAT, measure_ms, print_perf_table
from console import print_section, read_matrix
from mac import EPSILON, judge, mac

SIZE = 3
TIE = "판정 불가"


def run_user_mode():
    print_section("[1] 필터 입력")
    filter_a = read_matrix("필터 A", SIZE)
    print()
    filter_b = read_matrix("필터 B", SIZE)
    print()
    print("✓ 필터 A, B 저장 완료")
    print(f"[필터 A]\n{filter_a}")
    print(f"[필터 B]\n{filter_b}")

    print_section("[2] 패턴 입력")
    pattern = read_matrix("패턴", SIZE)

    print_section("[3] MAC 결과")
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    # A, B 모두 3×3이라 연산량이 같다 → 각각 REPEAT회 재서 MAC 1회 평균 시간을 낸다.
    elapsed = (measure_ms(mac, pattern, filter_a) + measure_ms(mac, pattern, filter_b)) / 2
    verdict = judge(score_a, score_b, "A", "B", TIE)
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/{REPEAT}회): {elapsed:.4f} ms")
    if verdict == TIE:
        print(f"판정: {TIE} (|A-B| < {EPSILON})")
    else:
        print(f"판정: {verdict}")

    print_section(f"[4] 성능 분석 (3×3, 평균/{REPEAT}회)")
    print_perf_table([(SIZE, elapsed)])