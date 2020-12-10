from models.student import *
from models.room import *
from models.assign import *
from models.parser import *
from models.fsave import *
from models.eval import *
import random

# Setup
args = parse_args()
random.seed(args.seed)

# Read from files
stdts = Student.parse_stdt(args.student)
stdts = Student.parse_stdt_partners(args.partner, stdts)
rm = Room.create_room(args.seats)

# Assign seats
alg = Algorithm.choose_algorithm(args.algorithm)
alg.assign_empty_seats(rm, stdts)
alg.assign_seats_rand(rm, stdts)

if args.eval:
    # Eval
    eval_chunk_size(rm)

if not args.nosave:
    # Save output
    save_file(rm, args.out, stdts, args.fmt, args.seed)
    save_gfile(rm, args.gout)

