#!/system/bin/sh
rm -f /sdcard/flick_*.png
i=0
while [ $i -le 10 ]; do
    n=$(printf %02d $i)
    screencap -p /sdcard/flick_$n.png
    if [ $i -eq 2 ] || [ $i -eq 5 ] || [ $i -eq 8 ]; then
        echo "shot $n then dispatch next at $(date +%H:%M:%S.%N)"
        /system/bin/media dispatch next
    fi
    i=$((i+1))
    sleep 0.6
done
ls /sdcard/flick_*.png
