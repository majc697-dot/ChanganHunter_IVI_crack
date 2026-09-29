#!/system/bin/sh
DB=/data/data/com.autoai.project.launcher/databases/com.bon.da.launcher.db
mkdir -p /data/local/tmp/dbbackup
cp -p "$DB" /data/local/tmp/dbbackup/launcher.db.orig
echo "===== rows ====="
sqlite3 "$DB" "SELECT id,title,icon,screen,cellX,cellY,type,container,pkgName FROM shortcut ORDER BY screen,cellY,cellX;"
echo "===== count type=0 ====="
sqlite3 "$DB" "SELECT count(*) FROM shortcut WHERE type=0;"
echo "===== tables ====="
sqlite3 "$DB" ".tables"
