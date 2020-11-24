# LupSeat
LupSeats assigns seats to students in a smart and automatic away.

## Instructions
Run with 
`python3 main.py students_file seats_file [--partner partner_file] [--out output_file] [--fmt output_format] [--gout output_gfile] [--seed seed_num]`

-students\_file - A csv file containing first name, middle name, last name, student id, dominant hand, special needs flag (see students.csv for example)

-seats\_file - A yaml file containing the room seating information. (see seats.txt for example)

-partner\_file - A csv file containing student ids of people who were partnered up previously (see partners.csv for example)

-output\_file - Name of output file

-output\_format - Output format string

-output\_gfile - Name of output image file

-seed\_num - A seed for the randomizer to produce deterministic results.

## Output format string
The output format string specifies how students are identified in the output file.

Variable names: sid, fname, lname.

Variable names in format string must be encased by brackets, and can be sliced using the bar operator.

### Examples
`{fname} {lname} has sid {sid}`

`{sid|-5,-1}`

`{fname|0}.{lname|0}.`


## Unit Tests
Run unit tests with `python3 -m unittest tests/*_test.py`
