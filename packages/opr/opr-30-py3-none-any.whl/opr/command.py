# This file is placed in the Public Domain.


"handler"


from opr.message import Message


def __dir__():
    return (
            'Command',
           )


__all__ = __dir__()


class Command(Message):


    def __init__(self):
        Message.__init__(self)
        self.type = "command"
