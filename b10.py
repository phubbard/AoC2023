
import inspect
import os


def safe_dictionary_insert(key, value, dictionary):
    if key in dictionary: raise Exception(f"Key {key} already in dictionary")
    dictionary[key] = value
    return value


def log(message):
    frameNudge = 0
    caller = inspect.getframeinfo(inspect.stack(context=1 + frameNudge)[1 + frameNudge][0])
    _, filename = os.path.split(caller.filename)
    print("%s(%d): %s" % (filename, caller.lineno, message))


class Field:
    def __init__(self):
        self.__field_tiles = {}
        self.__field_start = None
        self.__field_max_row = 0
        self.__field_max_col = 0

    def make_tile(self, row, col, char):
        self.__field_max_row = max(self.__field_max_row, row)
        self.__field_max_col = max(self.__field_max_col, col)
        tile = Tile(row, col, char)
        safe_dictionary_insert((row, col), tile, self.__field_tiles)
        if tile.TILE_CHAR == 'S':
            if self.__field_start is not None: raise Exception("Multiple starts")
            self.__field_start = tile

    def crosslink(self):
        if self.__field_start is None: raise Exception("No start")
        for tile in self.__field_tiles.values():
            candidate_ordinates = tile.get_nonstart_neighbor_ordinates()
            for candidate_ordinate in candidate_ordinates:
                if candidate_ordinate not in self.__field_tiles: continue
                other = self.__field_tiles[candidate_ordinate]
                tile_ordinate = (tile.TILE_ROW, tile.TILE_COL)
                if tile_ordinate not in other.get_nonstart_neighbor_ordinates() and other.TILE_CHAR != 'S': continue
                tile.add_neighbor(other)
                other.add_neighbor(tile)
        if len(self.__field_start.get_neighbors()) != 2:
            raise Exception("Start has wrong number of neighbors")

    def show(self):
        log(f"Start tile at: {self.__field_start}")
        prev_tile = self.__field_start
        next_tile = self.__field_start.get_neighbors()[0]
        while next_tile is not self.__field_start:
            candidates = set(next_tile.get_neighbors())
            # log(f"{next_tile=}")
            # for candidate in candidates: log(f"  {candidate=}")
            candidates.discard(prev_tile)
            if len(candidates) != 1: raise Exception(f"Wrong number of candidates for {next_tile=}")
            following_tile  = tuple(candidates)[0]
            prev_tile       = next_tile
            next_tile       = following_tile

    def find_largest_step(self):
        current_tips    = [self.__field_start]
        current_step    = 0
        traversed_tiles = set(current_tips)
        while current_step == 0 or len(current_tips) > 1:
            current_step += 1
            traversed_tiles.update(current_tips)
            
            candidate_tiles = set()
            for tip in current_tips:
                for neighbor in tip.get_neighbors():
                    if neighbor not in traversed_tiles:
                        candidate_tiles.add(neighbor)
            
            current_tips = candidate_tiles
        return current_step, traversed_tiles
    
    def get_extents(self):
        return self.__field_max_row, self.__field_max_col


class Tile:
    def __init__(self, row, col, char):
        self.TILE_ROW  = row
        self.TILE_COL  = col
        self.TILE_CHAR = char
        self.__tile_neigbors = set()

    def get_nonstart_neighbor_ordinates(self):
        if   self.TILE_CHAR == '.': return []
        elif self.TILE_CHAR == '|': return [(self.TILE_ROW-1, self.TILE_COL+0), (self.TILE_ROW+1, self.TILE_COL+0)]
        elif self.TILE_CHAR == '-': return [(self.TILE_ROW+0, self.TILE_COL-1), (self.TILE_ROW+0, self.TILE_COL+1)]
        elif self.TILE_CHAR == 'L': return [(self.TILE_ROW-1, self.TILE_COL+0), (self.TILE_ROW+0, self.TILE_COL+1)]
        elif self.TILE_CHAR == 'F': return [(self.TILE_ROW+1, self.TILE_COL+0), (self.TILE_ROW+0, self.TILE_COL+1)]
        elif self.TILE_CHAR == '7': return [(self.TILE_ROW+1, self.TILE_COL+0), (self.TILE_ROW+0, self.TILE_COL-1)]
        elif self.TILE_CHAR == 'J': return [(self.TILE_ROW-1, self.TILE_COL+0), (self.TILE_ROW+0, self.TILE_COL-1)]
        elif self.TILE_CHAR == 'S': return [] # Handle separately
        else: raise Exception(f"Unhandled tile character {self.TILE_CHAR}")

    def add_neighbor(self, tile):
        self.__tile_neigbors.add(tile)

    def get_neighbors(self):
        return tuple(self.__tile_neigbors)

    def __str__(self) -> str:
        return f"Tile({self.TILE_ROW=}, {self.TILE_COL=}, {self.TILE_CHAR=})"
    
    def __repr__(self) -> str:
        return f"Tile({self.TILE_ROW=}, {self.TILE_COL=}, {self.TILE_CHAR=})"


class Profile:
    def __init__(self, max_row, max_col, tiles):

        # Make a 2d array sized for rows and columns
        ground = []
        for row in range(max_row + 1):
            ground.append([])
            for col in range(max_col + 1):
                ground[row].append(None)
        
        # Mark location of all tiles in the ground array
        for tile in tiles:
            ground[tile.TILE_ROW][tile.TILE_COL] = tile

        contained_cells = 0
        for row in ground:
            is_inside = False
            for col in row:
                if col is None:
                    if is_inside: contained_cells += 1
                else:
                    is_inside = not is_inside
        self.PROFILE_CONTAINED_COUNT = contained_cells


primal_data = \
""".....
.S-7.
.|.|.
.L-J.
....."""

sample_data = \
"""..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""


if __name__ == '__main__':

    real_data = open("data/10.txt").read()

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("primal", primal_data,    4,      -1),
                ("sample", sample_data,    8,      -1),
                ("real",   real_data,   7097,    1729),
            ]:
        log(f"Considering -> {tag}")
        
        field = Field()

        for row, line in enumerate(dataset.split('\n')):
            # log(f"Considering {row=} with {line=}")
            for col, character in enumerate(line):
                field.make_tile(row, col, character)

        field.crosslink()
        field.show()
        steps, boundary_tiles = field.find_largest_step()
        log(f"Steps: {steps=} with {expected_p1_answer=}")
        assert steps == expected_p1_answer

        if expected_p2_answer > -1:
            max_row, max_col = field.get_extents()
            log(f"Extents: {max_row=} {max_col=}")
            profile = Profile(max_row, max_col, boundary_tiles)
            found_p2_answer = profile.PROFILE_CONTAINED_COUNT
            log(f"expected_p2_answer={expected_p2_answer} and found_p2_answer={found_p2_answer}")
            assert found_p2_answer == expected_p2_answer
        else:
            log(f"Skipping part two")

    log(f"Success")

