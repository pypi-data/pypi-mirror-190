class gEventHeader:
    def __init__(self):
        self.reset()
        import logging
        self.logger = logging.getLogger('gEventHeader')

    def reset(self):
        self.photons_sampling_weight = 1      # statistical weight of photons
        self.om_area_weight          = 1      # weight accounts for a larger area of optical module = np.power(true_radius/radius,2)
        self.n_bunches               = 0      # number of photons bunches
        self.n_photons_total         = 0      # total number of photons

    def set_photons_sampling_weight(self,w):
        self.photons_sampling_weight = w

    def get_photons_sampling_weight(self):
        return self.photons_sampling_weight

    def set_om_area_weight(self,w):
        self.om_area_weight = w

    def get_om_area_weight(self):
        return self.om_area_weight

    def print(self):
        self.logger.info(f'om_area_weight={self.om_area_weight:6.3E}')
        self.logger.info(f'photons_sampling_weight={self.photons_sampling_weight:6.3E}')
        self.logger.info(f'n_bunches={self.n_bunches:6.3E}')
        self.logger.info(f'n_photons_total={self.n_photons_total:6.3E}')
