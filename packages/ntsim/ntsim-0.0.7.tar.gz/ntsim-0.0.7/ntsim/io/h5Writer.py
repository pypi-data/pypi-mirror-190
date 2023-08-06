import h5py
import numpy as np
import logging
log = logging.getLogger('h5Writer')
from ntsim.utils.report_timing import report_timing

class h5Writer:
    def __init__(self):
        self.event_folder = None

    def __del__(self):
        self.close()

    def configure(self,options):
        #
        self.save_geometry       = True # options.h5_save_geometry
        self.save_medium_model   = True # options.h5_save_medium_model
        self.save_prod_header    = True # options.h5_save_prod_header
        self.save_primary_header = True # options.h5_save_primary_header
        self.save_event_header   = True # options.h5_save_event_header
        #
        self.save_tracks       = options.h5_save_tracks
        self.save_particles    = options.h5_save_particles
        self.save_photons      = options.h5_save_photons
        self.save_hits         = options.h5_save_hits
        self.save_vertices     = options.h5_save_vertices
        self.h5_output_file    = options.h5_output_file
        self.h5_output_dir     = options.h5_output_dir
        log.info('configured')
        return

    def init_h5(self):
        import os
        if not os.path.exists(self.h5_output_dir):
            os.makedirs(self.h5_output_dir)
        log.info(f"open  {self.h5_output_dir}/{self.h5_output_file}.h5")
        self.h5_file =  h5py.File(f'{self.h5_output_dir}/{self.h5_output_file}.h5', 'w')

    def make_clones_folder(self,event_id):
        clone_folder = f'event_{event_id}/clones'
        print(f'{clone_folder}')
        if clone_folder not in self.h5_file.keys():
            self.h5_file.create_group(clone_folder)


    def add_clone_folder(self,event_id,clone_id):
        clone_folder = f'event_{event_id}/clones/clone_{clone_id}_hits'
        if clone_folder not in self.h5_file.keys():
            self.h5_file.create_group(clone_folder)
        folder = self.h5_file[clone_folder]

    def new_event(self, event_id):
        event_folder = f'event_{event_id}'
        if event_folder not in self.h5_file.keys():
            self.event_folder = self.h5_file.create_group(event_folder)
            if self.save_particles:
                self.event_folder.create_group('particles')
            if self.save_tracks:
                self.event_folder.create_group('tracks')
            if self.save_photons:
                self.event_folder.create_group('photons')
            if self.save_hits:
                self.event_folder.create_group('hits')
        else:
            self.event_folder = self.h5_file[event_folder]

    @report_timing
    def write_data(self, data_list, folder_name):
        if len(data_list) == 0:
            log.info(f"no {folder_name} to write to {folder_name}")
        if folder_name in self.event_folder.keys():
            folder = self.event_folder[folder_name]
            for data in data_list:
                log.info(f"writing {folder_name} ({data.label})")
                folder.create_dataset(data.label, data=data.get_named_data())


    def write_photons(self, photons, bunch_id):
        log.info(f"writing photon bunch #{bunch_id}")# ({list_of_bunches[0].label})")
        photon_folder = self.event_folder['photons']
        bunch_folder = photon_folder.create_group(f'photons_{bunch_id}')
        bunch_folder.create_dataset("weight",     data=photons.weight)
        bunch_folder.create_dataset("n_tracks",   data=photons.n_tracks)
        bunch_folder.create_dataset("n_steps",    data=photons.n_steps)
        bunch_folder.create_dataset("r",          data=photons.r)
        bunch_folder.create_dataset("t",          data=photons.t)
        bunch_folder.create_dataset("dir",        data=photons.dir)
        bunch_folder.create_dataset("wavelength", data=photons.wavelength)
        bunch_folder.create_dataset("ta",         data=photons.ta)
        bunch_folder.create_dataset("ts",         data=photons.ts)
        bunch_folder.attrs["label"] = photons.label

    def write_prod_header(self,productionHeader):
        if self.save_prod_header:
            g_header = self.h5_file.create_group('ProductionHeader')
            g_header.create_dataset("n_events_original",data=productionHeader.n_events_original)
            g_header.create_dataset("n_events_cloned",data=productionHeader.n_events_cloned)
            g_header.create_dataset("n_events_total",data=productionHeader.n_events_total)
            g_header.create_dataset("primary_generator",data=productionHeader.primary_generator)
            g_header.create_dataset("primary_propagators",data=productionHeader.primary_propagators)
            g_header.create_dataset("photon_propagator",data=productionHeader.photon_propagator)
            g_header.create_dataset("ray_tracer",data=productionHeader.ray_tracer)
            g_header.create_dataset("cloner",data=productionHeader.cloner)
            g_header.create_dataset("photons_n_scatterings",data=productionHeader.photons_n_scatterings)
            g_header.create_dataset("photons_wave_range",data=productionHeader.photons_wave_range)
            g_header.create_dataset("cloner_accumulate_hits",data=productionHeader.cloner_accumulate_hits)
            g_header.create_dataset("medium_scattering_model",data=productionHeader.medium_scattering_model)
            g_header.create_dataset("medium_anisotropy",data=productionHeader.medium_anisotropy)

    def write_primary_header(self,primHeader):
        if self.save_primary_header:
            g_header = self.h5_file.create_group('PrimaryHeader')
            g_header.create_dataset("name",data=primHeader.name)
            g_header.create_dataset("track",data=primHeader.track)

    def write_geometry(self,geometry):
        if self.save_geometry:
            geometry_folder = self.h5_file.create_group('geometry')
            geometry_folder.create_dataset('geom',data=geometry.geom)
            geometry_folder.create_dataset('bounding_box_strings',data=geometry.bounding_box_strings)
            geometry_folder.create_dataset('bounding_box_cluster',data=geometry.bounding_box_cluster)
            geometry_folder.create_dataset('det_normals',data=geometry.det_normals)


    def write_event_header(self,evtHeader):
        g_header = self.event_folder.create_group('event_header')
        g_header.create_dataset("photons_sampling_weight",data=evtHeader.photons_sampling_weight)
        g_header.create_dataset("om_area_weight",data=evtHeader.om_area_weight)
        g_header.create_dataset("n_bunches",data=evtHeader.n_bunches)
        g_header.create_dataset("n_photons_total",data=evtHeader.n_photons_total)

        return g_header

    @report_timing
    def close(self):
        try:
            log.info(f"close {self.h5_output_dir}/{self.h5_output_file}.h5")
            self.h5_file.close()
        except:
            log.warning("can not close h5 file properly")
