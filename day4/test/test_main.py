import os

import mock

from day4.main import PassportChecker

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def test_parse_input_file():
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_1.txt')
    test_raw_input = pc.parse_input_file()
    assert len(test_raw_input) == 4


def test_parse_passport():
    expected_passport1 = {'ecl': 'gry', 'pid': '860033327', 'eyr': '2020', 'hcl': '#fffffd', 'byr': '1937',
                          'iyr': '2017', 'cid': '147', 'hgt': '183cm'}
    expected_passport2 = {'iyr': '2013', 'ecl': 'amb', 'cid': '350', 'eyr': '2023', 'pid': '028048884',
                          'hcl': '#cfa07d', 'byr': '1929'}
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_1.txt')
    test_raw_input = pc.parse_input_file()
    pc.parse_passports(test_raw_input)
    assert pc.input_data[0] == expected_passport1
    assert pc.input_data[1] == expected_passport2


def test_check_passport_valid(test_passport):
    mocked_check_valid_passport_data = mock.Mock()
    with mock.patch.object(PassportChecker, 'check_valid_passport_data', mocked_check_valid_passport_data):
        pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_1.txt')
        pc.check_passport_valid(test_passport)
        assert pc.valid_passport_count == 1


def test_check_passport_invalid(test_passport):
    mocked_check_valid_passport_data = mock.Mock()
    with mock.patch.object(PassportChecker, 'check_valid_passport_data', mocked_check_valid_passport_data):
        pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_1.txt')
        test_passport.pop('ecl')
        pc.check_passport_valid(test_passport)
        assert pc.valid_passport_count == 0


def test_check_passport_valid_with_missing(test_passport):
    mocked_check_valid_passport_data = mock.Mock()
    with mock.patch.object(PassportChecker, 'check_valid_passport_data', mocked_check_valid_passport_data):
        pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_1.txt', valid_missing=['cid'])
        test_passport.pop('cid')
        pc.check_passport_valid(test_passport)
        assert pc.valid_passport_count == 1


def test_check_passport_invalid_with_missing(test_passport):
    mocked_check_valid_passport_data = mock.Mock()
    with mock.patch.object(PassportChecker, 'check_valid_passport_data', mocked_check_valid_passport_data):
        pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_1.txt', valid_missing=['cid'])
        test_passport.pop('ecl')
        test_passport.pop('cid')
        pc.check_passport_valid(test_passport)
        assert pc.valid_passport_count == 0


def test_check_valid_passport_check_data_called(test_passport):
    mocked_check_valid_passport_data = mock.Mock()
    with mock.patch.object(PassportChecker, 'check_valid_passport_data', mocked_check_valid_passport_data):
        pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
        pc.check_passport_valid(test_passport)
        assert mocked_check_valid_passport_data.call_count == 1


def test_check_invalid_passport_check_data_not_called(test_passport):
    mocked_check_valid_passport_data = mock.Mock()
    with mock.patch.object(PassportChecker, 'check_valid_passport_data', mocked_check_valid_passport_data):
        pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
        test_passport.pop('ecl')
        pc.check_passport_valid(test_passport)
        assert mocked_check_valid_passport_data.call_count == 0


def test_check_invalid_passport_data_byr(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['byr'] = '1910'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 0


def test_check_valid_passport_data_byr(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['byr'] = '2000'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 1


def test_check_invalid_passport_data_iyr(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['iyr'] = '2000'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 0


def test_check_valid_passport_data_iyr(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['iyr'] = '2015'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 1


def test_check_invalid_passport_data_eyr(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['eyr'] = '2000'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 0


def test_check_valid_passport_data_eyr(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['eyr'] = '2020'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 1


def test_check_invalid_passport_data_hgt_no_units(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['hgt'] = '190'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 0


def test_check_invalid_passport_data_hgt(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['hgt'] = '200cm'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 0


def test_check_valid_passport_data_hgt(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['hgt'] = '60in'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 1


def test_check_invalid_passport_data_hcl(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['hcl'] = '#123agc'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 0


def test_check_invalid_passport_data_hcl_special_characters(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['hcl'] = '#123ab^'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 0


def test_check_valid_passport_data_hcl(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['hcl'] = '#abc123'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 1


def test_check_invalid_passport_data_ecl(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['ecl'] = 'test'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 0


def test_check_valid_passport_data_ecl(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['ecl'] = 'amb'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 1


def test_check_invalid_passport_data_pid(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['pid'] = 'abc123123'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 0


def test_check_valid_passport_data_pid(test_passport):
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    test_passport['pid'] = '000123123'
    pc.check_passport_valid(test_passport)
    assert pc.valid_passport_count == 1


def test_part_1():
    mocked_check_valid_passport_data = mock.Mock(return_value=True)
    with mock.patch.object(PassportChecker, 'check_valid_passport_data', mocked_check_valid_passport_data):
        pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_1.txt', valid_missing=['cid'])
        pc.check_all_passports()
        assert pc.valid_passport_count == 2


def test_part_2():
    pc = PassportChecker(input_file_path=f'{FILE_PATH}/test_input_part_2.txt', valid_missing=['cid'])
    pc.check_all_passports()
    assert pc.valid_passport_count == 4
