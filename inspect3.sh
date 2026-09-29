#!/system/bin/sh
DB=/data/data/com.autoai.project.launcher/databases/com.bon.da.launcher.db
echo "########## SHORTCUT TABLE ##########"
sqlite3 -header "$DB" "SELECT id,title,screen,cellX,cellY,type,container,pkgName FROM shortcut ORDER BY container,screen,cellY,cellX;"
echo
echo "########## distinct pkgName in workspace ##########"
sqlite3 "$DB" "SELECT DISTINCT pkgName FROM shortcut;"
echo
echo "########## INPUT DEVICES ##########"
cat /proc/bus/input/devices
echo
echo "########## KEY LAYOUT FILES ##########"
ls -la /system/usr/keylayout/ /vendor/usr/keylayout/ 2>/dev/null
