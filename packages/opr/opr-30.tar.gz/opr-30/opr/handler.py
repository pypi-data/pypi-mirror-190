# This file is placed in the Public Domain.


"handler"


import inspect
import queue
import threading


from opv.objects import Object


from .listens import Listens
from .threads import launch


class Handler(Object):

    cmds = Object()
    errors = []


    def __init__(self):
        Object.__init__(self)
        self.cbs = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        Listens.add(self)

    def dispatch(self, event):
        if not event.isparsed:
            event.parse(event.txt)
        if not event.orig:
            event.orig = repr(self)
        func = getattr(Handler.cmds, event.cmd, None)
        if func:
            try:
                func(event)
            except Exception as ex:
                exc = ex.with_traceback(ex.__traceback__)
                Handler.errors.append(exc)
                event.ready()
                return None
            event.show()
        event.ready()

    def handle(self, event):
        func = getattr(self.cbs, event.type, None)
        if not func:
            event.ready()
            return
        event.__thr__ = launch(func, event)

    def loop(self):
        while not self.stopped.set():
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def put(self,event):
        if not event.orig:
            event.orig = repr(self)
        self.queue.put_nowait(event)

    def register(self, typ, cbs):
        if typ not in self.cbs:
            setattr(self.cbs, typ, cbs)

    def stop(self):
        self.stopped.set()

    def start(self):
        self.stopped.clear()
        launch(self.loop)


def scan(mod):
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        names = cmd.__code__.co_varnames
        if "event" in names:
            setattr(Handler.cmds, key, cmd)

