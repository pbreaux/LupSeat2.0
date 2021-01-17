import random
import argparse
import math

def parse():
    parser = argparse.ArgumentParser(description="Create seats.txt file")
    parser.add_argument("seats", help="Number of total seats", type=int)

    parser.add_argument("--num_rows", help="Number of rows", type=int, default=random.randint(5,10))
    parser.add_argument("--num_breaks", help="Number of breaks", type=int, default=random.randint(2,4))

    parser.add_argument("--filename", help="Output filename", default="testseat.txt")
    parser.add_argument("--add_flags", help="Randomly add specifier flags", default=False, action='store_true')
    parser.add_argument("--lchance", help="Chance of being left handed", default=0.05, type=float)
    parser.add_argument("--schance", help="Chance of being special needs", default=0.01, type=float)
    parser.add_argument("--bchance", help="Chance of being broken", default=0.005, type=float)
    return parser.parse_args()

def get_seats_per_row(args):
    seats_per_row = math.floor(args.seats / args.num_rows)
    seats_last_row = seats_per_row + (args.seats % args.num_rows)
    return seats_per_row, seats_last_row

def get_current_seats_per_row(args, row_index):
    seats_per_row, seats_last_row = get_seats_per_row(args)
    seats_in_row = seats_per_row
    if row_index == args.num_rows - 1:
        seats_in_row = seats_last_row
    return seats_in_row

def get_seats_per_brk(args, row_index):
    seats_in_row = get_current_seats_per_row(args, row_index)
    seats_per_brk = math.floor(seats_in_row / args.num_breaks)
    seats_last_brk = seats_per_brk + (seats_in_row % args.num_breaks)
    return seats_per_brk, seats_last_brk

def get_current_seats_per_brk(args, row_index, brk_index):
    seats_per_brk, seats_last_brk = get_seats_per_brk(args, row_index)
    num_seat_current_brk =  seats_per_brk
    if brk_index == args.num_breaks:
        num_seat_current_brk = seats_last_brk
    return num_seat_current_brk

def get_flag_per_seat(cur_row, cur_col):
    # Specify flag
    left = sp = False
    if args.lchance > random.random():
        left = True
    if args.schance > random.random():
        sp = True

    if left or sp:
        return "{row}{col}: {left}{sp}\n".format(row=cur_row, col=cur_col, left="l" if left else "", sp="s" if sp else "")
    return ""

def increment_row(cur_row):
    return chr(ord(cur_row) + 1)

args = parse()
flagged_seats = []

with open(args.filename, 'w') as f:
    # Add seats
    cur_row = 'a'
    f.write("Seats:\n")
    # Iterate over each row
    for row_index in range(args.num_rows):
        # Iterate over each chunk
        num_seat_counter = 0
        for brk_index in range(args.num_breaks + 1):
            if brk_index != 0:
                f.write(",")
            num_seat_current_brk = get_current_seats_per_brk(args, row_index, brk_index)
            f.write("{row}{col1}-{row}{col2}".format(row=cur_row, col1=num_seat_counter+1, col2=num_seat_counter+num_seat_current_brk))
            num_seat_counter += num_seat_current_brk
        f.write("\n")
        cur_row = increment_row(cur_row)

    # Return if flags not needed
    if not args.add_flags:
        exit

    # Add specifiers
    cur_row = 'a'
    f.write("Specifiers:\n")
    # Iterate over each seat
    for row_index in range(args.num_rows):
        seats_in_row = get_current_seats_per_row(args, row_index)
        for col_index in range(1, seats_in_row + 1):
            f.write(get_flag_per_seat(cur_row, col_index))
        cur_row = increment_row(cur_row)


