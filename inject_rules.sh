#!/system/bin/sh
# 补齐 init -> su 域转换所需的完整 SELinux 规则
MP=/data/local/tmp/magiskpolicy

echo "=== before inject ==="
$MP --live "allow init su process transition"
echo "rule1(transition) RC=$?"
$MP --live "allow init su process rlimitinh"
echo "rule2(rlimitinh) RC=$?"
$MP --live "allow init su process siginh"
echo "rule3(siginh) RC=$?"
$MP --live "allow init su process sigchld"
echo "rule4(sigchld) RC=$?"
$MP --live "allow init su process sigkill"
echo "rule5(sigkill) RC=$?"
$MP --live "allow su system_file file entrypoint"
echo "rule6(entrypoint) RC=$?"
$MP --live "allow su system_file file read"
echo "rule7(read) RC=$?"
$MP --live "allow su system_file file execute"
echo "rule8(execute) RC=$?"
$MP --live "allow su system_file file getattr"
echo "rule9(getattr) RC=$?"
$MP --live "allow su system_file file open"
echo "rule10(open) RC=$?"

echo "=== switch to enforcing ==="
setenforce 1
getenforce

echo "=== restart hh_rootd ==="
setprop ctl.stop hh_rootd
sleep 1
setprop ctl.start hh_rootd
sleep 2

echo "=== dmesg ==="
dmesg | grep hh_rootd | tail -6

echo "=== ps ==="
ps -A | grep hh_rootd | grep -v grep

echo "=== test connect ==="
echo "id; exit" | toybox nc -w 3 127.0.0.1 9753
echo "NC_RC=$?"
