from models.student import *
from models.room import *
from models.assign import *
from models.parser import *

args = parse_args()

stdts = Student.parse_stdt(args.student)
if args.partner != None:
    stdts = Student.parse_stdt_partners(args.partner, stdts)
rm = Room.create_room(args.seats)

assign_seats(rm, stdts)

rm.save_file(args.out)

