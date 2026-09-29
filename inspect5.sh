#!/system/bin/sh
echo "########## NETEASE package dump (components) ##########"
dumpsys package com.netease.cloudmusic.iot > /data/local/tmp/netease_pkg.txt
wc -l /data/local/tmp/netease_pkg.txt
echo "---- Receivers section ----"
grep -n -A40 '^  Receivers:' /data/local/tmp/netease_pkg.txt | head -80
echo "---- MEDIA_BUTTON anywhere ----"
grep -n -i 'media_button\|MEDIA_PREFERENCE\|becoming_noisy' /data/local/tmp/netease_pkg.txt
echo "---- launchable activities ----"
cmd package query-activities --components -a android.intent.action.MAIN -c android.intent.category.LAUNCHER com.netease.cloudmusic.iot 2>/dev/null || dumpsys package com.netease.cloudmusic.iot | grep -B2 -A8 'android.intent.action.MAIN'
echo
echo "########## Vendor services (car/key/media related) ##########"
dumpsys -l | grep -iE 'car|vehicle|key|media|audio|can|mcu|input|hardkey'
echo
echo "########## CarService dumpsys (key events handling) ##########"
dumpsys car_service 2>/dev/null | head -60
