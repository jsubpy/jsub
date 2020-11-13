#-- start of make_header -----------------

#====================================
#  Document JsubDummyAlg_python
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

cmt_JsubDummyAlg_python_has_no_target_tag = 1

#--------------------------------------------------------

ifdef cmt_JsubDummyAlg_python_has_target_tag

tags      = $(tag),$(CMTEXTRATAGS),target_JsubDummyAlg_python

JsubDummyAlg_tag = $(tag)

#cmt_local_tagfile_JsubDummyAlg_python = $(JsubDummyAlg_tag)_JsubDummyAlg_python.make
cmt_local_tagfile_JsubDummyAlg_python = $(bin)$(JsubDummyAlg_tag)_JsubDummyAlg_python.make

else

tags      = $(tag),$(CMTEXTRATAGS)

JsubDummyAlg_tag = $(tag)

#cmt_local_tagfile_JsubDummyAlg_python = $(JsubDummyAlg_tag).make
cmt_local_tagfile_JsubDummyAlg_python = $(bin)$(JsubDummyAlg_tag).make

endif

include $(cmt_local_tagfile_JsubDummyAlg_python)
#-include $(cmt_local_tagfile_JsubDummyAlg_python)

ifdef cmt_JsubDummyAlg_python_has_target_tag

cmt_final_setup_JsubDummyAlg_python = $(bin)setup_JsubDummyAlg_python.make
cmt_dependencies_in_JsubDummyAlg_python = $(bin)dependencies_JsubDummyAlg_python.in
#cmt_final_setup_JsubDummyAlg_python = $(bin)JsubDummyAlg_JsubDummyAlg_pythonsetup.make
cmt_local_JsubDummyAlg_python_makefile = $(bin)JsubDummyAlg_python.make

else

cmt_final_setup_JsubDummyAlg_python = $(bin)setup.make
cmt_dependencies_in_JsubDummyAlg_python = $(bin)dependencies.in
#cmt_final_setup_JsubDummyAlg_python = $(bin)JsubDummyAlgsetup.make
cmt_local_JsubDummyAlg_python_makefile = $(bin)JsubDummyAlg_python.make

endif

#cmt_final_setup = $(bin)setup.make
#cmt_final_setup = $(bin)JsubDummyAlgsetup.make

#JsubDummyAlg_python :: ;

dirs ::
	@if test ! -r requirements ; then echo "No requirements file" ; fi; \
	  if test ! -d $(bin) ; then $(mkdir) -p $(bin) ; fi

javadirs ::
	@if test ! -d $(javabin) ; then $(mkdir) -p $(javabin) ; fi

srcdirs ::
	@if test ! -d $(src) ; then $(mkdir) -p $(src) ; fi

help ::
	$(echo) 'JsubDummyAlg_python'

binobj = 
ifdef STRUCTURED_OUTPUT
binobj = JsubDummyAlg_python/
#JsubDummyAlg_python::
#	@if test ! -d $(bin)$(binobj) ; then $(mkdir) -p $(bin)$(binobj) ; fi
#	$(echo) "STRUCTURED_OUTPUT="$(bin)$(binobj)
endif

${CMTROOT}/src/Makefile.core : ;
ifdef use_requirements
$(use_requirements) : ;
endif

#-- end of make_header ------------------
#-- start of install_python_header ------


installarea = ${CMTINSTALLAREA}
install_python_dir = $(installarea)

ifneq ($(strip "$(source)"),"")
src = ../$(source)
dest = $(install_python_dir)/python
else
src = ../python
dest = $(install_python_dir)
endif

ifneq ($(strip "$(offset)"),"")
dest = $(install_python_dir)/python
endif

JsubDummyAlg_python :: JsubDummyAlg_pythoninstall

install :: JsubDummyAlg_pythoninstall

JsubDummyAlg_pythoninstall :: $(install_python_dir)
	@if [ ! "$(installarea)" = "" ] ; then\
	  echo "installation done"; \
	fi

$(install_python_dir) ::
	@if [ "$(installarea)" = "" ] ; then \
	  echo "Cannot install header files, no installation source specified"; \
	else \
	  if [ -d $(src) ] ; then \
	    echo "Installing files from $(src) to $(dest)" ; \
	    if [ "$(offset)" = "" ] ; then \
	      $(install_command) --exclude="*.py?" $(src) $(dest) ; \
	    else \
	      $(install_command) --exclude="*.py?" $(src) $(dest) --destname $(offset); \
	    fi ; \
	  else \
	    echo "no source  $(src)"; \
	  fi; \
	fi

JsubDummyAlg_pythonclean :: JsubDummyAlg_pythonuninstall

uninstall :: JsubDummyAlg_pythonuninstall

JsubDummyAlg_pythonuninstall ::
	@if test "$(installarea)" = ""; then \
	  echo "Cannot uninstall header files, no installation source specified"; \
	else \
	  echo "Uninstalling files from $(dest)"; \
	  $(uninstall_command) "$(dest)" ; \
	fi


#-- end of install_python_header ------
#-- start of cleanup_header --------------

clean :: JsubDummyAlg_pythonclean ;
#	@cd .

ifndef PEDANTIC
.DEFAULT::
	$(echo) "(JsubDummyAlg_python.make) $@: No rule for such target" >&2
else
.DEFAULT::
	$(error PEDANTIC: $@: No rule for such target)
endif

JsubDummyAlg_pythonclean ::
#-- end of cleanup_header ---------------
