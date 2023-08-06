from ntsim.primaryGenerators.PrimaryGeneratorBase import PrimaryGeneratorBase
from ntsim.primaryGenerators.Diffuser import DiffuserExponential,DiffuserCone
from ntsim.utils.gen_utils import generate_cherenkov_spectrum
import numpy as np

class Laser(PrimaryGeneratorBase):
    def __init__(self):
        super().__init__('Laser')
#        import logging
#        self.log = logging.getLogger('Laser')
        self.diffuser = None

    def configure(self,opts):
        self.waves = opts.photons_wave_range
        self.n_bunches = opts.photons_bunches
        self.photon_weight = opts.photons_weight
        self.steps = 1
        self.n_photons = int(opts.laser_n_photons/opts.photons_bunches)
        self.direction = opts.laser_direction
        self.position = opts.laser_position
        if opts.laser_diffuser[0] == 'exp':
            self.diffuser = DiffuserExponential(float(opts.laser_diffuser[1]))
        elif opts.laser_diffuser[0] == 'cone':
            self.diffuser = DiffuserCone(float(opts.laser_diffuser[1]))
        from ntsim.io.gPhotons import gPhotons
        self.photons = gPhotons()
        self.log.info('configured')
        return

    def get_direction(self):
        dir0 = np.array(self.direction,dtype=np.float64)
        if not self.diffuser:
            self.dir = np.tile(dir0,(self.steps,self.n_photons,1))
        else:
            dir = np.tile(dir0,(self.n_photons,1))
            dir = self.diffuser.random_direction(dir)
            dir = np.tile(dir,(self.steps))
            dir = np.reshape(dir,(self.n_photons,self.steps,3))
            dir = np.swapaxes(dir, 0, 1)
            self.dir = dir

    def make_photons(self):
        self.get_direction()
        self.r  = np.tile(np.array(self.position,dtype=np.float64), (self.steps,self.n_photons,1))
        self.t = np.tile(np.array([0.],dtype=np.float64),(self.steps,self.n_photons))
        wavelengths = np.tile(np.array([self.waves[0]],dtype=np.float64),self.n_photons)
        self.photons.init(self.n_photons,self.steps,self.r,self.t,self.dir,wavelengths,weight=self.photon_weight)
        return self.photons

    def make_event(self, event):
        event.photons_generator = self.make_photons_generator()

    def make_photons_generator(self):
        for i in range(self.n_bunches):
            yield self.make_photons()
