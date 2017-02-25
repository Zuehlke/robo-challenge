# -*- coding: utf-8 -*-
import unittest
import common as api


class Caller:

    def __init__(self):
        self.foo_called = False
        self.one_called = False
        self.two_called = False

    def foo(self):
        self.foo_called = True

    def one(self, arg1):
        self.one_called = True

    def two(self, arg1, arg2):
        self.two_called = True


class BasicTestSuite(unittest.TestCase):

    def test_init(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        self.assertTrue(len(ce.strategies) == 3)

    def test_exec(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        ce.exec({'command': 'foo'})
        self.assertEqual(True, caller.foo_called)

    def test_exec_one_args(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        ce.exec({'command': 'one', 'args': ['test']})
        self.assertEqual(True, caller.one_called)

    def test_exec_tow_args(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        ce.exec({'command': 'two', 'args': ['test1', 'test2']})
        self.assertEqual(True, caller.two_called)

    def test_exec_with_simple_args(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        ce.exec({'command': 'one', 'args': 'test'})
        self.assertEqual(True, caller.one_called)

    def test_command_not_found(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        with self.assertRaises(NameError):
            ce.exec({'command': 'missing'})
            self.fail()

    def test_exec_missing_args(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        with self.assertRaises(TypeError):
            ce.exec({'command': 'one'})
            self.fail()

    def test_wrong_format(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        with self.assertRaises(RuntimeError):
            ce.exec({'cmd': 'd'})
            self.fail()

    def test_command_null(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        with self.assertRaises(RuntimeError):
            ce.exec({'command'})
            self.fail()

    def test_none(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        with self.assertRaises(RuntimeError):
            ce.exec(None)
            self.fail()


class TopicCaller:
    def __init__(self):
        self.topic = None
        self.arg = None

    def one(self, topic, arg):
        self.topic = topic
        self.arg = arg

    def two(self, topic):
        self.topic = topic


class TopicAwareCommandDispatcher(unittest.TestCase):
    def test_init(self):
        caller = TopicCaller()
        dispatcher = api.TopicAwareCommandDispatcher(caller)

        self.assertIsNotNone(dispatcher.command_dispatcher)

    def test_exec(self):
        caller = TopicCaller()
        dispatcher = api.TopicAwareCommandDispatcher(caller)

        dispatcher.exec("topic", {'command': 'one', 'args': ['arg']})

        self.assertEqual(caller.topic, "topic")
        self.assertEqual(caller.arg, "arg")

    def test_no_args_exec(self):
        caller = TopicCaller()
        dispatcher = api.TopicAwareCommandDispatcher(caller)

        dispatcher.exec("topic", {'command': 'two'})

        self.assertEqual(caller.topic, "topic")
        self.assertEqual(caller.arg, None)
