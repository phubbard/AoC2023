## ©️ 2023 Scale Invariant, Inc.  All rights reserved.
##      Reference: https://www.termsfeed.com/blog/sample-copyright-notices/
##
## Unauthorized copying of this file, via any medium is strictly prohibited
## Proprietary and confidential
##
## Written by Brad Hyslop <bhyslop@scaleinvariant.org> December 2023


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
include $(AOC23V_TOOLS_RELDIR)/mbde.MakefileBashDockerEphemeral.mk


################################
# Log file diagnostic tools

elbm-true.sh:
	$(MBC_PASS) "Truth, no errors."

elbm-false.sh:
	$(MBC_SHOW_RED) "false, about to error."  &&  $(MBC_FAIL)

%.dkrpy-3p12p1.sh:
	@docker run --rm $(MBDE_CONTAINER_BASEARGS) \
	python $(MBC_TTPARAM__FIRST).py
	$(MBC_PASS) "no errors."


#################################
# Tagalong stuff
mbde-Znb__nbodyCudaCharacterization.%.sh:
	@docker run --rm $(MBDE_CONTAINER_BASEARGS) nbody˘ -benchmark

mbde-BA__BuildAllDockerImages.sh:
	$(MBC_SHOW_WHITE) "Building all docker images..."
	tt/mbde-B__BuildDockerImage.python-3p12p1.sh
	$(MBC_PASS) "No errors seen."


# EOF
