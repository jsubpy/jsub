#v1.1
* Enabled some variations for the writting of TDF and configuration files.
* Added some prompt message for errors handling.
* Some bug fixes.

#v1.0
* Enabled pythonic eval for jobvars to let them work like variables. 
* Changed output folder structure to enable the output files of different steps to be put under different folders.
* Various bug fixes.

#v0.3
* Simpler jsubrc file for user.
* Reworked juno package.
* On dirac backend, job group reflect user name to avoid conflict.
* Changed the folder structure of jsub dirs. Now the top layer is , and there are logfiles/runtime/taskInfo in the 2nd layer.
* Changed the behavior of jsub getlog command. Now it dump results to //logfiles.
