#-- start of make_header -----------------

#====================================
#  Library JsubHelloWorld
#
#   Generated Mon Nov  2 16:03:30 2020  by yangyf
#
#====================================

include ${CMTROOT}/src/Makefile.core

ifdef tag
CMTEXTRATAGS = $(tag)
else
tag       = $(CMTCONFIG)
endif

cmt_JsubHelloWorld_has_no_target_tag = 1

#--------------------------------------------------------

ifdef cmt_JsubHelloWorld_has_target_tag

tags      = $(tag),$(CMTEXTRATAGS),target_JsubHelloWorld

JsubHelloWorld_tag = $(tag)

#cmt_local_tagfile_JsubHelloWorld = $(JsubHelloWorld_tag)_JsubHelloWorld.make
cmt_local_tagfile_JsubHelloWorld = $(bin)$(JsubHelloWorld_tag)_JsubHelloWorld.make

else

tags      = $(tag),$(CMTEXTRATAGS)

JsubHelloWorld_tag = $(tag)

#cmt_local_tagfile_JsubHelloWorld = $(JsubHelloWorld_tag).make
cmt_local_tagfile_JsubHelloWorld = $(bin)$(JsubHelloWorld_tag).make

endif

include $(cmt_local_tagfile_JsubHelloWorld)
#-include $(cmt_local_tagfile_JsubHelloWorld)

ifdef cmt_JsubHelloWorld_has_target_tag

cmt_final_setup_JsubHelloWorld = $(bin)setup_JsubHelloWorld.make
cmt_dependencies_in_JsubHelloWorld = $(bin)dependencies_JsubHelloWorld.in
#cmt_final_setup_JsubHelloWorld = $(bin)JsubHelloWorld_JsubHelloWorldsetup.make
cmt_local_JsubHelloWorld_makefile = $(bin)JsubHelloWorld.make

else

cmt_final_setup_JsubHelloWorld = $(bin)setup.make
cmt_dependencies_in_JsubHelloWorld = $(bin)dependencies.in
#cmt_final_setup_JsubHelloWorld = $(bin)JsubHelloWorldsetup.make
cmt_local_JsubHelloWorld_makefile = $(bin)JsubHelloWorld.make

endif

#cmt_final_setup = $(bin)setup.make
#cmt_final_setup = $(bin)JsubHelloWorldsetup.make

#JsubHelloWorld :: ;

dirs ::
	@if test ! -r requirements ; then echo "No requirements file" ; fi; \
	  if test ! -d $(bin) ; then $(mkdir) -p $(bin) ; fi

javadirs ::
	@if test ! -d $(javabin) ; then $(mkdir) -p $(javabin) ; fi

srcdirs ::
	@if test ! -d $(src) ; then $(mkdir) -p $(src) ; fi

help ::
	$(echo) 'JsubHelloWorld'

binobj = 
ifdef STRUCTURED_OUTPUT
binobj = JsubHelloWorld/
#JsubHelloWorld::
#	@if test ! -d $(bin)$(binobj) ; then $(mkdir) -p $(bin)$(binobj) ; fi
#	$(echo) "STRUCTURED_OUTPUT="$(bin)$(binobj)
endif

${CMTROOT}/src/Makefile.core : ;
ifdef use_requirements
$(use_requirements) : ;
endif

#-- end of make_header ------------------
#-- start of libary_header ---------------

JsubHelloWorldlibname   = $(bin)$(library_prefix)JsubHelloWorld$(library_suffix)
JsubHelloWorldlib       = $(JsubHelloWorldlibname).a
JsubHelloWorldstamp     = $(bin)JsubHelloWorld.stamp
JsubHelloWorldshstamp   = $(bin)JsubHelloWorld.shstamp

JsubHelloWorld :: dirs  JsubHelloWorldLIB
	$(echo) "JsubHelloWorld ok"

cmt_JsubHelloWorld_has_prototypes = 1

#--------------------------------------

ifdef cmt_JsubHelloWorld_has_prototypes

JsubHelloWorldprototype :  ;

endif

JsubHelloWorldcompile : $(bin)Hello.o ;

#-- end of libary_header ----------------
#-- start of libary ----------------------

JsubHelloWorldLIB :: $(JsubHelloWorldlib) $(JsubHelloWorldshstamp)
	$(echo) "JsubHelloWorld : library ok"

$(JsubHelloWorldlib) :: $(bin)Hello.o
	$(lib_echo) "static library $@"
	$(lib_silent) [ ! -f $@ ] || \rm -f $@
	$(lib_silent) $(ar) $(JsubHelloWorldlib) $(bin)Hello.o
	$(lib_silent) $(ranlib) $(JsubHelloWorldlib)
	$(lib_silent) cat /dev/null >$(JsubHelloWorldstamp)

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

$(JsubHelloWorldlibname).$(shlibsuffix) :: $(JsubHelloWorldlib) requirements $(use_requirements) $(JsubHelloWorldstamps)
	$(lib_echo) "shared library $@"
	$(lib_silent) if test "$(makecmd)"; then QUIET=; else QUIET=1; fi; QUIET=$${QUIET} bin="$(bin)" ld="$(shlibbuilder)" ldflags="$(shlibflags)" suffix=$(shlibsuffix) libprefix=$(library_prefix) libsuffix=$(library_suffix) $(make_shlib) "$(tags)" JsubHelloWorld $(JsubHelloWorld_shlibflags)
	$(lib_silent) cat /dev/null >$(JsubHelloWorldshstamp)

$(JsubHelloWorldshstamp) :: $(JsubHelloWorldlibname).$(shlibsuffix)
	$(lib_silent) if test -f $(JsubHelloWorldlibname).$(shlibsuffix) ; then cat /dev/null >$(JsubHelloWorldshstamp) ; fi

JsubHelloWorldclean ::
	$(cleanup_echo) objects JsubHelloWorld
	$(cleanup_silent) /bin/rm -f $(bin)Hello.o
	$(cleanup_silent) /bin/rm -f $(patsubst %.o,%.d,$(bin)Hello.o) $(patsubst %.o,%.dep,$(bin)Hello.o) $(patsubst %.o,%.d.stamp,$(bin)Hello.o)
	$(cleanup_silent) cd $(bin); /bin/rm -rf JsubHelloWorld_deps JsubHelloWorld_dependencies.make

#-----------------------------------------------------------------
#
#  New section for automatic installation
#
#-----------------------------------------------------------------

install_dir = ${CMTINSTALLAREA}/$(tag)/lib
JsubHelloWorldinstallname = $(library_prefix)JsubHelloWorld$(library_suffix).$(shlibsuffix)

JsubHelloWorld :: JsubHelloWorldinstall ;

install :: JsubHelloWorldinstall ;

JsubHelloWorldinstall :: $(install_dir)/$(JsubHelloWorldinstallname)
ifdef CMTINSTALLAREA
	$(echo) "installation done"
endif

$(install_dir)/$(JsubHelloWorldinstallname) :: $(bin)$(JsubHelloWorldinstallname)
ifdef CMTINSTALLAREA
	$(install_silent) $(cmt_install_action) \
	    -source "`(cd $(bin); pwd)`" \
	    -name "$(JsubHelloWorldinstallname)" \
	    -out "$(install_dir)" \
	    -cmd "$(cmt_installarea_command)" \
	    -cmtpath "$($(package)_cmtpath)"
endif

##JsubHelloWorldclean :: JsubHelloWorlduninstall

uninstall :: JsubHelloWorlduninstall ;

JsubHelloWorlduninstall ::
ifdef CMTINSTALLAREA
	$(cleanup_silent) $(cmt_uninstall_action) \
	    -source "`(cd $(bin); pwd)`" \
	    -name "$(JsubHelloWorldinstallname)" \
	    -out "$(install_dir)" \
	    -cmtpath "$($(package)_cmtpath)"
endif

#-- end of libary -----------------------
#-- start of dependencies ------------------
ifneq ($(MAKECMDGOALS),JsubHelloWorldclean)
ifneq ($(MAKECMDGOALS),uninstall)
ifneq ($(MAKECMDGOALS),JsubHelloWorldprototype)

$(bin)JsubHelloWorld_dependencies.make : $(use_requirements) $(cmt_final_setup_JsubHelloWorld)
	$(echo) "(JsubHelloWorld.make) Rebuilding $@"; \
	  $(build_dependencies) -out=$@ -start_all $(src)Hello.cc -end_all $(includes) $(app_JsubHelloWorld_cppflags) $(lib_JsubHelloWorld_cppflags) -name=JsubHelloWorld $? -f=$(cmt_dependencies_in_JsubHelloWorld) -without_cmt

-include $(bin)JsubHelloWorld_dependencies.make

endif
endif
endif

JsubHelloWorldclean ::
	$(cleanup_silent) \rm -rf $(bin)JsubHelloWorld_deps $(bin)JsubHelloWorld_dependencies.make
#-- end of dependencies -------------------
#-- start of cpp_library -----------------

ifneq (,)

ifneq ($(MAKECMDGOALS),JsubHelloWorldclean)
ifneq ($(MAKECMDGOALS),uninstall)
-include $(bin)$(binobj)Hello.d

$(bin)$(binobj)Hello.d :

$(bin)$(binobj)Hello.o : $(cmt_final_setup_JsubHelloWorld)

$(bin)$(binobj)Hello.o : $(src)Hello.cc
	$(cpp_echo) $(src)Hello.cc
	$(cpp_silent) $(cppcomp)  -o $@ $(use_pp_cppflags) $(JsubHelloWorld_pp_cppflags) $(lib_JsubHelloWorld_pp_cppflags) $(Hello_pp_cppflags) $(use_cppflags) $(JsubHelloWorld_cppflags) $(lib_JsubHelloWorld_cppflags) $(Hello_cppflags) $(Hello_cc_cppflags)  $(src)Hello.cc
endif
endif

else
$(bin)JsubHelloWorld_dependencies.make : $(Hello_cc_dependencies)

$(bin)JsubHelloWorld_dependencies.make : $(src)Hello.cc

$(bin)$(binobj)Hello.o : $(Hello_cc_dependencies)
	$(cpp_echo) $(src)Hello.cc
	$(cpp_silent) $(cppcomp) -o $@ $(use_pp_cppflags) $(JsubHelloWorld_pp_cppflags) $(lib_JsubHelloWorld_pp_cppflags) $(Hello_pp_cppflags) $(use_cppflags) $(JsubHelloWorld_cppflags) $(lib_JsubHelloWorld_cppflags) $(Hello_cppflags) $(Hello_cc_cppflags)  $(src)Hello.cc

endif

#-- end of cpp_library ------------------
#-- start of cleanup_header --------------

clean :: JsubHelloWorldclean ;
#	@cd .

ifndef PEDANTIC
.DEFAULT::
	$(echo) "(JsubHelloWorld.make) $@: No rule for such target" >&2
else
.DEFAULT::
	$(error PEDANTIC: $@: No rule for such target)
endif

JsubHelloWorldclean ::
#-- end of cleanup_header ---------------
#-- start of cleanup_library -------------
	$(cleanup_echo) library JsubHelloWorld
	-$(cleanup_silent) cd $(bin) && \rm -f $(library_prefix)JsubHelloWorld$(library_suffix).a $(library_prefix)JsubHelloWorld$(library_suffix).$(shlibsuffix) JsubHelloWorld.stamp JsubHelloWorld.shstamp
#-- end of cleanup_library ---------------
