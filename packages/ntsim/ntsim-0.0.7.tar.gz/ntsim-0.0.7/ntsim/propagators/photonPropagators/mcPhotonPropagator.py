from ntsim.utils.report_timing import report_timing
from ntsim.propagators.PropagatorBase import PropagatorBase

import numpy as np

class mcPhotonPropagator(PropagatorBase):
    def __init__(self):
        super().__init__('mcPhotonPropagator')

    def configure(self,opts):
        self.n_steps = opts.photons_n_scatterings
        self.log.info('configured')

    @report_timing
    def propagate(self, photons, medium) -> None:
        photons.n_steps = self.n_steps
        n_steps  = self.n_steps
        n_photons = photons.r.shape[1]
        photons.r = np.concatenate((photons.r, np.zeros((n_steps-1, n_photons, 3))), axis=0)
        photons.dir = np.concatenate((photons.dir, np.zeros((n_steps-1, n_photons, 3))), axis=0)
        photons.t = np.concatenate((photons.t, np.zeros((n_steps-1, n_photons))), axis=0)
        self.random_trajectories(photons, medium.get_model(photons))
        return

    def random_trajectories(self,photons,model):
        for step in range(1,photons.n_steps):
            photons.r[step], t_step = self.random_trajectory_step(photons.r[step-1], photons.dir[step-1],model)
            photons.t[step] = photons.t[step-1]+t_step
            photons.dir[step] = model.random_direction(photons.dir[step-1])
#            import IPython; IPython.embed(colors='neutral')
            photons.add_absorption_time(model.ta)
            photons.add_scattering_time(model.ts)

    def random_trajectory_step(self,r0,omega0,model):
        # make a random trajectory step starting from r0 in direction omega0
        # step length is random according to exp(-t/ts)
        # random time
        t = np.random.exponential(scale=model.ts)
        # make step in space
        dr = omega0*t[:,None]*model.light_velocity_medium[:,None]
        r = r0 + dr
        return r,t
