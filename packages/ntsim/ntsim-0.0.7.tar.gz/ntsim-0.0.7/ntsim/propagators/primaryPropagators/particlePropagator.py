import numpy as np
from ntsim.propagators.PropagatorBase import PropagatorBase
from ntsim.propagators.primaryPropagators.g4propagator import g4propagator
from ntsim.propagators.primaryPropagators.trackCherenkov import trackCherenkov
from ntsim.propagators.primaryPropagators.cascadeCherenkov import cascadeCherenkov
from ntsim.io.gTracks import gTracks
from ntsim.io.gParticles import gParticles
from ntsim.utils.report_timing import report_timing
from ntsim.utils.gen_utils import get_particle_name_by_pdgid

class particlePropagator(PropagatorBase):

    def __init__(self, g4cherenkov=False):
        super().__init__('particlePropagator')
        self.g4prop = g4propagator(cherenkov=g4cherenkov)
        self.ccprop = cascadeCherenkov()
        self.tcprop = trackCherenkov()

    def configure(self, opts):
        self.g4prop.configure(opts)
        self.ccprop.configure(opts)
        self.tcprop.configure(opts)
        self.log.info("configured")

    @report_timing
    def propagate(self, event) -> None:
        particles = gParticles(100000, "g4_cascade_starters")
        tracks = gTracks("g4_tracks")

        for input_particles in event.particles:
            for ip, input_particle_data in enumerate(input_particles.get_particles()):
                gen, pdgid, x_m, y_m, z_m, t_ns, Px_GeV, Py_GeV, Pz_GeV, Etot_GeV, status = input_particle_data
                if status != 0: # propagate particles only with status '0'
                    continue
                particle_name = get_particle_name_by_pdgid(pdgid)
                self.g4prop.setGunParticle(particle_name)
                self.g4prop.setGunPosition(x_m, y_m, z_m, "m")
                self.g4prop.setGunDirection(Px_GeV, Py_GeV, Pz_GeV)
                self.g4prop.setGunEnergy(Etot_GeV, "GeV")
                #
                g4output = self.g4prop.propagate()
                if self.g4prop.cherenkov:
                    casc_starters, new_tracks, g4_photons = g4output
                    event['photons'].append([g4_photons])
                else:
                    casc_starters, new_tracks = g4output

                #particles = np.concatenate((particles, casc_starters))
                for casc_data in casc_starters:
                    particles.add_particle(*casc_data, 0)
                tracks.add_tracks(new_tracks)
            tracks.rearrange_uids()

        event.add_particles(particles)
        event.add_tracks(tracks)
        event.add_photons_generator([self.ccprop.propagate(casc_starters)])
        event.add_photons_generator([self.tcprop.propagate(new_tracks)])

        return
