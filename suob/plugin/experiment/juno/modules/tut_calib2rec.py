#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao

import Sniper

def get_parser():

    import argparse

    parser = argparse.ArgumentParser(description='Run Atmospheric Simulation.')
    parser.add_argument("--evtmax", type=int, default=-1, help='events to be processed')
    parser.add_argument("--seed", type=int, default=42, help='seed')
    parser.add_argument("--input", default="sample_calib.root", help="input file name")
    parser.add_argument("--output", default="sample_rec.root", help="output file name")

    parser.add_argument("--detoption", default="Acrylic", 
                                       choices=["Acrylic", "Balloon"],
                                       help="Det Option")
    parser.add_argument("--gdml", action="store_true", help="Use GDML.")
    return parser

TOTALPMTS = {"Acrylic": 17746, "Balloon": 18306}
DEFAULT_GDML_OUTPUT = {"Acrylic": "geometry_acrylic.gdml", 
                       "Balloon": "geometry_balloon.gdml"}

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    total_pmt = TOTALPMTS[args.detoption]
    gdml_filename = "default"
    if args.gdml:
        gdml_filename = DEFAULT_GDML_OUTPUT[args.detoption]

    task = Sniper.Task("rectask")
    task.asTop()
    task.setEvtMax(args.evtmax)
    task.setLogLevel(0)

    # == Create Data Buffer Svc ==
    import DataRegistritionSvc
    drs = task.createSvc("DataRegistritionSvc")
    drs.property("EventToPath").set({
            #"JM::SimEvent": "/Event/SimEvent"
        })

    import BufferMemMgr
    bufMgr = task.createSvc("BufferMemMgr")
    bufMgr.property("TimeWindow").set([-0.01, 0.01])

    # == Create IO Svc ==
    import RootIOSvc
    inputsvc = task.createSvc("RootInputSvc/InputSvc")
    inputsvc.property("InputFile").set([args.input])

    # === load dict ===
    #Sniper.loadDll("libSimEventV2.so")
    Sniper.loadDll("libCalibEvent.so")
    Sniper.loadDll("libRecEvent.so")
    roSvc = task.createSvc("RootOutputSvc/OutputSvc")
    outputdata = {"/Event/RecEvent": args.output,
                  "/Event/CalibEvent": args.output}
                  #"/Event/SimEvent": args.output}
    roSvc.property("OutputStreams").set(outputdata)

    # == Geometry Svc ==
    import Geometry
    geom = task.createSvc("RecGeomSvc")
    geom.property("GeomFile").set(gdml_filename)

    # == RecTimeLikeAlg ==
    import RecTimeLikeAlg
    import os
    # FIXME: should user set the PMT_R and Ball_R ???
    alg = task.createAlg("RecTimeLikeAlg")
    alg.property("TotalPMT").set(total_pmt)
    alg.property("PMT_R").set(18.750)
    alg.property("Ball_R").set(18.496)
    alg.property("Energy_Scale").set(3414.5454)
    alg.property("File_path").set( 
                    os.path.join(os.environ["RECTIMELIKEALGROOT"],"share",""))
    alg.setLogLevel(2)

    task.show()
    task.run()
