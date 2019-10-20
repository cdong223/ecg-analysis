import pytest
import numpy as np


@pytest.mark.parametrize("filename, expected", [
                                ("folder/file.csv", "file"),
                                ("a/b.csv", "b"),
                                ("test_data/test_data9.csv", "test_data9"),
                                ("folder/23402.csv", "23402"),
                                ("8768/8758.csv", "8758"),
                                ("folder12.,/file0134.csv", "file0134"),
                                ("test_data/test_data10.csv", "test_data10"),
                                ("folder1/file1.csv", "file1"),
                                ("aaa/bbb.csv", "bbb"),
                                ("lakd/laksdfj.csv", "laksdfj")
])
def test_out_name(filename, expected):
    from ecg_analysis import out_name
    result = out_name(filename)
    assert result == expected


@pytest.mark.parametrize("time, peaks, expected_beats, expected_num", [
                                ([1, 2, 3, 4, 5, 6], np.array([0, 2, 4]),
                                    [1, 3, 5], 3),
                                ([1, 2, 3, 4, 5, 6], np.array([2, 5]), [3, 6],
                                    2),
                                ([1, 2, 3, 4, 5, 6], np.array([1]), [2], 1),
                                ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                    np.array([0, 1, 2, 3, 4, 5]),
                                    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6], 6),
                                ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                    np.array([3, 4, 5]),
                                    [0.4, 0.5, 0.6], 3),
                                ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                    np.array([1, 3, 5]),
                                    [0.2, 0.4, 0.6], 3),
                                ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6], np.array([0]),
                                    [0.1], 1),
                                ([0, 0.01, 0.04, 0.06, 0.09, 0.14],
                                    np.array([1, 4]),
                                    [0.01, 0.09], 2),
                                ([0.1, 0.5, 0.6, 1.0], np.array([3]), [1.0],
                                    1),
                                ([0, 5, 10], np.array([1]), [5], 1)
])
def test_find_beats(time, peaks, expected_beats, expected_num):
    from ecg_analysis import find_beats
    beats, num_beats = find_beats(time, peaks)
    assert beats == expected_beats
    assert num_beats == expected_num
