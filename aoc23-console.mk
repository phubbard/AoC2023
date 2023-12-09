## � 2019 Scale Invariant, Inc.  All rights reserved.
##      Reference: https://www.termsfeed.com/blog/sample-copyright-notices/
##
## Unauthorized copying of this file, via any medium is strictly prohibited
## Proprietary and confidential
##
## Written by Brad Hyslop <bhyslop@scaleinvariant.org> March 2019
##
##  Pretty version:   https://github.com/bhyslop/usi-UtilitiesScaleInvariant/blob/master/usi-project.mk
##


include usi-variables.sh

include $(USIV_STATION_FILE)
include $(USIV_SECRETS_FILE)

# Common utilities for tabtarget implementation including console colors
include $(USIV_TOOLS_RELDIR)/mbc.MakefileBashConsole.variables.mk

# Prefix used to distinguish commentary created by this makefile
USIMK_PFX = "$(USIV_MAKEFILE): "

zUSIMK_REPONAME        = $(shell basename $(shell pwd))


zUSIMK_TABTARGET_DIRECTORY = tt


default:
	$(MBC_SHOW_RED) "NO TARGET SPECIFIED.  Check" $(zUSIMK_TABTARGET_DIRECTORY) "directory for options." && $(MBC_FAIL)


include $(USIV_TOOLS_RELDIR)/mbc.MakefileBashConsole.rules.mk


################################
# SlickEdit Project Wrangling
#

zUSIMK_VSEP_RELDIR=../_vs/$(zUSIMK_REPONAME)

vsr__ReplaceSlickEditWorkspace.sh:
	-rm -rf                                               $(zUSIMK_VSEP_RELDIR)
	mkdir -p                                              $(zUSIMK_VSEP_RELDIR)
	cp $(USIV_TOOLS_RELDIR)/vsep_VisualSlickEditProject/* $(zUSIMK_VSEP_RELDIR)
	@echo $(USIMK_PFX) "Done, no errors."


################################
# Git Wrangling
#
#   GWU- Git Wrangling Utilities

CPM_GWU_BRANCH =
CPM_GWU_MASTER = master

zUSIMK_TTARG_REPO = ../$(MBC_TTPARAM__SECOND)

# command to filter precedents that I want to hide
zUSIMK_FILTER_BRANCHES_SNIPPET = grep -v yyy- zzz-

gwu-bc-BranchCreate.sh:
	@echo $(USIMK_PFX) "Set up exchange branch --> CPM_GWU_BRANCH" $(CPM_GWU_BRANCH)
	@echo $(USIMK_PFX) " off of -->                CPM_GWU_MASTER" $(CPM_GWU_MASTER)
	cd  $(zUSIMK_FILTER_BRANCHES_SNIPPET)  &&  test ! -z "$(CPM_GWU_BRANCH)"  ||  \
	    (                                                           \
	        echo "NEED branch name argument CPM_GWU_BRANCH=xxx"   &&\
	        git branch -a                                 |         \
	            grep remotes/origin/personal/bhyslop      |         \
	            sed 's,remotes/origin/,CPM_GWU_BRANCH=,g' |         \
		    $(_cpm_cut_old_branch_precedents)         |         \
	            sort | tail                                       &&\
	        false                                                   \
	    )
	cd  $(zUSIMK_TTARG_REPO)  &&  git checkout                         $(CPM_GWU_MASTER)
	-cd $(zUSIMK_TTARG_REPO)  &&  git fetch
	-cd $(zUSIMK_TTARG_REPO)  &&  git pull
	-cd $(zUSIMK_TTARG_REPO)  &&  git fetch
	cd  $(zUSIMK_TTARG_REPO)  &&  git pull
	cd  $(zUSIMK_TTARG_REPO)  &&  git checkout -b    $(CPM_GWU_BRANCH) $(CPM_GWU_MASTER)
	cd  $(zUSIMK_TTARG_REPO)  &&  git push -u origin $(CPM_GWU_BRANCH)
	cd  $(zUSIMK_TTARG_REPO)  &&  git submodule update
	cd  $(zUSIMK_TTARG_REPO)  &&  git status
	@echo $(USIMK_PFX) "No errors reported."


################################
# Log file tools
#
# ELBM: Execute Logging Bash Make
#  (should rename to mbit for Makefile Bash Invocation Tools, here and below)

elbm-true.sh:
	$(MBC_PASS) "Truth, no errors."

elbm-false.sh:
	$(MBC_SHOW_RED) "false, about to error."  &&  $(MBC_FAIL)


################################
# Tab Target Maintenance (TTM)
#
# This creates tabtarget executables that set the current working directory to
#  the root of the repo and then transfer control to the makefile definition.

zTTM_TABTARGET_FULLNAME=$(zUSIMK_TABTARGET_DIRECTORY)/$(CPM_TTM_TABTARGET).sh

zTTM_SET_CWD       = 'USIC_SCRIPT_DIR="$$(dirname "$$0")" && cd "$$USIC_SCRIPT_DIR/.."'
zTTM_LOGGING_SH    = $(USIV_TOOLS_RELDIR)/elbm_ExecuteLoggingBashMake.sh
zTTM_NONLOGGING_SH = $(USIV_TOOLS_RELDIR)/enbm_ExecuteNonloggingBashMake.sh


ttml-TabTargetMaintenance-createLogging.sh:
	test ! -z       "$(CPM_TTM_TABTARGET)"  ||  (echo Must provide argument without tt dir or trailing sh && false)
	test ! -f "$(zTTM_TABTARGET_FULLNAME)"  ||  (echo Must provide new filename && false)
	echo "#!/bin/sh"                              > $(zTTM_TABTARGET_FULLNAME)
	echo $(zTTM_SET_CWD)                         >> $(zTTM_TABTARGET_FULLNAME)
	echo "$(zTTM_LOGGING_SH) \$$(basename \$$0)" >> $(zTTM_TABTARGET_FULLNAME)
	chmod +x                                        $(zTTM_TABTARGET_FULLNAME)
	@echo $(USIMK_PFX) "Done, no errors."


ttmn-TabTargetMaintenance-createNonlogging.sh:
	test ! -z       "$(CPM_TTM_TABTARGET)"  ||  (echo Must provide argument without tt dir or trailing sh && false)
	test ! -f "$(zTTM_TABTARGET_FULLNAME)"  ||  (echo Must provide new filename && false)
	echo "#!/bin/sh"                                 > $(zTTM_TABTARGET_FULLNAME)
	echo $(zTTM_SET_CWD)                            >> $(zTTM_TABTARGET_FULLNAME)
	echo "$(zTTM_NONLOGGING_SH) \$$(basename \$$0)" >> $(zTTM_TABTARGET_FULLNAME)
	chmod +x                                           $(zTTM_TABTARGET_FULLNAME)
	@echo $(USIMK_PFX) "Done, no errors."


################################
# Cygwin Maintenance
#
#   Resource: https://stackoverflow.com/questions/46829532/cygwin-save-package-selections-for-later-reinstall
# 
#     I've brought this into my tree at: tools/cyci_CygwinControlledInstall/from-stack-overflow-46829532.sh
#
#     A key comment from that entry: 
#           Your solution is OUTSTANDING! Just what I was looking for. I just had to edit 
#           the resulting batch to add my favourite site -s and my LAN's cygwin local-package-dir -l.  
#           If you could edit your script to ask for such details before building the list it would 
#           be PERFECT, because at this point, unattended -q can be added too. Also, the batch was  
#           produced with three whitespaces between the executable name and the first "-P" switch  
#           but this is pure formality. � Marco Oct 20 '17 at 17:02 
#
#   Resource (older): https://blag.nullteilerfrei.de/2014/01/31/import-and-export-cygwin-list-of-installed-packages/
#


################################
# MC:  Microsoft Code Tools
# FTT: Foundational Tabtarget Tools
#

FTT_MC_SETTINGS_CACHE_RELDIR = $(USIV_TOOLS_RELDIR)/mcs-MicrosoftCodeSettingsCache

ftt-mccs-MicrosoftCodeCaptureSettings.sh:
	test -e $(USI_MICROSOFT_CODE_SETTINGS_FILE)
	cp $(USI_MICROSOFT_CODE_SETTINGS_FILE)  $(FTT_MC_SETTINGS_CACHE_RELDIR)
	@echo $(USIMK_PFX) "Done, no errors."

ftt-mcis-MicrosoftCodeInstallSettings.sh:
	test -e $(USI_MICROSOFT_CODE_SETTINGS_FILE)
	cp $(FTT_MC_SETTINGS_CACHE_RELDIR)/* $(dir $(USI_MICROSOFT_CODE_SETTINGS_FILE))
	@echo $(USIMK_PFX) "Done, no errors."


################################
# LWM: Layout WinSplit Manager
#

FTT_LWM_APP_ROOT_NAME = WinSplit.exe
FTT_LWM_APP_FULL_NAME = $(USI_WINSPLIT_DIRECTORY)/$(FTT_LWM_APP_ROOT_NAME)

FTT_LWM_LAYOUT_ROOT_NAME = layout.xml
FTT_LWM_LAYOUT_REPO_NAME = ./Tools/wsl_WinSplitLayout/$(FTT_LWM_LAYOUT_ROOT_NAME)
FTT_LWM_LAYOUT_FULL_NAME = $(USI_WINSPLIT_DIRECTORY)/$(FTT_LWM_LAYOUT_ROOT_NAME)


### Painful Lesson
# 
# While improving the default WinSplit layout (finally!) I discovered something
# totally surprising: while cygwin windows seem to follow the layouts that are
# proscribed by layout.xml, it seems that slickedit refuses some of the later 
# new combinations and instead skips back to the beginning of the multikey 
# cycle.  When I force the issue by putting a 'problematic' layout early in
# the sequence, slickedit window just plain gets stuck at that size and will
# not move.  Gonna chalk it up to how a 15 year old hobby app doesn't work with
# new APIs and grin'n'bear it.  Ouch.
#
# Concluding work on this.  The cognitive model is that each key roughly
# shrinks the area, alternating between x4 and x9 underlying layout. Single
# key toggle works great...
#

sw_StartWinsplitWindowManager.sh:
	test -e $(FTT_LWM_APP_FULL_NAME)
	@echo $(USIMK_PFX) "App found."
	@echo $(USIMK_PFX) "Winname is $(FTT_LWM_APP_WIN_NAME)"
	@echo $(USIMK_PFX) "Killing..."
	-taskkill /im $(FTT_LWM_APP_ROOT_NAME) /f
	sleep 2
	@echo $(USIMK_PFX) "Pidline is" $(FTT_LWM_PID_LINE)
	@echo $(USIMK_PFX) "Refresh Layout..."
	cp $(FTT_LWM_LAYOUT_REPO_NAME) $(FTT_LWM_LAYOUT_FULL_NAME)
	@echo $(USIMK_PFX) "Restarting..."
	cygstart $(FTT_LWM_APP_FULL_NAME)
	sleep 3
	@echo $(USIMK_PFX) "New Pidnum is" $(shell ps -efW | grep $(FTT_LWM_APP_ROOT_NAME) | awk '{print $$2}')


################################
# DEW: Docker External Wrangling
#
#   A set of tabtargets related to getting docker images maintained outside of this local
#   repo up and running locally


# This just in!  maybe better docker way -> https://vsupalov.com/buildkit-cache-mount-dockerfile/

zUSIMK_DEW_AGN_RELDIR = dockext-app-cacher-ng
zUSIMK_DEW_AGN_IMAGE  = apt-cacher-ng


dew-agn-g-StartAptCacherNGDocker.sh:
	@echo $(USIMK_PFX) "Stop previous with compose..."
	-cd $(zUSIMK_DEW_AGN_RELDIR)  &&  docker-compose down
	-cd $(zUSIMK_DEW_AGN_RELDIR)  &&  docker-compose rm
	-cd $(zUSIMK_DEW_AGN_RELDIR)  &&  docker rm $(zUSIMK_DEW_AGN_IMAGE)
	@echo $(USIMK_PFX) "Start with compose..."
	cd $(zUSIMK_DEW_AGN_RELDIR)  &&  docker-compose up -d
	@echo $(USIMK_PFX) "No errors seen."

dew-agn-m-MonitorAptCacherNGDocker.sh:
	@echo $(USIMK_PFX) "Hit ctrl-c to stop log spew..."
	docker exec -it $(zUSIMK_DEW_AGN_IMAGE) tail -f /var/log/apt-cacher-ng/apt-cacher.log
  

################################
# DFP: Docker First play
#

zUSIMK_AWAIT_DOCKER = until docker container ls; do time; sleep 1; done

dfp-go-StartDockerFirstPlay.sh:
	@echo $(USIMK_PFX) "Spin until docker available..."
	@$(zUSIMK_AWAIT_DOCKER)
	@echo $(USIMK_PFX) "Step 1 from tutorial..."
	docker run --name repo alpine/git clone https://github.com/docker/getting-started.git
	@echo $(USIMK_PFX) "Step 2 from tutorial..."
	docker cp repo:/git/getting-started .
	@echo $(USIMK_PFX) "No errors seen."


# From https://hub.docker.com/r/plantuml/plantuml-server
zUSIMK_PLANTUML_PORT = 8080
zUSIMK_PLANTUML_CONTAINER = plantuml/plantuml-server:jetty

# A 'docknome' is a usi domain term for a directory that contains a Docker genome, i.e. the Dockerfile
#  plus ancillary files needed to construct a specific container.

# Deferred project: Prevent guest containers that I don't understand from
#   reaching out to the internet (and maybe leaking my secrets).  I did try
#   the `--network none` directive, but that broke the VS Code plugin which
#   is the whole point of this.
#
#   https://stackoverflow.com/questions/69544970
#   https://stackoverflow.com/questions/39913757
#
# I may need to rethink this completely and instead just build up a plantuml
#   docker container of my own when it comes to the second deferred project,
#   the stabilization of plantuml SVGs for easy delta detections without 
#   distraction.  Here's a good looking clue for starting a java docker 
#   project:    https://github.com/bhyslop/usi-UtilitiesScaleInvariant/blob/master/ref/20220813-java-docker-container-advice/java-docker-help.png
#
# RELATED: use plantweb to interface with above docker 
#   https://plantweb.readthedocs.io/
#   https://blog.toast38coza.me/easy-plantuml-with-python/
#
# LATER ADD: Rakuten (of all organizations!) may have a naked Dockerfile
#   that will let me work on this at -> https://github.com/rakutentech/plantuml-docker/blob/main/Dockerfile

sp-StartPlantUmlDocker.sh:
	@echo $(USIMK_PFX) "Spin until docker available..."
	@$(zUSIMK_AWAIT_DOCKER)
	@echo $(USIMK_PFX) "Try to kll any pre-existing (failures ignored)..."
	-docker rm $$(docker stop $$(docker ps -a -q --filter ancestor=$(zUSIMK_PLANTUML_CONTAINER) --format="{{.ID}}"))
	@echo $(USIMK_PFX) "Attempting update..."
	@echo $(USIMK_PFX) https://hub.docker.com/r/plantuml/plantuml-server
	docker run -d                                                            \
	  -p $(zUSIMK_PLANTUML_PORT):$(zUSIMK_PLANTUML_PORT)                     \
	  $(zUSIMK_PLANTUML_CONTAINER)
	@echo $(USIMK_PFX) "BEWARE: for VS Code, assure you have settings configured right:"
	@echo $(USIMK_PFX) "   This means that Ctrl+shift+P -> 'Preferences: Open Settings (JSON) must have..."
	@echo
	$(MBC_SHOW_WHITE) "      plantuml.server  --->" http://localhost:$(zUSIMK_PLANTUML_PORT)
	$(MBC_SHOW_WHITE) "      plantuml.render  --->" "PlantUMLServer"
	@echo
	@echo $(USIMK_PFX) "No errors seen."


################################
# BDI: Basic Docker Image
#

bdi-CE-BasicDockerImage_ClearExitedContainers.sh:
	$(MBC_SHOW_WHITE) "Clear exited from tutorial -> https://docker-curriculum.com/"
	docker rm $(shell docker ps -a -q -f status=exited)
	$(MBC_PASS) "No errors seen."

bdi-lc-BasicDockerImage_ListCurrentContainers.sh:
	$(MBC_SHOW_WHITE) "List current docker containers..."
	docker ps -a
	$(MBC_PASS) "No errors seen."

bdi-s-BasicDockerImage_Setup.sh:
	$(MBC_SHOW_WHITE) "Running a tutorial -> https://docker-curriculum.com/"
	$(MBC_SHOW_WHITE) "Docker setup assurance..."
	docker run hello-world
	$(MBC_SHOW_WHITE) "From section -> Playing with Busybox"
	$(MBC_SHOW_WHITE) "Pull..."
	docker pull busybox
	$(MBC_SHOW_WHITE) "Run and auto remove..."
	docker run --rm busybox echo "Hello from busybox"
	$(MBC_PASS) "No errors seen."


################################
# UDI: Ubuntu Docker Image
#
# Constructed while rescuing sister files.

zUSIMK_UBUNTU_IMAGE = ubuntu:lunar-20221207

udi-g-UbuntuDockerImage_Go.sh:
	@echo $(USIMK_PFX) "From section -> Playing with Busybox"
	@echo $(USIMK_PFX) "Pull..."
	docker pull $(zUSIMK_UBUNTU_IMAGE)
	@echo $(USIMK_PFX) "Run and auto remove..."
	docker run -it --rm -v "\\wsl$$\docker-desktop\dev:/dev/brad3" $(zUSIMK_UBUNTU_IMAGE)  /bin/bash
	@echo $(USIMK_PFX) "No errors seen."



################################
# LPD: Learn Python Django
#


_USIMK_DJPROTO_RELDIR = djproto-play

_USIMK_DJPROTO_PIP          = pip3
_USIMK_DJPROTO_PYTHON       = python3
_USIMK_DJPROTO_SITE         = mysite
_USIMK_DJPROTO_APP          = polls
_USIMK_DJPROTO_PROJECT_DIR  = $(_USIMK_DJPROTO_RELDIR)/$(_USIMK_DJPROTO_SITE)


lpd-s-LearnPythonDjango-Setup.sh:
	@echo $(USIMK_PFX) "THIS FOLLOWS THE SEQEUENCE OF THE TUTORIAL AT https://docs.djangoproject.com/en/4.0/intro/tutorial01/"
	@echo
	@echo $(USIMK_PFX) "Assure installed..."
	$(_USIMK_DJPROTO_PIP) install django
	@echo $(USIMK_PFX) "Check installed..."
	$(_USIMK_DJPROTO_PYTHON) -m django --version
	@echo $(USIMK_PFX) "Assure configuration..."
	test ! -z "$(_USIMK_DJPROTO_RELDIR)"
	@echo $(USIMK_PFX) "Prepare directory..."
	mkdir -p                                         $(_USIMK_DJPROTO_RELDIR)
	$(USIV_TOOLS_RELDIR)/tste_ToolsSafeTreeEmpty.py  $(_USIMK_DJPROTO_RELDIR)
	touch                                            $(_USIMK_DJPROTO_RELDIR)/testmedium.py
	@echo $(USIMK_PFX) "Tune gitignore..."
	echo "**/db.sqlite3"  >> $(_USIMK_DJPROTO_RELDIR)/.gitignore
	echo "**/__pycache__" >> $(_USIMK_DJPROTO_RELDIR)/.gitignore
	@echo $(USIMK_PFX) "Create base project as in -> https://docs.djangoproject.com/en/4.0/intro/tutorial01/#creating-a-project"
	cd $(_USIMK_DJPROTO_RELDIR)  &&  django-admin startproject $(_USIMK_DJPROTO_SITE)
	@echo $(USIMK_PFX) "Create app as in -> https://docs.djangoproject.com/en/4.0/intro/tutorial01/#creating-the-polls-app"
	cd $(_USIMK_DJPROTO_PROJECT_DIR)  &&  $(_USIMK_DJPROTO_PYTHON) manage.py startapp $(_USIMK_DJPROTO_APP)
	@echo $(USIMK_PFX) "No errors seen."


lpd-r-LearnPythonDjango-RunServer.sh:
	@echo $(USIMK_PFX) "Run the provided server..."
	cd $(_USIMK_DJPROTO_PROJECT_DIR)  &&  $(_USIMK_DJPROTO_PYTHON) manage.py runserver
	@echo $(USIMK_PFX) "No errors seen."


lpd-d-LearnPythonDjango-DoDatabaseThings.sh:
	@echo $(USIMK_PFX) "Perform migrate command as in -> https://docs.djangoproject.com/en/4.0/intro/tutorial02/#database-setup"
	@echo $(USIMK_PFX) "(This looks at the settings.py::INSTALLED_APPS and assures the"
	@echo $(USIMK_PFX) "  requisite tables are created in whatever db is configured there)"
	cd $(_USIMK_DJPROTO_PROJECT_DIR)  &&  $(_USIMK_DJPROTO_PYTHON) manage.py migrate
	@echo
	@echo $(USIMK_PFX) "Activate model as in -> https://docs.djangoproject.com/en/4.0/intro/tutorial02/#activating-models"
	cd $(_USIMK_DJPROTO_PROJECT_DIR)  &&  $(_USIMK_DJPROTO_PYTHON) manage.py makemigrations $(_USIMK_DJPROTO_APP)
	@echo
	@echo $(USIMK_PFX) "Show the sql that will be run- note its database specific"
	cd $(_USIMK_DJPROTO_PROJECT_DIR)  &&  $(_USIMK_DJPROTO_PYTHON) manage.py sqlmigrate $(_USIMK_DJPROTO_APP) 0001
	@echo
	@echo $(USIMK_PFX) "Carry out an integrity check, optional:"
	cd $(_USIMK_DJPROTO_PROJECT_DIR)  &&  $(_USIMK_DJPROTO_PYTHON) manage.py check
	@echo
	@echo $(USIMK_PFX) "One last migrate, that in the flow of the demo, applied a hand added migration"
	cd $(_USIMK_DJPROTO_PROJECT_DIR)  &&  $(_USIMK_DJPROTO_PYTHON) manage.py migrate
	@echo
	@echo $(USIMK_PFX) "No errors seen."
	@echo


# Now running the https://docs.djangoproject.com/en/4.0/intro/tutorial02/#playing-with-the-api
#
# Had a problem with demo code, and ...
#   https://stackoverflow.com/questions/33167629/confused-by-django-timezone-support
# ... led me to ...
#   from django.utils import timezone
# ... which repaired my statement.  Okay.

lpd-i-LearnPythonDjango-InteractiveShell.sh:
	@echo
	@echo $(USIMK_PFX) "TYPICAL FIRST STATEMENTS MUST BE AS FOLLOWS:"
	@echo $(USIMK_PFX) "     from polls.models import Choice, Question"
	@echo $(USIMK_PFX) "     from django.utils import timezone"
	@echo
	@echo $(USIMK_PFX) "About to go interactive..."
	cd $(_USIMK_DJPROTO_PROJECT_DIR)  &&  $(_USIMK_DJPROTO_PYTHON) manage.py shell
	@echo $(USIMK_PFX) "No errors seen."


# Doing manually -> https://docs.djangoproject.com/en/4.0/intro/tutorial02/#creating-an-admin-user
# Did https://docs.djangoproject.com/en/4.0/intro/tutorial03/ 


######################################
# UBUNTU TOOLING CONTROL


uts_UbuntuToolsSetup.sh:
	@echo "Assure sudo is armed..."
	sudo ls
	@echo "Search for better terminal window..."
	@echo https://www.linuxandubuntu.com/home/10-best-linux-terminals-for-ubuntu-and-fedora
	@echo https://www.makeuseof.com/best-terminal-alternatives-ubuntu/
	@echo https://zoomadmin.com/HowToInstall/UbuntuPackage/xterm
	@echo https://askubuntu.com/questions/211292/a-terminal-which-provides-select-to-copy-and-right-click-to-paste 
	@echo "Installing Terminator... ->" https://askubuntu.com/questions/829045/how-do-i-install-terminator
	sudo apt-get update
	sudo apt-get install -y terminator
	@echo "Installing xterm, doesn't work great but could with more work..."
	sudo apt-get install -y xterm
	@echo "Set default font size for xterm as per https://askubuntu.com/questions/161652/how-to-change-the-default-font-size-of-xterm ..."
	@echo SKIPPING
	-rm                                         $(HOME)/.Xresources
	echo "xterm*font:     *-fixed-*-*-*-24-*" > $(HOME)/.Xresources
	@echo "Incorporate changes..."
	xrdb -merge ~/.Xresources
	@echo "TO FINISH SETUP FOR TERMINATOR:"
	@echo "1. Open a terminator window"
	@echo "2. Right click on it and pick 'Preferences'"
	@echo "3. Pick 'Profiles' tab and 'General' subtab"
	@echo "4. Uncheck 'Use the system fixed width font' and choose font size"
	@echo "5. Check 'PuTTY style paste'"
	@echo "6. Check 'Copy on selection'"
	@echo "7. pick 'Profiles' tab and 'Scrolling' subtab"
	@echo "8. select Infinite Scrollback"
	@echo "Complete without errors."



include $(USIV_TOOLS_RELDIR)/mbde.MakefileBashDockerEphemeral.mk

usi-Znb__nbodyCudaCharacterization.%.sh:
	@docker run --rm $(zDME_CONTAINER_BASEARGS) nbody -gpu -benchmark

usi-BA__BuildAllDockerImages.sh:
	$(MBC_SHOW_WHITE) "Building all docker images..."
	tt/mbde-B__BuildDockerImage.busybox-test.sh
	tt/mbde-B__BuildDockerImage.cuda-basic.sh
	tt/mbde-B__BuildDockerImage.cuda-nbody.sh
	tt/mbde-B__BuildDockerImage.python-3p11p5.sh
	tt/mbde-B__BuildDockerImage.ubuntu-stripped.sh
	$(MBC_PASS) "No errors seen."


# EOF
