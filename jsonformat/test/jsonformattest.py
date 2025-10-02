#!/usr/bin/python3

import unittest


class TestX(unittest.TestCase):
    def test_x(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
