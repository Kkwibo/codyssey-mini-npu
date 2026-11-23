"""Mini NPU Simulator - 성능 측정(평균 시간)과 성능 표 출력."""

import time

from generator import make_cross, make_x
from mac import mac

REPEAT = 10  # 크기별 반복 측정 횟수
BENCH_SIZES = (3, 5, 13, 25)  # 성능 분석 기본 크기


def measure_ms(func, *args, repeat=REPEAT):
    """func(*args)를 repeat번 실행하고 1회 평균 시간(ms)을 돌려준다.

    - 입력/출력/파일 읽기는 미리 끝내 두고 '연산 함수 호출 구간'만 잰다.
    - 첫 호출은 준비 동작(워밍업)으로 1번 실행하고 측정에서 뺀다.
    """
    func(*args)  # 워밍업 (측정 제외)
    total = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        func(*args)
        total += time.perf_counter() - start
    return total / repeat * 1000  # 초 → 밀리초(ms)


def benchmark_sizes(sizes):
    """크기별로 Cross 패턴과 X 필터를 생성해 MAC 1회 평균 시간을 잰다.

    연산 시간은 값이 아니라 크기(N²)에 따라 달라지므로 생성기 패턴으로 잰다.
    반환: [(N, 평균 ms), ...]
    """
    results = []
    for n in sizes:
        pattern = make_cross(n)  # 준비 작업은 측정 구간 밖에서
        filt = make_x(n)
        results.append((n, measure_ms(mac, pattern, filt)))
    return results


def print_perf_table(rows):
    """rows: [(N, 평균 ms), ...] 를 '크기 / 평균 시간 / 연산 횟수(N²)' 표로 출력한다."""
    print("크기(N×N)    평균 시간(ms)    연산 횟수(N²)")
    print("-" * 43)
    for n, avg_ms in rows:
        size = f"{n}×{n}"
        print(f"{size:<10}{avg_ms:>16.4f}{n * n:>17}")