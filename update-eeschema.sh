set -e
set -u

SCH=$1

Xvfb :99 &
export DISPLAY=:99

eeschema $SCH &

FWID=""
while [ "$FWID" = "" ]; do
    sleep 1
    FWID=$(xdotool search --onlyvisible --sync --classname Eeschema)
done
echo "Found first eeschema window $FWID"
WINDOW_NAME=$(xdotool getwindowname $FWID)
echo "window name: [$WINDOW_NAME]"
if [[ "$WINDOW_NAME" == "Project Rescue Helper" ]]; then
    # click in the lower right
    eval $(xwininfo -id $FWID |
    sed -n -e "s/^ \+Absolute upper-left X: \+\([0-9]\+\).*/x=\1/p" \
           -e "s/^ \+Absolute upper-left Y: \+\([0-9]\+\).*/y=\1/p" \
           -e "s/^ \+Width: \+\([0-9]\+\).*/w=\1/p" \
           -e "s/^ \+Height: \+\([0-9]\+\).*/h=\1/p" )
    BTN_X=$(echo "$w * 0.95" | bc)
    BTN_Y=$(echo "$h * 0.98" | bc)
    xdotool mousemove --window $FWID $BTN_X $BTN_Y click 1

    # Save
    MWID=""
    while [ "$MWID" = "" ]; do
        echo "Waiting for main window..."
        sleep 1
        MWID=$(xdotool search --onlyvisible --sync --classname Eeschema || true)
    done
    echo "Found main window $MWID"
    xdotool key --window $MWID ctrl+s

    echo "Waiting for error window..."
    sleep 0.2
    EWID=$(xdotool search --onlyvisible --sync --classname Eeschema | grep -v $MWID || true)
    if [ "$EWID" != "" ]; then
        xdotool key --window $EWID "Return"
    fi
    xdotool key --window $MWID ctrl+q
fi

kill %1
kill %2 || true
