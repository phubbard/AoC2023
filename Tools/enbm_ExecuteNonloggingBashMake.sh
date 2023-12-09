#!/bin/sh

# © 2019 Scale Invariant, Inc.  All rights reserved.
#      Reference: https://www.termsfeed.com/blog/sample-copyright-notices/

# Trigger the named executable in a bash shell while saving logs off

set -e

LLB_EXE=$1
shift
LLB_ARG="$@"

# Acquire repository specific variables
source ./usi-variables.sh

make -f $USIV_MAKEFILE $LLB_EXE $LLB_ARG 2>&1
test ${PIPESTATUS[0]} -eq 0



