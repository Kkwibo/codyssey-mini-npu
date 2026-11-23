"""Mini NPU Simulator - 실행 파일 (모드 선택). 실행: python3 main.py"""

from mode_user import run_user_mode


def main():
    print("=== Mini NPU Simulator ===")
    while True:
        print()
        print("[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("0. 종료")
        choice = input("선택: ").strip()
        if choice == "1":
            run_user_mode()
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("입력 오류: 메뉴에 있는 번호를 입력하세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):  # Ctrl+C, Ctrl+D(입력 끝)도 정상 종료
        print("\n프로그램을 종료합니다.")