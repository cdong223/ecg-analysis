import csv
import math


def parse_add(t, v, time, voltage):
    try:  # if t is non-numeric or empty then skip
        t = float(t)
    except ValueError:
        return
    try:  # if v is non-numeric or empty then skip
        v = float(v)
    except ValueError:
        return
    if math.isnan(t) is True or math.isnan(v) is True:  # if NaN
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
    return time, voltage


def main():
    filename = input("Enter filename: ")
    time, voltage = import_data(filename)


if __name__ == '__main__':
    main()
