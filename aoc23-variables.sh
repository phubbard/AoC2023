# Variables that are used throughout the tabtargets in this launcher complex
#
#  Beware this file is used in makefiles as well as shell scripts, with 
#  following implications:
#
#  * DO NOT USE SPACES AROUND '='
#  * USE ONLY ${xxx} VARIABLE EXPANSIOIN, NOT $xxx NOR $(xxx)
#

USIV_STATION_FILE=../AOC23_STATION.mk
USIV_SECRETS_FILE=../secrets/AOC23_SECRETS_DO_NOT_DISTRIBUTE.mk

USIV_LOG_EXTENSION=ltxt
USIV_LOG_ABSDIR=$HOME/_logs
USIV_LOG_LAST=${USIV_LOG_ABSDIR}/last.${USIV_LOG_EXTENSION}
USIV_MAKEFILE=usi-console.mk
USIV_TOOLS_RELDIR=Tools
