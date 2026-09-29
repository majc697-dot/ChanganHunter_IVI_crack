#!/system/bin/sh
# kill every daemon instance running netease_hk_v4.sh and its logcat pipe
for p in /proc/[0-9]*; do
    pid=${p#/proc/}
    cmd=$(tr '\0' ' ' < $p/cmdline 2>/dev/null)
    case "$cmd" in
        sh\ */data/local/tmp/netease_hk_v4.sh*)
            echo "kill daemon pid=$pid cmd=$cmd"
            kill "$pid" 2>/dev/null
            ;;
        logcat*Launcher-library-common*)
            echo "kill logcat pid=$pid"
            kill "$pid" 2>/dev/null
            ;;
    esac
done
sleep 1
echo remaining:
for p in /proc/[0-9]*; do
    pid=${p#/proc/}
    cmd=$(tr '\0' ' ' < $p/cmdline 2>/dev/null)
    case "$cmd" in
        *netease_hk_v4.sh*|logcat*Launcher-library-common*) echo "STILL $pid $cmd" ;;
    esac
done
echo done
