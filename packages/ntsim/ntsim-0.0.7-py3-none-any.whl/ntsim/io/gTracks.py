import numpy as np
import logging
log = logging.getLogger('Tracks')

class gTracks:

    def __init__(self, label="") -> None:
        self.label = label
        self.data = np.empty((0,8), dtype=float)


    def __len__(self):
        return self.get_number_of_tracks()


    def add_tracks(self, new_data):
        self.data = np.concatenate((self.data, new_data))


    def rearrange_uids(self):
        new_uid = np.ones(np.shape(self.data[:, 0]), dtype=float)
        counter = 1
        mind = self.data[:, 0][0]
        for n in range(len(new_uid)-1):
            new_uid[n+1] = counter
            if mind == self.data[:, 0][n+1]:
                mind = self.data[:, 0][n+1]
            else:
                new_uid[n+1] += 1
                mind = self.data[:, 0][n+1]
                counter += 1
        self.data[:, 0] = new_uid


    def get_named_data(self):
        self.data_type = [('uid', int), ('gen', int), ('pdgid', int),
                          ('x_m', float), ('y_m', float), ('z_m', float),
                          ('t_ns', float), ('E_GeV', float)]
        return np.array([tuple(row) for row in self.data], dtype=self.data_type)


    def get_number_of_tracks(self):
        return len(np.unique(self.data[:,0]))
