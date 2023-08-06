from ntsim.Primary import *

class ChargedPrimary(Primary):

    def configure(self, opts):
        self.primary_name = 'ChargedTrack'
        self.configure_generator(opts)
        self.configure_propagators(opts)
        log.info('configured')

    def next(self):
        self.clear_data()
        print(self.primary_generator)
        primaries = self.primary_generator.next()
        while True:
            try:
                photons = next(primaries)
                hits = self.primary_propagator['mcPhotonTransporter'].transport(photons,
                                                                                self.medium.get_model(photons),
                                                                                self.geometry)
                self.add_photons(photons)
                self.add_hits(hits)
            except StopIteration:
                break
        self.write_data()

    def get_photons_sampling_weight(self):
        return 1.

    def get_vertices(self):
        return []
