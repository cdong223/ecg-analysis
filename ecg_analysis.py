import csv
import math
import logging


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


if __name__ == '__main__':
    main()
