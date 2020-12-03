from models.student import *
from models.room import *
from models.assign import *
from models.parser import *
from models.fsave import *
import random

# Setup
args = parse_args()
random.seed(args.seed)

# Read from files
stdts = Student.parse_stdt(args.student)
stdts = Student.parse_stdt_partners(args.partner, stdts)
rm = Room.create_room(args.seats)

# Assign seats
alg = ConsecDivide()
alg.assign_empty_seats(rm, stdts)
alg.assign_seats_rand(rm, stdts)

# Save output
save_file(rm, args.out, stdts, args.fmt, args.seed)
save_gfile(rm, args.gout)

