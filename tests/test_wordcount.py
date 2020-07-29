#!/usr/bin/env python3
"""
Unit Test cases for wordcount

Students should not modify this file.
"""

import sys
import unittest
import importlib
try:
    # python2
    from StringIO import StringIO
except ImportError:
    # python3
    from io import StringIO

small_dict = {
    '--': 1, 'are': 3, 'at': 1, 'be': 3, 'but': 1, 'coach': 1, 'football': 1, 'least': 1,
    'need': 1, 'not': 3, 'should': 1, 'to': 2, 'used': 1, 'we': 6, 'what': 3
}

alice_top_20 = [
    '1605', '766', '706', '614', '518', '493', '421', '362',
    '352', '333', '265', '261', '249', '222', '221', '208',
    '206', '176', '169', '155'
    ]


class Capturing(list):
    """Context Mgr helper for capturing stdout from a function call"""
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


class TestWordcount(unittest.TestCase):
    def setUp(self):
        module_name = 'wordcount'
        """import the module(s) under test, in the context of this test fixture"""
        try:
            self.wc = importlib.import_module(module_name)
        except ImportError:
            self.fail('Unable to import module: ' + module_name)

    def test_function_defs(self):
        """Check if required functions are defined and callable"""
        self.assertTrue(callable(self.wc.create_word_dict),
                        "The create_word_dict() function is not defined")
        self.assertTrue(callable(self.wc.print_words),
                        "The print_words() function is not defined")
        self.assertTrue(callable(self.wc.print_top),
                        "The print_top() function is not defined")

    def test_print_words(self):
        """
        Check the console output from print_words()"""
        with Capturing() as output:
            self.wc.print_words("books/alice.txt")
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 4950)

    def test_print_top(self):
        """Check the console output from print_topcount()"""
        with Capturing() as output:
            self.wc.print_top("books/alice.txt")
        self.assertIsInstance(output, list)
        self.assertGreaterEqual(len(output), 20)
        self.assertLess(len(output), 25)
        for count in alice_top_20:
            self.assertIn(count, str(output))

    def test_create_word_dict(self):
        """Check if correct dict is generated"""
        filename = "books/small.txt"
        d = self.wc.create_word_dict(filename)
        self.assertIsInstance(d, dict)
        self.assertDictEqual(d, small_dict)

        filename = "books/alice.txt"
        d = self.wc.create_word_dict(filename)
        self.assertEqual(len(d), 4950)

    def test_frankenstein(self):
        """Check if Frankenstein book can be counted"""
        filename = "books/good/Frankenstein.txt"
        d = self.wc.create_word_dict(filename)
        self.assertEqual(len(d), 11724)


if __name__ == "__main__":
    unittest.main()
