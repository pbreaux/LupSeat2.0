# LupSeat
LupSeats assigns seats to students in a smart and automatic away.

View gitlab pages link: [luplab.gitlab.io/lupseat/](https://luplab.gitlab.io/lupseat/)

View pypi link: [pypi.org/project/LupSeat](https://pypi.org/project/LupSeat/)

## Instructions
Install with
```
pip3 install lupseat
```

Run with 
```
lupseat --student students_file --seats seats_file [OPTS]
```

### Required Args
* `students_file` - A csv file containing first name, middle name, last name, student id, dominant hand, special needs flag (see students.csv for example)

* `seats_file` - A yaml file containing the room seating information. (see seats.txt for example)

### Optional Args

* `--out output_file_name`

* `--fmt output_format_string`

* `--sort_by sort_criteria`

* `--g_chart output_chart_image_file_name`

* `--g_room output_image_file_name`

* `--g_chart_size output_chart_image_size`

* `--g_room_size output_image_size`

* `--seed seed_for_rand`

* `--algorithm algorithm_type`

* `--partner partner_file` - Specifies whiich students have worked together as partners before.

* `--gui` - A flag to open GUI mode.

* `--eval` - A flag to produce evaluation score (average number of students sitting next to each other). Lower score is better.

* `--nosave` - A flag to disable saving output files (used primarily for automated evaluation).

### Algorithm Types
* RandomAssign - random assignment of seats
* ChunkIncrease - slowly increase chunk size (i.e. number of students sitting together) until all students can fit in a room. A bottom up approach.
* ConsecDivice (Default) - consecutively divide the room until all empty seats are allocated. A top down approach.

### Sort Criteria
Sorting can be done via fname, lname, sid, or seat.

### Image Sizes
Image sizes can be done by specifying a standard paper size (e.g. A4). Then, an extra keyword "flip" can be appended to the argument to flip between landscape and portrait.

### Output format string
The output format string specifies how students are identified in the output file.

Variable names: sid, fname, lname.

Variable names in format string must be encased by brackets, and can be sliced using the bar operator.

#### Examples
`{fname} {lname} has sid {sid}`

`{sid|-5,-1}`

`{fname|0}.{lname|0}.`

## Unit Tests
Run unit tests with `python3 -m unittest unit-tests/*_test.py`

## Fuzz Test & Algorithm Evaluation
Run fuzz test with `cd scripts && ./alg_evaluator.sh`.
This will produce run 500 tests with randomized seats and students for each algorithm, then average out the evaluation scores (see --eval).


The lowest score is the best performing test.

## Build Instructions
Building for pip requires `setup_tools`, `wheel`, `tqdm`, and `twine` to be installed with pip.
```
python3 setup.py bdist_wheel
python3 -m twine upload dist/*
```

### Build for Mac
Since Mac has python installed by default, the executable only makes sure lupseat is installed via pip, then calls the lupseat command.
Note: The mac app can be modified using Automator. In essence, it is a glorified shell script.

### Build for Windows
First install lupseat and pyinstaller with python-pip.

```
py -m pip install lupseat pyinstaller
```

Next, navigate to `C:\Users\{user}\AppData\Local\Programs\Python\Python39\Scripts` and run the following command

```
.\pyinstaller.exe --onefile --noconsole lupseat
```

The exe file generated in the dist\\ directory is a standalone executable.

