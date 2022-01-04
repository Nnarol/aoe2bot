#!/bin/bash

scriptDir=$(dirname "$(readlink -e "$0")")

[ -r envconf.sh ] && . envconf.sh || { 1>&2 echo "$0: error: no readable envconf.sh found in script directory '$scriptDir'!"; exit 1; }

"${scriptDir}/main.py" "$@"
