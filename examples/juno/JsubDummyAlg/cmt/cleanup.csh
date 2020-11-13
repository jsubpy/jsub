# echo "cleanup JsubDummyAlg v0 in /junofs/users/yangyf/jsub/examples/juno"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-branch/ExternalLibs/CMT/v1r26
endif
source ${CMTROOT}/mgr/setup.csh
set cmtJsubDummyAlgtempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if $status != 0 then
  set cmtJsubDummyAlgtempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt cleanup -csh -pack=JsubDummyAlg -version=v0 -path=/junofs/users/yangyf/jsub/examples/juno  $* >${cmtJsubDummyAlgtempfile}
if ( $status != 0 ) then
  echo "${CMTROOT}/mgr/cmt cleanup -csh -pack=JsubDummyAlg -version=v0 -path=/junofs/users/yangyf/jsub/examples/juno  $* >${cmtJsubDummyAlgtempfile}"
  set cmtcleanupstatus=2
  /bin/rm -f ${cmtJsubDummyAlgtempfile}
  unset cmtJsubDummyAlgtempfile
  exit $cmtcleanupstatus
endif
set cmtcleanupstatus=0
source ${cmtJsubDummyAlgtempfile}
if ( $status != 0 ) then
  set cmtcleanupstatus=2
endif
/bin/rm -f ${cmtJsubDummyAlgtempfile}
unset cmtJsubDummyAlgtempfile
exit $cmtcleanupstatus

