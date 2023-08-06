from ntsim.Detector.BaseDetector import BaseDetector

class testDetector(BaseDetector):
    def __init__(self):
        super().__init__('testDetector')

    def configure(self,opts):
        import logging
        self.log = logging.getLogger('testDetector')
        self.log.info('configured')
