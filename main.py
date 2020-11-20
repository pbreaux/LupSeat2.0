from models.student import *
from models.room import *
from models.assign import *
from models.parser import *
from models.fsave import *

import random
import time

# Setup
args = parse_args()
if args.seed != None:
    seed = args.seed
else:
    seed = int(time.time())
random.seed(seed)

# Read from files
stdts = Student.parse_stdt(args.student)
stdts = Student.parse_stdt_partners(args.partner, stdts)
rm = Room.create_room(args.seats)

# Assign seats
assign_empty_seats(Algorithm.CHUNK_INCREASE, rm, stdts)
assign_seats(rm, stdts)

# Save output
save_file(rm, args.out, seed)
save_gfile(rm, args.gout)

