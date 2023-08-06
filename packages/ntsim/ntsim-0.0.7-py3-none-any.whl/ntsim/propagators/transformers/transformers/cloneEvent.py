import numpy as np
from ntsim.propagators.PropagatorBase import PropagatorBase

class cloneEvent(PropagatorBase):
    # transform photons: shift and rotate
    def __init__(self):
        super().__init__('cloneEvent')

    def configure(self, opts):
        self.n_events            = opts.clone_events
        self.cylinder_center     = opts.clone_cylinder_center_m
        self.cylinder_dimensions = opts.clone_cylinder_dimensions_m
        log.info("configured")
