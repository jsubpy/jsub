#-- start of make_header -----------------

#====================================
#  Library JsubDummyAlg
#
#   Generated Sun Nov  1 16:51:49 2020  by yangyf
#
#====================================

include ${CMTROOT}/src/Makefile.core

ifdef tag
CMTEXTRATAGS = $(tag)
else
tag       = $(CMTCONFIG)
endif

cmt_JsubDummyAlg_has_no_target_tag = 1

#--------------------------------------------------------

ifdef cmt_JsubDummyAlg_has_target_tag

tags      = $(tag),$(CMTEXTRATAGS),target_JsubDummyAlg

JsubDummyAlg_tag = $(tag)

#cmt_local_tagfile_JsubDummyAlg = $(JsubDummyAlg_tag)_JsubDummyAlg.make
cmt_local_tagfile_JsubDummyAlg = $(bin)$(JsubDummyAlg_tag)_JsubDummyAlg.make

else

tags      = $(tag),$(CMTEXTRATAGS)

JsubDummyAlg_tag = $(tag)

#cmt_local_tagfile_JsubDummyAlg = $(JsubDummyAlg_tag).make
cmt_local_tagfile_JsubDummyAlg = $(bin)$(JsubDummyAlg_tag).make

endif

include $(cmt_local_tagfile_JsubDummyAlg)
#-include $(cmt_local_tagfile_JsubDummyAlg)

ifdef cmt_JsubDummyAlg_has_target_tag

cmt_final_setup_JsubDummyAlg = $(bin)setup_JsubDummyAlg.make
cmt_dependencies_in_JsubDummyAlg = $(bin)dependencies_JsubDummyAlg.in
#cmt_final_setup_JsubDummyAlg = $(bin)JsubDummyAlg_JsubDummyAlgsetup.make
cmt_local_JsubDummyAlg_makefile = $(bin)JsubDummyAlg.make

else

cmt_final_setup_JsubDummyAlg = $(bin)setup.make
cmt_dependencies_in_JsubDummyAlg = $(bin)dependencies.in
#cmt_final_setup_JsubDummyAlg = $(bin)JsubDummyAlgsetup.make
cmt_local_JsubDummyAlg_makefile = $(bin)JsubDummyAlg.make

endif

#cmt_final_setup = $(bin)setup.make
#cmt_final_setup = $(bin)JsubDummyAlgsetup.make

#JsubDummyAlg :: ;

dirs ::
	@if test ! -r requirements ; then echo "No requirements file" ; fi; \
	  if test ! -d $(bin) ; then $(mkdir) -p $(bin) ; fi

javadirs ::
	@if test ! -d $(javabin) ; then $(mkdir) -p $(javabin) ; fi

srcdirs ::
	@if test ! -d $(src) ; then $(mkdir) -p $(src) ; fi

help ::
	$(echo) 'JsubDummyAlg'

binobj = 
ifdef STRUCTURED_OUTPUT
binobj = JsubDummyAlg/
#JsubDummyAlg::
#	@if test ! -d $(bin)$(binobj) ; then $(mkdir) -p $(bin)$(binobj) ; fi
#	$(echo) "STRUCTURED_OUTPUT="$(bin)$(binobj)
endif

${CMTROOT}/src/Makefile.core : ;
ifdef use_requirements
$(use_requirements) : ;
endif

#-- end of make_header ------------------
#-- start of libary_header ---------------

JsubDummyAlglibname   = $(bin)$(library_prefix)JsubDummyAlg$(library_suffix)
JsubDummyAlglib       = $(JsubDummyAlglibname).a
JsubDummyAlgstamp     = $(bin)JsubDummyAlg.stamp
JsubDummyAlgshstamp   = $(bin)JsubDummyAlg.shstamp

JsubDummyAlg :: dirs  JsubDummyAlgLIB
	$(echo) "JsubDummyAlg ok"

cmt_JsubDummyAlg_has_prototypes = 1

#--------------------------------------

ifdef cmt_JsubDummyAlg_has_prototypes

JsubDummyAlgprototype :  ;

endif

JsubDummyAlgcompile : $(bin)JsubDummyTool.o $(bin)JsubDummyAlg.o ;

#-- end of libary_header ----------------
#-- start of libary ----------------------

JsubDummyAlgLIB :: $(JsubDummyAlglib) $(JsubDummyAlgshstamp)
	$(echo) "JsubDummyAlg : library ok"

$(JsubDummyAlglib) :: $(bin)JsubDummyTool.o $(bin)JsubDummyAlg.o
	$(lib_echo) "static library $@"
	$(lib_silent) [ ! -f $@ ] || \rm -f $@
	$(lib_silent) $(ar) $(JsubDummyAlglib) $(bin)JsubDummyTool.o $(bin)JsubDummyAlg.o
	$(lib_silent) $(ranlib) $(JsubDummyAlglib)
	$(lib_silent) cat /dev/null >$(JsubDummyAlgstamp)

#------------------------------------------------------------------
#  Future improvement? to empty the object files after
#  storing in the library
#
##	  for f in $?; do \
##	    rm $${f}; touch $${f}; \
##	  done
#------------------------------------------------------------------

#
# We add one level of dependency upon the true shared library 
# (rather than simply upon the stamp file)
# this is for cases where the shared library has not been built
# while the stamp was created (error??) 
#

$(JsubDummyAlglibname).$(shlibsuffix) :: $(JsubDummyAlglib) requirements $(use_requirements) $(JsubDummyAlgstamps)
	$(lib_echo) "shared library $@"
	$(lib_silent) if test "$(makecmd)"; then QUIET=; else QUIET=1; fi; QUIET=$${QUIET} bin="$(bin)" ld="$(shlibbuilder)" ldflags="$(shlibflags)" suffix=$(shlibsuffix) libprefix=$(library_prefix) libsuffix=$(library_suffix) $(make_shlib) "$(tags)" JsubDummyAlg $(JsubDummyAlg_shlibflags)
	$(lib_silent) cat /dev/null >$(JsubDummyAlgshstamp)

$(JsubDummyAlgshstamp) :: $(JsubDummyAlglibname).$(shlibsuffix)
	$(lib_silent) if test -f $(JsubDummyAlglibname).$(shlibsuffix) ; then cat /dev/null >$(JsubDummyAlgshstamp) ; fi

JsubDummyAlgclean ::
	$(cleanup_echo) objects JsubDummyAlg
	$(cleanup_silent) /bin/rm -f $(bin)JsubDummyTool.o $(bin)JsubDummyAlg.o
	$(cleanup_silent) /bin/rm -f $(patsubst %.o,%.d,$(bin)JsubDummyTool.o $(bin)JsubDummyAlg.o) $(patsubst %.o,%.dep,$(bin)JsubDummyTool.o $(bin)JsubDummyAlg.o) $(patsubst %.o,%.d.stamp,$(bin)JsubDummyTool.o $(bin)JsubDummyAlg.o)
	$(cleanup_silent) cd $(bin); /bin/rm -rf JsubDummyAlg_deps JsubDummyAlg_dependencies.make

#-----------------------------------------------------------------
#
#  New section for automatic installation
#
#-----------------------------------------------------------------

install_dir = ${CMTINSTALLAREA}/$(tag)/lib
JsubDummyAlginstallname = $(library_prefix)JsubDummyAlg$(library_suffix).$(shlibsuffix)

JsubDummyAlg :: JsubDummyAlginstall ;

install :: JsubDummyAlginstall ;

JsubDummyAlginstall :: $(install_dir)/$(JsubDummyAlginstallname)
ifdef CMTINSTALLAREA
	$(echo) "installation done"
endif

$(install_dir)/$(JsubDummyAlginstallname) :: $(bin)$(JsubDummyAlginstallname)
ifdef CMTINSTALLAREA
	$(install_silent) $(cmt_install_action) \
	    -source "`(cd $(bin); pwd)`" \
	    -name "$(JsubDummyAlginstallname)" \
	    -out "$(install_dir)" \
	    -cmd "$(cmt_installarea_command)" \
	    -cmtpath "$($(package)_cmtpath)"
endif

##JsubDummyAlgclean :: JsubDummyAlguninstall

uninstall :: JsubDummyAlguninstall ;

JsubDummyAlguninstall ::
ifdef CMTINSTALLAREA
	$(cleanup_silent) $(cmt_uninstall_action) \
	    -source "`(cd $(bin); pwd)`" \
	    -name "$(JsubDummyAlginstallname)" \
	    -out "$(install_dir)" \
	    -cmtpath "$($(package)_cmtpath)"
endif

#-- end of libary -----------------------
#-- start of dependencies ------------------
ifneq ($(MAKECMDGOALS),JsubDummyAlgclean)
ifneq ($(MAKECMDGOALS),uninstall)
ifneq ($(MAKECMDGOALS),JsubDummyAlgprototype)

$(bin)JsubDummyAlg_dependencies.make : $(use_requirements) $(cmt_final_setup_JsubDummyAlg)
	$(echo) "(JsubDummyAlg.make) Rebuilding $@"; \
	  $(build_dependencies) -out=$@ -start_all $(src)JsubDummyTool.cc $(src)JsubDummyAlg.cc -end_all $(includes) $(app_JsubDummyAlg_cppflags) $(lib_JsubDummyAlg_cppflags) -name=JsubDummyAlg $? -f=$(cmt_dependencies_in_JsubDummyAlg) -without_cmt

-include $(bin)JsubDummyAlg_dependencies.make

endif
endif
endif

JsubDummyAlgclean ::
	$(cleanup_silent) \rm -rf $(bin)JsubDummyAlg_deps $(bin)JsubDummyAlg_dependencies.make
#-- end of dependencies -------------------
#-- start of cpp_library -----------------

ifneq (,)

ifneq ($(MAKECMDGOALS),JsubDummyAlgclean)
ifneq ($(MAKECMDGOALS),uninstall)
-include $(bin)$(binobj)JsubDummyTool.d

$(bin)$(binobj)JsubDummyTool.d :

$(bin)$(binobj)JsubDummyTool.o : $(cmt_final_setup_JsubDummyAlg)

$(bin)$(binobj)JsubDummyTool.o : $(src)JsubDummyTool.cc
	$(cpp_echo) $(src)JsubDummyTool.cc
	$(cpp_silent) $(cppcomp)  -o $@ $(use_pp_cppflags) $(JsubDummyAlg_pp_cppflags) $(lib_JsubDummyAlg_pp_cppflags) $(JsubDummyTool_pp_cppflags) $(use_cppflags) $(JsubDummyAlg_cppflags) $(lib_JsubDummyAlg_cppflags) $(JsubDummyTool_cppflags) $(JsubDummyTool_cc_cppflags)  $(src)JsubDummyTool.cc
endif
endif

else
$(bin)JsubDummyAlg_dependencies.make : $(JsubDummyTool_cc_dependencies)

$(bin)JsubDummyAlg_dependencies.make : $(src)JsubDummyTool.cc

$(bin)$(binobj)JsubDummyTool.o : $(JsubDummyTool_cc_dependencies)
	$(cpp_echo) $(src)JsubDummyTool.cc
	$(cpp_silent) $(cppcomp) -o $@ $(use_pp_cppflags) $(JsubDummyAlg_pp_cppflags) $(lib_JsubDummyAlg_pp_cppflags) $(JsubDummyTool_pp_cppflags) $(use_cppflags) $(JsubDummyAlg_cppflags) $(lib_JsubDummyAlg_cppflags) $(JsubDummyTool_cppflags) $(JsubDummyTool_cc_cppflags)  $(src)JsubDummyTool.cc

endif

#-- end of cpp_library ------------------
#-- start of cpp_library -----------------

ifneq (,)

ifneq ($(MAKECMDGOALS),JsubDummyAlgclean)
ifneq ($(MAKECMDGOALS),uninstall)
-include $(bin)$(binobj)JsubDummyAlg.d

$(bin)$(binobj)JsubDummyAlg.d :

$(bin)$(binobj)JsubDummyAlg.o : $(cmt_final_setup_JsubDummyAlg)

$(bin)$(binobj)JsubDummyAlg.o : $(src)JsubDummyAlg.cc
	$(cpp_echo) $(src)JsubDummyAlg.cc
	$(cpp_silent) $(cppcomp)  -o $@ $(use_pp_cppflags) $(JsubDummyAlg_pp_cppflags) $(lib_JsubDummyAlg_pp_cppflags) $(JsubDummyAlg_pp_cppflags) $(use_cppflags) $(JsubDummyAlg_cppflags) $(lib_JsubDummyAlg_cppflags) $(JsubDummyAlg_cppflags) $(JsubDummyAlg_cc_cppflags)  $(src)JsubDummyAlg.cc
endif
endif

else
$(bin)JsubDummyAlg_dependencies.make : $(JsubDummyAlg_cc_dependencies)

$(bin)JsubDummyAlg_dependencies.make : $(src)JsubDummyAlg.cc

$(bin)$(binobj)JsubDummyAlg.o : $(JsubDummyAlg_cc_dependencies)
	$(cpp_echo) $(src)JsubDummyAlg.cc
	$(cpp_silent) $(cppcomp) -o $@ $(use_pp_cppflags) $(JsubDummyAlg_pp_cppflags) $(lib_JsubDummyAlg_pp_cppflags) $(JsubDummyAlg_pp_cppflags) $(use_cppflags) $(JsubDummyAlg_cppflags) $(lib_JsubDummyAlg_cppflags) $(JsubDummyAlg_cppflags) $(JsubDummyAlg_cc_cppflags)  $(src)JsubDummyAlg.cc

endif

#-- end of cpp_library ------------------
#-- start of cleanup_header --------------

clean :: JsubDummyAlgclean ;
#	@cd .

ifndef PEDANTIC
.DEFAULT::
	$(echo) "(JsubDummyAlg.make) $@: No rule for such target" >&2
else
.DEFAULT::
	$(error PEDANTIC: $@: No rule for such target)
endif

JsubDummyAlgclean ::
#-- end of cleanup_header ---------------
#-- start of cleanup_library -------------
	$(cleanup_echo) library JsubDummyAlg
	-$(cleanup_silent) cd $(bin) && \rm -f $(library_prefix)JsubDummyAlg$(library_suffix).a $(library_prefix)JsubDummyAlg$(library_suffix).$(shlibsuffix) JsubDummyAlg.stamp JsubDummyAlg.shstamp
#-- end of cleanup_library ---------------
