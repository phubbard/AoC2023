## ©️ 2023 Scale Invariant, Inc.  All rights reserved.
##      Reference: https://www.termsfeed.com/blog/sample-copyright-notices/
##
## Unauthorized copying of this file, via any medium is strictly prohibited
## Proprietary and confidential
##
## Written by Brad Hyslop <bhyslop@scaleinvariant.org> December 2023


##############################################
#  MBDE: Makefile Bash Docker Ephimeral
#
#   The following tabtargets are applicable when
#   an application needs simply to create a docker
#   container during the course of a single command
#   to carry out a filesystem-only operation and then
#   self delete.  The entire project directory is
#   visible to the docker container via a bind mount.
#   The docker container is _not_ permitted to use
#   the network. 

MBDE_MONIKER = $(MBC_TTPARAM__SECOND)

zMBDE_SELECTED_DOCKERFILE = MBDE-dockerfiles/$(MBDE_MONIKER).dockerfile

zMBDE_SELECTED_IMAGE_NAME = $(MBDE_MONIKER)-image

zMBDE_SELECTED_CONTAINER_NAME = $(MBDE_MONIKER)-container

# Docker for Windows and Docker for Mac need host side mounts to be expressed
# using an absolute host path.
#  ref: https://stackoverflow.com/questions/54457535
#  ref: https://stackoverflow.com/questions/58996134
zMBDE_OUTER_ABSDIR = $(MBC_ROOT_ABSDIR)

# Path within container where the project directory is mounted
zMBDE_INNER_ABSDIR = /app

MBDE_CONTAINER_BASEARGS =                        \
  --name $(zMBDE_SELECTED_CONTAINER_NAME)        \
  --network none                                 \
  -e COLUMNS=$(MBC_CONSOLEPARAM__COLS)           \
  -e LINES=$(MBC_CONSOLEPARAM__LINES)            \
  -v $(zMBDE_OUTER_ABSDIR):$(zMBDE_INNER_ABSDIR) \
     $(zMBDE_SELECTED_IMAGE_NAME)


mbde-B__BuildDockerImage.%.sh:
	$(MBC_SHOW_WHITE) "Building image" $(zMBDE_SELECTED_IMAGE_NAME) "..."
	-docker rmi -f $(zMBDE_SELECTED_IMAGE_NAME)
	docker builder prune -f
	docker build --no-cache -f $(zMBDE_SELECTED_DOCKERFILE) -t $(zMBDE_SELECTED_IMAGE_NAME) .
	$(MBC_PASS) "Done, no errors."

mbde-i__InteractDockerContainer.%.sh:
	$(MBC_SHOW_WHITE) "Attempt to invoke..."
	docker run --rm  -it --init $(MBDE_CONTAINER_BASEARGS)
	$(MBC_PASS) "Done, no errors."

mbde-z__ZapDockerContainer.%.sh:
	$(MBC_SHOW_WHITE) "Kill any preexisting eponymous container..."
	-docker kill $(zMBDE_SELECTED_CONTAINER_NAME)
	-docker rm   $(zMBDE_SELECTED_CONTAINER_NAME)
	$(MBC_PASS) "Done, no errors."

mbde-u__Uname.%.sh:
	@docker run --rm $(MBDE_CONTAINER_BASEARGS) \
	uname -a

# Example of running a script in a particular image
uptime-hours.python-3p12p1.sh:
	@docker run --rm $(MBDE_CONTAINER_BASEARGS) \
	python -c 'mins=float(open("/proc/uptime").read().split()[0])/60;h=mins//60;m=mins-h*60;print(f"uptime -> {int(h)}h{int(m)}m");'



# EOF
