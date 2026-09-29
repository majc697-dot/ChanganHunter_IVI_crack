#!/system/bin/sh
DB=/data/data/com.autoai.project.launcher/databases/com.bon.da.launcher.db
echo "########## SHORTCUT INTENTS (music related) ##########"
sqlite3 "$DB" "SELECT id,title,intent FROM shortcut WHERE title LIKE '%音%' OR pkgName LIKE '%music%' OR pkgName LIKE '%kugou%' OR pkgName LIKE '%kuwo%';"
echo
echo "########## music packages installed ##########"
pm list packages | grep -iE 'kuwo|kugou|netease|ximalaya'
echo
echo "########## system priv-app list ##########"
ls /system/priv-app/
echo "---- system/app ----"
ls /system/app/
echo
echo "########## NETEASE manifest: receivers/services key bits ##########"
dumpsys package com.netease.cloudmusic.iot | grep -iE 'MEDIA_BUTTON|MEDIA_PREFERENCE|AUDIO_BECOMING_NOISY|receiver|BroadcastReceiver' | head -40
echo
echo "########## KUGOU manifest media button receiver ##########"
dumpsys package com.kugou.android.auto | grep -B2 -A2 -iE 'MEDIA_BUTTON' | head -40
