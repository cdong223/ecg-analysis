import pytest


@pytest.mark.parametrize("voltage, expected", [
                                ([-0.01, 0.02, 0.03], (-0.01, 0.03)),
                                ([-0.5, -0.04, -0.03], (-0.5, -0.03)),
                                ([0.1, 0.02, 0.04, 0.06], (0.02, 0.1)),
                                ([-5, 0.05, 0.01, -0.04, 0.08], (-5, 0.08)),
                                ([0.01, -0.02, 0.03, 0.04, -0.05],
                                    (-0.05, 0.04)),
                                ([-0.01, -0.02, -0.03, 0.04, 0.05, 0.06],
                                    (-0.03, 0.06)),
                                ([0.02, 0.04, -0.06, 0.08, 0.10, -0.12],
                                    (-0.12, 0.10)),
                                ([0.4, 0.04, 0.05, -0.06, 0.08], (-0.06, 0.4)),
                                ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
                                    (1.0, 7.0)),
                                ([0.5, 1.8], (0.5, 1.8))
])
def test_calc_extremes(voltage, expected):
    """Unit test for the calc_extremes function in ecg_analysis.py

    Args:
        voltage (float): complete list of voltages pulled from original file
        expected (float): expected tuple containing min and max voltages

    Returns:
        None
    """
    from ecg_analysis import calc_extremes
    result = calc_extremes(voltage)
    assert result == expected
