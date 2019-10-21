# References:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
# https://www.biopac.com/knowledge-base/extracting-heart-rate-from-a-noisy-ecg-signal/
# https://en.wikipedia.org/wiki/Pan-Tompkins_algorithm
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
# https://github.com/marianpetruk/ECG_analysis

import csv
import numpy as np
import math
import logging
import matplotlib.pyplot as plt
from scipy.signal import butter, find_peaks, sosfiltfilt
import json


def create_metrics(duration, voltage_extremes, num_beats, mean_hr_bpm, beats):
    """Create metrics for an ECG data file

    Args:
        duration (float): time duration of ECG strip
        voltage_extremes (float): tuple of min and max lead voltages
        num_beats (int): number of detected beats in strip
        mean_hr_bpm (float): average heart rate over length of strip
        beats (float): list of times when a beat occurred

    Returns:
        dictionary: metrics
    """
    metrics = {"duration":  duration,
               "voltage_extremes":  voltage_extremes,
               "num_beats":  num_beats,
               "mean_hr_bpm": mean_hr_bpm,
               "beats": beats}
    return metrics


def out_name(filename_input):
    """Retrieves appropriate filename to match json file to original file

    Args:
        filename_input (string): name of original file (ex. folder/file.csv)

    Returns:
        string: filename
    """
    filename_data = filename_input.split("/")[1]
    return filename_data.split(".")[0]


def output_metrics(duration, voltage_extremes, num_beats, mean_hr_bpm, beats,
                   filename):
    """Outputs metrics data into respective JSON files

    Args:
        duration (float): time duration of ECG strip
        voltage_extremes (float): tuple of min and max lead voltages
        num_beats (int): number of detected beats in strip
        mean_hr_bpm (float): average heart rate over length of strip
        beats (float): list of times when a beat occured

    Returns:
        None
    """
    filename = out_name(filename)
    logging.info("Assigning metrics (dictionary entry)...")
    metrics = create_metrics(duration, voltage_extremes, num_beats,
                             mean_hr_bpm, beats)
    out_file = open("{}.json".format(filename), "w")
    json.dump(metrics, out_file)
    out_file.close()
    logging.info("Generated JSON file containing metrics.")
    return


def find_beats(time, peaks):
    """Returns list of times corresponding to beats in the ECG strip

    Args:
        time (float): complete list of times pulled from original file
        peaks (ndarray): array of indices corresponding to location of R peaks

    Returns:
        float: list of times corresponding to beats
        int: length of beats, i.e. number of beats in ECG strip
    """
    beats = np.array(time)[peaks]
    beats = beats.tolist()
    return beats, len(beats)


def calc_bpm(peaks, fs):
    """Calculates average HR based on array of peaks found in ECG strip

    Args:
        peaks (ndarray): array of indices corresponding to location of R peaks
        fs (float): sampling frequency of ECG strip

    Returns:
        float: average heart rate in bpm
    """
    sec_per_beat = ((peaks[-1] - peaks[0])/len(peaks))/fs
    mean_hr_bpm = 60/sec_per_beat
    return mean_hr_bpm


def bandpass_filter(voltage, low_cutoff, high_cutoff, fs, order):
    """Applies bandpass butterworth filter to voltage data set

    Lower cutoff frequency helps eliminate baseline drift, while the higher
    cutoff frequency eliminates possible high frequency noise, allowing
    smoothing out of the signal.
    References:
    -en.wikipedia.org/wiki/Pan-Tompkins_algorithm
    -docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
    -docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfiltfilt.html
    -github.com/marianpetruk/ECG_analysis

    Args:
        voltage (float): complete list of voltages pulled from original file
        low_cutoff (float): lower cutoff frequency for filter
        high_cutoff (float): upper cutoff frequency for filter
        fs (float): sampling frequency of ECG strip
        order (int): order of filter

    Returns:
        ndarray: filtered signal
    """
    nyq_freq = 0.5 * fs
    low = low_cutoff / nyq_freq
    high = high_cutoff / nyq_freq
    sos = butter(order, [low, high], btype='band', output='sos')
    filtered = sosfiltfilt(sos, np.array(voltage))
    return filtered


def sampling_freq(time):
    """Calculates the average sampling frequency of the ECG strip

    Args:
        time (float): complete list of times pulled from original file

    Returns:
        float: average sampling frequency
    """
    sum = 0
    count = 0
    for i in range(len(time)):
        if i == 0:
            continue
        sum += time[i] - time[i - 1]
        count += 1
    average_period = sum/count
    return 1/average_period


def qrs_detection(time, voltage, fs):
    """Detects the number and locations of QRS complexes in an ECG strip

    Process based on the Pan-Tompkins algorithm:
    - bandpass filter: minimize baseline wander and noise
    - differentiation: emphasize R peaks, which have steeper slopes
    - squaring: further enhance the dominant (R) peaks
    - integration: smooth out the signal for more accurate peak detection
    References:
    - en.wikipedia.org/wiki/Pan-Tompkins_algorithm
    - biopac.com/knowledge-base/extracting-heart-rate-from-a-noisy-ecg-signal/
    - docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
    - github.com/marianpetruk/ECG_analysis

    Args:
        time (float): complete list of times pulled from original file
        voltages (float): complete list of voltages pulled from original file
        fs (float): sampling frequency of ECG strip

    Returns:
        ndarray: array of locations (indices) of peaks in signal
    """
    low_cutoff = 5.0
    high_cutoff = 35.0
    filtered = bandpass_filter(voltage, low_cutoff, high_cutoff, fs, order=5)
    diff_signal = np.ediff1d(filtered)
    squared_signal = diff_signal * diff_signal
    integrated_signal = 10*np.convolve(squared_signal, np.ones(int(fs*0.15)))
    peaks, _ = find_peaks(integrated_signal, distance=0.45*fs, prominence=0.05)
    return peaks
    # fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, sharex=True)
    # ax1.plot(voltage)
    # ax1.plot(peaks, np.array(voltage)[peaks], "or")
    # ax2.plot(filtered)
    # ax3.plot(diff_signal)
    # ax4.plot(squared_signal)
    # ax5.plot(integrated_signal)
    # ax5.plot(peaks, np.array(integrated_signal)[peaks], "ob")
    # plt.show()


def calc_extremes(voltage):
    """Retrieves the minimum and maximum lead voltages from the ECG strip

    Args:
        voltages (float): complete list of voltages pulled from original file

    Returns:
        float: tuple containing min and max lead voltages
    """
    max_voltage = max(voltage)
    min_voltage = min(voltage)
    return (min_voltage, max_voltage)


def calc_duration(time):
    """Calculates the duration of the ECG strip

    Args:
        time (float): complete list of times pulled from original file

    Returns:
        float: duration of ECG strip
    """
    return time[-1] - time[0]


def check_range(voltage):
    """Checks to see if the file contains a voltage reading outside +/- 300mV

    Args:
        voltages (float): complete list of voltages pulled from original file

    Returns:
        boolean: the file contains a voltage outside the normal range
    """
    for v in voltage:
        if v < -300 or v > 300:
            return False
    return True


def parse_add(t, v, time, voltage):
    """Analyzes time-voltage data points and stores them in respective lists.
       If either value in a time-voltage pair is missing, contains a
       non-numeric string, or is NaN, this occurrence is logged and the pair is
       skipped over.

    Args:
        time (float): complete list of times pulled from original file
        voltages (float): complete list of voltages pulled from original file
        t (string): time entry currently being analyzed from file
        v (string): voltage entry currently being analyzed from file

    Returns:
        None
    """
    try:  # if t is non-numeric or empty then skip
        t = float(t)
    except ValueError:
        logging.error("'{}' cannot be cast as a float.".format(t))
        return
    try:  # if v is non-numeric or empty then skip
        v = float(v)
    except ValueError:
        logging.error("'{}' cannot be cast as a float.".format(v))
        return
    if math.isnan(t) is True or math.isnan(v) is True:  # if NaN then skip
        logging.error("Value is NaN.")
        return
    time.append(t)
    voltage.append(v)


def import_data(filename):
    """Parses through file for time-voltage data points and calls parse_add()
       function for further analysis. Calls function to checl if the file
       contains a voltage outside the normal range.

    Args:
        time (float): complete list of times pulled from original file
        voltages (float): complete list of voltages pulled from original file
        t (string): time entry currently being analyzed from file
        v (string): voltage entry currently being analyzed from file

    Returns:
        float: list of valid time points from file
        float: list of valid voltage points from file
    """
    time = []
    voltage = []
    logging.info("Opening file...")
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            t = row[0]
            v = row[1]
            parse_add(t, v, time, voltage)
    isNormal = check_range(voltage)
    if isNormal is False:
        logging.warning("File contains voltage(s) outside the normal range.")
    logging.info("Finished reading file.")
    return time, voltage


def main():
    logging.basicConfig(filename="sequence.log", level=logging.DEBUG,
                        filemode="w")
    filename = input("Enter filename: ")
    logging.info("Starting analysis of a new ECG trace: {}".format(filename))
    time, voltage = import_data(filename)
    fs = sampling_freq(time)
    duration = calc_duration(time)
    voltage_extremes = calc_extremes(voltage)
    peaks = qrs_detection(time, voltage, fs)
    mean_hr_bpm = calc_bpm(peaks, fs)
    beats, num_beats = find_beats(time, peaks)
    output_metrics(duration, voltage_extremes, num_beats, mean_hr_bpm,
                   beats, filename)


if __name__ == '__main__':
    main()
