# echo "cleanup JsubHelloWorld v1 in /junofs/users/yangyf/jsub/examples/juno"

if test "${CMTROOT}" = ""; then
  CMTROOT=/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc830/Pre-Release/J20v1r1-branch/ExternalLibs/CMT/v1r26; export CMTROOT
fi
. ${CMTROOT}/mgr/setup.sh
cmtJsubHelloWorldtempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if test ! $? = 0 ; then cmtJsubHelloWorldtempfile=/tmp/cmt.$$; fi
${CMTROOT}/mgr/cmt cleanup -sh -pack=JsubHelloWorld -version=v1 -path=/junofs/users/yangyf/jsub/examples/juno  $* >${cmtJsubHelloWorldtempfile}
if test $? != 0 ; then
  echo >&2 "${CMTROOT}/mgr/cmt cleanup -sh -pack=JsubHelloWorld -version=v1 -path=/junofs/users/yangyf/jsub/examples/juno  $* >${cmtJsubHelloWorldtempfile}"
  cmtcleanupstatus=2
  /bin/rm -f ${cmtJsubHelloWorldtempfile}
  unset cmtJsubHelloWorldtempfile
  return $cmtcleanupstatus
fi
cmtcleanupstatus=0
. ${cmtJsubHelloWorldtempfile}
if test $? != 0 ; then
  cmtcleanupstatus=2
fi
/bin/rm -f ${cmtJsubHelloWorldtempfile}
unset cmtJsubHelloWorldtempfile
return $cmtcleanupstatus

