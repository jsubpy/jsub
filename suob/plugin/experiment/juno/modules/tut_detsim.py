#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao

import sys
import os
import Sniper

def get_parser():

    import argparse

    class MakeTVAction(argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            #print "__init__ begin"
            #print option_strings 
            #print dest 
            #print nargs
            #print kwargs
            #print "__init__ end"
            super(MakeTVAction, self).__init__(option_strings, dest, nargs, **kwargs)
        def __call__(self, parser, namespace, values, option_string=None):
            #print "__call__ begin"
            #print parser
            #print namespace
            #print values
            # == convert a list into 3-tuple ==
            if len(values) % 3:
                print("please set %s like x1 y1 z1 x2 y2 z2 ..." %option_string)
                sys.exit(-1)
            it = iter(values)
            values = zip(*([it]*3))
            setattr(namespace, self.dest, values)
            #print option_string
            #print "__call__ end"


    parser = argparse.ArgumentParser(description='Run Atmospheric Simulation.')
    parser.add_argument("--evtmax", type=int, default=10, help='events to be processed')
    parser.add_argument("--seed", type=int, default=42, help='seed')
    parser.add_argument("--output", default="sample_detsim.root", help="output file name")
    parser.add_argument("--user-output", default="sample_detsim_user.root", help="output file name")
    parser.add_argument("--mac", default="run.mac", help="mac file")

    parser.add_argument("--detoption", default="Acrylic", 
                                       choices=["Acrylic", "Balloon"],
                                       help="Det Option")
    parser.add_argument("--gdml", action="store_true", help="Save GDML.")

    # = gentool =
    subparsers = parser.add_subparsers(help='Please select the generator mode', 
                                       dest='gentool_mode')
    # == gun mode ==
    parser_gun = subparsers.add_parser("gun", help="gun mode")
    parser_gun.add_argument("--particles",default="gamma", nargs='+',
                            help="Particles to do the simulation.")
    parser_gun.add_argument("--momentums",default=1.0, nargs='+',
                            type=float, 
                            help="Momentums(MeV) p1 p2 ....")
    parser_gun.add_argument("--positions",default=[(0,0,0)], nargs='+',
                            type=float, action=MakeTVAction,
                            help="Positions(mm) x1 y1 z1 x2 y2 z2 ....")
    parser_gun.add_argument("--directions",default=None, nargs='+',
                            type=float, action=MakeTVAction,
                            help="If you don't set, the directions are randoms. "
                                 "Directions dx1 dy1 dz1 dx2 dy2 dz2 ....")
    parser_gun.add_argument("--material", default="None", help="material")
    parser_gun.add_argument("--volume", default="None", 
                                     choices=["PMT_20inch_body_phys", 
                                              "pCentralDetector",
                                              "pTarget"],
                                     help="Volume name")
    # == gendecay mode ==
    parser_gendecay = subparsers.add_parser("gendecay", help="GenDecay mode")
    parser_gendecay.add_argument("--nuclear", default="U-238", help="mother nuclide name")
    parser_gendecay.add_argument("--material", default="None", help="material")
    parser_gendecay.add_argument("--volume", default="PMT_20inch_body_phys", 
                                     choices=["PMT_20inch_body_phys", 
                                              "pCentralDetector",
                                              "pTarget"],
                                     help="Volume name")
    # == hepevt mode ==
    parser_hepevt = subparsers.add_parser("hepevt", help="HepEvt mode")
    parser_hepevt.add_argument("--exe", default="IBD", 
                                         choices=[
                                                "IBD", "IBD-eplus",
                                                "IBD-neutron",
                                                "Muon",
                                             ],
                                         help="select the Generator to run")
    parser_hepevt.add_argument("--material", default="None", help="material")
    parser_hepevt.add_argument("--volume", default="PMT_20inch_body_phys", 
                                     choices=["PMT_20inch_body_phys", 
                                              "pCentralDetector",
                                              "pTarget"],
                                     help="Volume name")

    return parser
    
def setup_generator(task):
    import GenTools
    from GenTools import makeTV
    gt = task.createAlg("GenTools")

    gun = gt.createTool("GtGunGenTool/gun")
    gun.property("particleNames").set(args.particles)
    gun.property("particleMomentums").set(args.momentums)
    if args.directions:
        gun.property("DirectionMode").set("Fix")
        gun.property("Directions").set([makeTV(px,py,pz) for px,py,pz in args.directions])
    print args.positions
    if len(args.positions) == 1:
        gun.property("PositionMode").set("FixOne")
    else:
        gun.property("PositionMode").set("FixMany")
    gun.property("Positions").set([makeTV(x,y,z) for x,y,z in args.positions])

    gt.property("GenToolNames").set([gun.objName()])

    if args.volume == "None":
        return
    # = enable the gen in volume mode =
    # == positioner related ==
    gun_pos = gt.createTool("GtPositionerTool")
    gun_pos.property("GenInVolume").set(args.volume)
    if args.material == "None":
        gun_pos.property("Material").set(DATA_MATERIALS[args.volume])
    else:
        gun_pos.property("Material").set(args.material)
    gt.property("GenToolNames").append(gun_pos.objName())

def setup_generator_gendecay(task):
    import GenTools
    from GenTools import makeTV
    gt = task.createAlg("GenTools")
    # == gendecay related ==
    Sniper.loadDll("libGenDecay.so")
    era = gt.createTool("GtDecayerator")
    era.property("ParentNuclide").set(args.nuclear)
    era.property("CorrelationTime").set(DECAY_DATA[args.nuclear])
    era.property("ParentAbundance").set(5e16)
    # == positioner related ==
    gun_pos = gt.createTool("GtPositionerTool")
    gun_pos.property("GenInVolume").set(args.volume)
    if args.material == "None":
        gun_pos.property("Material").set(DATA_MATERIALS[args.volume])
    else:
        gun_pos.property("Material").set(args.material)
    # == GtTimeOffsetTool ==
    toffset = gt.createTool("GtTimeOffsetTool")

    gt.property("GenToolNames").set([era.objName(),gun_pos.objName(),toffset.objName()])

def setup_generator_hepevt(task):
    import GenTools
    from GenTools import makeTV
    gt = task.createAlg("GenTools")
    # == HepEvt to HepMC ==
    gun = gt.createTool("GtHepEvtGenTool/gun")
    #gun.property("Source").set("K40.exe -seed 42 -n 100|")
    gun.property("Source").set(
            GENERATOR_EXEC[args.exe].format(SEED=args.seed,
                                            EVENT=args.evtmax)
            )
    gt.property("GenToolNames").set([gun.objName()])
    # == positioner related ==
    # === if muon event, use the hepevt file's position ===
    if args.exe == "Muon":
        pass
    else:
        gun_pos = gt.createTool("GtPositionerTool")
        gun_pos.property("GenInVolume").set(args.volume)
        if args.material == "None":
            gun_pos.property("Material").set(DATA_MATERIALS[args.volume])
        else:
            gun_pos.property("Material").set(args.material)
        gt.property("GenToolNames").append([gun_pos.objName()])
    # == GtTimeOffsetTool ==
    toffset = gt.createTool("GtTimeOffsetTool")
    gt.property("GenToolNames").append([toffset.objName()])

DEFAULT_GDML_OUTPUT = {"Acrylic": "geometry_acrylic.gdml", 
                       "Balloon": "geometry_balloon.gdml"}
DATA_MATERIALS = {"PMT_20inch_body_phys": "Pyrex",
                  "pCentralDetector": "Steel",
                  "pTarget": "LS"}
DECAY_DATA = {"U-238": 1.5e5, "Th-232": 280, "K-40": 1e9, "Co-60": 1e9} # unit: ns

if os.environ.get("MUONROOT", None) is None:
    print "Missing MUONROOT"
    print "Please setup the JUNO Offline Software."
    sys.exit(0)
muon_data = os.path.join(os.environ["MUONROOT"], "data")
GENERATOR_EXEC = {"IBD": "IBD.exe -n {EVENT} -seed {SEED}|",
                  "IBD-eplus": "IBD.exe -n {EVENT} -seed {SEED} -eplus_only|",
                  "IBD-neutron": "IBD.exe -n {EVENT} -seed {SEED} -neutron_only|",
                  "Muon": "Muon.exe -n {EVENT} -seed {SEED} -s juno -music_dir %s|"%muon_data,
                  }

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    print args
    
    gdml_filename = None
    if args.gdml:
        gdml_filename = DEFAULT_GDML_OUTPUT[args.detoption]

    task = Sniper.Task("detsimtask")
    task.asTop()
    task.setEvtMax(args.evtmax)
    task.setLogLevel(3)
    # = I/O Related =
    import DataRegistritionSvc
    task.createSvc("DataRegistritionSvc")
    
    import RootIOSvc
    task.createSvc("RootOutputSvc/OutputSvc")
    ro = task.find("OutputSvc")
    ro.property("OutputStreams").set({"/Event/SimEvent": args.output})
    # = Data Buffer =
    import BufferMemMgr
    bufMgr = task.createSvc("BufferMemMgr")

    # = random svc =
    import RandomSvc
    task.property("svcs").append("RandomSvc")
    rndm = task.find("RandomSvc")
    rndm.property("Seed").set(args.seed)

    # = root writer =
    import RootWriter
    rootwriter = task.createSvc("RootWriter")

    rootwriter.property("Output").set({"SIMEVT":args.user_output})

    # = generator related =
    if args.gentool_mode == "gun":
        setup_generator(task)
    elif args.gentool_mode == "gendecay":
        setup_generator_gendecay(task)
    elif args.gentool_mode == "hepevt":
        setup_generator_hepevt(task)

    # = geant4 related =
    import DetSimOptions
    if args.detoption == "Acrylic":
        from DetSimOptions.ConfAcrylic import ConfAcrylic
        acrylic_conf = ConfAcrylic(task)
        acrylic_conf.configure()
        if gdml_filename:
            acrylic_conf.set_gdml_output(gdml_filename)
    elif args.detoption == "Balloon":
        from DetSimOptions.ConfBalloon import ConfBalloon
        balloon_conf = ConfBalloon(task)
        balloon_conf.configure()
        if gdml_filename:
            balloon_conf.set_gdml_output(gdml_filename)
    # = begin run =
    task.show()
    task.run()
   
