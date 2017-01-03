#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao

import Sniper

def get_parser():

    import argparse

    parser = argparse.ArgumentParser(description='Run Atmospheric Simulation.')
    parser.add_argument("--evtmax", type=int, default=-1, help='events to be processed')
    parser.add_argument("--seed", type=int, default=42, help='seed')
    parser.add_argument("--input", default="sample_detsim.root", help="input file name")
    parser.add_argument("--output", default="sample_calib.root", help="output file name")

    parser.add_argument("--detoption", default="Acrylic", 
                                       choices=["Acrylic", "Balloon"],
                                       help="Det Option")

    return parser

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    task = Sniper.Task("calibtask")
    task.asTop()
    task.setEvtMax(args.evtmax)
    task.setLogLevel(0)

    # Create Data Buffer Svc
    import DataRegistritionSvc
    task.createSvc("DataRegistritionSvc")

    import BufferMemMgr
    bufMgr = task.createSvc("BufferMemMgr")
    bufMgr.property("TimeWindow").set([-0.01, 0.01])

    # Create IO Svc
    import RootIOSvc
    inputsvc = task.createSvc("RootInputSvc/InputSvc")
    inputsvc.property("InputFile").set([args.input])

    roSvc = task.createSvc("RootOutputSvc/OutputSvc")
    outputdata = {"/Event/CalibEvent": args.output,
                  "/Event/SimEvent": args.output}
    roSvc.property("OutputStreams").set(outputdata)

    #alg

    Sniper.loadDll("libPmtRec.so")
    #pullSimAlg = task.createAlg("PullSimHeaderAlg")
    task.property("algs").append("PullSimHeaderAlg")

    task.show()
    task.run()

