import mock
import os
import pytest

from day3.main import TobogganTrajectory, OutOfBoundsError

TEST_FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def test_check_for_tree():
    with open(f"{TEST_FILE_PATH}/test_input.txt") as f:
        test_map = f.read().splitlines()
    test_tt = TobogganTrajectory(input_map=test_map)
    test_tt.current_x = 4
    test_tt.current_y = 1
    test_tt.check_for_tree()
    assert test_tt.trees_found == 1


def test_extend_map():
    expected_extended_map = [
        "..##.........##.......",
        "#...#...#..#...#...#..",
        ".#....#..#..#....#..#.",
        "..#.#...#.#..#.#...#.#",
        ".#...##..#..#...##..#.",
        "..#.##.......#.##.....",
        ".#.#.#....#.#.#.#....#",
        ".#........#.#........#",
        "#.##...#...#.##...#...",
        "#...##....##...##....#",
        ".#..#...#.#.#..#...#.#",
    ]

    with open(f"{TEST_FILE_PATH}/test_input.txt") as f:
        test_map = f.read().splitlines()
    test_tt = TobogganTrajectory(input_map=test_map)
    test_tt.extend_map()
    assert test_tt.full_map == expected_extended_map


def test_out_of_boundary_extend_called():
    mocked_extend = mock.Mock()
    with open(f"{TEST_FILE_PATH}/test_input.txt") as f:
        test_map = f.read().splitlines()
    with mock.patch.object(TobogganTrajectory, "extend_map", mocked_extend):
        test_tt = TobogganTrajectory(input_map=test_map, move_x=3, move_y=1)
        test_tt.current_x = test_tt.boundary
        test_tt.move()
    assert mocked_extend.call_count == 1


def test_move():
    with open(f"{TEST_FILE_PATH}/test_input.txt") as f:
        test_map = f.read().splitlines()
    test_tt = TobogganTrajectory(input_map=test_map, move_x=3, move_y=1)
    test_tt.move()
    assert test_tt.current_x == 3
    assert test_tt.current_y == 1


def test_move_y_boundary():
    with open(f"{TEST_FILE_PATH}/test_input.txt") as f:
        test_map = f.read().splitlines()
    test_tt = TobogganTrajectory(input_map=test_map, move_x=3, move_y=1)
    test_tt.current_y = len(test_tt.base_map)
    with pytest.raises(OutOfBoundsError):
        test_tt.move()


def test_traverse_slope_part_1():
    with open(f"{TEST_FILE_PATH}/test_input.txt") as f:
        test_map = f.read().splitlines()
    test_tt = TobogganTrajectory(input_map=test_map, move_x=3, move_y=1)
    test_tt.traverse_slope()
    assert test_tt.trees_found == 7


def test_traverse_slope_part_2():
    from functools import reduce

    with open(f"{TEST_FILE_PATH}/test_input.txt") as f:
        test_map = f.read().splitlines()
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
            input_map=test_map, move_x=slope[0], move_y=slope[1]
        )
        test_tt.traverse_slope()
        trees_found_list.append(test_tt.trees_found)
    assert reduce((lambda x, y: x * y), trees_found_list) == 336
