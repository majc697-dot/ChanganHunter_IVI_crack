#!/system/bin/sh
DUR=100
rm -f /data/local/tmp/getevent.log /data/local/tmp/cap.log /data/local/tmp/session_before.txt /data/local/tmp/session_after.txt
dumpsys media_session > /data/local/tmp/session_before.txt
logcat -c -b all
getevent -lt > /data/local/tmp/getevent.log 2>&1 &
GE=$!
timeout $DUR logcat -b all -v threadtime > /data/local/tmp/cap.log 2>&1
kill $GE 2>/dev/null
dumpsys media_session > /data/local/tmp/session_after.txt
echo "CAPTURE DONE"
wc -l /data/local/tmp/cap.log /data/local/tmp/getevent.log
