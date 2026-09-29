#!/system/bin/sh
# capture steering-wheel keys: NetEase scenario + Kugou scenario
logcat -c
timeout 180 logcat -v time Launcher-library-common:V MediaSessionService:I MediaButtonEventReceiver:I '*:S' > /data/local/tmp/keycap.log 2>&1
echo DONE >> /data/local/tmp/keycap.log
