from ntsim.propagators.RayTracers.utils import ray_tracing_gvd, detector_hits
from ntsim.utils.report_timing import report_timing
from ntsim.propagators.PropagatorBase import PropagatorBase
from ntsim.io.gHits import gHits

class smartRayTracer(PropagatorBase):
    def __init__(self):
        super().__init__('smartRayTracer')

    def configure(self):
        pass

    '''
    @report_timing
    def propagate(self, photons, detector) -> None:
        # find intersections of photon tracks with OM spheres
        hits      = ray_tracing_gvd(photons.r,photons.t,
                                    detector.geom, detector.bounding_box_cluster,
                                    detector.bounding_box_strings)
        # calculate expected signal in OMs (using numba)
        hit_data = detector_hits(photons.r,photons.t, photons.wavelength, photons.weight,
                                 detector.det_normals,hits, photons.ta)
#        hits = gHits("all_hits")
#        hits.data = hit_data
#        event.add_hits(hits, "all_hits")
        return hit_data

    '''

    @report_timing
    def propagate(self, event, detector, hit_label="all_hits") -> None:
        photons = event.photons
        # find intersections of photon tracks with OM spheres
        # TODO : rename 'hits' to something more specific ('hits' is used later for gHits instances)
        hits      = ray_tracing_gvd(photons.r,photons.t,
                                    detector.geom, detector.bounding_box_cluster,
                                    detector.bounding_box_strings)
        # calculate expected signal in OMs (using numba)
        hit_data = detector_hits(photons.r,photons.t, photons.wavelength, photons.weight,
                                 detector.det_normals,hits, photons.ta)
        hits = gHits(hit_label)
        hits.data = hit_data
        event.add_hits(hits)
