import yaml

def str_to_int(char):
    '''Convert row char to row number
    Args:
        row (char): ('a', 'b', '1', '2')

    Returns:
        int:  row number (1 to max_row)
    '''
    if char.isalpha():
        return ord(char.lower()) - ord('a') + 1
    return int(char)

def int_to_str(row, num_flag):
    '''Convert row number to row char
    Args:
        row (int): 0 to max_row-1
        num_flag (bool): Flag whether to convert to alpha or number.

    Returns:
        int: row char ('a', 'b', '1', '2')
    '''
    # Input: 0 to max_rows-1
    if num_flag:
        return str(row + 1)
    return chr(ord('a') + row)

class Room:
    """Contains grid representation of room containing seat instances"""
    def __init__(self):
        self.max_row = 1
        self.max_col = 1
        self.seats = []
        self.seat_groups = []
        # Describes whether rows are described by numbers or letters
        self.num_row_spec = True

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
        with open(filepath, 'r') as yamlfile:
            yaml_raw = yamlfile.read()
        yaml_parsed = yaml.load(yaml_raw, Loader=yaml.SafeLoader)

        rm = cls()
        rm._update_size(yaml_parsed)
        rm._add_seats(yaml_parsed)
        rm._add_seat_specifiers(yaml_parsed)
        return rm

    def _update_size(self, yaml_parsed):
        """Gets dimensions of room (during instantiation)"""
        for block in yaml_parsed.items():
            # Find whether rows are specified by letter or number
            if block[1]['row'].isalpha():
                self.num_row_spec = False

            cur_row = str_to_int(block[1]['row'])
            cur_cols = str(block[1]['col']).replace(' ', '').split(',')

            for cur_col_range in cur_cols:
                cur_col = int(cur_col_range.split('-')[-1])
                if cur_row > self.max_row:
                    self.max_row = cur_row
                if cur_col > self.max_col:
                    self.max_col = cur_col

    def _add_seats(self, yaml_parsed):
        """Adds seats to room (during instantiation)"""
        # Row major
        for row in range(self.max_row):
            self.seats.append([None] * self.max_col)


        for block in yaml_parsed.items():
            cur_row = str_to_int(block[1]['row'])
            cur_cols = str(block[1]['col']).replace(' ', '').split(',')
            for cur_col_range in cur_cols:
                for cur_col in self._get_col_inds(cur_col_range):
                    self.seats[cur_row-1][cur_col-1] = Seat()

    def _add_seat_specifiers(self,  yaml_parsed):
        """Adds seat features to each seat (during instantiation)"""
        for block in yaml_parsed.items():
            cur_row = str_to_int(block[1]['row'])
            for specifiers in block[1]['specifiers']:
                cur_cols = str(specifiers['seat-col']).replace(' ', '').split(',')

                # Gather specifier flags
                (left_handed, special_needs, broken) = self._specifier_flags(specifiers)

                # Add flags to all specified seats
                for cur_col_range in cur_cols:
                    for cur_col in self._get_col_inds(cur_col_range):
                        if self.seats[cur_row-1][cur_col-1] == None:
                            raise Exception("Adding quality to seat that doesn't exist")
                        else:
                            self.seats[cur_row-1][cur_col-1].left_handed = left_handed
                            self.seats[cur_row-1][cur_col-1].special_needs = special_needs
                            self.seats[cur_row-1][cur_col-1].broken = broken

    def _get_col_inds(self, col_range):
        """Gets column indices in iterator form"""
        if '-' in col_range:
            begin = int(col_range.split('-')[0])
            end = int(col_range.split('-')[1])
            return range(begin, end+1)
        elif str.isdigit(col_range):
            return range(int(col_range), int(col_range)+1)
        else:
            raise Exception("Unknown col range format: {}".format(cur_col_range))

    def _specifier_flags(self, specifiers):
        """Gather specifier flags for each feature"""
        left_handed, special_needs, broken = (False, False, False)
        for flag in specifiers.keys():
            if flag == 'seat-col':
                continue
            elif flag == 'left-handed':
                left_handed = specifiers[flag]
                pass
            elif flag == 'special-needs':
                special_needs = specifiers[flag]
                pass
            elif flag == 'broken':
                broken = specifiers[flag]
            else:
                raise Exception("Unknown flag: {}".format(flag))
        return (left_handed, special_needs, broken)

    def save_file(self, filepath):
        """Saves seats with student info to a file

        Args:
            filepath (str): filepath for output
        """
        with open(filepath, 'w') as outfile:
            for row in range(self.max_row):
                for col in range(self.max_col):
                    if self.seats[row][col] == None:
                        continue

                    if self.seats[row][col].sid == -1:
                        continue

                    row_chr = int_to_str(row, self.num_row_spec)
                    col_chr = int_to_str(col, True)
                    sid = self.seats[row][col].sid

                    outfile.write("{}{}: {}\n".format(row_chr, col_chr, sid))
        print("Finished saving to file: {}".format(filepath))

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

    def split_to_groups():
        for row in range(self.max_row):
            current_group_size = 0

            for col in range(self.max_col):
                if self.seats[row][col] != None and self.seats[row][col]:
                    pass
                    # TODO
                    # current_group_size += 1
                    # self.seat_groups.append()


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
    def __init__(self):
        self.chunk_size = 0
        self.chunk_begin_indices = (0, 0)

    def split():
        # Split SeatGroups into 2 seatgroups. Split near center, where not specialized
        pass

    def sorter():
        # Implement sorter for list of SeatGroups
        pass


