# References:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
# https://www.biopac.com/knowledge-base/extracting-heart-rate-from-a-noisy-ecg-signal/
# https://en.wikipedia.org/wiki/Pan-Tompkins_algorithm
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html

import csv
import numpy as np
import math
import logging
import matplotlib.pyplot as plt
from scipy.signal import butter, find_peaks, sosfiltfilt


def calc_bpm(peaks, fs):
    sec_per_beat = ((peaks[-1] - peaks[0])/len(peaks))/fs
    mean_hr_bpm = 60/sec_per_beat
    return mean_hr_bpm


def bandpass_filter(data, low_cutoff, high_cutoff, fs, order):
    nyq_freq = 0.5 * fs
    low = low_cutoff / nyq_freq
    high = high_cutoff / nyq_freq
    sos = butter(order, [low, high], btype='band', output='sos')
    filtered = sosfiltfilt(sos, np.array(data))
    return filtered


def sampling_freq(time):
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
    low_cutoff = 5.0
    high_cutoff = 35.0
    filtered = bandpass_filter(voltage, low_cutoff, high_cutoff, fs, order=5)
    diff_signal = np.ediff1d(filtered)
    squared_signal = diff_signal * diff_signal
    integrated_signal = 10*np.convolve(squared_signal, np.ones(int(fs/8)))
    peaks, _ = find_peaks(integrated_signal, distance=0.35*fs, prominence=0.2)
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
    max_voltage = max(voltage)
    min_voltage = min(voltage)
    return (min_voltage, max_voltage)


def calc_duration(time):
    return time[-1] - time[0]


def check_range(voltage):
    for v in voltage:
        if v < -300 or v > 300:
            return False
    return True


def parse_add(t, v, time, voltage):
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
    time = []
    voltage = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            t = row[0]
            v = row[1]
            parse_add(t, v, time, voltage)
    isNormal = check_range(voltage)
    if isNormal is False:
        logging.warning("Voltage contains values outside the normal range")
    return time, voltage


def main():
    logging.basicConfig(filename="sequence.log", level=logging.DEBUG,
                        filemode="w")
    filename = input("Enter filename: ")
    time, voltage = import_data(filename)
    fs = sampling_freq(time)
    duration = calc_duration(time)
    voltage_extremes = calc_extremes(voltage)
    peaks = qrs_detection(time, voltage, fs)
    mean_hr_bpm = calc_bpm(peaks, fs)
    print(duration)
    print(voltage_extremes)
    print(fs)
    print(peaks)
    print(len(peaks))
    print(mean_hr_bpm)


if __name__ == '__main__':
    main()
