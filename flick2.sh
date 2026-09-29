#!/system/bin/sh
# usage: sh flick2.sh <tag> <action>  action: tap | next | none
tag=$1
act=$2
d=/data/local/tmp/f_$tag
rm -rf $d; mkdir -p $d
i=0
while [ $i -le 7 ]; do
    screencap -p $d/f_$(printf %02d $i).png
    if [ $i -eq 2 ]; then
        if [ "$act" = tap ]; then input tap 1400 320; fi
        if [ "$act" = next ]; then /system/bin/media dispatch next; fi
    fi
    i=$((i+1))
    sleep 0.25
done
md5sum $d/*.png
