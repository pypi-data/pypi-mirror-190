class gProductionHeader:
    def __init__(self):
        self.n_events_original = -1
        self.n_events_cloned   = -1
        self.n_events_total    = -1
        self.primary_generator = ''
        self.primary_propagators = []
        self.photon_propagator = ''
        self.ray_tracer = ''
        self.cloner = ''
        self.photons_n_scatterings = 0
        self.photons_wave_range = []
        self.cloner_accumulate_hits = -1
        self.medium_scattering_model = ''
        self.medium_anisotropy = -2
