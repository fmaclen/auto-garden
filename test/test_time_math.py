import unittest
from lib.time_math import TimeMath

class TestTimeMath(unittest.TestCase):
    def setUp(self):
        self.tm = TimeMath()

    def test_datetime_str_to_tuple(self):
        self.assertEqual(
            self.tm.datetime_str_to_tuple('2023-07-23 12:30:00Z'), 
            (2023, 7, 23, 0, 12, 30, 0, 0, 0)
        )

    def test_datetime_str_to_timestamp(self):
        # '1970-01-01 00:00:00Z' is the start of Unix time, so it should be 0
        self.assertEqual(
            self.tm.datetime_str_to_timestamp('1970-01-01 00:00:00Z'), 
            0
        )

    def test_extract_datetime_components(self):
        self.assertEqual(
            self.tm.extract_datetime_components('2023-07-23 12:30:00Z'), 
            (2023, 7, 23, 12, 30, 0)
        )

    def test_is_leap_year(self):
        self.assertTrue(self.tm.is_leap_year(2000))  # 2000 is a leap year
        self.assertFalse(self.tm.is_leap_year(2001))  # 2001 is not a leap year

    def test_days_in_year(self):
        self.assertEqual(self.tm.days_in_year(2000), 366)  # 2000 is a leap year
        self.assertEqual(self.tm.days_in_year(2001), 365)  # 2001 is not a leap year

if __name__ == '__main__':
    unittest.main()
