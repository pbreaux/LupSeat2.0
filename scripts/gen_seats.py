import sys
import random
import argparse
import math

parser = argparse.ArgumentParser(description="Create seats.txt file")
parser.add_argument("count_per_row", help="Number of seats per row", type=int)
parser.add_argument("numrows", help="Number of rows", type=int)
parser.add_argument("numrow_breaks", help="Number of row breaks", type=int)
parser.add_argument("--filename", help="Output filename", default="testseat.txt")
parser.add_argument("--flags", help="Randomly add specifier flags", default=False)
parser.add_argument("--lchance", help="Chance of being left handed", default=0.1, type=float)
parser.add_argument("--schance", help="Chance of being special needs", default=0.01, type=float)
parser.add_argument("--bchance", help="Chance of being broken", default=0.005, type=float)
args = parser.parse_args()

# TODO Add more robust and accurate seating specification

num_seats_per_chk = args.count_per_row / args.numrow_breaks
num_seats = [math.floor(num_seats_per_chk)] * args.numrow_breaks
num_seats[-1] = math.ceil(num_seats_per_chk)

with open(args.filename, 'w') as f:
    cur_row = 'a'
    f.write("Seats:\n")
    for i in range(int(args.numrows)):

        left = ""
        sp = ""
        if args.flags:
            if args.lchance > random.random():
                left = "left"
            if args.schance > random.random():
                sp = "special"

        cur_num_seat = 0
        for index, num_seat in enumerate(num_seats):
            f.write("{row}{col1}-{row}{col2}".format(row=cur_row, col1=cur_num_seat+1, col2=cur_num_seat+num_seat))
            cur_num_seat += num_seat
            if index != len(num_seats) - 1:
                f.write(',')

        f.write('\n')

        cur_row = chr(ord(cur_row) + 1)

