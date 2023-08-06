import abc
from argparse import Namespace

# abstract class for all propagators
class PrimaryGeneratorBase(metaclass=abc.ABCMeta):
    def __init__(self,name):
        self.name = name
        self.module_type = 'generator'
#        self.data = {}
        import logging
        self.log = logging.getLogger(name)
        self.log.info("initialized Primary Generator")

#    @abc.abstractmethod
#    def next(self):
#        pass

    @abc.abstractmethod
    def configure(self,opts: Namespace) -> bool:
        pass

    @abc.abstractmethod
    def make_event(self,event):
        pass

#    @abc.abstractmethod
#    def __next__(self):
#        pass
