import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def chr_to_int(char):
    '''Convert row char to row number
    Args:
        row (char): ('a', 'b')

    Returns:
        int:  row number (1 to max_row)
    '''
    return ord(char.lower()) - ord('a') + 1

def int_to_chr(num):
    '''Convert row number to row char
    Args:
        row (int): 0 to max_row-1

    Returns:
        int: row char ('a', 'b')
    '''
    return chr(ord('a') + num)

def seat_inds(seat):
    '''Get seat indices'''
    if not seat[0].isalpha():
        raise Exception("Seat {} not formatted correctly".format(seat))
    if not seat[1:].isnumeric():
        raise Exception("Seat {} not formatted correctly".format(seat))

    cur_row = chr_to_int(seat[0])
    cur_col = int(seat[1:])
    return (cur_row, cur_col)

def process_str(raw_str):
    '''Removes all whitespace and makes lowercase. Removes any trailing colons'''
    if raw_str == '':
        return ''
    if raw_str[-1] == ':':
        raw_str = raw_str[:-1]
    return "".join(raw_str.lower().split())


class Room:
    """Contains grid representation of room containing seat instances"""
    def __init__(self):
        self.max_row = 1
        self.max_col = 1
        self.seats = []
        self.seat_groups = []

    def __str__(self):
        output = ''
        for rows in self.seats:
            for seat in rows:
                if seat == None:
                    output += "{0: <3}".format('n')
                else:
                    output += "{0: <3}".format(seat.sid)
                output += ' '
            output += '\n'
        return output

    def __repr__(self):
        return str(self)

    @classmethod
    def create_room(cls, filepath):
        """Instantiates room class with correct size and seats.
        Args:
            filepath (str): path to yaml file describing room layout.

        Returns:
            Room: Room instance with correct size, seats & seat qualities specified
        """
        with open(filepath, 'r') as f:
            f_raw = f.read()

        rm = cls()
        rm._update_size(f_raw)
        rm._add_seats(f_raw)
        rm._add_seat_specifiers(f_raw)
        return rm

    def _update_size(self, f_raw):
        """Gets dimensions of room (during instantiation)"""
        seat_flag = False
        for line in f_raw.splitlines():
            line = process_str(line)
            if line == "seats" or line == "seat":
                seat_flag = True
            elif line == "specifiers" or line == "specifier":
                seat_flag = False
            elif seat_flag:
                # Skip if empty line
                if line == "":
                    continue

                # Otherwise check if seat range is new max
                for seat_range in line.split(','):
                    # Skip if empty range
                    if seat_range == '':
                        continue

                    cur_row, cur_col = seat_inds(seat_range.split('-')[-1])

                    if cur_row > self.max_row:
                        self.max_row = cur_row
                    if cur_col > self.max_col:
                        self.max_col = cur_col

    def _add_seats(self, f_raw):
        """Adds seats to room (during instantiation)"""
        # Row major
        for row in range(self.max_row):
            self.seats.append([None] * self.max_col)

        seat_flag = False
        for line in f_raw.splitlines():
            line = process_str(line)
            if line == "seats" or line == "seat":
                seat_flag = True
            elif line == "specifiers" or line == "specifier":
                seat_flag = False
            elif seat_flag:
                # Skip if empty line
                if line == "":
                    continue

                # Add seats per each range
                for row_range in line.split(','):
                    # Skip if empty range
                    if row_range == '':
                        continue

                    # Add seat
                    cur_row = chr_to_int(row_range[0])
                    for cur_col in self._get_col_inds(row_range):
                        self.seats[cur_row-1][cur_col-1] = Seat()

                    # Populate seat_groups
                    beg_seat = self._get_col_inds(row_range).start
                    end_seat = self._get_col_inds(row_range).stop
                    inds = ((cur_row, beg_seat), (cur_row, end_seat))
                    self.seat_groups.append(SeatGroups(inds))

        self.seat_groups.sort(key=(lambda x : x.chunk_size), reverse=True)

    def _add_seat_specifiers(self, f_raw):
        """Adds seat features to each seat (during instantiation)"""
        spec_flag = False
        for line in f_raw.splitlines():
            line = process_str(line)
            if line == "specifiers" or line == "specifier":
                spec_flag = True
            elif line == "seats" or line == "seat":
                spec_flag = False
            elif spec_flag:
                # Skip if empty line
                if line == "":
                    continue

                # Check if line formatted correctly
                if len(line.split(':')) != 2:
                    raise Exception("Line not formatted correctly: {}".format(line))

                # Get seat indices
                cur_row, cur_col = seat_inds(line.split(':')[0])
                if self.seats[cur_row-1][cur_col-1] == None:
                    raise Exception("Adding quality to seat that doesn't exist {}".format(line))

                # Apply flag to seat
                flags = line.split(':')[1]
                for flag in flags:
                    if flag == 'b':
                        self.seats[cur_row-1][cur_col-1].broken = True
                        # If broken, need to split seats
                    if flag == 'l':
                        self.seats[cur_row-1][cur_col-1].left_handed = True
                    if flag == 's':
                        self.seats[cur_row-1][cur_col-1].special_needs = True

    def _get_col_inds(self, col_range):
        """Gets column indices in iterator form"""
        if '-' in col_range:
            beg_seat = col_range.split('-')[0]
            end_seat = col_range.split('-')[1]
            if beg_seat[0] != end_seat[0]:
                raise Exception("Non matching row char {} and {}".format(beg_seat[0], end_seat[0]))

            beg = int(beg_seat[1:])
            end = int(end_seat[1:])
            return range(beg, end+1)
        elif str.isdigit(col_range[1:]):
            return range(int(col_range[1:]), int(col_range[1:])+1)
        else:
            raise Exception("Unknown col range format: {}".format(cur_col_range))


    def save_file(self, filepath, seed):
        """Saves seats with student info to a file

        Args:
            filepath (str): filepath for output
            seed (int): seed for randomizer
        """
        with open(filepath, 'w') as outfile:
            for row in range(self.max_row):
                for col in range(self.max_col):
                    if self.seats[row][col] == None:
                        continue

                    if self.seats[row][col].sid == -1:
                        continue

                    row_chr = int_to_chr(row)
                    col_chr = str(col + 1)
                    sid = self.seats[row][col].sid

                    outfile.write("{}{}: {}\n".format(row_chr, col_chr, sid))

            outfile.write("\nSeed:{}\n".format(seed))

        print("Finished saving to file: {}".format(filepath))

    def save_gfile(self, filepath):
        """Saves seats with student info to an image file

        Args:
            filepath (str): filepath for output
        """
        data = np.zeros((self.max_row, self.max_col))

        for row in range(self.max_row):
            for col in range(self.max_col):
                if self.seats[row][col] == None:
                    data[row][col] = -2
                elif self.seats[row][col].broken:
                    data[row][col] = -1 
                elif self.seats[row][col].sid == -1:
                    data[row][col] = 0
                else:
                    data[row][col] = 1

        fig, ax = plt.subplots()
        im = ax.imshow(data)

        # TODO Add discrete colors rather than heatmap (use cmap)
        # TODO Add legend

        col_ticks = list(range(1,self.max_col+1))
        row_ticks = [int_to_chr(row) for row in range(self.max_row)]

        ax.set_xticks(np.arange(len(col_ticks)))
        ax.set_yticks(np.arange(len(row_ticks)))

        ax.set_xticklabels(col_ticks)
        ax.set_yticklabels(row_ticks)

        # Loop over data dimensions and create text annotations.
        for i in range(len(col_ticks)):
            for j in range(len(row_ticks)):
                label = row_ticks[j] + str(col_ticks[i])
                text = ax.text(i, j, label,ha="center", va="center", color="w")

        ax.set_title("Seating Chart")
        fig.tight_layout()
        plt.savefig(filepath)

        print("Finished saving to image file: {}".format(filepath))

    def add_student(self, indices, sid):
        self.seats[indices[0]][indices[1]].sid = sid

    def get_spec_seats(self, left_hand=False, special_needs=False):
        """Gets specified seats or seats with more specificity
        e.g. If getting left_handed seats, will look for both special_needs and non_sp_needs seats

        Args:
            left_hand (bool): flag for whether to search for left or right handed students
            special_needs (bool): flag for whether to search for special needs students

        Returns:
            List of tuples: List of indices corresponding to seat locations
        """
        match_seats = []

        for row in range(self.max_row):
            for col in range(self.max_col):
                # Ignore if seat not there
                if self.seats[row][col] == None:
                    continue

                # Ignore broken seats
                if self.seats[row][col].broken:
                    continue

                # Ignore if seat is taken
                if self.seats[row][col].sid != -1:
                    continue

                # Add seats based on condition
                if left_hand and special_needs:
                    if self.seats[row][col].left_handed and self.seats[row][col].special_needs:
                        match_seats.append((row, col))
                elif left_hand:
                    if self.seats[row][col].left_handed:
                        match_seats.append((row, col))
                elif special_needs:
                    if self.seats[row][col].special_needs:
                        match_seats.append((row, col))
                else:
                    match_seats.append((row, col))

        # Ensure that seats are sorted by row
        match_seats.sort()

        return match_seats

class Seat:
    """Seat contains features of the seat"""
    def __init__(self):
        self.left_handed = False
        self.special_needs = False
        self.broken = False

        # Describes sid of person sitting there
        self.sid = -1

class SeatGroups:
    """SeatGroups define a contiguous seats in a row. 
    This helps determine how to place empty seats in order to minimize student chunks
    """
    def __init__(self, inds):
        self.chunk_size = inds[1][1] - inds[0][1]
        self.chunk_begin_indices = inds[0]
        
    def contains(self, current_inds):
        '''Whether this SeatGroup contains a seat index'''
        if self.chunk_begin_indices[0] != current_inds[0]:
            return False

        lo_bound = self.chunk_begin_indices[1]
        hi_bound = self.chunk_begin_indices[1] + self.chunk_size
        if lo_bound <= current_inds[1] and hi_bound >= current_inds[1]:
            return True

        return False

    def split(self):
        '''Split SeatGroups into 2 seatgroups by emptying the center seat'''
        pass

    def __str__(self):
        return self.chunk_size

    def __repr__(self):
        return str(self.chunk_size)

