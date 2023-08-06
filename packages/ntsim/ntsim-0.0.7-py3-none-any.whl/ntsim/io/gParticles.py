import numpy as np
import logging
log = logging.getLogger('Particles')

class gParticles():
    def __init__(self,number_of_particles=2, label="") -> None:
        self.n_particles = 0
        self.label = label
        self.data_type = [('gen',int),('pdgid',int),
                          ('x_m',float),('y_m',float),('z_m',float),('t_ns',float),
                          ('Px_GeV',float),('Py_GeV',float),('Pz_GeV',float),('Etot_GeV',float),
                          ('status', int)]
        self.max_number = number_of_particles
        self.data = np.zeros(shape=(self.max_number), dtype=self.data_type)
        return

    def add_particle(self, gen, pdgid, x_m, y_m, z_m, t_ns, Px_GeV, Py_GeV, Pz_GeV, Etot_GeV, status=0) -> None:

        if self.n_particles>self.max_number-1:
            # the number of particles exceed assumed array size.
            particles = np.zeros(shape=(self.max_number),dtype=self.data_type)
            self.data = np.concatenate((self.data,particles),axis=0)
            self.max_number = self.data.shape[0]

        self.data[self.n_particles]['gen'] = gen
        self.data[self.n_particles]['pdgid'] = pdgid
        self.data[self.n_particles]['x_m'] = x_m
        self.data[self.n_particles]['y_m'] = y_m
        self.data[self.n_particles]['z_m'] = z_m
        self.data[self.n_particles]['t_ns'] = t_ns
        self.data[self.n_particles]['Px_GeV'] = Px_GeV
        self.data[self.n_particles]['Py_GeV'] = Py_GeV
        self.data[self.n_particles]['Pz_GeV'] = Pz_GeV
        self.data[self.n_particles]['Etot_GeV'] = Etot_GeV
        self.data[self.n_particles]['status'] = status
        self.n_particles +=1
        return

    def get_particles(self): # FIXME : depricated, use get_data()
        return self.data[0:self.n_particles] ## TODO: check it!

    def get_data(self):
        return self.data[0:self.n_particles] ## TODO: check it!
        
    def get_named_data(self):
        return self.get_data()

    def get_number_of_particles(self):
        return self.n_particles

    def print(self):
        for i in range(self.n_particles):
            pdgid = self.data[i]['pdgid']
            x = self.data[i]['x_m']
            y = self.data[i]['y_m']
            z = self.data[i]['z_m']
            t = self.data[i]['t_ns']
            px = self.data[i]['Px_GeV']
            py = self.data[i]['Py_GeV']
            pz = self.data[i]['Pz_GeV']
            status = self.data[i]['status']

            log.info(f'particle status={status}, pdgid={pdgid}, (x,y,z)=({x},{y},{z}), (px,py,pz)=({px},{py},{pz})')
