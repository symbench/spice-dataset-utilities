#! /bin/bash
#
# Original source from Ian Eure (2019).
# Modifications made to interacting with the export window made by Brian Broll (2020).
#
# This code is in the public domain.
#

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

PREV_IDS=$(getEeschemaWindowID initial)
MWID=$(echo $PREV_IDS | cut -d"\\" -f1)

WINDOW_NAME=$(xdotool getwindowname $MWID)
echo "window name: \"$WINDOW_NAME\" (Try to remap if it is \"Not Found\")"
if [[ "$WINDOW_NAME" == "Not Found" ]]; then
    xdotool key --window $MWID Escape

    PREV_IDS=$(getEeschemaWindowID Remap)
    RWID=$(echo $PREV_IDS | cut -d"\\" -f1)
    WINDOW_NAME=$(xdotool getwindowname $RWID)
    if [[ "$WINDOW_NAME" != "Remap Symbols" ]]; then
        exit 1
    fi
    xdotool key --window $RWID Escape
    PREV_IDS=$(getEeschemaWindowID initial)
    MWID=$(echo $PREV_IDS | cut -d"\\" -f1)
fi

xdotool key --window $MWID alt+t n

# Wait for the export window.
PREV_IDS=$(getEeschemaWindowID "export")
EWID=$(echo $PREV_IDS | cut -d"\\" -f1)

unset x y w h
eval $(xwininfo -id $EWID |
sed -n -e "s/^ \+Absolute upper-left X: \+\([0-9]\+\).*/x=\1/p" \
       -e "s/^ \+Absolute upper-left Y: \+\([0-9]\+\).*/y=\1/p" \
       -e "s/^ \+Width: \+\([0-9]\+\).*/w=\1/p" \
       -e "s/^ \+Height: \+\([0-9]\+\).*/h=\1/p" )
echo -n "$x $y $w $h"
BTN_X=$(echo "$w * 0.8" | bc)
BTN_Y=$(echo "$h * 0.1" | bc)
TAB_X=$(echo "$w * 0.6" | bc)
TAB_Y=$(echo "$h * 0.08" | bc)
xdotool mousemove --window $EWID $TAB_X $TAB_Y click 1
xdotool mousemove --window $EWID $BTN_X $BTN_Y click 1

# Wait for the file dialog window
PREV_IDS=$(getEeschemaWindowID "file dialog")
FWID=$(echo $PREV_IDS | cut -d"\\" -f1)
echo "Found file window $FWID"

xdotool key --window $FWID "Return"

# Wait for the window to close
function tryCloseAnnotateWindow() {
    AWID="$(xdotool search --onlyvisible --classname Eeschema | grep -v "\($PREV_IDS\)" || true)"
    echo "Trying to close annotate window. AWID: $AWID"
    if [[ "$AWID" != "" ]]; then
        eval $(xwininfo -id $AWID |
        sed -n -e "s/^ \+Width: \+\([0-9]\+\).*/w=\1/p" \
               -e "s/^ \+Height: \+\([0-9]\+\).*/h=\1/p" )
        echo -n "$w $h"
        BTN_X=$(echo "$w * 0.95" | bc)
        BTN_Y=$(echo "$h * 0.95" | bc)
        xdotool mousemove --window $AWID $BTN_X $BTN_Y click 1
    fi
}

tryCloseAnnotateWindow
_CLOSED="$EWID"
while [ "$_CLOSED" = "$EWID" ]; do
    echo "Waiting for export window $EWID to close..."
    sleep 1
    _CLOSED="$(xdotool search --onlyvisible --classname Eeschema | grep $EWID || true)"
    tryCloseAnnotateWindow
done
echo "Export window closed."

echo "Closing eeschema"
xdotool key --window $MWID alt+f c

kill %1
kill %2 || true
