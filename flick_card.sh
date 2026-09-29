#!/system/bin/sh
rm -f /sdcard/card_*.png
i=0
while [ $i -le 8 ]; do
    n=$(printf %02d $i)
    screencap -p /sdcard/card_$n.png
    if [ $i -eq 2 ] || [ $i -eq 5 ]; then
        echo "tap AMap card next at $(date +%H:%M:%S.%N)"
        input tap 827 596
    fi
    i=$((i+1))
    sleep 0.4
done
