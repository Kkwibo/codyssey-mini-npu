"""Mini NPU Simulator - MAC(Multiply-Accumulate) 연산과 점수 비교 정책."""

EPSILON = 1e-9  # 두 점수의 차이가 이 값보다 작으면 같은 점수(동점)로 본다.


def mac(pattern, filt):  # filter는 파이썬 내장 함수 이름이라 filt로 쓴다
    """패턴과 필터를 같은 위치끼리 곱하고(Multiply) 그 결과를 모두 더한다(Accumulate).

    NumPy 같은 외부 라이브러리 없이 이중 반복문으로 직접 계산한다.
    N×N이면 곱셈 N²번 + 덧셈 N²번 → 시간 복잡도 O(N²)
    """
    if pattern.n != filt.n:
        raise ValueError(
            f"크기 불일치: 패턴 {pattern.n}×{pattern.n}, 필터 {filt.n}×{filt.n}"
        )
    n = pattern.n
    p = pattern.rows
    f = filt.rows
    total = 0.0
    for r in range(n):
        for c in range(n):
            total += p[r][c] * f[r][c]
    return total


def is_tie(score_a, score_b, epsilon=EPSILON):
    """부동소수점 오차를 고려해, 두 점수의 차이가 epsilon보다 작으면 동점으로 본다."""
    return abs(score_a - score_b) < epsilon


def judge(score_a, score_b, label_a, label_b, tie_label):
    """점수가 더 큰 쪽의 라벨을 돌려준다. 동점이면 tie_label을 돌려준다."""
    if is_tie(score_a, score_b):
        return tie_label
    if score_a > score_b:
        return label_a
    return label_b