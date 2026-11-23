"""Mini NPU Simulator - 실행 파일 (모드 선택).

실행: python3 main.py               → 모드 2에서 같은 폴더의 data.json 사용
      python3 main.py 다른파일.json  → 모드 2에서 지정한 파일 사용
"""

import sys

from mode_json import DATA_PATH, run_json_mode
from mode_user import run_user_mode


def main(data_path):
    print("=== Mini NPU Simulator ===")
    while True:
        print()
        print("[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("0. 종료")
        choice = input("선택: ").strip()
        if choice == "1":
            run_user_mode()
        elif choice == "2":
            run_json_mode(data_path)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("입력 오류: 메뉴에 있는 번호를 입력하세요.")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else DATA_PATH
    try:
        main(path)
    except (KeyboardInterrupt, EOFError):  # Ctrl+C, Ctrl+D(입력 끝)도 정상 종료
        print("\n프로그램을 종료합니다.")