#!/system/bin/sh
LOG=/data/local/tmp/keytest.log
: > $LOG

state_snap() {
  dumpsys media_session | grep -A18 'SessionTag com.netease' | grep -E 'state=|description=|updated=|actions='
}

echo "########## BASELINE ##########" | tee -a $LOG
state_snap | tee -a $LOG

# 87=NEXT 86=PREV 85=PLAY/PAUSE
for KC in 87 86 85; do
  echo "" | tee -a $LOG
  echo "########## input keyevent $KC ##########" | tee -a $LOG
  logcat -c
  input keyevent $KC
  sleep 2
  state_snap | tee -a $LOG
  echo "---- logcat hits ----" | tee -a $LOG
  logcat -d -v brief 2>/dev/null | grep -iE 'MediaSession|MediaButton|netease|kugou|dispatchMedia|TransportControl' | grep -viE 'chatty' | tail -20 | tee -a $LOG
done

echo "" | tee -a $LOG
echo "########## media dispatch next (framework media key path) ##########" | tee -a $LOG
logcat -c
media dispatch next 2>&1 | tee -a $LOG
sleep 2
state_snap | tee -a $LOG
logcat -d -v brief 2>/dev/null | grep -iE 'MediaSession|MediaButton|netease|kugou' | grep -viE 'chatty' | tail -20 | tee -a $LOG
