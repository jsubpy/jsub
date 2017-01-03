#!/bin/bash

executable=$1

unset MARLIN_DLL
export ILC_HOME=/cvmfs/cepc.ihep.ac.cn/cepcsoft/x64_SL6/xuyin/ilcsoft/v01-17-05
source $ILC_HOME/init_ilcsoft.sh
(time ${executable} reco.xml) &> reco.log
