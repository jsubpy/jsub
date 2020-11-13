#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao

# using the new Mgr.

import Sniper

if __name__ == "__main__":

	Sniper.setLogLevel(2)
	Sniper.setColorful(2)
	#Sniper.setShowTime(True)

	task = Sniper.Task("task")
	task.setEvtMax(3)

	import PyDataStore
	task.createSvc("PyDataStoreSvc/DataStore")

	# SO files should be put into input sandbox; the loading folder in script would be redirecte
	Sniper.loadDll("/junofs/users/.../jsub/examples/juno/JsubHelloWorld/amd64_linux26/libJsubHelloWorld.so") 

	jsubHello=task.createAlg("JsubHelloAlg")

	jsubHello.property("VarString").set("GOD")
	jsubHello.property("VectorInt").set(range(6))
	jsubHello.property("MapStrInt").set( {"str%d"%v:v for v in range(6)} )
	print "After setting properties"
	jsubHello.show()

#	y = JsubHelloWorld.HelloPy("PyAlg")
#	task.addAlg(y)

#	z = task.createAlg("JsubHelloAlg/GetAlg")

	#task.show()

	task.run()
