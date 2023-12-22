# Variables that are used throughout the tabtargets in this launcher complex
#
#  Beware this file is used in makefiles as well as shell scripts, with 
#  following implications:
#
#  * DO NOT USE SPACES AROUND '='
#  * USE ONLY ${xxx} VARIABLE EXPANSIOIN, NOT $xxx NOR $(xxx)
#

AOC23V_STATION_FILE=../AOC23_STATION.mk
AOC23V_SECRETS_FILE=../secrets/AOC23_SECRETS_DO_NOT_DISTRIBUTE.mk

AOC23V_LOG_EXTENSION=txt
AOC23V_LOG_ABSDIR=$HOME/_aoc23_logs
AOC23V_LOG_LAST=${AOC23V_LOG_ABSDIR}/last.${AOC23V_LOG_EXTENSION}
AOC23V_MAKEFILE=aoc23-console.mk
AOC23V_TOOLS_RELDIR=Tools
