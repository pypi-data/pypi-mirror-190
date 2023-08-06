def parser():
    import configargparse, argparse

    p = configargparse.get_argument_parser()
# ntsim options
    p.add_argument('-l', '--log-level', choices=('deepdebug', 'debug', 'info', 'warning', 'error', 'critical'), default='INFO', help='logging level')
#    p.add_argument('-p', '--primary_config',is_config_file=True,help='add primary config')
    p.add_argument('--geometry_config',is_config_file=True,default='configs/geometry.cfg',help='geometry config')
    p.add_argument("--h5writer_config", is_config_file=True,default='configs/h5writer.cfg',help="h5writer config")
    p.add_argument('--n_events',type=int,default=2,
                    help='number of events to process')
    # p.add_argument('-j','--jobs',type=int,default=-1,help='number of multithread jobs [-1:singlethread;0:automatic;N:N jobs]')
    p.add_argument('--multithread',choices=('true','false'),default='false',
                    help='run multithreaded') # TODO add limitation of number of threads
    p.add_argument('--primary_generator',
                    help='primary particle generator')
    p.add_argument('--primary_propagators',nargs='+',default=[],
                    help='simulation chain: primary --> photon emission')
    p.add_argument('--photon_propagator',default='mcPhotonPropagator',
                    help='simulation chain: emitted photons --> propagated photons')
    p.add_argument('--ray_tracer',default='smartRayTracer',
                    help="simulation chain: photons --> hits")
    p.add_argument('--cloner',default='cloneEvent',
                    help="clone events shifting and rotating photons")
    p.add_argument('--photon_suppression',type=int,default=1000,
                    help="only every n-th photon is stored")
    p.add_argument("--photons_weight",type=float,default=1,
                    help="statistical weight of a photon")
    p.add_argument("--photons_bunches",type=int,default=1,
                    help="number of bunches")
    p.add_argument("--photons_n_scatterings",type=int,default=5,
                    help="number of scatterings=n_steps")
    p.add_argument("--photons_wave_range",nargs='+',type=float,default=[350,600],
                    help="wavelengths interval")
    p.add_argument("--particle", default='mu-',
                   help="set particle by name, e.g. 'e-', 'gamma', 'mu+' (Geant4 names)")
    p.add_argument("--energy", default=100, type=float,
                   help="set particle total energy in GeV")
    p.add_argument("--position", nargs=3, default=[0, 0, 0], type=float,
                    help="set particle position in meters (format: x, y, z)")
    p.add_argument("--direction", nargs=3, default=[0, 0, 1], type=float,
                   help="set particle direction (format: dx, dy, dz))")
    p.add_argument("--cloner_accumulate_hits",type=bool,default=False,
                    help="accumulate hits for cloned events")

# Geometry options
    p.add_argument('--detector_name',default='testDetector',help='detector name')
    p.add_argument('--geometry_input',help='input file with geometry')
    p.add_argument('--geometry_output',help='output file with geometry')
    p.add_argument('--geometry_time_interval',nargs='+',help='time interval to read the geometry')
    p.add_argument('--geometry_clusters',nargs='+',type=int,help='list of clusters')
    p.add_argument('--geometry_true_radius',type=float,help='Optical Module true radius in m')
    p.add_argument('--geometry_prod_radius',type=float,help='Optical Module production radius in m')
# Medium options
    p.add_argument("--medium_scattering_model",default='HG',help="scattering model name: HG, Rayleigh, HG+Rayleigh")
    p.add_argument("--medium_anisotropy",type=float,default=0.99,help="light scattering anisotropy")
# h5Writer options
    p.add_argument("--h5_output_file",help="output file name")
    p.add_argument("--h5_output_dir",default="h5_output",help="output directory name")
    p.add_argument("--h5_save_geometry",default=False,help="Boolean to save geometry")
    p.add_argument("--h5_save_medium_model",default=False,help="Boolean to save water model: absorption & scattering")
    p.add_argument("--h5_save_prod_header",default=False,help="Boolean to save production header")
    p.add_argument("--h5_save_event_header",default=False,help="Boolean to save event header")
    p.add_argument("--h5_save_primary_header",default=False,help="Boolean to save event header")
    p.add_argument("--h5_save_tracks",type=bool,default=False,help="Boolean to save tracks")
    p.add_argument("--h5_save_particles",type=bool,default=False,help="Boolean to save particles")
    p.add_argument("--h5_save_photons",type=bool,default=False,help="Boolean to save photons")
    p.add_argument("--h5_save_hits",type=bool,default=False,help="Boolean to save hits")
    p.add_argument("--h5_save_vertices",default=False,help="Boolean to save vertices")
# clone options
    p.add_argument("--cloner_n",type=int,default=0,help="number of events to clone")
    p.add_argument("--cloner_cylinder_center_m",nargs='+',type=float,default=[0.,0.,0.],help="center of the cylinder used by photonTransformer")
    p.add_argument("--cloner_cylinder_dimensions_m",nargs='+',type=float,default=[0.,0.],help="[radius,height] of the cylinder used by photonTransformer")

# LaserPrimary options
    p.add_argument("--laser_n_photons",type=int,default=10000, help="number of photons to generate")
    p.add_argument("--laser_direction",nargs='+',type=float,default=[0.,0.,1.],help="unit three vector for photons direction")
    p.add_argument("--laser_position",nargs='+',type=float,default=[0.,0.,0.],help="three vector for laser position")
    p.add_argument("--laser_diffuser",nargs='+',default=('none',0),help="laser diffuser mode: (exp,sigma) or (cone, angle)")
# CorsikaGVDDataBankReader options
    p.add_argument("--corsika_GVD_DB_reader-config", is_config_file=True,default='configs/CorsikaGVDDataBankReader.cfg',help="Config for CorsikaGVDDataBankReader")
    p.add_argument('--corsika_GVD_DB_reader_input',help='Corsika GVD DataBase input file')
    p.add_argument('--corsika_GVD_DB_reader_max_records',default=0,help='Corsika GVD DataBase maximum number of readed rows')
# Geant4 options
    p.add_argument("--g4_casc_max", type=float, default=0.05,
                   help="set maximal energy to store cascade starters (as fraction of initial energy)")
    p.add_argument("--g4_enable_cherenkov", dest="g4_cherenkov", action="store_true",
                   help="enable production of phtons in Geant4")
    p.add_argument("--g4_random_seed", type=float, default=1,
                   help="set random seed for Geant4")
    p.add_argument("--g4_detector_height", type=float, default=1360.,
                   help="set height (in meters) of cylindrical detector volume")
    p.add_argument("--g4_detector_radius", type=float, default=1000.,
                   help="set radius (in meters) of cylindrical detector volume")
# particlePropagator options
#   cascadeCherenkov options
    p.add_argument("--casc_param_X0", type=float, default=0.3608, help="radiation lenght, in meters")
#   trackCherenkov options
    p.add_argument("--cherenkov_wavelengths", nargs=2, type=float, default=[350,650],
                   help="wavelength range")
    p.add_argument("--refraction_index", type=float, default=1.34,
                   help="average refraction index for photon generators")
# ChargedPrimary options
    #p.add_argument("--charged_energy",nargs='+',type=float,default=200,help="wavelengths interval")
    p.add_argument("--charged_primary_cherenkov_waves",nargs='+',type=float,default=[350,600],help="wavelengths interval")
    p.add_argument("--charged_direction",nargs='+',type=float,default=[0.,0.,1.],help="unit three vector for charged particle direction")
    p.add_argument("--charged_position_m",nargs='+',type=float,default=[0.,0.,0.],help="three vector for charged particle position")
    p.add_argument("--charged_length_m",nargs='+',type=float,default=100,help="travel length of charged particle")
# NeutrinoPrimary options
    p.add_argument("--neutrinoPrimary_pdgid",type=int,default=14,help="PDGID of neutrino")
    p.add_argument("--neutrinoPrimary_energy_mode",default='fixed',help="random or fixed")
    p.add_argument("--neutrinoPrimary_direction_mode",default='fixed',help="random or fixed")
    p.add_argument("--neutrinoPrimary_target_mode",default='random',help="random or fixed")
    p.add_argument("--neutrinoPrimary_current_mode",default='random',help="random or fixed")
    p.add_argument("--neutrinoPrimary_pdf_model",default='CT10nlo',help="LHAPDF model for nucleon")
    p.add_argument("--neutrinoPrimary_energy_GeV",type=float,default=100,help="energy of neutrino in GeV")
    p.add_argument("--neutrinoPrimary_target",default='proton',help="proton/neutron")
    p.add_argument("--neutrinoPrimary_direction",nargs='+',type=float,default=[0.,0.,1.],help="unit three vector for neutrino direction")

    ''' The following does not work with Python v. < 3.9
    p.add_argument("--h5_save_geometry",default=False, action=argparse.BooleanOptionalAction,help="Boolean to save geometry")
    p.add_argument("--h5_save_medium_model",default=False, action=argparse.BooleanOptionalAction,help="Boolean to save water model: absorption & scattering")
    p.add_argument("--h5_save_prod_header",default=False, action=argparse.BooleanOptionalAction,help="Boolean to save production header")
    p.add_argument("--h5_save_event_header",default=False, action=argparse.BooleanOptionalAction,help="Boolean to save event header")
    p.add_argument("--h5_save_primary_header",default=False, action=argparse.BooleanOptionalAction,help="Boolean to save event header")
    p.add_argument("--h5_save_tracks",type=bool,default=False, action=argparse.BooleanOptionalAction,help="Boolean to save tracks")
    p.add_argument("--h5_save_photons",type=bool,default=False, action=argparse.BooleanOptionalAction,help="Boolean to save photons")
    p.add_argument("--h5_save_hits",type=bool,default=False, action=argparse.BooleanOptionalAction,help="Boolean to save hits")
    p.add_argument("--h5_save_vertices",default=False, action=argparse.BooleanOptionalAction,help="Boolean to save vertices")
    '''

    return p
