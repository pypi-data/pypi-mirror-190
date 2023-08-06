import abc
from argparse import Namespace
# abstract class for all propagators
class PropagatorBase(metaclass=abc.ABCMeta):
    def __init__(self,name):
        self.name = name
        self.module_type = 'propagator'
        import logging
        self.log = logging.getLogger(name)
        self.log.info("initialized propagator")

    @abc.abstractmethod
    def propagate(self,event):
        pass

    @abc.abstractmethod
    def configure(self,opts: Namespace) -> bool:
        pass
