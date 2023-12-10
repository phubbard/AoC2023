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


include aoc23-variables.sh

include $(AOC23V_STATION_FILE)
include $(AOC23V_SECRETS_FILE)

# Common utilities for tabtarget implementation including console colors
MBC_ARG__CONTEXT_STRING = aoc23mk
include $(AOC23V_TOOLS_RELDIR)/mbc.MakefileBashConsole.variables.mk


zAOC23MK_TABTARGET_DIRECTORY = tt


default:
	$(MBC_SHOW_RED) "NO TARGET SPECIFIED.  Check" $(zAOC23MK_TABTARGET_DIRECTORY) "directory for options." && $(MBC_FAIL)


include $(AOC23V_TOOLS_RELDIR)/mbc.MakefileBashConsole.rules.mk


################################
# Log file tools
#
# ELBM: Execute Logging Bash Make
#  (should rename to mbit for Makefile Bash Invocation Tools, here and below)

elbm-true.sh:
	$(MBC_PASS) "Truth, no errors."

elbm-false.sh:
	$(MBC_SHOW_RED) "false, about to error."  &&  $(MBC_FAIL)



include $(AOC23V_TOOLS_RELDIR)/mbde.MakefileBashDockerEphemeral.mk

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
