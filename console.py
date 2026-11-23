"""Mini NPU Simulator - 콘솔 입출력 도우미 (구분선 출력, 행렬 입력과 검증)."""

import math

from matrix import Matrix


def print_section(title):
    """'#---' 구분선 사이에 제목을 출력한다."""
    print()
    print("#" + "-" * 39)
    print(f"# {title}")
    print("#" + "-" * 39)


def parse_row(line, n):
    """한 줄을 숫자 n개의 리스트로 바꾼다. 형식이 틀리면 ValueError(이유)를 발생시킨다."""
    parts = line.split()
    if not parts:
        raise ValueError(f"행 수 불일치: 빈 줄이 입력됐습니다. {n}줄을 모두 입력해야 합니다")
    if len(parts) != n:
        raise ValueError(f"열 수 불일치: {n}개가 필요한데 {len(parts)}개입니다")
    row = []
    for part in parts:
        try:
            value = float(part)
        except ValueError:
            raise ValueError(f"숫자 파싱 실패: {part!r}") from None
        if not math.isfinite(value):  # nan, inf 차단
            raise ValueError(f"사용할 수 없는 값: {part!r}")
        row.append(value)
    return row


def read_matrix(title, n):
    """n줄을 한 줄씩 입력받아 Matrix로 돌려준다. 틀린 줄은 안내 후 그 줄만 다시 입력받는다."""
    print(f"{title} ({n}줄 입력, 공백 구분)")
    rows = []
    while len(rows) < n:
        line = input().strip()
        try:
            rows.append(parse_row(line, n))
        except ValueError as error:
            print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요. ({error})")
            print(f"→ {len(rows) + 1}번째 줄을 다시 입력하세요.")
    return Matrix.from_rows(rows)