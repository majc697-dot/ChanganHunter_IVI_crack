#!/system/bin/sh
CP=/data/local/tmp/cap.log
echo "=== file size ==="
wc -l $CP
echo
echo "=== 1) HardKey / CAN-RPC related ==="
grep -inE 'hardkey|HardKey|HardkeyKey|RpcIviGrp_HardKey|STEERING|keyName|Keyname|Keystatus' $CP | head -80
echo
echo "=== 2) keyevent dispatch ==="
grep -inE 'KeyEvent|keyCode|interceptKey|dispatchKey' $CP | grep -viE 'InputMethod|IME ' | head -60
echo
echo "=== 3) kugou / netease / adapter / source routing ==="
grep -inE 'kugou|netease|AdapterMusic|currentSource|updateSourcePkg|KgAuto' $CP | head -80
