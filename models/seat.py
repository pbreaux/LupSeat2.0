class Seat:
    """Seat contains features of the seat"""
    def __init__(self):
        self.left_handed = False
        self.special_needs = False
        self.broken = False

        # Describes sid of person sitting there
        self.sid = -1

        # Used for ChunkIncrease
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
        if self.chunk_begin[0] != self.chunk_end[0]:
            raise Exception("Rows don't match, can't be a chunk.")

    def size(self):
        return self.chunk_end[1] - self.chunk_begin[1] + 1

    def __str__(self):
        return self.chunk_size

    def __repr__(self):
        return str(self.chunk_size)

