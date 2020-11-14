class Seat:
    """Seat contains features of the seat"""
    def __init__(self):
        self.left_handed = False
        self.special_needs = False
        self.broken = False

        # Describes sid of person sitting there
        self.sid = -1

        # True to use the seat, False to keep empty
        self.enable = True

class SeatGroups:
    """SeatGroups define a contiguous seats in a row. 
    This helps determine how to place empty seats in order to minimize student chunks
    """
    def __init__(self, _chunk_begin, _chunk_end):
        # Chunk ranges from (chunk_begin, chunk_end) inclusive
        self.chunk_begin = _chunk_begin
        self.chunk_end = _chunk_end

    def num_seats(self, max_chunk_size):
        '''Determines the number of seats possible in this chunk given with some maximum chunk size.
        Args:
            max_chunk_size (int): Max size of students sitting together

        Returns:
            (int): Number of students who can be seated within this chunk
        '''
        size = self.chunk_end - chunk_begin + 1
        taken = 0
        while True:
            size -= max_chunk_size
            if size < 0:
                return taken
            taken += max_chunk_size
            # Leave space to separate chunk
            size -= 1

    def get_empty_seats_inds(self, max_chunk_size):
        '''Gets list of indices where empty seats should go
        Args:
            max_chunk_size (int): Max size of students sitting together

        Returns:
            (List[Tuple(int, int)]): List of empty seat indices
        '''
        pass

    def __str__(self):
        return self.chunk_size

    def __repr__(self):
        return str(self.chunk_size)

