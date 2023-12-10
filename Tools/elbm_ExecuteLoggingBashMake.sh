#!/bin/bash

# � 2019 Scale Invariant, Inc.  All rights reserved.
#      Reference: https://www.termsfeed.com/blog/sample-copyright-notices/

# Trigger the named executable in a bash shell while saving logs off

set -e

LLB_EXE=$1
shift
LLB_ARG="$@"

# Acquire repository specific variables
source ./aoc23-variables.sh

LLB_LOG_DIR=$AOC23V_LOG_ABSDIR

LLB_LOG_LAST=$AOC23V_LOG_LAST
LLB_LOG_SAME=$LLB_LOG_DIR/same-$LLB_EXE.$AOC23V_LOG_EXTENSION
LLB_LOG_HIST=$LLB_LOG_DIR/hist-$(date +'%Y%m%d-%H%M%Sp%N')-$LLB_EXE.$AOC23V_LOG_EXTENSION

# Assure log directory exists
mkdir -p $LLB_LOG_DIR

# I do not know why, but the 'tee' sequence zaps stderror emissions.
make -f $AOC23V_MAKEFILE $LLB_EXE $LLB_ARG 2>&1 \
                          | tee $LLB_LOG_LAST \
                          | tee $LLB_LOG_SAME \
                          | tee $LLB_LOG_HIST \

test ${PIPESTATUS[0]} -eq 0



