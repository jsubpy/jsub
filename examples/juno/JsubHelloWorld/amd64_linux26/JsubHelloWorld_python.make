#-- start of make_header -----------------

#====================================
#  Document JsubHelloWorld_python
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

cmt_JsubHelloWorld_python_has_no_target_tag = 1

#--------------------------------------------------------

ifdef cmt_JsubHelloWorld_python_has_target_tag

tags      = $(tag),$(CMTEXTRATAGS),target_JsubHelloWorld_python

JsubHelloWorld_tag = $(tag)

#cmt_local_tagfile_JsubHelloWorld_python = $(JsubHelloWorld_tag)_JsubHelloWorld_python.make
cmt_local_tagfile_JsubHelloWorld_python = $(bin)$(JsubHelloWorld_tag)_JsubHelloWorld_python.make

else

tags      = $(tag),$(CMTEXTRATAGS)

JsubHelloWorld_tag = $(tag)

#cmt_local_tagfile_JsubHelloWorld_python = $(JsubHelloWorld_tag).make
cmt_local_tagfile_JsubHelloWorld_python = $(bin)$(JsubHelloWorld_tag).make

endif

include $(cmt_local_tagfile_JsubHelloWorld_python)
#-include $(cmt_local_tagfile_JsubHelloWorld_python)

ifdef cmt_JsubHelloWorld_python_has_target_tag

cmt_final_setup_JsubHelloWorld_python = $(bin)setup_JsubHelloWorld_python.make
cmt_dependencies_in_JsubHelloWorld_python = $(bin)dependencies_JsubHelloWorld_python.in
#cmt_final_setup_JsubHelloWorld_python = $(bin)JsubHelloWorld_JsubHelloWorld_pythonsetup.make
cmt_local_JsubHelloWorld_python_makefile = $(bin)JsubHelloWorld_python.make

else

cmt_final_setup_JsubHelloWorld_python = $(bin)setup.make
cmt_dependencies_in_JsubHelloWorld_python = $(bin)dependencies.in
#cmt_final_setup_JsubHelloWorld_python = $(bin)JsubHelloWorldsetup.make
cmt_local_JsubHelloWorld_python_makefile = $(bin)JsubHelloWorld_python.make

endif

#cmt_final_setup = $(bin)setup.make
#cmt_final_setup = $(bin)JsubHelloWorldsetup.make

#JsubHelloWorld_python :: ;

dirs ::
	@if test ! -r requirements ; then echo "No requirements file" ; fi; \
	  if test ! -d $(bin) ; then $(mkdir) -p $(bin) ; fi

javadirs ::
	@if test ! -d $(javabin) ; then $(mkdir) -p $(javabin) ; fi

srcdirs ::
	@if test ! -d $(src) ; then $(mkdir) -p $(src) ; fi

help ::
	$(echo) 'JsubHelloWorld_python'

binobj = 
ifdef STRUCTURED_OUTPUT
binobj = JsubHelloWorld_python/
#JsubHelloWorld_python::
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

JsubHelloWorld_python :: JsubHelloWorld_pythoninstall

install :: JsubHelloWorld_pythoninstall

JsubHelloWorld_pythoninstall :: $(install_python_dir)
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

JsubHelloWorld_pythonclean :: JsubHelloWorld_pythonuninstall

uninstall :: JsubHelloWorld_pythonuninstall

JsubHelloWorld_pythonuninstall ::
	@if test "$(installarea)" = ""; then \
	  echo "Cannot uninstall header files, no installation source specified"; \
	else \
	  echo "Uninstalling files from $(dest)"; \
	  $(uninstall_command) "$(dest)" ; \
	fi


#-- end of install_python_header ------
#-- start of cleanup_header --------------

clean :: JsubHelloWorld_pythonclean ;
#	@cd .

ifndef PEDANTIC
.DEFAULT::
	$(echo) "(JsubHelloWorld_python.make) $@: No rule for such target" >&2
else
.DEFAULT::
	$(error PEDANTIC: $@: No rule for such target)
endif

JsubHelloWorld_pythonclean ::
#-- end of cleanup_header ---------------
