#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao

import Sniper

task = Sniper.Task("task")
task.setLogLevel(2)

import RootWriter
task.property("svcs").append("RootWriter")
rw = task.find("RootWriter")
rw.property("Output").set({"FILE1": OUTPUT1, "FILE2": OUTPUT2})


import JsubDummyAlg  #infact JsubDummyTool is imported at the same time
alg = task.createAlg("JsubDummyAlg/dalg")
alg.createTool("JsubDummyTool/dtool")

task.setEvtMax(5)
task.show()
task.run()
