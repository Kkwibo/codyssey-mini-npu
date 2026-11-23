"""Mini NPU Simulator - N×N 행렬(패턴/필터) 데이터 구조."""

import math


class Matrix:
    """N×N 크기의 2차원 숫자 배열(패턴 또는 필터)을 저장한다.

    - rows: 실제 값이 들어 있는 2차원 리스트 (rows[r][c])
    - get(r, c) / set(r, c, value): 특정 위치의 값을 읽고 저장한다.
    """

    def __init__(self, n):
        if isinstance(n, bool) or not isinstance(n, int) or n < 1:
            raise ValueError(f"크기 N은 1 이상의 정수여야 합니다: {n!r}")
        self.n = n
        self.rows = [[0.0] * n for _ in range(n)]

    @classmethod
    def from_rows(cls, rows):
        """2차원 리스트로 Matrix를 만든다.

        N×N 정사각형이 아니거나 숫자가 아닌 값이 있으면 ValueError를 발생시킨다.
        """
        if not isinstance(rows, list) or len(rows) == 0:
            raise ValueError("2차원 배열(리스트 안의 리스트)이 아닙니다.")
        n = len(rows)
        matrix = cls(n)
        for r, row in enumerate(rows):
            if not isinstance(row, list):
                raise ValueError(f"{r + 1}행이 배열이 아닙니다.")
            if len(row) != n:
                raise ValueError(
                    f"행/열 수 불일치: 행은 {n}개인데 {r + 1}번째 행의 값은 {len(row)}개입니다."
                )
            for c, value in enumerate(row):
                matrix.set(r, c, value)
        return matrix

    def get(self, r, c):
        """r행 c열(0부터 셈)의 값을 읽는다."""
        return self.rows[r][c]

    def set(self, r, c, value):
        """r행 c열(0부터 셈)에 값을 저장한다. 숫자만 허용한다."""
        # True/False는 파이썬에서 int의 한 종류라 숫자 검사를 통과하므로 따로 막는다.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{r + 1}행 {c + 1}열 값이 숫자가 아닙니다: {value!r}")
        try:
            number = float(value)
        except OverflowError:
            raise ValueError(f"{r + 1}행 {c + 1}열 값이 너무 큽니다.") from None
        if not math.isfinite(number):  # NaN, Infinity 차단
            raise ValueError(f"{r + 1}행 {c + 1}열 값이 유한한 숫자가 아닙니다: {value!r}")
        self.rows[r][c] = number

    def __str__(self):
        return "\n".join(" ".join(_format(value) for value in row) for row in self.rows)


def _format(value):
    """1.0 → '1', 0.5 → '0.5' 처럼 보기 좋게 바꾼다."""
    return str(int(value)) if value.is_integer() else str(value)