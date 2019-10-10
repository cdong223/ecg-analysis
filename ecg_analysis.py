import csv
import math


def parse_add(t, v, time, voltage):
    return


def import_data(filename):
    time = []
    voltage = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            t = row[0]
            v = row[1]
            # parse_add(t, v, time, voltage)
            time.append(t)
            voltage.append(v)
    return time, voltage


def main():
    filename = input("Enter filename: ")
    time, voltage = import_data(filename)
    print(time)
    print(voltage)


if __name__ == '__main__':
    main()
