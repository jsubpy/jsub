# echo "setup JsubDummyAlg v0 in /junofs/users/yangyf/jsub/examples/juno"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-branch/ExternalLibs/CMT/v1r26
endif
source ${CMTROOT}/mgr/setup.csh
set cmtJsubDummyAlgtempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if $status != 0 then
  set cmtJsubDummyAlgtempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt setup -csh -pack=JsubDummyAlg -version=v0 -path=/junofs/users/yangyf/jsub/examples/juno  -no_cleanup $* >${cmtJsubDummyAlgtempfile}
if ( $status != 0 ) then
  echo "${CMTROOT}/mgr/cmt setup -csh -pack=JsubDummyAlg -version=v0 -path=/junofs/users/yangyf/jsub/examples/juno  -no_cleanup $* >${cmtJsubDummyAlgtempfile}"
  set cmtsetupstatus=2
  /bin/rm -f ${cmtJsubDummyAlgtempfile}
  unset cmtJsubDummyAlgtempfile
  exit $cmtsetupstatus
endif
set cmtsetupstatus=0
source ${cmtJsubDummyAlgtempfile}
if ( $status != 0 ) then
  set cmtsetupstatus=2
endif
/bin/rm -f ${cmtJsubDummyAlgtempfile}
unset cmtJsubDummyAlgtempfile
exit $cmtsetupstatus

