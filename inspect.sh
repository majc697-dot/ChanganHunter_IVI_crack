#!/system/bin/sh
echo "########## 1. LAUNCHER DATA DIRS ##########"
ls -la /data/data/com.autoai.project.launcher/databases/
echo "---- files ----"
ls -la /data/data/com.autoai.project.launcher/files/
echo "---- shared_prefs ----"
ls -la /data/data/com.autoai.project.launcher/shared_prefs/
echo
echo "########## 2. config.properties ##########"
cat /data/data/com.autoai.project.launcher/cache/config.properties
echo
echo "########## 3. shared_prefs content ##########"
for f in /data/data/com.autoai.project.launcher/shared_prefs/*.xml; do
  echo "==== $f ===="
  cat "$f"
done
echo
echo "########## 4. system CA_Launcher dir ##########"
ls -la /system/app/CA_Launcher/
echo
echo "########## 5. system etc configs (autoai/launcher) ##########"
ls /system/etc/ | grep -iE 'autoai|launcher|whitelist|blacklist|applist|car'
ls /vendor/etc/ 2>/dev/null | grep -iE 'autoai|launcher|whitelist|blacklist|applist|car'
echo
echo "########## 6. preinstalled autoai dirs ##########"
ls /system/app/ | grep -iE 'autoai|kugou|netease|music'
ls /system/priv-app/ 2>/dev/null | grep -iE 'autoai|kugou|netease|music'
