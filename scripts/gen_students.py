import sys
import random
import argparse

def parse():
    parser = argparse.ArgumentParser(description="Create students.csv file")
    parser.add_argument("count", help="Number of students")
    parser.add_argument("--filename", help="Output filename", default="teststudents.csv")

    parser.add_argument("--add_flags", help="Randomly add specifier flags", default=False, action='store_true')
    parser.add_argument("--lchance", help="Chance of being left handed", default=0.05)
    parser.add_argument("--schance", help="Chance of being special needs", default=0.005)
    return parser.parse_args()

def gen_sid(sid_list):
    ''' Generate sid and add to lis t'''
    sid = random.randint(0, sys.maxsize)
    while sid in sid_list:
        sid = random.randint(0, sys.maxsize)

    sid_list.append(sid)
    return sid, sid_list

def get_flags(args):
    ''' Generate flags '''
    left = sp = ""
    if args.add_flags:
        if args.lchance > random.random():
            left = "left"
        if args.schance > random.random():
            sp = "special"

    return left, sp


args = parse()
sid_list = []
with open(args.filename, 'w') as f:
    for i in range(int(args.count)):
        sid, sid_list = gen_sid(sid_list)

        left, sp = get_flags(args)

        f.write("Fname{0},Lname{0},{1},{2},{3}\n".format(i, sid, left, sp))

