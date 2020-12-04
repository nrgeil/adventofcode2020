# Part 1
import re

num_valid = 0
with open("2.txt") as f:
    for password_line in f.readlines():
        num_occurrences, letter, password = password_line.split(" ")
        test_password = re.findall(rf'{letter.replace(":", "")}', password)
        min_occ, max_occ = num_occurrences.split("-")
        if int(min_occ) <= len(test_password) <= int(max_occ):
            num_valid += 1
print(num_valid)

# Part 2
num_valid = 0
with open("2.txt") as f:
    for password_line in f.readlines():
        positions, letter, password = password_line.split(" ")
        letter = letter.replace(":", "")
        include_position, exclude_position = positions.split("-")
        pos1_has_letter = (
            True if password[int(include_position) - 1] == letter else False
        )
        pos2_has_letter = (
            True if password[int(exclude_position) - 1] == letter else False
        )
        if (pos1_has_letter and not pos2_has_letter) or (
            not pos1_has_letter and pos2_has_letter
        ):
            num_valid += 1
print(num_valid)
