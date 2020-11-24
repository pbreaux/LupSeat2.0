import sys
import random
import argparse

parser = argparse.ArgumentParser(description="Create students.csv file")
parser.add_argument("count", help="Number of students")
parser.add_argument("--filename", help="Output filename", default="teststudents.csv")
parser.add_argument("--flags", help="Randomly add specifier flags", default=False)
parser.add_argument("--lchance", help="Chance of being left handed", default=0.1)
parser.add_argument("--schance", help="Chance of being special needs", default=0.01)
args = parser.parse_args()

sid_list = []
with open(args.filename, 'w') as f:
    for i in range(int(args.count)):
        sid = random.randint(0, sys.maxsize)
        while sid in sid_list:
            sid = random.randint(0, sys.maxsize)

        left = ""
        sp = ""
        if args.flags:
            if args.lchance > random.random():
                left = "left"
            if args.schance > random.random():
                sp = "special"

        sid_list.append(sid)
        f.write("Fname{0},Lname{0},{1},{2},{3}\n".format(i, sid, left, sp))

