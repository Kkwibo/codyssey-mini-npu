"""Mini NPU Simulator - N×N 십자가(Cross)·X 패턴 자동 생성기.

성능 분석에서 3×3을 포함한 모든 크기의 패턴을 만들 때 쓴다.
"""

from matrix import Matrix


def make_cross(n):
    """가운데 행과 가운데 열이 1인 십자가 패턴. (N이 짝수면 가운데 2줄)"""
    matrix = Matrix(n)
    centers = [n // 2] if n % 2 == 1 else [n // 2 - 1, n // 2]
    for center in centers:
        for i in range(n):
            matrix.set(center, i, 1)  # 가로줄
            matrix.set(i, center, 1)  # 세로줄
    return matrix


def make_x(n):
    """두 대각선이 1인 X 패턴."""
    matrix = Matrix(n)
    for i in range(n):
        matrix.set(i, i, 1)          # ↘ 대각선
        matrix.set(i, n - 1 - i, 1)  # ↙ 대각선
    return matrix