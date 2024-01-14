#!/bin/sh
USIC_SCRIPT_DIR="$(dirname "$0")" && cd "$USIC_SCRIPT_DIR/.."
Tools/elbm_ExecuteLoggingBashMake.sh $(basename $0)
