import csv
import math
import logging


def check_range(voltage):
    for v in voltage:
        if v < -300 or v > 300:
            logging.warning("Voltage contains values outside the normal range")
            return


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
    check_range(voltage)
    return time, voltage


def main():
    logging.basicConfig(filename="sequence.log", level=logging.DEBUG,
                        filemode="w")
    filename = input("Enter filename: ")
    time, voltage = import_data(filename)


if __name__ == '__main__':
    main()
