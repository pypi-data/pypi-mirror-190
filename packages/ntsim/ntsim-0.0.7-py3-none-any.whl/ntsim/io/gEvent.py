import itertools
from ntsim.io.gEventHeader import gEventHeader
from ntsim.io.gProductionHeader import gProductionHeader
from ntsim.io.gPrimaryHeader import gPrimaryHeader

class gEvent(object):
    def __init__(self):
        self.prodHeader    = gProductionHeader()
        self.primaryHeader = gPrimaryHeader()
        self.evtHeader     = gEventHeader()
        self.photons           = None # gPhotons object
        self.particles         = []   # list of objects of class gParticles
        self.tracks            = []   # list of objects of class gTracks
        self.hits              = []   # list of objects of class gHits
        self.photons_generator = ()   # generator of gPhotons objects

        self.reset()

        import logging
        self.log = logging.getLogger('gEvent')

    def copy(self):
        new_event = gEvent()
        new_event.evtHeader     = self.evtHeader
        new_event.prodHeader    = self.prodHeader
        new_event.primaryHeader = self.primaryHeader
        new_event.photons       = self.photons
        new_event.particles     = self.particles
        new_event.tracks        = self.tracks
        new_event.hits          = self.hits
        return new_event

    def reset(self):
        self.evtHeader.n_bunches = 0
        self.evtHeader.n_photons_total = 0
        self.photons           = None
        self.particles         = []   # list of objects of class gParticles
        self.tracks            = []   # list of objects of class gTracks
        self.hits              = []   # list of objects of class gHits
        self.photons_generator = () # generator of gPhotons objects

    def has_particles(self):
        return len(self.particles) > 0

    def has_tracks(self):
        return len(self.tracks) > 0

    def has_hits(self):
        return len(self.hits) > 0

    def __print__(self):
        self.print_event()

    def add_particles(self, new_particles):
        self.particles.append(new_particles)

    def add_tracks(self, new_tracks):
        self.tracks.append(new_tracks)

    def add_photons_generator(self, new_generator):
        self.photons_generator = itertools.chain(self.photons_generator, new_generator)

    def add_hits(self, new_hits):
        # if label exists, add hits to the same folder
        # else create new folder
        label = new_hits.label
        hits_labels = [h.label for h in self.hits]
        try:
            i = hits_labels.index(label)
            self.hits[i].add_hits(new_hits.data)
        except:
            self.hits.append(new_hits)

    def print_event(self): # TODO : implement print()
        self.log.info("...................")
        #self.gEventHeader.print()
        self.log.info("Event summary:")
        self.log.info("  Particles: ")
        for p in self.particles:
            self.log.info(f"    {p.label}: {p.n_particles} particles")
        self.log.info("  Tracks: ")
        for t in self.tracks:
            self.log.info(f"    {t.label}: {len(t)} tracks")
        self.log.info("  Photons: ")
        self.log.info(f"    {self.evtHeader.n_photons_total} photons in {self.evtHeader.n_bunches} bunches")
        self.log.info("  Hits: ")
        for h in self.hits:
            self.log.info(f"    {h.label}: {len(h)} hits")
        self.log.info("...................")
