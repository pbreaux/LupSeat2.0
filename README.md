# LupSeat
LupSeats assigns seats to students in a smart and automatic away.

## Instructions
Run with 
`python3 main.py students_file seats_file [--out output_file] [--gout output_gfile] [--partner partner_file] [--seed seed_num]`

-students\_file - A csv file containing first name, middle name, last name, student id, dominant hand, special needs flag (see students.csv for example)

-seats\_file - A yaml file containing the room seating information. (see seats.txt for example)

-output\_file - Name of output file

-output\_gfile - Name of output image file

-partner\_file - A csv file containing student ids of people who were partnered up previously (see partners.csv for example)

-seed\_num - A seed for the randomizer to produce deterministic results.
