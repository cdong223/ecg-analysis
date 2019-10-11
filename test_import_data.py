import pytest


@pytest.mark.parametrize("t, v, expected_t, expected_v", [
                                ("", "0.075", [], []),
                                ("0.04", "", [], []),
                                ("bad", "-0.087", [], []),
                                ("0.101", "bad", [], []),
                                ("NaN", "-0.1375", [], []),
                                ("0.056", "NaN", [], []),
                                ("", "", [], []),
                                ("t", "v", [], []),
                                ("NaN", "NaN", [], []),
                                ("0.09", "-0.085", [0.09], [-0.085])
])
def test_parse_add(t, v, expected_t, expected_v):
    from ecg_analysis import parse_add
    time = []
    voltage = []
    parse_add(t, v, time, voltage)
    assert time == expected_t
    assert voltage == expected_v


@pytest.mark.parametrize("voltage, expected", [
                                ([-0.05, 0.1, 0.2], True),
                                ([-299.9, 299.9], True),
                                ([-300.01, -0.02, 0.05], False),
                                ([1.0], True),
                                ([-1.0], True),
                                ([123.1], True),
                                ([-313, 0.1, -0.2, 3.0, 5.0, 10.0], False),
                                ([202.5, 299.9, -202.5, -299.9], True),
                                ([0.01, 0.02, 0.03], True),
                                ([-0.01, -0.02, -0.03], True)
])
def test_check_range(voltage, expected):
    from ecg_analysis import check_range
    result = check_range(voltage)
    assert result == expected
