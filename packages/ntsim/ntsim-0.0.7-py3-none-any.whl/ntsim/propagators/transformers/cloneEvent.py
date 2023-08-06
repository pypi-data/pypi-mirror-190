import numpy as np

class cloneEvent():
    # transform photons: shift and rotate
    def __init__(self):
        self.name = 'cloneEvent'
        import logging
        self.log = logging.getLogger(self.name)
        self.log.info('initialized')

    def configure(self, opts):
        self.n_events            = opts.cloner_n
        self.cylinder_center     = opts.cloner_cylinder_center_m
        self.cylinder_dimensions = opts.cloner_cylinder_dimensions_m
        self.accumulate_hits     = opts.cloner_accumulate_hits

    def transform(self,photons,id):
        photons.r = photons.r+self.random_shift[None,id,:]

    def generate_random_shifts(self) -> None:
        R = self.cylinder_dimensions[0]
        H = self.cylinder_dimensions[1]
        r = R*np.sqrt(np.random.uniform(size=self.n_events))
        phi = 2*np.pi*np.random.uniform(size=self.n_events)
        x = self.cylinder_center[0] + r*np.cos(phi)
        y = self.cylinder_center[1] + r*np.sin(phi)
        z = self.cylinder_center[2] + H*np.random.uniform(size=self.n_events)-0.5*H
        self.random_shift = np.array([x,y,z]).T
