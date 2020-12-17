pkill eeschema
set -e
set -u

SCH=$@

Xvfb :99 &
export DISPLAY=:99

eeschema "$SCH" &

PREV_IDS="NONE"
function getEeschemaWindowID() {
    local NAME=$@
    local WID=""
    WID=""
    while [ "$WID" = "" ]; do
        echo "Waiting for $NAME window... ($(xdotool search --onlyvisible --sync --classname Eeschema | tr '\n' ','); $PREV_IDS)" 1>&2
        sleep 0.1
        WID=$(xdotool search --onlyvisible --sync --classname Eeschema | grep -v "\($PREV_IDS\)" || true)
    done
    echo "$WID\|$PREV_IDS"
}

cleanUp() {
    pkill eeschema
}

PREV_IDS=$(getEeschemaWindowID initial)
MWID=$(echo $PREV_IDS | cut -d"\\" -f1)

WINDOW_NAME=$(xdotool getwindowname $MWID)
if [[ "$WINDOW_NAME" != "Not Found" ]]; then
    echo $WINDOW_NAME
    cleanUp
    exit 0
fi

xdotool key --window $MWID Escape

PREV_IDS=$(getEeschemaWindowID Remap)
RWID=$(echo $PREV_IDS | cut -d"\\" -f1)
WINDOW_NAME=$(xdotool getwindowname $RWID)
if [[ "$WINDOW_NAME" == "Remap Symbols" ]]; then
    xdotool key --window $RWID Escape
    PREV_IDS=$(getEeschemaWindowID initial)
    FWID=$(echo $PREV_IDS | cut -d"\\" -f1)
    echo $(xdotool getwindowname $FWID)
    cleanUp
    exit 0
fi

echo $WINDOW_NAME
cleanUp
exit 0
