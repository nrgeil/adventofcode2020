import os
import re

import yaml

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


class PassportChecker:
    EXPECTED_FIELDS = {
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
        'cid',
    }

    def __init__(self, input_file_path, valid_missing=None):
        self.input_data = None
        self.input_file_path = input_file_path
        raw_input = self.parse_input_file()
        self.parse_passports(raw_input)
        self.valid_missing = valid_missing
        if valid_missing:
            self.EXPECTED_FIELDS = self.EXPECTED_FIELDS.difference(set(valid_missing))
        self.valid_passport_count = 0
        with open(f'{FILE_PATH}/data_rules.yml') as f:
            self.data_rules = yaml.safe_load(f)

    def parse_input_file(self):
        input_list = []
        with open(self.input_file_path) as f:
            read_bytes = 0
            file_size = os.path.getsize(self.input_file_path)
            while read_bytes < file_size:
                passport = ''
                while True:
                    read_bytes += 1
                    c = f.read(1)
                    passport += c
                    if passport.endswith('\n\n') or read_bytes > file_size:
                        input_list.append(passport.replace('\n', ' ').strip())
                        break
        return input_list

    def parse_passports(self, raw_input):
        passport_list = []
        for passport in raw_input:
            passport_as_dict = {}
            data = passport.split(' ')
            for d in data:
                key, value = d.split(':')
                passport_as_dict[key] = value
            passport_list.append(passport_as_dict)
        self.input_data = passport_list

    def check_passport_valid(self, passport):
        if not self.EXPECTED_FIELDS.difference(set(passport.keys())):
            if self.check_valid_passport_data(passport):
                self.valid_passport_count += 1

    def check_valid_passport_data(self, passport):
        for k, v in passport.items():
            if k in ['byr', 'iyr', 'eyr']:
                length = self.data_rules[k]['length']
                min_value = self.data_rules[k]['min']
                max_value = self.data_rules[k]['max']
                if len(v) != length:
                    return False
                if int(v) < min_value or int(v) > max_value:
                    return False
            if k == 'hgt':
                unit = v[-2:]
                height = v[:-2]
                if unit not in ['cm', 'in']:
                    return False
                min_value = self.data_rules[k][unit]['min']
                max_value = self.data_rules[k][unit]['max']
                if int(height) < min_value or int(height) > max_value:
                    return False
            if k == 'hcl':
                start_character = self.data_rules[k]['starts_with']
                length = self.data_rules[k]['length']
                valid_characters = self.data_rules[k]['valid_characters']
                regex = re.compile(valid_characters)
                if not v.startswith(start_character):
                    return False
                if not len(v) == length:
                    return False
                if not re.match(regex, v[1:]):
                    return False
            if k == 'ecl':
                valid_values = self.data_rules[k]['valid_values']
                if v not in valid_values:
                    return False
            if k == 'pid':
                length = self.data_rules[k]['length']
                valid_characters = self.data_rules[k]['valid_characters']
                regex = re.compile(valid_characters)
                if len(v) != length:
                    return False
                if not re.match(regex, v):
                    return False
        return True

    def check_all_passports(self):
        for passport in self.input_data:
            self.check_passport_valid(passport)


if __name__ == '__main__':
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/input.txt', valid_missing=['cid'])
    pc.check_all_passports()
    print(pc.valid_passport_count)
