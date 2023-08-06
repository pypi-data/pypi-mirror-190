import numpy as np
import logging
log = logging.getLogger('Hits')

class gHits:

    def __init__(self, label=""):
        self.data = np.empty((0,15), dtype=float)
        self.label = label

    def __len__(self):
        return self.data.shape[0]


    def add_hits(self, new_data):
        self.data = np.concatenate((self.data, new_data))


    def get_named_data(self):
        self.data_type = [('uid', int), ('cluster', int), ('id', int),
                          ('time_ns', float),
                          ('w_noabs', float), ('w_pde', float), 
                          ('w_gel', float), ('w_angular', float),
                          ('x_m', float), ('y_m', float), ('z_m', float),
                          ('outside_mask', float), ('photon_id', int),
                          ('step_number', int), ('weight',float)]
        return np.array([tuple(row) for row in self.data], dtype=self.data_type)


    def get_number_of_hits(self):
        return len(self.data)
