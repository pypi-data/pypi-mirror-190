import unittest

from sense_hat_matrix.LedMatrixUtil import list_to_matrix
from sense_hat_matrix.LedMatrixUtil import shift_matrix_to_left
from test.PrettyPrint import pretty_print


o = [0, 0, 0]  # Black
R = [255, 0, 0]  # Red
G = [0, 255, 0]  # Green


class LedMatrixUtilSpec(unittest.TestCase):

    def test_should_make_matrix_from_list(self):
        name_of_test = "should_make_matrix_from_list"
        result = list_to_matrix([
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R
            ])
        pretty_print(name_of_test, result)
        assert result == [
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R]
            ], name_of_test

    def test_should_left_shift_matrix_by_one(self):
        name_of_test = "should_left_shift_matrix_by_one"
        matrix = [
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R]
            ]
        result = shift_matrix_to_left(matrix)
        pretty_print(name_of_test, result)
        assert result == [
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o]
            ], name_of_test


if __name__ == "__main__":
    unittest.main()
