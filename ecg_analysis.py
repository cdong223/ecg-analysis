import csv
import math
import logging
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import pandas as pd


def moving_average(data):
    df = pd.DataFrame(data)
    rolling = df.rolling(window=40).mean()
    return rolling


def bandpass_filter(data, low_cutoff, high_cutoff, fs, order):
    nyq_freq = 0.5 * fs
    low = low_cutoff / nyq_freq
    high = high_cutoff / nyq_freq
    b, a = butter(order, [low, high], btype='band')
    filtered = lfilter(b, a, data)
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


def qrs_detection(time, voltage):
    fs = sampling_freq(time)
    low_cutoff = 5.0
    high_cutoff = 15.0
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)
    ax1.plot(time, voltage)
    filtered = bandpass_filter(voltage, low_cutoff, high_cutoff, fs, 2)
    ax2.plot(time, filtered)
    ax3.plot(time, filtered*filtered)
    rolling = moving_average(filtered*filtered)
    ax4.plot(time, rolling)
    plt.show()


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
    duration = calc_duration(time)
    extremes = calc_extremes(voltage)
    qrs_detection(time, voltage)


if __name__ == '__main__':
    main()
