#
# coding=utf-8

import cmd2
import thg_test


class Example(thg_test.darkcode, cmd2.Cmd):
    """An class to show how to use a plugin"""
    def __init__(self, *args, **kwargs):
        # gotta have this or neither the plugin or cmd2 will initialize
        super().__init__(*args, **kwargs)

    @thg_test.empty_decorator
    def do_something(self, arg):
        self.poutput('this is the something command')


if __name__ == '__main__':
    app = Example()
    app.cmdloop()
