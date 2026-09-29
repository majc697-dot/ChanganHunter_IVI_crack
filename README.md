# ChanganHunter_IVI_crack
This project aims to expand the functionality of the car entertainment system host that can enable ADB and has a MediaTek MT8666 processor
# MT8666 车机 方向盘媒体键 → 第三方播放器 桥接技术总结

> 日期：2026-09-24
> 设备：MT8666 安卓车机，型号 `spm8666p2_64_car`，Android 9 (SDK 28)，userdebug，已 root，SELinux Enforcing
> 序列号：`FNASF432DS4BR81141`
> ADB：`C:\Program Files\AYA\resources\adb\adb.exe`
> 涉及应用：酷狗车机版 `com.kugou.android.auto`、网易云车机版 `com.netease.cloudmusic.iot`、原车桌面 `com.autoai.project.launcher`

---

## 1. 最终效果（已真车验证）

- 方向盘 **下一曲 / 上一曲 / 播放暂停** 在网易云播放、以及暂停后 10 分钟内，均控制网易云，酷狗不会被唤起、不会抢控。
- 酷狗的私有 SDK 控制通道被禁用后，原车链路对这三个键变为空操作，不会崩溃、不会乱控制。
- 桌面已恢复为原车 Launcher（HOME 键回到原车桌面）。
- **高德地图前台/导航中按切歌键导致 dock 与状态栏导航图标疯狂闪烁的问题已修复**（根因与修复见第 4A 节，用户现场确认）。

## 2. 方向盘按键的真实链路（关键结论：不走 Linux input）

方向盘键 **不是标准 KeyEvent，不出现在任何 /dev/input 设备里**，getevent/`input keyevent` 完全无关：

```
方向盘按键 → CAN 总线 → MCU → CCCI(Modem 共享内存通道) → RpcManager(/system/framework/RpcManager.jar, BOOTCLASSPATH)
          → Launcher 进程 CommonService$3.onHKChange()
          → HKManager.notice() → CmdManager → MediaCmdExecutor / LocalCmdExecutor
```

### 2.1 键码表（抓包 + 反编译双重确认）

| keyCode | 含义 | 原车路由 |
|---|---|---|
| 2 | 上一曲 | MediaCmdExecutor（按当前音源分发） |
| 3 | 下一曲 | 同上 |
| 12 | 播放/暂停 | 同上（非 20/34 源时按 isRealPlaying 决定 play/pause） |
| 9 | MODE 切音源 | 音源切换逻辑 |
| 6 | 语音 | LocalCmdExecutor |
| 7 / 8 | 音量+ / 音量- | LocalCmdExecutor |
| 11 | DVR | LocalCmdExecutor |

`keyState`：**0 = 按下边沿（只处理 0），1 = 松开**。

### 2.2 日志指纹（桥接程序就是靠它取键）

每次按键，Launcher 会打两条（按下+松开）logcat，tag 恒为 `Launcher-library-common`：

```
I/Launcher-library-common(12153): [ (CommonService.java:548)#OnHKChange ] HK onHKChange   keyCode  :  3  keyState  : 0 source 0
```

**两个大坑：**
1. `#OnHKChange ]` 的 **`]` 前有一个空格**，匹配串少了空格会一条都抓不到。
2. 同一格式还可能带前缀（见 raw 日志中有 `I [ (...)#OnHKChange ]` 双 I 的形式），所以匹配模式用宽松的 `*"OnHKChange"*"keyCode"*` 最稳。

## 3. 为什么原车按键永远控制酷狗

### 3.1 音源白名单

- 中枢 SourceManager 的 currentSource 由 FocusManager 监听系统广播 `android.media.AUDIO_FOCUS_CHANGED_ACTION` 后按**硬编码包名白名单**更新；白名单：QQ 音乐 / 喜马拉雅 / 酷我 / 酷狗 / 优酷 / 唱吧 / common.app。
- **网易云不在白名单**，即使拿到音频焦点也被忽略（日志 "other media source ignore"）。
- 音源号：21=酷狗（实测恒为 21）、17=酷我、19=QQ、20=唱吧、34=优酷、1/2=FM/AM、11=U 盘、14=蓝牙。网易云虽有 `MODULE_NETEASE_MUSIC=5`，但 `MainService$1.getNetEaseMusic()` 恒返回 null。
- LiveDataBus 是进程内总线，SourceManager 无导出接口，两个 service 都不在 binder service list → **外部无法直接改 currentSource**。

### 3.2 酷狗 SDK 的绑定关系（杀不掉的根因）

Launcher（uid 1000）在开机后 bindService 绑定酷狗的 AIDL 服务：

```
com.kugou.android.auto/com.kugou.auto.proxy.AutoSdkAIDLRemoteService
action: android.intent.action.AutoSdkAIDLRemoteService
```

`dumpsys activity services com.kugou.android.auto` 可见 AppBindRecord（Launcher 是绑定方）。所以即使清最近任务、force-stop，酷狗进程也会被绑定关系拉起。按键时 KeyGouController 直接调 `IKgAutoInterface.executeAction("PLAYER_NEXT"/"PLAYER_PREVIOUS"/"PLAYER_PLAY"/"PLAYER_PAUSE", Bundle)`。

### 3.3 SDK 客户端的断连兜底（禁用服务为何安全）

反编译 Launcher 内嵌的酷狗 SDK（`com.kugou.auto.proxy.KgAutoProxy / ActionExecute`）：

- 每次调用前先 `checkAidlServiceAndAutoBind()`；服务未连接时：
  - 布尔/对象查询返回 `new BooleanResult(7, "AIDL 服务未连接")`，**不抛异常**；
  - `isAppRunning()` 返回 errorCode=7（非成功），KeyGouController 据此认为酷狗没运行而直接 return；
  - Void 动作（play/pause/next）只缓存 action，返回 errorCode=7；
- `ServiceConnection.onServiceDisconnected()` 仅把 aidl 引用置 0 并打日志，无重连风暴；
- transact 失败也被 catch 成 errorCode=7（"AIDL 服务调用失败"）。

**结论：让该组件无法绑定/启动后，原车链路全部空转，Launcher 进程不受影响（实测 pid 12153 全程未重启）。**

## 4. 解决方案（已实施）

### 4.1 禁用酷狗私有服务（root，持久，可回滚）

```sh
# 生效（注意 disable-user 在本机返回 default 不生效，必须 root 下用 pm disable）
pm disable com.kugou.android.auto/com.kugou.auto.proxy.AutoSdkAIDLRemoteService
# 回滚：
pm enable  com.kugou.android.auto/com.kugou.auto.proxy.AutoSdkAIDLRemoteService
```

禁用后 `dumpsys package com.kugou.android.auto` 的 `disabledComponents:` 中出现该组件；酷狗 App 本身仍可手动打开使用（打开后只是 Launcher 不再能私有控制它，方向盘对它空转）。

### 4.2 桥接守护脚本

文件：设备 `/data/local/tmp/netease_hk_v4.sh`（工作区同名副本），日志：
- `/data/local/tmp/netease_hk.log`（转发决策）
- `/data/local/tmp/netease_hk.raw`（原始按键行）

原理：`logcat` 监听 OnHKChange → 解析 keyCode/keyState（只处理 state=0）→ 查 `dumpsys media_session` 找到正在播放或暂停不久的第三方会话 → 用系统自带 media 命令转发标准媒体键。

启动方式（必须 setsid 脱离 shell，且不要在同一条命令里用 pkill 匹配自身命令行，否则 exit 143 自杀）：

```sh
setsid sh /data/local/tmp/netease_hk_v4.sh </dev/null >/dev/null 2>&1 &
```

### 4.3 设备自带 media 命令（无需自己写 binder）

```sh
# 实际是：
CLASSPATH=/system/framework/media_cmd.jar app_process / com.android.commands.media.Media dispatch next
# 设备上 /system/bin/media 已包好，直接：
media dispatch play | pause | play-pause | stop | next | previous
media list-sessions
```

实测即使 "Media button session is null"，只要有 active 的播放会话，`media dispatch` 也能正确路由到它。

### 4.4 会话状态判定

`dumpsys media_session` 的 Sessions Stack 中，每个会话有：

- `package=` 包名
- `active=true/false`
- `state=PlaybackState {state=N, ..., updated=<ms>}`：**3=播放，2=暂停**
- `updated=` 是 `SystemClock.elapsedRealtime()` 毫秒，可与 `/proc/uptime`（秒）比较，得出"暂停了多久"。

**门控策略（v4）**：
- state=3：无条件转发；
- state=2：暂停后 600 秒（10 分钟，脚本里 `GRACE`）内仍转发——所以暂停后可按播放键恢复、按上下曲直接切歌并续播；超过 10 分钟不再接管，把方向盘让回原车音源（收音机等本来就没有 MediaSession，无法被标准接口感知，只能靠时间窗折中）；
- 优先级：网易云 > 酷狗。

### 4.5 toybox awk 坑

设备 `/system/bin/awk` 是 toybox 精简版，`match($0,/re/)` + RSTART/RLENGTH 会报 `awk: illegal jump type 339`。提取数字改用 sub 链：

```awk
ps=$0; sub(/.*state=/,"",ps); sub(/[^0-9].*/,"",ps)
up=$0; sub(/.*updated=/,"",up); sub(/[^0-9].*/,"",up)
```

## 4A. 高德前台切歌时图标疯狂闪烁（AutoSdkEmptyActivity 重连风暴）

### 4A.1 现象

高德地图在前台（尤其 turn-by-turn 导航中）按方向盘切歌键：
- 左侧悬浮 dock（第三方悬浮球 `com.shere.assistivetouch`）的导航纸飞机按钮以 ~10Hz 亮灭/变样式；
- 顶部状态栏（实为原车 Launcher 的 `ChangAn-StatusBar` 窗口）右上角导航纸飞机图标时有时无、疯狂闪烁。

### 4A.2 根因（logcat 铁证，非媒体键/音频焦点问题）

只禁用 `AutoSdkAIDLRemoteService` **不够**。Launcher 内嵌酷狗 SDK 的 `KgAutoProxy.bindKgAidlService()`（见 `decomp_kgproxy_full.txt` L66-126）断线重连有三级兜底：

1. `bindService(AutoSdkAIDLRemoteService)` → 服务被禁，返回 false；
2. `startForegroundService(...)` → AMS 报 "Unable to start service ... not found"，返回 null；
3. `startKgAidlActivity()` → **startActivity 启动酷狗的透明页 `com.kugou.auto.proxy.AutoSdkEmptyActivity`（FLAG_ACTIVITY_NEW_TASK）**——该 Activity 当时未禁用，启动成功并成为新顶层任务。

而 EmptyActivity 一创建就广播 `android.intent.action.AutoSdkEmptyActivity.onCreate`，`KgAutoProxy$4.onReceive` 收到后**再次调用 bindKgAidlService()**，回到第 1 步——自激死循环，每圈 70~120ms。另外每次方向盘媒体键，`KeyGouController` 都会先调 `checkAidlServiceAndAutoBind()`（反编译 L186）再执行动作，给风暴续一次命——所以"按键后闪得最凶"。

实测日志（风暴期每秒十余次，累计 4300+）：

```
23:05:06.371 CAR.AM: New top task: ...AutoSdkEmptyActivity  taskId=26506
23:05:06.371 CAR.AM: New top task: ...MainMapActivity(高德)  taskId=5375
23:05:06.453 CAR.AM: New top task: ...AutoSdkEmptyActivity  taskId=26507
23:05:06.537 CAR.AM: New top task: ...MainMapActivity(高德)
23:05:06.607 CAR.AM: New top task: ...AutoSdkEmptyActivity  taskId=26508
```

顶层任务在 高德 ↔ 酷狗透明页之间以 ~12Hz 反复抢夺。dock 与状态栏都在监听前台任务/导航状态，各自重绘导航指示图标 → 两处同步闪烁；非导航界面没有导航指示图标可闪，所以不易察觉。

### 4A.3 为什么前期受控实验复现不出来

- `media dispatch` 走 MediaSession 直投，**不触发** Launcher 的 checkAidl 重连，录屏/screencap 均无变化；
- `log -t` 注入 OnHKChange 只能骗过守护脚本，同样不触发原生 HK 链路；
- screenrecord 对该类抖动取证不如 logcat 直接（最终靠 `CAR.AM New top task` 日志定性）。

### 4A.4 修复（已实施，持久，已真车确认）

把透明页组件也禁用，循环在第 3 步被打断：

```sh
pm disable com.kugou.android.auto/com.kugou.auto.proxy.AutoSdkEmptyActivity
# 回滚：
pm enable  com.kugou.android.auto/com.kugou.auto.proxy.AutoSdkEmptyActivity
```

禁用后行为（已验证安全）：

- startActivity 对已禁用组件抛 `ActivityNotFoundException`，被 `checkAidlServiceAndAutoBind()` 自身的 try/catch 捕获（日志 `checkAidlServiceAndAutoBind bindKgAidlService e：android.content.ActivityNotFoundException...`），**Launcher 不崩溃（pid 12153 全程未变）**；
- EmptyActivity 无法创建 → 无 onCreate 广播 → 无自激循环，`New top task` 抖动归零；
- 每次按键仍会留一条 ActivityNotFoundException 错误日志（无害噪音）；
- 录屏 ROI 帧差：修复前 dock 区持续 8.6~34.6 灰度差脉动，修复后切歌窗口与静默期均 ≈ 0；
- 用户现场连按上一曲/下一曲/音量键确认：两处图标稳定，切歌正常。

`dumpsys package com.kugou.android.auto` 的 `disabledComponents:` 现包含两个组件：
`AutoSdkAIDLRemoteService`、`AutoSdkEmptyActivity`（均写入 package-restrictions.xml，重启保持）。

> 教训：对这类"绑定方在系统进程、被绑定 App 内带透明拉起 Activity"的私有 SDK，只禁 Service 会把重连流量赶到 Activity 拉起路径并造成前台任务抖动；**Service + EmptyActivity 必须成对禁用**。

## 5. 桌面（HOME）切换备忘

原车 Launcher 硬编码应用列表（DB shortcut 固定 20 槽 + 包名 if-else 链，第三方包名走 `HomeUtils.startCommonApp` 必崩），无法显示第三方图标。曾临时切换到 Taskbar：

```sh
# 切到 Taskbar 桌面：
cmd package set-home-activity com.farmerbb.taskbar/.activity.HomeActivity
# 恢复原车桌面（当前状态）：
cmd package set-home-activity com.autoai.project.launcher/com.autoai.project.home.LauncherActivity
am force-stop com.farmerbb.taskbar     # 同时去掉它的底部 dock 栏
# 查询当前默认桌面：
cmd package resolve-activity -a android.intent.action.MAIN -c android.intent.category.HOME
```

原车 Launcher DB 备份：设备 `/data/local/tmp/dbbackup/launcher.db.orig`。

## 6. 开机持久化（当前未做，守护重启会丢失）

桥接目前是 setsid 临时进程，重启失效。可选路线（按推荐度）：

1. **Magisk 服务脚本**（若装了 Magisk）：`/data/adb/service.d/netease_hk.sh`，开机 late_start 后以 root 常驻，最省事且不动 /system。
2. **init.rc 注入**：root remount 后在 `/system/etc/init/` 或 vendor init 里加一个 `service`，`class late_start`、`user root`、`seclabel u:r:su:s0`（本环境 su 上下文跑 logcat+media 实测 SELinux 不拒）；OTA/校验风险自担。
3. **做成 App（见第 7 节）**。

禁用酷狗组件那条 `pm disable` 已经持久（写 /data/system/users/0/package-restrictions.xml），重启保持，无需再处理。

## 7. 给后续 App 开发的路线建议

要把脚本变成正式 App，需要两个能力：**①拿到方向盘键事件；②控制媒体会话**。

### 7.1 控制媒体（无 root 也可做）

走 **NotificationListenerService（通知使用权）**：

- Manifest 注册 `android.service.notification.NotificationListenerService`，引导用户在"设置→通知使用权"里授权；
- 通过 `getCurrentMediaNotificationSession()`（API 21+）/ 注册 `MediaController` 回调拿到当前媒体会话的 `MediaController`；
- 用 `MediaController.getTransportControls()` 的 `play() / pause() / skipToNext() / skipToPrevious()` 控制，**无需系统签名**；
- 包名过滤、播放状态（`PlaybackState.STATE_PLAYING=3 / STATE_PAUSED=2`）、position 时间戳都能直接从 MediaController 拿到，比解析 dumpsys 干净；
- 该服务还能监听通知/MediaSession 变化（`onNotificationPosted` 里 MediaStyle 通知带 session token），实现"谁在播控制谁"。

⚠️ 不要依赖 `MediaSessionManager.dispatchMediaKeyEvent()`——它要 `STATUS_BAR_SERVICE`（系统签名）；`MediaSessionManager.getActiveSessions()` 也要 `android.permission.MEDIA_CONTENT_CONTROL`（签名级），第三方 App 只有 NLS 这条路能合法拿到 MediaController。

### 7.2 拿方向盘键（本平台必须特权）

按键不经过 input 子系统，普通 App/无障碍服务都收不到，只有三条路：

1. **root 伴随进程（本设备最现实）**：App 内 `Runtime.getRuntime().exec("su")`，起 `logcat -s Launcher-library-common:V` 子进程读 OnHKChange，解析逻辑与现有脚本相同；配合 7.1 的 NLS 做控制，App 本体只管 UI/策略/开机自启（`BOOT_COMPLETED` + 前台服务）。
2. **系统特权 App**：放入 `/system/priv-app/`（或 /vendor/priv-app），在 privapp-permissions 白名单里授 `READ_LOGS`，App 直接 `Runtime.exec("logcat")` 读键；控制仍建议 NLS（`MEDIA_CONTENT_CONTROL` 是 signature 级，需要平台签名，本系统 APK 均为 NavInfo 私钥签名，拿不到平台 key）。
3. **直连 RpcManager**：`/system/framework/RpcManager.jar` 在 BOOTCLASSPATH，理论上可反射/编译期引用其类直接订阅 HK 事件，但接口非公开、需要系统权限与平台签名配合，成本最高，不建议优先尝试。

### 7.3 App 与现方案的功能等价清单

- 键值映射：2=prev, 3=next, 12=play-pause，只响应 keyState=0；
- 日志匹配用 `OnHKChange` 宽松子串，解析两个字段注意多空格；
- 目标选择：active 会话 + 包名白名单(cloudmusic/kugou) + state∈{2,3}；
- 暂停宽限期：用 `PlaybackState.getPosition()` 不可靠（暂停时 position 冻结），应记录**收到 STATE_PAUSED 的时刻**自行计时（App 里这是顺手的事，脚本里才用 dumpsys updated 字段对 /proc/uptime）；
- 保留"超过宽限期不接管"，避免用户切回收音机后按键误唤起网易云；
- 酷狗组件禁用是**一次性 root 操作**，App 首次运行时用 su 执行并提供"恢复"按钮（`pm enable`），不要每次开机执行；**必须成对禁用 Service 与 AutoSdkEmptyActivity**，只禁 Service 会触发透明页重连风暴导致前台 UI 闪烁（见 4A 节）。

## 8. 回滚总表

| 改动 | 回滚命令 |
|---|---|
| 酷狗 SDK 服务被禁用 | `pm enable com.kugou.android.auto/com.kugou.auto.proxy.AutoSdkAIDLRemoteService` |
| 酷狗透明拉起页被禁用（防闪烁，见 4A） | `pm enable com.kugou.android.auto/com.kugou.auto.proxy.AutoSdkEmptyActivity` |
| 桥接守护 | `pkill -f netease_hk_v4[.]sh`（另开一条 adb 命令执行） |
| 桌面（当前已是原车） | 无需操作；如再切到 Taskbar 想回来：`cmd package set-home-activity com.autoai.project.launcher/com.autoai.project.home.LauncherActivity && am force-stop com.farmerbb.taskbar` |

## 9. 现场产物索引（工作区）

- `netease_hk_v4.sh`：当前在用的守护脚本（设备同路径 `/data/local/tmp/`）
- `test_parser.sh`：dumpsys 会话解析的最小验证脚本
- `keycap.log`：首轮全键抓包原始日志
- `decomp_hardkey.txt`：KeyGouController（L430+）等硬键控制器
- `decomp_kgproxy_full.txt` / `decomp_actionexec.txt`：酷狗 SDK 代理与 errorCode=7 兜底
- `decomp_routing.txt`：HKStateControl、CommonManager.next/pre/play/pause/getCurrentSource
- `decomp_common_adapter.txt` / `decomp_focus.txt`：SourceManager、FocusManager 音源白名单
- `decomp_cmd.txt` / `decomp_exec.txt` / `decomp_more.txt`：HKManager 命令分发全量
- `decomp_launcher.txt` / `decomp_homeutils.txt`：桌面应用列表/启动硬编码链
- `s_home_orig.png`、`s_n_now.png`：恢复原车桌面、网易云播放页截图
- 闪烁排查（4A 节）：`analyze_nav.py` / `analyze_video.py` / `analyze_study.py`（ROI 帧差分析）、`burst_evt.sh` / `fastcap.sh`（并发 screencap）、`study_nav.mp4`（修复前风暴期录屏，dock 区持续脉动）、`study_fix.mp4`（修复后录屏，帧差≈0）、`fix_now.png`（修复后导航界面）、`realkey.log`（设备 `/data/local/tmp/`，真实按键验证日志）
