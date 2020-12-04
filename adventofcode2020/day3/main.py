from functools import reduce
import os

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


class OutOfBoundsError(Exception):
    pass


class TobogganTrajectory:
    def __init__(self, input_map=None, move_x=None, move_y=None):
        self.full_map = input_map.copy()
        self.base_map = input_map.copy()
        self.move_x = move_x
        self.move_y = move_y
        self.current_x = 0
        self.current_y = 0
        self.trees_found = 0
        self.boundary = len(input_map[0])

    def check_for_tree(self):
        if self.full_map[self.current_y][self.current_x] == "#":
            self.trees_found += 1

    def extend_map(self):
        for idx, row in enumerate(self.base_map):
            self.full_map[idx] = self.full_map[idx] + row

    def move(self):
        self.current_x += self.move_x
        self.current_y += self.move_y
        if self.current_y >= len(self.base_map):
            raise OutOfBoundsError('Tried to move beyond "bottom" of slope')
        if self.current_x >= self.boundary:
            self.boundary = self.boundary + len(self.base_map[0])
            self.extend_map()

    def traverse_slope(self):
        while self.current_y < len(self.base_map) - 1:
            self.move()
            self.check_for_tree()


if __name__ == "__main__":
    with open(f"{FILE_PATH}/input.txt") as f:
        day3_input_map = f.read().splitlines()
        # Part 1
        tt = TobogganTrajectory(input_map=day3_input_map, move_x=3, move_y=1)
        tt.traverse_slope()
        print(tt.trees_found)

        # Part 2
        trees_found_list = []
        slopes_to_check = [
            [1, 1],
            [3, 1],
            [5, 1],
            [7, 1],
            [1, 2],
        ]
        for slope in slopes_to_check:
            test_tt = TobogganTrajectory(
                input_map=day3_input_map, move_x=slope[0], move_y=slope[1]
            )
            test_tt.traverse_slope()
            trees_found_list.append(test_tt.trees_found)
        print(reduce((lambda x, y: x * y), trees_found_list))
