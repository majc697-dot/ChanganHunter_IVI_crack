#!/system/bin/sh
# Steering-wheel -> NetEase CloudMusic bridge (v2)
# keys: 2=previous 3=next 12=play/pause, state 0 = press edge
LOG=/data/local/tmp/netease_hk.log
RAW=/data/local/tmp/netease_hk.raw
PKG=com.netease.cloudmusic.iot

echo "$(date) bridge v2 start pid=$$" > $LOG
: > $RAW
logcat -c 2>/dev/null

logcat -v brief 'Launcher-library-common:V' '*:S' 2>/dev/null | while IFS= read -r line; do
    case "$line" in
        *"#OnHKChange] HK onHKChange"*)
            echo "$line" >> $RAW
            t=${line##*keyCode : }; code=${t%% keyState*}
            t=${line##*keyState : }; state=${t%% source*}
            [ "$state" = "0" ] || continue
            case "$code" in
                2) key=previous ;;
                3) key=next ;;
                12) key=play-pause ;;
                *) continue ;;
            esac
            mbs=$(dumpsys media_session 2>/dev/null | grep 'Media button session')
            case "$mbs" in
                *$PKG*)
                    echo "$(date) FWD code=$code -> $key | $mbs" >> $LOG
                    /system/bin/media dispatch "$key" >> $LOG 2>&1
                    ;;
                *)
                    echo "$(date) skip code=$code | $mbs" >> $LOG
                    ;;
            esac
            ;;
    esac
done
echo "$(date) bridge exit" >> $LOG
