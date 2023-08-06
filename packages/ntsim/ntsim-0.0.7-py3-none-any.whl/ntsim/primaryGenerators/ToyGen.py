import numpy as np
from ntsim.io.gParticles import gParticles
#from ntsim.utils import gen_utils
from ntsim.primaryGenerators.PrimaryGeneratorBase import PrimaryGeneratorBase
from particle import Particle
from math import sqrt
class ToyGen(PrimaryGeneratorBase):
    def __init__(self):
        super().__init__('ToyGen')

    def configure(self, opts):
        self.particles = gParticles(1, "primary")
        gen = 0
        pdgid = int(Particle.from_evtgen_name(opts.particle).pdgid)
        mass_GeV = Particle.from_pdgid(pdgid).mass/1000 # in GeV
        energy = opts.energy
        abs_momentum = sqrt(energy**2-mass_GeV**2)
        position = opts.position
        time = 0
        momentum = np.array(opts.direction)*abs_momentum

        self.particles.add_particle(gen, pdgid, *position, time, *momentum, energy)
        self.log.info(f"  pdgid = {pdgid}, energy = {energy} GeV, momentum = {momentum} GeV")
        self.log.info(f"  position = {position} m")
        self.log.info(f"  direction = {opts.direction}")
        self.log.info('configured')

    def make_event(self, event):
        event.add_particles(self.particles)
