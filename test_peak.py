import pytest


@pytest.mark.parametrize("time, expected", [
                                ([0.01, 0.02], 100),
                                ([0, 0.01, 0.02], 100),
                                ([0, 0.02, 0.04, 0.06], 50),
                                ([0, 0.01, 0.02, 0.04, 0.08], 50),
                                ([0.01, 0.02, 0.03, 0.04, 0.05], 100),
                                ([0.01, 0.02, 0.03, 0.04, 0.05, 0.06], 100),
                                ([0.02, 0.04, 0.06, 0.08, 0.10, 0.12], 50),
                                ([0, 0.04, 0.05, 0.06, 0.08], 50),
                                ([0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], 1.0),
                                ([0.5, 0.7, 0.75, 0.8, 1.5], 4)
])
def test_sampling_freq(time, expected):
    from ecg_analysis import sampling_freq
    result = sampling_freq(time)
    assert result == pytest.approx(expected)
