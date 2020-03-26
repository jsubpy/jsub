#!/bin/bash

# the example script of which the jsub needs to do the equivalent job;
#	- iterating ekin from 0 to 9;
# 	- 20 k events for each

num=$1
seed=$2
ekin=$3
of_name="eplus_${ekin}MeV"

source /afs/ihep.ac.cn/soft/juno/JUNO-ALL-SLC6/Pre-Release/J19v1r0-Pre3/setup.sh
source /afs/ihep.ac.cn/soft/juno/JUNO-ALL-SLC6/contrib/compat/bashrc

cd /afs/ihep.ac.cn/users/y/yury/spmt_dir/yury/2019/test_eplus_2k-2

if [[ ! -d ROOT ]]
then
  mkdir ROOT
fi

if [[ ! -d ROOT_user ]]
then
  mkdir ROOT_user
fi


python ${TUTORIALROOT}/share/tut_detsim.py --evtmax=${num} --seed=${seed} --no-gdml --output=${of_name}.root --user-output=${of_name}_user.root gun --volume pTarget --particles e+ --momentums ${ekin} --momentums-interp KineticEnergy

