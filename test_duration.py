import pytest


@pytest.mark.parametrize("time, expected", [
                                ([0.01, 0.02], 0.01),
                                ([0, 0.01, 0.02], 0.02),
                                ([0, 0.02, 0.04, 0.06], 0.06),
                                ([0, 0.01, 0.02, 0.04, 0.08], 0.08),
                                ([0.01, 0.02, 0.03, 0.04, 0.05], 0.04),
                                ([0.01, 0.02, 0.03, 0.04, 0.05, 0.06], 0.05),
                                ([0.02, 0.04, 0.06, 0.08, 0.10, 0.12], 0.1),
                                ([0, 0.04, 0.05, 0.06, 0.08], 0.08),
                                ([0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], 7.0),
                                ([0.5, 1.8], 1.3)
])
def test_calc_duration(time, expected):
    from ecg_analysis import calc_duration
    result = calc_duration(time)
    assert result == pytest.approx(expected)
