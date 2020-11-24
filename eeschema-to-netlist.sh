#! /bin/bash
#
# Original source from Ian Eure (2019).
# Modifications made to interacting with the export window made by Brian Broll (2020).
#
# This code is in the public domain.
#

set -e
set -u

SCH=$1

Xvfb :99 &
export DISPLAY=:99

eeschema $SCH &

MWID=""
while [ "$MWID" = "" ]; do
    sleep 1
    MWID=$(xdotool search --onlyvisible --sync --classname Eeschema)
done
echo "Found eeschema window $MWID"

xdotool key --window $MWID alt+t n

# Wait for the export window.
EWID=""
while [ "$EWID" = "" ]; do
    echo "Waiting for export window..."
    sleep 1
    EWID=$(xdotool search --onlyvisible --sync --classname Eeschema | grep -v $MWID || true)
done
echo "Found export window $MWID"

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
FWID=""
while [ "$FWID" = "" ]; do
    echo "Waiting for file window..."
    sleep 1
    FWID=$(xdotool search --onlyvisible --sync --classname Eeschema | grep -v $MWID | grep -v $EWID || true)
done
echo "Found file window $FWID"

xdotool key --window $FWID "Return"

# Wait for the window to close
    # TODO: if not closed, we should check for another window
function tryCloseAnnotateWindow() {
    AWID="$(xdotool search --onlyvisible --classname Eeschema | grep -v $EWID | grep -v $MWID | grep -v $FWID || true)"
    echo "Trying to close annotate window. AWID: $AWID"
    if [[ "$AWID" -ne "" ]]; then
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
