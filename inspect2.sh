#!/system/bin/sh
DB=/data/data/com.autoai.project.launcher/databases/com.bon.da.launcher.db
echo "########## sqlite3 check ##########"
which sqlite3 || echo "NO_SQLITE3"
echo
echo "########## DB schema ##########"
sqlite3 "$DB" ".schema" 2>&1 | head -100
echo
echo "########## tables row count ##########"
for t in $(sqlite3 "$DB" "SELECT name FROM sqlite_master WHERE type='table';" 2>/dev/null); do
  cnt=$(sqlite3 "$DB" "SELECT COUNT(*) FROM $t;" 2>/dev/null)
  echo "TABLE $t rows=$cnt"
done
echo
echo "########## MEDIA SESSION DUMPSYS ##########"
dumpsys media_session 2>&1 | head -120
