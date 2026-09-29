#!/system/bin/sh
OUT=/data/local/tmp/hktest.log
: > $OUT
logcat -c 2>/dev/null
timeout 120 logcat -v brief 'Launcher-library-common:V' 'MediaSessionService:I' 'MediaButtonReceiver:I' '*:S' >> $OUT 2>&1
# also capture unfiltered media session dispatch markers
echo DONE >> $OUT
