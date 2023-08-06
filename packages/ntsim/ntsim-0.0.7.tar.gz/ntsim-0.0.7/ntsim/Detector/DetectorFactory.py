from argparse import Namespace
import sys
from ntsim.Detector.testDetector import testDetector

class DetectorFactory():
    def __init__(self):
        import logging
        self.log = logging.getLogger('DetectorFactory')

        self.detector = None
        self.known_detectors = {'testDetector': testDetector}
        '''
        # it knows only about pip packages (we want to use also those from PYTHONPATH)
        import pkg_resources
        available_packages = [pkg.key for pkg in pkg_resources.working_set]
        if 'bgvd-model' in available_packages:
            from ntsim.Detector.GVDDetector import GVDDetector
            self.known_detectors['GVDDetector'] = GVDDetector
        '''
        try:
            import bgvd_model
            from ntsim.Detector.GVDDetector import GVDDetector
            self.known_detectors['GVDDetector'] = GVDDetector
        except:
            self.log.warning("No package bgvd-model")


    def configure(self,opts: Namespace) -> None:
        if opts.detector_name in self.known_detectors:
            self.detector = self.known_detectors[opts.detector_name]()
        else:
            self.log.error(f'unknown detector name={opts.detector_name}')
            self.log.info(f'known detectors are: {list(self.known_detectors.keys())}. EXIT')
            sys.exit()

    def get_detector(self):
        return self.detector
