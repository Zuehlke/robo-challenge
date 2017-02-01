# -*- coding: utf-8 -*-
import unittest
import common as api


class Caller:
    def foo(self):
        print('foo')

    def one(self, arg1):
        print('one')

    def two(self, arg1, arg2):
        print('two')


class BasicTestSuite(unittest.TestCase):

    def test_init(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        self.assertTrue(len(ce.strategies) == 3)

    def test_exec(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        ce.exec({'command': 'foo'})

    def test_exec_one_args(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        ce.exec({'command': 'one', 'args': ['test']})

    def test_command_not_found(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        with self.assertRaises(NameError):
            ce.exec({'command': 'missing'})

    def test_exec_missing_args(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        with self.assertRaises(TypeError):
            ce.exec({'command': 'one'})

    def test_wrong_format(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        with self.assertRaises(RuntimeError):
            ce.exec({'cmd': 'd'})

    def test_command_null(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        with self.assertRaises(RuntimeError):
            ce.exec({'command'})

    def test_none(self):
        caller = Caller()
        ce = api.CommandDispatcher(caller)
        with self.assertRaises(RuntimeError):
            ce.exec(None)


class TopicCaller:
    def __init__(self):
        self.topic = None
        self.arg = None

    def one(self, topic, arg):
        self.topic = topic
        self.arg = arg


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
