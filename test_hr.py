import pytest


@pytest.mark.parametrize("peaks, fs, expected", [
                                ([50, 300, 500], 300, 120),
                                ([99, 392, 684], 200, 61.5385),
                                ([85, 585, 1000], 483.5, 95.1148),
                                ([90, 350, 500, 750, 1000], 200, 65.9341),
                                ([98, 393, 685, 968, 1260], 382.3, 98.7005),
                                ([1, 100, 201, 302, 403, 504], 100, 71.5706),
                                ([30, 200, 392, 593, 701], 194.3, 86.8703),
                                ([35, 200], 98, 71.2727),
                                ([100, 300, 500, 700, 900, 1000], 108, 43.2),
                                ([0, 200, 400, 600, 800], 108, 40.5)
])
def test_calc_bpm(peaks, fs, expected):
    """Unit test for the calc_bpm function in ecg_analysis.py

    Args:
        peaks (ndarray): array of indices corresponding to location of R peaks
        fs (float): sampling frequency of ECG strip
        expected (float): expected calculated bpm value

    Returns:
        None
    """
    from ecg_analysis import calc_bpm
    result = calc_bpm(peaks, fs)
    assert pytest.approx(result) == expected
