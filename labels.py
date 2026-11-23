"""Mini NPU Simulator - 라벨 정규화(표준화).

data.json에는 같은 뜻의 라벨이 여러 모양('+', 'cross', 'x' ...)으로 들어 있다.
프로그램 안에서는 표준 라벨 2가지(Cross, X)만 쓰도록 한 곳에서 바꿔 준다.
"""

CROSS = "Cross"
X = "X"
UNDECIDED = "UNDECIDED"  # 두 점수가 동점(epsilon 이내)일 때의 판정

# 소문자로 바꾼 입력 → 표준 라벨
_ALIASES = {
    "+": CROSS,      # expected 값
    "cross": CROSS,  # filter 키, 'Cross'도 소문자로 바꾸면 여기에 걸린다
    "x": X,          # expected 값과 filter 키, 'X'도 포함
}


def normalize_label(raw):
    """'+', 'cross', ' Cross ' → 'Cross' / 'x', 'X' → 'X' / 해석할 수 없으면 None"""
    if not isinstance(raw, str):
        return None
    return _ALIASES.get(raw.strip().lower())