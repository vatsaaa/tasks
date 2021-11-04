"""
This is the class that every executor should inherit and implement run() at least
"""
from zope.interface import Interface
import json


class ITask(Interface):
    def run(self, countdown: int = 0):
        pass

    def persist(self, todb: bool = False):
        pass