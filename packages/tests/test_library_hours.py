""" Test for working library_hours.py """
import unittest
from academic.library_hours import find_open


class test_library_hours(unittest.TestCase):

    # call function, check return type - string
    def test_find_open(self):
        print("Test Function: Find Open - Library \n")
        open_lib = find_open()
        return open_lib

    # def test_libraries_msg(self):
    # 	result = "hey"
    # 	lib = libraries_msg(result)
    # 	return lib


# run test, print to stdout
if __name__ == '__main__':
    unittest.main()
