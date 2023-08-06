#!/usr/bin/bash
HELP="
Executes pytest every time a change in src/ or test/ directories occur.

USAGE:

    $0


an alternative is the watchtests.bash script.
"
SCRIPT_NEEDS=(bash inotifywait pytest)


# Scripting Helpers
_abort()   { echo "$1"; exit 1; }
_trycmd()  { which $1 >/dev/null 2>&1; }


# Abort Script On Missing Arguments Or Required Programs 
    # first activate virtualenv
    VENV_ACTIVATE=$(find . -path '*/venv/*/activate')
    source "$VENV_ACTIVATE"

    [ "$#" -gt 0 ] && _abort "$HELP"
    for CMD in ${SCRIPT_NEEDS[@]}; do
        _trycmd $CMD || PLEASE_INSTALL+="$CMD "
    done

    test -n "$PLEASE_INSTALL" \
        && _abort "Failed to check due to missing programs: $PLEASE_INSTALL" 

## restart pytest every 5 seconds
    echo "Waiting for change to trigger pytest"
    while inotifywait -q -r -e modify test/ src/
    do
        clear
        pytest
    done
    deactivate

# vi: et sw=4 ts=4 list

