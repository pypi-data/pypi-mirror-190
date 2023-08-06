import abc
from argparse import Namespace
# abstract class for all detectors
class BaseDetector(metaclass=abc.ABCMeta):
    def __init__(self,name):
        self.module_type = 'detector'
        self.geometry = None
        self.optical_module_model = None
        import logging
        self.log = logging.getLogger(name)
        self.log.info("initialized Detector")

    @abc.abstractmethod
    def configure(self,opts: Namespace) -> bool:
        self.log.info("configured")
