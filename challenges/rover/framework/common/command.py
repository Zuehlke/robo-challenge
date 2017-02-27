# -*- coding: utf-8 -*-


def getattr_caller(dispatcher, command, args):
    if type(args) is list:
        getattr(dispatcher, command)(*args)
    else:
        getattr(dispatcher, command)(args)


def join_args(*args):
    out = []

    for outer in args:
        if type(outer) is list:
            for inner in outer:
                out.append(inner)
        else:
            out.append(outer)

    return out


class CommandDispatcher:
    """
    Command dispatcher
    """

    MSG_COMMAND = 'command'
    MSG_ARGS = 'args'

    def __init__(self, cmd):
        """

        :param cmd:
        """
        strategies = {}

        methods = [method for method in dir(cmd) if callable(getattr(cmd, method))]

        for m in methods:

            if not m.startswith('_'):
                strategies[m] = m

        self.strategies = strategies
        self.dispatcher = cmd

    def exec(self, msg, method_caller=getattr_caller):
        """
        :param msg: the command as msg (dict) which should be executed ({command: 'foo', args = []})
        :param method_caller: the function used to call the method on the dispatcher
        :return:
        """
        if not msg:
            raise RuntimeError('Wrong format "None"!')

        if not hasattr(msg, "__getitem__"):
            raise RuntimeError('Wrong format, property "command" has no value!')

        if self.MSG_COMMAND in msg:

            command = msg[self.MSG_COMMAND]

            if command in self.strategies:
                if self.MSG_ARGS in msg:
                    # command has args
                    method_caller(self.dispatcher, command, msg[self.MSG_ARGS])

                else:
                    # command has no args
                    method_caller(self.dispatcher, command, [])

            else:
                raise NameError('The command "%s" was not found in strategies!' % command)

        else:
            raise RuntimeError('Wrong format, property "command" not found!')


class TopicAwareCommandDispatcher:
    def __init__(self, cmd):
        self.command_dispatcher = CommandDispatcher(cmd)

    def exec(self, topic, msg):
        self.command_dispatcher.exec(msg, method_caller=TopicAwareCommandDispatcher.call_with_topic(topic))

    @staticmethod
    def call_with_topic(topic):
        return lambda dispatcher, command, args: getattr_caller(dispatcher, command, join_args(topic, args))

