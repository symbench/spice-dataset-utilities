pkill eeschema
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
WINDOW_NAME=$(xdotool getwindowname $FWID)
echo $WINDOW_NAME

kill %1
kill %2 || true
