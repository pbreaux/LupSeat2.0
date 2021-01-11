# LupSeat
LupSeats assigns seats to students in a smart and automatic away.

## Instructions
Run with 
```
lupseat students_file seats_file [OPTS]
```

### Required Args
* `students_file` - A csv file containing first name, middle name, last name, student id, dominant hand, special needs flag (see students.csv for example)

* `seats_file` - A yaml file containing the room seating information. (see seats.txt for example)

### Optional Args

* `--out output_file_name`

* `--fmt output_format_string`

* `--gout output_image_file_name`

* `--seed seed_for_rand`

* `--algorithm algorithm_type` (Algorithm can be chunkincrease or consecdivide)

* `--eval' - A flag to produce evaluation score (average number of students sitting next to each other). Lower score is better.

* `--nosave' - A flag to disable saving output files (used primarily for automated evaluation).

### Output format string
The output format string specifies how students are identified in the output file.

Variable names: sid, fname, lname.

Variable names in format string must be encased by brackets, and can be sliced using the bar operator.

#### Examples
`{fname} {lname} has sid {sid}`

`{sid|-5,-1}`

`{fname|0}.{lname|0}.`

## Unit Tests
Run unit tests with `python3 -m unittest tests/*_test.py`

## Build Instructions
Building for pip requires `setup_tools`, `wheel`, `tqdm`, and `twine` to be installed with pip.
```
python3 setup.py bdist_wheel
python3 -m twine upload dist/*
```
