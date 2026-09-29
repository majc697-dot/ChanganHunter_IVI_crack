#!/system/bin/sh
DB=/data/data/com.autoai.project.launcher/databases/com.bon.da.launcher.db
echo "===== tables ====="
sqlite3 "$DB" "SELECT name FROM sqlite_master WHERE type='table';"
echo "===== schema ====="
sqlite3 "$DB" ".schema shortcut"
echo "===== id=15 full row ====="
sqlite3 "$DB" "SELECT * FROM shortcut WHERE id=15;"
echo "===== id=19 full row (amap) ====="
sqlite3 "$DB" "SELECT * FROM shortcut WHERE id=19;"
echo "===== id=3 media ====="
sqlite3 "$DB" "SELECT * FROM shortcut WHERE id=3;"
echo "===== distinct icon ====="
sqlite3 "$DB" "SELECT DISTINCT icon FROM shortcut;"
echo "===== distinct type/container/span ====="
sqlite3 "$DB" "SELECT DISTINCT type,container,spanX,spanY FROM shortcut;"
echo "===== prefs ====="
ls -l /data/data/com.autoai.project.launcher/shared_prefs/ 2>/dev/null
for f in /data/data/com.autoai.project.launcher/shared_prefs/*.xml; do echo "--- $f"; cat "$f"; done
