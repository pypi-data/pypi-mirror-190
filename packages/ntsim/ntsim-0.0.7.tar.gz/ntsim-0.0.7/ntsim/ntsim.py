import logging
log=logging.getLogger('NTsim')
logformat='[%(name)20s ] %(levelname)8s: %(message)s'
logging.basicConfig(format=logformat)
import sys
from argparse                       import Namespace
from email.policy                   import default
from ntsim.utils.report_timing      import report_timing
from ntsim.io.gHits                 import gHits
from ntsim.Medium.Medium            import Medium
from ntsim.io.h5Writer              import h5Writer
from ntsim.io.gEvent                import gEvent
from ntsim.Detector.DetectorFactory import DetectorFactory
import numpy as np

class NTsim:
    def __init__(self, opts):
        self.detector                  = None
        self.primary_generator         = None
        self.primary_propagators       = []
        self.photon_propagator         = None
        self.cloner                    = None
        self.known_primary_generators  = {}
        self.known_primary_propagators = {}
        self.known_photon_propagators  = {}
        self.known_ray_tracers         = {}
        self.known_transformers        = {}
        #
        self.init_known_primary_generators()
        self.init_known_propagators()
        self.init_known_transformers()
        self.init_primary_generator(opts)
        self.init_propagators(opts)
        self.detectorFactory = DetectorFactory()
        self.medium          = Medium()
        self.event           = gEvent()
        self.writer          = h5Writer()
        self.opts = opts
        log.info('initialized')

    def init_known_primary_generators(self) -> None:
        from ntsim.primaryGenerators.Laser  import Laser
        from ntsim.primaryGenerators.ToyGen import ToyGen
        self.known_primary_generators['Laser'] = Laser
        self.known_primary_generators['ToyGen'] = ToyGen

    def init_known_propagators(self) -> None:
        from ntsim.propagators.primaryPropagators.particlePropagator import particlePropagator
        from ntsim.propagators.photonPropagators.mcPhotonPropagator  import mcPhotonPropagator
        from ntsim.propagators.RayTracers.smartRayTracer             import smartRayTracer
        self.known_primary_propagators['particlePropagator'] = particlePropagator
        self.known_photon_propagators['mcPhotonPropagator']  = mcPhotonPropagator
        self.known_ray_tracers['smartRayTracer']             = smartRayTracer

    def init_known_transformers(self) -> None:
        from ntsim.propagators.transformers.cloneEvent import cloneEvent
        self.known_transformers['cloneEvent'] = cloneEvent

    def init_primary_generator(self,opts) -> None:
        if opts.primary_generator in self.known_primary_generators:
            self.primary_generator = self.known_primary_generators[opts.primary_generator]()
        else:
            log.error(f'unknown primary generator name={opts.primary_generator}')
            log.error('set primary generator with "--primary_generator" argument')
            log.error(f'known primary generators are: {list(self.known_primary_generators.keys())}. EXIT')
            sys.exit()

    def init_propagators(self,opts):
        if len(opts.primary_propagators):
            for p in opts.primary_propagators:
                if p in self.known_primary_propagators:
                    self.primary_propagators.append(self.known_primary_propagators[p]())
                else:
                    log.error(f"'{p}': no such propagator!")
                    sys.exit()
        if opts.photon_propagator in self.known_photon_propagators:
            self.photon_propagator = self.known_photon_propagators[opts.photon_propagator]()
        if opts.cloner in self.known_transformers:
            self.cloner = self.known_transformers[opts.cloner]()

        if opts.ray_tracer in self.known_ray_tracers:
            self.ray_tracer = self.known_ray_tracers[opts.ray_tracer]()

    def configure(self,opts: Namespace) -> None:
        self.n_events = opts.n_events
        self.detectorFactory.configure(opts)
        self.detector = self.detectorFactory.get_detector()
        self.detector.configure(opts)
        self.medium.configure(opts)
        self.primary_generator.configure(opts)
        self.configure_propagators(opts)
        self.writer.configure(opts)
        log.info('configured')

    def configure_propagators(self,opts):
        for p in self.primary_propagators:
            p.configure(opts)
        self.photon_propagator.configure(opts)
        self.cloner.configure(opts)


    def writePrimaryHeader(self): # FIXME : should be implemented in h5Writer / gEvent?
        self.event.gPrimaryHeader.set_name(self.primary.primary_name)
        self.event.gPrimaryHeader.set_track(self.primary.primary_track)
        self.writer.write_primary_header(self.event.gPrimaryHeader)

    def writeProductionHeader(self): # FIXME : should be implemented in h5Writer / gEvent?
        prodHeader = self.event.prodHeader
        prodHeader.n_events_original = self.n_events
        prodHeader.n_events_cloned   = self.cloner.n_events
        prodHeader.n_events_total    = self.n_events
        if self.cloner.n_events:
            prodHeader.n_events_total *= self.cloner.n_events

        prodHeader.primary_generator   = self.primary_generator.name
        prodHeader.primary_propagators = [p.name for p in self.primary_propagators]
        prodHeader.photon_propagator   = self.photon_propagator.name
        prodHeader.ray_tracer          = self.ray_tracer.name
        prodHeader.cloner              = self.cloner.name

        prodHeader.photons_n_scatterings = self.opts.photons_n_scatterings
        prodHeader.photons_wave_range = self.opts.photons_wave_range
        prodHeader.cloner_accumulate_hits = self.cloner.accumulate_hits
        prodHeader.medium_scattering_model = self.medium.model.name
        prodHeader.medium_anisotropy = self.medium.model.g
        self.writer.write_prod_header(self.event.prodHeader)


    def write_event_header(self): # FIXME : should be implemented in h5Writer / gEvent?
        eventHeader = self.event.evtHeader
        eventHeader.set_photons_sampling_weight(opts.photon_suppression)
        eventHeader.set_om_area_weight(self.get_om_area_weight())
        self.writer.write_event_header(eventHeader)

    def propagate_primaries(self, event):
        if len(self.primary_propagators):
            for propagator in self.primary_propagators:
                propagator.propagate(event)
            return

    def get_om_area_weight(self):
        return np.power(self.detector.true_radius/self.detector.prod_radius,2)

    def process_clones(self):
        self.cloner.generate_random_shifts()
        photons = self.event.photons
        r = photons.r
        for clone_id in range(self.cloner.n_events):
            self.cloner.transform(photons,clone_id)
            if self.cloner.accumulate_hits:
                hit_label = "all_hits"
            else:
                hit_label = f"clone_{clone_id}"
            self.ray_tracer.propagate(self.event, self.detector, hit_label=hit_label)

    @report_timing
    def process(self):
        # yet under development

#        if opts.multithread:
#            self.primary.next_multithread(self.n_events)
#            return
        self.writer.init_h5()
        self.writer.write_geometry(self.detector)
        event_id = 0
        for i in range(self.n_events):
            log.info("---------------------------")
            log.info(f"Event #{i}")
            self.event.reset()
            #
            # photon emission
            self.primary_generator.make_event(self.event) # -> photons (in bunches) + primaries
            self.propagate_primaries(self.event) # adds photons + particles + tracks
            self.writer.new_event(i)
            self.writer.write_data(self.event.particles, folder_name='particles')
            self.writer.write_data(self.event.tracks, folder_name='tracks')
            for bunch_id, photons in enumerate(self.event.photons_generator):
                self.event.photons = photons
                self.photon_propagator.propagate(photons, self.medium) # simulate scattering steps for photons
                self.writer.write_photons(photons, bunch_id)
                self.event.evtHeader.n_bunches += 1
                self.event.evtHeader.n_photons_total += len(photons)
                if self.cloner.n_events:
                    self.process_clones()
                else:
                    self.ray_tracer.propagate(self.event, self.detector, hit_label="all_hits")
            self.event.print_event()
            self.write_event_header()
            self.writer.write_data(self.event.hits, folder_name='hits')

#
        self.writeProductionHeader() # must be called in the end
        log.info(f'events processed: total={event_id+1} (original/cloned = {self.n_events}/{self.cloner.n_events})')
        self.writer.close()



if __name__ == '__main__':
    __name__ = 'NTsim'
    from ntsim.arguments import parser
    p = parser()
    opts = p.parse_args()   # using p.parse_args() here may raise errors.
    if opts.log_level == 'deepdebug':
        print("Logging level deepdebug not implemented, using DEBUG instead")
        log.setLevel(logging.getLevelName("DEBUG"))
        logging.root.setLevel(logging.getLevelName("DEBUG")) # set global logging level
    else:
        log.setLevel(logging.getLevelName(opts.log_level.upper()))
        logging.root.setLevel(logging.getLevelName(opts.log_level.upper()))  # set global logging level

    opts.multithread = eval(opts.multithread.lower().capitalize())

#    log.info(p.format_values())

    simu= NTsim(opts)
    simu.configure(opts)
    simu.process()
