CMTPATH=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalInterface
CMT_tag=$(tag)
CMTROOT=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-branch/ExternalLibs/CMT/v1r26
CMT_root=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-branch/ExternalLibs/CMT/v1r26
CMTVERSION=v1r26
CMT_offset=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-branch/ExternalLibs
cmt_hardware_query_command=uname -m
cmt_hardware=`$(cmt_hardware_query_command)`
cmt_system_version_query_command=${CMTROOT}/mgr/cmt_linux_version.sh | ${CMTROOT}/mgr/cmt_filter_version.sh
cmt_system_version=`$(cmt_system_version_query_command)`
cmt_compiler_version_query_command=${CMTROOT}/mgr/cmt_gcc_version.sh | ${CMTROOT}/mgr/cmt_filter3_version.sh
cmt_compiler_version=`$(cmt_compiler_version_query_command)`
PATH=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline/InstallArea/${CMTCONFIG}/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/InstallArea/${CMTCONFIG}/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-branch/ExternalLibs/CMT/v1r26/${CMTBIN}:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/podio/master/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/python-yaml/5.1.2/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/libyaml/0.2.2/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/python-cython/0.29.16/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/mysql-connector-cpp/1.1.8/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/mysql-connector-c/6.1.9/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/libmore/0.8.3/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Geant4/10.05.p01/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/HepMC/2.06.09/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/ROOT/6.20.02/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/xrootd/4.10.0/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/CLHEP/2.4.1.0/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/tbb/2019_U8/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/sqlite3/3.29.0/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/fftw3/3.3.8/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/gsl/2.5/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Xercesc/3.2.2/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Cmake/3.17.0/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Boost/1.72.0/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Python/2.7.17/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/contrib/gcc/8.3.0/bin:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/contrib/binutils/2.28/bin:/afs/ihep.ac.cn/soft/common/sysgroup/container/bin/:/afs/ihep.ac.cn/users/y/yangyf/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/bin
CLASSPATH=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-branch/ExternalLibs/CMT/v1r26/java
debug_option=-g
cc=gcc
ccomp=$(cc) -c $(includes) $(cdebugflags) $(cflags) $(pp_cflags)
clink=$(cc) $(clinkflags) $(cdebugflags)
ppcmd=-I
preproc=c++ -MD -c 
cpp=g++
cppflags=-std=c++11 -fPIC -pipe -W -Wall -Wwrite-strings -Wpointer-arith -Woverloaded-virtual 
pp_cppflags=-D_GNU_SOURCE
cppcomp=$(cpp) -c $(includes) $(cppdebugflags) $(cppflags) $(pp_cppflags)
cpplink=$(cpp) $(cpplinkflags) $(cppdebugflags)
for=g77
fflags=$(debug_option)
fcomp=$(for) -c $(fincludes) $(fflags) $(pp_fflags)
flink=$(for) $(flinkflags)
javacomp=javac -classpath $(src):$(CLASSPATH) 
javacopy=cp
jar=jar
X11_cflags=-I/usr/include
Xm_cflags=-I/usr/include
X_linkopts=-L/usr/X11R6/lib -lXm -lXt -lXext -lX11 -lm
lex=lex $(lexflags)
yaccflags= -l -d 
yacc=yacc $(yaccflags)
ar=ar cr
ranlib=ranlib
make_shlib=${CMTROOT}/mgr/cmt_make_shlib_common.sh extract
shlibsuffix=so
shlibbuilder=g++ $(cmt_installarea_linkopts) 
shlibflags=-shared
symlink=/bin/ln -fs 
symunlink=/bin/rm -f 
library_install_command=python $(SniperPolicy_root)/cmt/fragments/install.py -xCVS -x.svn -x*~ -x*.stamp -s --log=./install.history 
build_library_links=$(cmtexe) build library_links -tag=$(tags)
remove_library_links=$(cmtexe) remove library_links -tag=$(tags)
cmtexe=${CMTROOT}/${CMTBIN}/cmt.exe
build_prototype=$(cmtexe) build prototype
build_dependencies=$(cmtexe) -tag=$(tags) build dependencies
build_triggers=$(cmtexe) build triggers
format_dependencies=${CMTROOT}/mgr/cmt_format_deps.sh
implied_library_prefix=-l
SHELL=/bin/sh
q="
src=../src/
doc=../doc/
inc=../src/
mgr=../cmt/
application_suffix=.exe
library_prefix=lib
unlock_command=rm -rf 
lock_name=cmt
lock_suffix=.lock
lock_file=${lock_name}${lock_suffix}
svn_checkout_command=python ${CMTROOT}/mgr/cmt_svn_checkout.py 
gmake_hosts=lx1 rsplus lxtest as7 dxplus ax7 hp2 aleph hp1 hpplus papou1-fe atlas
make_hosts=virgo-control1 rio0a vmpc38a
everywhere=hosts
install_command=python $(SniperPolicy_root)/cmt/fragments/install.py -xCVS -x.svn -x*~ -x*.stamp --log=./install.history 
uninstall_command=python $(SniperPolicy_root)/cmt/fragments/install.py -u --log=./install.history 
cmt_installarea_command=python $(SniperPolicy_root)/cmt/fragments/install.py -xCVS -x.svn -x*~ -x*.stamp -s --log=./install.history 
cmt_uninstallarea_command=/bin/rm -f 
cmt_install_area_command=$(cmt_installarea_command)
cmt_uninstall_area_command=$(cmt_uninstallarea_command)
cmt_install_action=$(CMTROOT)/mgr/cmt_install_action.sh
cmt_installdir_action=$(CMTROOT)/mgr/cmt_installdir_action.sh
cmt_uninstall_action=$(CMTROOT)/mgr/cmt_uninstall_action.sh
cmt_uninstalldir_action=$(CMTROOT)/mgr/cmt_uninstalldir_action.sh
mkdir=mkdir
cmt_cvs_protocol_level=v1r1
cmt_installarea_prefix=InstallArea
CMT_PATH_remove_regexp=/[^/]*/
CMT_PATH_remove_share_regexp=/share/
NEWCMTCONFIG=x86_64-slc78-gcc830
JsubHelloWorld_tag=$(tag)
JSUBHELLOWORLDROOT=/junofs/users/yangyf/jsub/examples/juno/JsubHelloWorld
JsubHelloWorld_root=/junofs/users/yangyf/jsub/examples/juno/JsubHelloWorld
JSUBHELLOWORLDVERSION=v1
JsubHelloWorld_offset=/junofs/users/yangyf/jsub/examples/juno
SniperKernel_tag=$(tag)
SNIPERKERNELROOT=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/SniperKernel
SniperKernel_root=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/SniperKernel
SNIPERKERNELVERSION=v2
SniperKernel_cmtpath=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper
SniperKernel_project=sniper
SniperPolicy_tag=$(tag)
SNIPERPOLICYROOT=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/SniperPolicy
SniperPolicy_root=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/SniperPolicy
SNIPERPOLICYVERSION=v0
SniperPolicy_cmtpath=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper
SniperPolicy_project=sniper
libraryshr_linkopts=-fPIC -ldl -Wl,--as-needed -Wl,--no-undefined 
application_linkopts=-Wl,--export-dynamic 
BINDIR=$(tag)
remove_command=$(cmt_uninstallarea_command)
Boost_tag=$(tag)
BOOSTROOT=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalInterface/Externals/Boost
Boost_root=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalInterface/Externals/Boost
BOOSTVERSION=v0
Boost_cmtpath=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalInterface
Boost_offset=Externals
Boost_project=ExternalInterface
Python_tag=$(tag)
PYTHONROOT=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalInterface/Externals/Python
Python_root=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalInterface/Externals/Python
PYTHONVERSION=v0
Python_cmtpath=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalInterface
Python_offset=Externals
Python_project=ExternalInterface
Python_linkopts= `pkg-config --libs python` 
Python_cppflags= `pkg-config --cflags python` 
Boost_home=${JUNO_EXTLIB_Boost_HOME}
Boost_pysuffix=${BOOST_PYTHON_SUFFIX}
Boost_linkopts= -L$(Boost_home)/lib  -lboost_python$(Boost_pysuffix) 
includes= $(ppcmd)"$(srcdir)" $(ppcmd)"/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline/InstallArea/include" $(ppcmd)"/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/InstallArea/include" $(use_includes)
PYTHONPATH=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline/InstallArea/python:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/InstallArea/python:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline/InstallArea/amd64_linux26/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/InstallArea/amd64_linux26/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/python-yaml/5.1.2/lib/python2.7/site-packages:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/python-cython/0.29.16/lib/python2.7/site-packages:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/ROOT/6.20.02/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/xrootd/4.10.0/lib64/python2.6/site-packages:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Python/2.7.17/lib/./python2.7/lib-dynload
SniperKernel_linkopts= -lSniperKernel  -lSniperPython 
SniperKernel_stamps=${SNIPERKERNELROOT}/${BINDIR}/SniperPython.stamp 
SniperKernel_linker_library=SniperPython
SniperPython_dependencies=SniperKernel
SniperPython_shlibflags= -lSniperKernel 
PyDataStore_tag=$(tag)
PYDATASTOREROOT=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/SniperUtil/PyDataStore
PyDataStore_root=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/SniperUtil/PyDataStore
PYDATASTOREVERSION=v0
PyDataStore_cmtpath=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper
PyDataStore_offset=SniperUtil
PyDataStore_project=sniper
PyDataStore_linkopts= -lRootWriter 
PyDataStore_stamps=${PYDATASTOREROOT}/${BINDIR}/RootWriter.stamp 
PyDataStore_linker_library=RootWriter
tag=amd64_linux26
package=JsubHelloWorld
version=v1
PACKAGE_ROOT=$(JSUBHELLOWORLDROOT)
srcdir=../src
bin=../$(JsubHelloWorld_tag)/
javabin=../classes/
mgrdir=cmt
BIN=/junofs/users/yangyf/jsub/examples/juno/JsubHelloWorld/amd64_linux26/
cmt_installarea_paths= $(cmt_installarea_prefix)/$(CMTCONFIG)/bin $(sniper_installarea_prefix)/$(CMTCONFIG)/lib $(sniper_installarea_prefix)/share/lib $(sniper_installarea_prefix)/share/bin $(offline_installarea_prefix)/$(CMTCONFIG)/lib $(offline_installarea_prefix)/share/lib $(offline_installarea_prefix)/share/bin
use_linkopts= $(cmt_installarea_linkopts)   $(JsubHelloWorld_linkopts)  $(PyDataStore_linkopts)  $(SniperKernel_linkopts)  $(SniperPolicy_linkopts)  $(Boost_linkopts)  $(Python_linkopts) 
ExternalInterface_installarea_prefix=$(cmt_installarea_prefix)
ExternalInterface_installarea_prefix_remove=$(ExternalInterface_installarea_prefix)
LD_LIBRARY_PATH=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline/InstallArea/${CMTCONFIG}/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/InstallArea/${CMTCONFIG}/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/podio/master/lib64:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/python-yaml/5.1.2/lib/python2.7/site-packages:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/python-yaml/5.1.2/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/libyaml/0.2.2/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/python-cython/0.29.16/lib/python2.7/site-packages:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/python-cython/0.29.16/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/mysql-connector-cpp/1.1.8/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/mysql-connector-c/6.1.9/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/libmore/0.8.3/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Geant4/10.05.p01/lib64:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/HepMC/2.06.09/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/ROOT/6.20.02/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/xrootd/4.10.0/lib64/python2.6/site-packages:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/xrootd/4.10.0/lib64:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/CLHEP/2.4.1.0/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/tbb/2019_U8/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/sqlite3/3.29.0/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/fftw3/3.3.8/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/gsl/2.5/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Xercesc/3.2.2/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Boost/1.72.0/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Python/2.7.17/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/contrib/gcc/8.3.0/lib64:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/contrib/gcc/8.3.0/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/contrib/binutils/2.28/lib64:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/contrib/binutils/2.28/lib:/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-branch/ExternalLibs/Xercesc/3.2.2/lib
sniper_installarea_prefix=$(cmt_installarea_prefix)
sniper_installarea_prefix_remove=$(sniper_installarea_prefix)
offline_installarea_prefix=$(cmt_installarea_prefix)
offline_installarea_prefix_remove=$(offline_installarea_prefix)
cmt_installarea_linkopts= -L/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline/$(offline_installarea_prefix)/$(CMTCONFIG)/lib  -L/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/$(sniper_installarea_prefix)/$(CMTCONFIG)/lib 
ExternalInterface_home=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalInterface
sniper_home=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper
offline_home=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline
offline_install_include= /cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline/$(offline_installarea_prefix)/include 
sniper_install_include= /cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/$(sniper_installarea_prefix)/include 
sniper_python_path=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/$(sniper_installarea_prefix)/$(tag)/lib
offline_python_path=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline/$(offline_installarea_prefix)/$(tag)/lib
sniper_install_python=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/sniper/$(sniper_installarea_prefix)/python
offline_install_python=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/offline/$(offline_installarea_prefix)/python
use_requirements=requirements $(CMT_root)/mgr/requirements $(PyDataStore_root)/cmt/requirements $(SniperKernel_root)/cmt/requirements $(SniperPolicy_root)/cmt/requirements $(Boost_root)/cmt/requirements $(Python_root)/cmt/requirements 
use_includes= $(ppcmd)"$(PyDataStore_root)/src" $(ppcmd)"$(SniperKernel_root)/src" $(ppcmd)"$(SniperPolicy_root)/src" $(ppcmd)"/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-Pre0/ExternalLibs/Boost/1.72.0/include" $(ppcmd)"$(Python_root)/src" 
use_fincludes= $(use_includes)
use_stamps=  $(JsubHelloWorld_stamps)  $(PyDataStore_stamps)  $(SniperKernel_stamps)  $(SniperPolicy_stamps)  $(Boost_stamps)  $(Python_stamps) 
use_cflags=  $(JsubHelloWorld_cflags)  $(PyDataStore_cflags)  $(SniperKernel_cflags)  $(SniperPolicy_cflags)  $(Boost_cflags)  $(Python_cflags) 
use_pp_cflags=  $(JsubHelloWorld_pp_cflags)  $(PyDataStore_pp_cflags)  $(SniperKernel_pp_cflags)  $(SniperPolicy_pp_cflags)  $(Boost_pp_cflags)  $(Python_pp_cflags) 
use_cppflags=  $(JsubHelloWorld_cppflags)  $(PyDataStore_cppflags)  $(SniperKernel_cppflags)  $(SniperPolicy_cppflags)  $(Boost_cppflags)  $(Python_cppflags) 
use_pp_cppflags=  $(JsubHelloWorld_pp_cppflags)  $(PyDataStore_pp_cppflags)  $(SniperKernel_pp_cppflags)  $(SniperPolicy_pp_cppflags)  $(Boost_pp_cppflags)  $(Python_pp_cppflags) 
use_fflags=  $(JsubHelloWorld_fflags)  $(PyDataStore_fflags)  $(SniperKernel_fflags)  $(SniperPolicy_fflags)  $(Boost_fflags)  $(Python_fflags) 
use_pp_fflags=  $(JsubHelloWorld_pp_fflags)  $(PyDataStore_pp_fflags)  $(SniperKernel_pp_fflags)  $(SniperPolicy_pp_fflags)  $(Boost_pp_fflags)  $(Python_pp_fflags) 
use_libraries= $(PyDataStore_libraries)  $(SniperKernel_libraries)  $(SniperPolicy_libraries)  $(Boost_libraries)  $(Python_libraries) 
fincludes= $(includes)
JsubHelloWorld_GUID={88BF15AB-5A2D-4bea-B64F-02752C2A1F4F}
JsubHelloWorld_use_linkopts=  $(JsubHelloWorld_linkopts)  $(PyDataStore_linkopts)  $(SniperKernel_linkopts)  $(SniperPolicy_linkopts)  $(Boost_linkopts)  $(Python_linkopts) 
JsubHelloWorld_python_GUID={88BF15AB-5A2D-4bea-B64F-02752C2A1F4F}
make_GUID={88BF15AB-5A2D-4bea-B64F-02752C2A1F4F}
constituents= JsubHelloWorld JsubHelloWorld_python 
all_constituents= $(constituents)
constituentsclean= JsubHelloWorld_pythonclean JsubHelloWorldclean 
all_constituentsclean= $(constituentsclean)
cmt_actions_constituents= make 
cmt_actions_constituentsclean= makeclean 
JsubHelloWorldprototype_dependencies= $(JsubHelloWorldcompile_dependencies)
