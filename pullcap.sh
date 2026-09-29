#!/system/bin/sh
echo "=== file sizes ==="
wc -l /data/local/tmp/cap.log /data/local/tmp/getevent.log
echo "=== getevent content ==="
cat /data/local/tmp/getevent.log
echo "=== hardkey / rpc hits in logcat ==="
grep -inE 'hardkey|HardKey|HardkeyKey|RpcIvi|STEERING|keyName|KeyStatus' /data/local/tmp/cap.log | head -60
