# -*- coding: utf-8 -*-
import unittest
import common as api

MIN = 5
MAX = 10


class TestWrapper:
    @api.min(MIN)
    def min_value(self, value):
        return value

    @api.max(MAX)
    def max_value(self, value):
        return value

    @api.max(MAX)
    @api.min(MIN)
    def range(self, value):
        return value

    @api.check_int
    def integer(self, value):
        return value

    @api.check_int
    @api.min(MIN)
    @api.max(MAX)
    def int_range(self, value):
        return value


class BasicTestSuite(unittest.TestCase):

    def test_min_not_ok(self):
        t = TestWrapper()

        try:
            t.min_value(MIN - 1)
            self.fail("Exception not thrown")
        except ValueError as e:
            pass

    def test_min_ok(self):
        t = TestWrapper()

        self.assertEqual(MIN, t.min_value(MIN))

    def test_min_is_float(self):
        t = TestWrapper()
        self.assertEqual(MIN, t.min_value(5.0))

    def test_min_float_not_ok(self):
        t = TestWrapper()

        try:
            t.min_value(4.9)
            self.fail("Exception not thrown")
        except ValueError as e:
            pass

    def test_max_ok(self):
        t = TestWrapper()

        self.assertEqual(MAX, t.max_value(MAX))

    def test_max_not_ok(self):
        t = TestWrapper()

        try:
            t.max_value(MAX + 1)
            self.fail("Exception not thrown")
        except ValueError as e:
            pass

    def test_range_ok(self):
        t = TestWrapper()
        self.assertEqual(MAX, t.range(MAX))
        self.assertEqual(MIN, t.range(MIN))

    def test_range_not_ok(self):
        t = TestWrapper()

        try:
            t.range(MAX + 1)
            self.fail("Exception not thrown")
        except ValueError as e:
            pass

        try:
            t.range(MIN - 1)
            self.fail("Exception not thrown")
        except ValueError as e:
            pass

    def test_integer_ok(self):
        t = TestWrapper()

        self.assertEqual(1, t.integer(1))

    def test_integer_nok(self):
        t = TestWrapper()

        try:
            t.integer(1.0)
            self.fail("Exception not thrown")
        except ValueError as e:
            pass

    def test_int_range(self):
        t = TestWrapper()

        self.assertEqual(MAX, t.int_range(MAX))
        self.assertEqual(MIN, t.int_range(MIN))
        
    def test_int_range_nok(self):
        t = TestWrapper()

        try:
            t.int_range(MAX + 1)
            self.fail("Exception not thrown")
        except ValueError as e:
            pass

        try:
            t.int_range(MIN - 1)
            self.fail("Exception not thrown")
        except ValueError as e:
            pass

        try:
            t.int_range(MIN + 0.0)
            self.fail("Exception not thrown")
        except ValueError as e:
            pass

        try:
            t.int_range(MAX + 0.0)
            self.fail("Exception not thrown")
        except ValueError as e:
            pass
