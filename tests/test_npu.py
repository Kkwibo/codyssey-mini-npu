"""Mini NPU Simulator 자동 테스트. 실행: python3 -m unittest discover -s tests -v"""

import os
import unittest

from console import parse_row
from generator import make_cross, make_x
from labels import CROSS, UNDECIDED, X, normalize_label
from loader import load_filters, load_json, load_patterns, size_from_key
from mac import judge, mac
from matrix import Matrix
from mode_json import evaluate_case

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 프로젝트 폴더
CROSS_3 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
X_3 = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]


def judge_file(path):
    """데이터 파일 하나를 모드 2와 같은 순서(로드 → 검증 → 판정)로 처리한 결과 목록."""
    data = load_json(path)
    filters, _ = load_filters(data["filters"])
    return [evaluate_case(case, filters) for case in load_patterns(data["patterns"])]


class MatrixTest(unittest.TestCase):
    def test_get_set(self):
        m = Matrix(3)
        m.set(1, 2, 7)  # 2행 3열에 저장
        self.assertEqual(m.get(1, 2), 7.0)

    def test_rejects_bad_shape_and_values(self):
        # 빈 배열, 정사각형 아님, 문자, True, NaN → 모두 거부
        for rows in ([], [[1, 2], [3]], [[1, "a"], [1, 1]], [[True]], [[float("nan")]]):
            with self.assertRaises(ValueError):
                Matrix.from_rows(rows)


class MacTest(unittest.TestCase):
    def test_mission_example(self):
        cross = Matrix.from_rows(CROSS_3)
        x = Matrix.from_rows(X_3)
        self.assertEqual(mac(cross, cross), 5.0)  # 일치
        self.assertEqual(mac(cross, x), 1.0)      # 불일치

    def test_size_mismatch(self):
        with self.assertRaises(ValueError):
            mac(Matrix(3), Matrix(5))


class JudgeTest(unittest.TestCase):
    def test_float_error_is_tie(self):
        ones = Matrix.from_rows([[1, 1, 1]] * 3)
        tenths = Matrix.from_rows([[0.1, 0.1, 0.1]] * 3)
        total = mac(ones, tenths)  # 0.1을 9번 더함 → 0.8999999999999999
        self.assertNotEqual(total, 0.9)  # == 로 비교하면 다르다고 나온다
        self.assertEqual(judge(0.9, total, CROSS, X, UNDECIDED), UNDECIDED)

    def test_bigger_score_wins(self):
        self.assertEqual(judge(5.0, 1.0, CROSS, X, UNDECIDED), CROSS)
        self.assertEqual(judge(1.0, 5.0, CROSS, X, UNDECIDED), X)


class LabelTest(unittest.TestCase):
    def test_normalize(self):
        for raw in ("+", "cross", "Cross", " CROSS "):
            self.assertEqual(normalize_label(raw), CROSS)
        for raw in ("x", "X", " x "):
            self.assertEqual(normalize_label(raw), X)
        for raw in ("circle", "", None, 1):
            self.assertIsNone(normalize_label(raw))


class InputTest(unittest.TestCase):
    def test_parse_row(self):
        self.assertEqual(parse_row("0 1 0", 3), [0.0, 1.0, 0.0])
        # 빈 줄(행 수), 개수 틀림(열 수), 문자·쉼표(파싱), nan → 모두 거부
        for line in ("", "0 1", "0 1 0 1", "a b c", "0,1,0", "nan 1 0"):
            with self.assertRaises(ValueError):
                parse_row(line, 3)


class GeneratorTest(unittest.TestCase):
    def test_shapes(self):
        self.assertEqual(make_cross(3).rows, CROSS_3)
        self.assertEqual(make_x(3).rows, X_3)


class LoaderTest(unittest.TestCase):
    def test_size_from_key(self):
        self.assertEqual(size_from_key("size_13", 2), 13)
        self.assertEqual(size_from_key("size_13_2", 3), 13)
        for key in ("size13_1", "size_a_1", "pattern_5_1"):
            with self.assertRaises(ValueError):
                size_from_key(key, 3)


class DataFileTest(unittest.TestCase):
    def test_data_json(self):
        results = judge_file(os.path.join(ROOT, "data.json"))
        failed = [r for r in results if not r["passed"]]
        self.assertEqual(len(results), 6)
        self.assertEqual(len(failed), 3)
        self.assertEqual([r["id"] for r in failed], ["size_5_1", "size_13_2", "size_25_1"])
        self.assertTrue(all(r["category"] == "수치 비교" for r in failed))

    def test_error_file_does_not_stop(self):
        results = judge_file(os.path.join(ROOT, "tests", "data_errors.json"))
        categories = [r["category"] for r in results if not r["passed"]]
        self.assertEqual(len(results), 8)
        self.assertEqual(categories.count("데이터/스키마"), 5)
        self.assertEqual(categories.count("로직"), 1)
        self.assertEqual(categories.count("수치 비교"), 1)


if __name__ == "__main__":
    unittest.main()