#!/usr/bin/env python3
"""
FusionOS 8.0 Mega Generator
Generates 1200 terminal commands + 890 features
"""
import re, sys, time

HTML_PATH = '/Users/murderdrones/Desktop/FusionOS.html'
WORK_PATH = '/Users/murderdrones/WorkBuddy/2026-06-15-12-25-08/vm-os.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# ─────────────────────────────────────────────────
# PART 1: Generate 1200 Terminal Commands
# ─────────────────────────────────────────────────

def esc(s):
    """Escape string for JS single-quoted string with unicode escapes"""
    return s.encode('unicode_escape').decode('ascii')

def cmd(name, output, comment=''):
    """Generate one terminal command entry"""
    c = f"  O['{name}']=function(){{return'{output}';}};"
    if comment:
        c = f"  /* {comment} */\n" + c
    return c + "\n"

def build_1200_commands():
    """Programmatically build 1200+ terminal commands"""
    entries = []
    
    # --- System Information (60 cmds) ---
    entries.append("  /* ── System Info ── */")
    for i, kv in enumerate([
        ('uname','\\u7cfb\\u7edf\\u4fe1\\u606f\\uff1aFusionOS 8.0 (kernel fusion-8.0.0)'),
        ('uname -a','FusionOS 8.0 hostname fusion-8.0.0 #1 SMP x86_64 GNU/Fusion'),
        ('uname -r','fusion-8.0.0'),
        ('uname -s','FusionOS'),
        ('uname -m','x86_64'),
        ('uname -n','fusion-desktop'),
        ('uname -v','#1 SMP Tue Jun 16 2026'),
        ('uname -o','GNU/Fusion'),
        ('hostname','fusion-desktop'),
        ('hostname -f','fusion-desktop.local'),
        ('hostname -i','127.0.0.1'),
        ('arch','x86_64'),
        ('lscpu','Architecture: x86_64\\nCPU(s): 16\\nThread(s) per core: 2\\nCore(s) per socket: 8\\nSocket(s): 1\\nModel: Fusion Virtual CPU @ 3.20GHz'),
        ('cpuinfo','processor: 0-15\\nvendor_id: GenuineFusion\\ncpu MHz: 3200.00\\ncache size: 8192 KB'),
        ('lspci','00:00.0 Host bridge\\n00:01.0 VGA display controller\\n00:02.0 Network controller\\n00:03.0 Audio device\\n00:04.0 USB controller'),
        ('lsusb','Bus 001 Device 001: ID 1d6b:0002\\nBus 002 Device 001: ID 1d6b:0003\\nBus 001 Device 002: ID 8087:0024'),
        ('lsblk','NAME   SIZE TYPE MOUNTPOINT\\nsda    256G disk\\n\\u251c\\u2500sda1 512M part /boot\\n\\u251c\\u2500sda2 200G part /\\n\\u2514\\u2500sda3  56G part /home'),
        ('lsmod','Module                  Size  Used by\\nfusion_core          262144  1\\nfusion_display        98304  2\\nfusion_net            65536  0\\nfusion_audio          49152  1\\nfusion_fs             81920  3'),
        ('dmesg','[0.000000] FusionOS 8.0 booting...\\n[0.100000] CPU: x86_64 (16 cores)\\n[0.200000] Memory: 16384MB\\n[0.300000] Fusion display initialized\\n[1.000000] Boot complete.'),
        ('dmesg -H','\\u250c\\u2500\\u2500 [2026-06-16 02:00] FusionOS 8.0 booting...\\n\\u2502\\n\\u251c\\u2500 [02:00:01] CPU initialized\\n\\u251c\\u2500 [02:00:02] Memory: 16GB OK\\n\\u2514\\u2500 [02:00:03] Boot complete'),
        ('uptime','02:00:41 up 3 days, 7:22, 1 user, load average: 0.08, 0.12, 0.09'),
        ('uptime -p','up 3 days, 7 hours, 22 minutes'),
        ('uptime -s','2026-06-12 18:38:41'),
        ('who','user      console  Jun 12 18:38'),
        ('whoami','user'),
        ('who -b','system boot  Jun 12 18:38'),
        ('who -r','run-level 5  Jun 12 18:38'),
        ('w','USER   TTY    FROM   LOGIN@   IDLE   JCPU   PCPU WHAT\\nuser   console -     18:38   3days  0.02s  0.01s -'),
        ('id','uid=1000(user) gid=1000(user) groups=1000(user),4(adm),27(sudo)'),
        ('id -u','1000'),
        ('id -g','1000'),
        ('groups','user adm sudo'),
        ('last','user     console        Tue Jun 16 02:00   still logged in\\nuser     console        Mon Jun 15 09:15 - 23:59  (14:44)\\nreboot   system boot    Fri Jun 12 18:38'),
        ('lastlog','Username   Port   From   Latest\\nroot       \\u2219\\u2219\\u2219    \\u2219\\u2219\\u2219   \\u2219\\u2219\\u2219 Never\\nuser       console       Tue Jun 16 02:00'),
        ('env','USER=user\\nHOME=/home/user\\nSHELL=/bin/fsh\\nPATH=/usr/local/bin:/usr/bin:/bin\\nLANG=zh_CN.UTF-8\\nTERM=xterm-256color\\nPWD=/home/user\\nFUSION_VERSION=8.0'),
        ('printenv','FUSION_VERSION=8.0\\nHOME=/home/user\\nLANG=zh_CN.UTF-8\\nPATH=/usr/bin:/bin'),
        ('printenv HOME','/home/user'),
        ('printenv PATH','/usr/local/bin:/usr/bin:/bin'),
        ('locale','LANG=zh_CN.UTF-8\\nLC_CTYPE=zh_CN.UTF-8\\nLC_NUMERIC=zh_CN.UTF-8\\nLC_TIME=zh_CN.UTF-8\\nLC_ALL='),
        ('locale -a','C\\nC.UTF-8\\nen_US.utf8\\nzh_CN.utf8\\nja_JP.utf8\\nko_KR.utf8'),
        ('localectl','System Locale: LANG=zh_CN.UTF-8\\nVC Keymap: us\\nX11 Layout: us'),
        ('timedatectl','Local time: Tue 2026-06-16 02:00:41 CST\\nUniversal time: Mon 2026-06-15 18:00:41 UTC\\nTimezone: Asia/Shanghai (CST, +0800)'),
        ('date','Tue Jun 16 02:00:41 CST 2026'),
        ('date +%Y-%m-%d','2026-06-16'),
        ('date +%H:%M:%S','02:00:41'),
        ('date -u','Mon Jun 15 18:00:41 UTC 2026'),
        ('date -I','2026-06-16'),
        ('cal','June 2026\\nSu Mo Tu We Th Fr Sa\\n    1  2  3  4  5  6\\n 7  8  9 10 11 12 13\\n14 15 16 17 18 19 20\\n21 22 23 24 25 26 27\\n28 29 30'),
        ('cal 2026','\\u663e\\u793a 2026 \\u5e74\\u5168\\u5e74\\u65e5\\u5386...'),
        ('cal -3','\\u4e0a\\u6708/\\u672c\\u6708/\\u4e0b\\u6708 \\u65e5\\u5386\\u663e\\u793a'),
        ('ncal','June 2026\\nMo  1  8 15 22 29\\nTu  2  9 16 23 30\\nWe  3 10 17 24\\nTh  4 11 18 25\\nFr  5 12 19 26\\nSa  6 13 20 27\\nSu  7 14 21 28'),
        ('date -d @0','Thu Jan  1 08:00:00 CST 1970'),
        ('date +%s','1718496041'),
        ('hwclock','2026-06-16 02:00:41.123456+08:00'),
        ('sysctl -a','kernel.hostname=fusion-desktop\\nkernel.version=8.0.0\\nkernel.threads=256\\nvm.swappiness=60\\nnet.ipv4.tcp_syncookies=1'),
        ('sysctl kernel.hostname','kernel.hostname = fusion-desktop'),
        ('sysctl vm.swappiness','vm.swappiness = 60'),
        ('getconf LONG_BIT','64'),
        ('getconf PAGE_SIZE','4096'),
        ('getconf _NPROCESSORS_ONLN','16'),
        ('nproc','16'),
        ('nproc --all','16'),
    ]):
        entries.append(cmd(kv[0], kv[1]))
    
    # --- System Monitoring (50 cmds) ---
    entries.append("  /* ── System Monitoring ── */")
    mons = [
        ('top -b -n 1','PID USER   PR  NI %CPU %MEM    TIME+  COMMAND\\n   1 user   20   0  0.0  0.1   0:02.34 fusion-init\\n 234 user   20   0  2.1  1.2   1:23.45 fusion-shell\\n 567 user   20   0  0.5  0.3   0:12.34 terminal'),
        ('htop','CPU[|||     8.2%] Mem[|||||  12.4%] Swp[0.0%] Tasks:89\\n  PID USER  PRI NI VIRT RES SHR S CPU% MEM% TIME+  Command\\n  234 user  20  0  256M 48M 32M S  2.1  1.2 1:23  fusion-shell'),
        ('free','              total    used    free  shared  buff/cache  available\\nMem:       16384000 2015488 12285440   98304   2083072  14368512\\nSwap:       8388608       0  8388608'),
        ('free -h','              total    used    free  shared  buff/cache  available\\nMem:           16Gi   1.9Gi   11.7Gi   96Mi     2.0Gi     13.7Gi\\nSwap:         8.0Gi      0B     8.0Gi'),
        ('free -m','              total    used    free  shared  buff/cache  available\\nMem:          16000    1968   11997      96      2035     14032\\nSwap:          8192       0    8192'),
        ('free -g','              total    used    free  shared  buff/cache  available\\nMem:             15       1      11       0         2        13\\nSwap:             8       0       8'),
        ('vmstat','procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----\\nr b  swpd  free  buff  cache si so bi bo  in  cs us sy id wa st\\n0 0     0 11.7G 0.5G  1.5G  0  0  2  1  23  15  2  1 96  1  0'),
        ('vmstat 1 3','procs ----------memory---------- ---swap--- ---io--- -system-- ----cpu----\\nr b swpd free buff cache si so bi bo  in  cs us sy id wa st\\n0 0    0 11.7 0.5 1.5   0  0  2  1  23  15  2  1 96  1  0'),
        ('vmstat -s','16384000 K total memory\\n2015488 K used memory\\n12285440 K free memory\\n98304 K shared memory\\n2083072 K buffer/cache'),
        ('iostat','avg-cpu:  %user  %nice %system %iowait  %steal  %idle\\n           2.10   0.00   1.20   0.80   0.00  95.90\\nDevice  tps  kB_read/s  kB_wrtn/s  kB_read  kB_wrtn\\nsda     3.20      12.40      25.60   102400   204800'),
        ('iostat -x','avg-cpu:  %user %nice %sys %iowait %steal %idle\\n           2.10  0.00 1.20    0.80   0.00 95.90\\nDevice r/s w/s rkB/s wkB/s await svctm %util\\nsda    1.2 2.0  12.4  25.6  0.50  0.30  0.10'),
        ('iostat -d sda','Device  tps  kB_read/s  kB_wrtn/s  kB_read  kB_wrtn\\nsda     3.20      12.40      25.60   102400   204800'),
        ('mpstat','CPU  %usr %nice %sys %iowait %irq %soft %steal %guest %idle\\nall  2.10 0.00 1.20  0.80   0.00 0.00  0.00   0.00  95.90'),
        ('mpstat -P ALL','CPU  %usr %nice %sys %iowait %irq %soft %steal %guest %idle\\n  0  2.50 0.00 1.50  0.50   0.00 0.00  0.00   0.00  95.50\\n  1  1.80 0.00 0.90  1.10   0.00 0.00  0.00   0.00  96.20'),
        ('pidstat','PID  %usr %system %guest %CPU  CPU  Command\\n 234  1.20   0.80   0.00 2.00    0  fusion-shell\\n 567  0.20   0.30   0.00 0.50    2  terminal'),
        ('sar','12:00:01 CPU %user %nice %system %iowait %steal %idle\\n12:10:01 all  2.10 0.00   1.20   0.80   0.00  95.90\\n12:20:01 all  1.80 0.00   1.00   0.60   0.00  96.60'),
        ('sar -u 1 3','Average: all 2.10 0.00 1.20 0.80 0.00 95.90'),
        ('sar -r','12:00:01 kbmemfree kbmemused %memused kbbuffers kbcached\\n12:10:01  12285440   2015488    12.31    524288  1558016'),
        ('iostat -k','Device  tps  kB_read/s  kB_wrtn/s  kB_read  kB_wrtn\\nsda     3.20      12.40      25.60   102400   204800'),
        ('iostat -m','Device  tps  MB_read/s  MB_wrtn/s  MB_read  MB_wrtn\\nsda     3.20       0.01       0.03       100       200'),
        ('dstat','----total-cpu-usage---- -dsk/total- -net/total- ---paging-- ---system--\\nusr sys idl wai hiq siq| read  writ| recv  send|  in   out | int   csw\\n  2   1  96   1   0   0|  12k   25k|   0     0 |   0     0 |  23    15'),
        ('dstat -c','----total-cpu-usage----\\nusr sys idl wai hiq siq\\n  2   1  96   1   0   0'),
        ('dstat -d','-dsk/total-\\nread  writ\\n 12k   25k'),
        ('dstat -n','-net/total-\\nrecv  send\\n   0     0'),
        ('dstat -m','------memory-usage-----\\nused  buff  cach  free\\n1.9G  512M  1.5G 11.7G'),
        ('iostat -p sda','sda        3.20  12.40  25.60  102400  204800\\nsda1       1.20   4.80   0.00   38400       0\\nsda2       1.50   5.20  20.80   41600  166400\\nsda3       0.50   2.40   4.80   22400   38400'),
        ('sar -n DEV','12:00:01 IFACE rxpck/s txpck/s rxkB/s txkB/s\\n12:10:01    lo   0.00   0.00  0.00  0.00\\n12:10:01  eth0  15.20  10.40  8.50  5.20'),
        ('sar -b','12:00:01 tps rtps wtps bread/s bwrtn/s\\n12:10:01 3.20 1.20 2.00  12.40  25.60'),
        ('sar -q','12:00:01 runq-sz plist-sz ldavg-1 ldavg-5 ldavg-15\\n12:10:01       0       89    0.08    0.12     0.09'),
        ('lsof','COMMAND  PID USER   FD  TYPE DEVICE SIZE/OFF NODE NAME\\nterm    567 user  cwd   DIR    8,2     4096    2 /\\nterm    567 user  txt   REG    8,2   131072 1001 /bin/term'),
        ('lsof -p 567','COMMAND PID USER  FD TYPE DEVICE SIZE/OFF NODE NAME\\nterm   567 user cwd  DIR    8,2     4096    2 /'),
        ('lsof -i','COMMAND  PID USER  FD TYPE DEVICE SIZE/OFF NODE NAME\\nhttpd   1234 user  4u IPv4  12345      0t0  TCP *:80 (LISTEN)'),
        ('lsof -u user','COMMAND PID USER  FD TYPE DEVICE SIZE/OFF NODE NAME\\nterm   567 user cwd  DIR    8,2     4096    2 /'),
        ('pgrep term','567'),
        ('pgrep -l term','567 term'),
        ('pgrep fusion','1\\n234'),
        ('pidof term','567'),
        ('pidof fusion-shell','234'),
        ('killall -l','1) SIGHUP  2) SIGINT  3) SIGQUIT  4) SIGILL  5) SIGTRAP\\n6) SIGABRT 7) SIGBUS  8) SIGFPE  9) SIGKILL 10) SIGUSR1\\n11) SIGSEGV 12) SIGUSR2 13) SIGPIPE 14) SIGALRM 15) SIGTERM'),
        ('pkill -l','HUP INT QUIT ILL TRAP ABRT BUS FPE KILL USR1 SEGV USR2 PIPE ALRM TERM'),
    ]
    for kv in mons:
        entries.append(cmd(kv[0], kv[1]))
    
    # --- File System (80 cmds) ---
    entries.append("  /* ── File System ── */")
    fs_cmds = [
        ('ls','Documents  Downloads  Music  Pictures  Videos  desktop.ini'),
        ('ls -l','total 24\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Documents\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Downloads\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Music\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Pictures\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Videos'),
        ('ls -la','total 32\\ndrwxr-xr-x 6 user user 4096 Jun 16 02:00 .\\ndrwxr-xr-x 3 root root 4096 Jun 12 18:38 ..\\n-rw-r--r-- 1 user user  220 Jun 12 18:38 .bashrc\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Documents\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Downloads\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Music'),
        ('ls -lh','total 24K\\ndrwxr-xr-x 2 user user 4.0K Jun 16 02:00 Documents\\ndrwxr-xr-x 2 user user 4.0K Jun 16 02:00 Downloads'),
        ('ls -lt','\\u6309\\u4fee\\u6539\\u65f6\\u95f4\\u6392\\u5e8f\\u663e\\u793a\\u6587\\u4ef6'),
        ('ls -ltr','\\u6309\\u4fee\\u6539\\u65f6\\u95f4\\u53cd\\u5411\\u6392\\u5e8f'),
        ('ls -lS','\\u6309\\u6587\\u4ef6\\u5927\\u5c0f\\u6392\\u5e8f'),
        ('ls -R','.:\\nDocuments  Downloads  Music  Pictures  Videos\\n./Documents:\\nnotes.txt  report.pdf\\n./Downloads:\\nimage.png'),
        ('ls -1','Documents\\nDownloads\\nMusic\\nPictures\\nVideos'),
        ('ls -F','Documents/  Downloads/  Music/  Pictures/  Videos/  script.sh*'),
        ('ls --color=auto','Documents/  Downloads/  Music/  Pictures/  Videos/'),
        ('ls *.txt','notes.txt  todo.txt  README.txt'),
        ('ls -d */','Documents/  Downloads/  Music/  Pictures/  Videos/'),
        ('ll','total 24\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Documents\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Downloads'),
        ('la','.  ..  .bashrc  .config  .local  Documents  Downloads  Music'),
        ('l','Documents/  Downloads/  Music/  Pictures/  Videos/'),
        ('pwd','/home/user'),
        ('pwd -P','/home/user'),
        ('cd','/home/user'),
        ('cd /','/'),
        ('cd ~','/home/user'),
        ('cd ..','/home'),
        ('cd -','/home/user'),
        ('dir','Documents  Downloads  Music  Pictures  Videos'),
        ('vdir','total 24\\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Documents'),
        ('mkdir newfolder','\\u5df2\\u521b\\u5efa\\u76ee\\u5f55: newfolder'),
        ('mkdir -p a/b/c','\\u5df2\\u9012\\u5f52\\u521b\\u5efa: a/b/c'),
        ('mkdir -m 755 mydir','\\u5df2\\u521b\\u5efa mydir (\\u6743\\u9650 755)'),
        ('rmdir empty_dir','\\u5df2\\u5220\\u9664\\u76ee\\u5f55: empty_dir'),
        ('rmdir -p a/b/c','\\u5df2\\u9012\\u5f52\\u5220\\u9664\\u76ee\\u5f55: a/b/c'),
        ('touch file.txt','\\u5df2\\u521b\\u5efa\\u6587\\u4ef6: file.txt'),
        ('touch -t 202606160200 file.txt','\\u5df2\\u4fee\\u6539\\u65f6\\u95f4\\u6233: file.txt'),
        ('touch file1.txt file2.txt','\\u5df2\\u521b\\u5efa: file1.txt file2.txt'),
        ('cp file1.txt file2.txt','\\u5df2\\u590d\\u5236: file1.txt \\u2192 file2.txt'),
        ('cp -r dir1 dir2','\\u5df2\\u9012\\u5f52\\u590d\\u5236: dir1 \\u2192 dir2'),
        ('cp -i file1.txt file2.txt','overwrite file2.txt? (y/n) n\\n\\u5df2\\u53d6\\u6d88'),
        ('cp -v file1.txt file2.txt',"'file1.txt' -> 'file2.txt'"),
        ('cp -a dir1 dir2','\\u5df2\\u5f52\\u6863\\u590d\\u5236: dir1 \\u2192 dir2'),
        ('mv old.txt new.txt','\\u5df2\\u79fb\\u52a8/\\u91cd\\u547d\\u540d: old.txt \\u2192 new.txt'),
        ('mv -i old.txt new.txt','overwrite new.txt? (y/n) n\\n\\u5df2\\u53d6\\u6d88'),
        ('mv -v old.txt new.txt',"'old.txt' -> 'new.txt'"),
        ('mv file.txt dir/','\\u5df2\\u79fb\\u52a8: file.txt \\u2192 dir/'),
        ('rm file.txt','\\u5df2\\u5220\\u9664: file.txt'),
        ('rm -f file.txt','\\u5df2\\u5f3a\\u5236\\u5220\\u9664: file.txt'),
        ('rm -i file.txt','remove file.txt? (y/n) n\\n\\u5df2\\u53d6\\u6d88'),
        ('rm -rf old_dir','\\u5df2\\u9012\\u5f52\\u5f3a\\u5236\\u5220\\u9664: old_dir'),
        ('rm -v *.tmp',"removed 'a.tmp'\\nremoved 'b.tmp'"),
        ('ln -s target link','\\u5df2\\u521b\\u5efa\\u7b26\\u53f7\\u94fe\\u63a5: link \\u2192 target'),
        ('ln target hardlink','\\u5df2\\u521b\\u5efa\\u786c\\u94fe\\u63a5: hardlink'),
        ('ln -sf target link','\\u5df2\\u66f4\\u65b0\\u7b26\\u53f7\\u94fe\\u63a5: link \\u2192 target'),
        ('stat file.txt','File: file.txt\\nSize: 1024  Blocks: 8  IO Block: 4096\\nAccess: (0644/-rw-r--r--) Uid: (1000/user) Gid: (1000/user)\\nAccess: 2026-06-16 02:00:41\\nModify: 2026-06-15 18:30:00\\nChange: 2026-06-15 18:30:00'),
        ('stat -c %s file.txt','1024'),
        ('stat -c %a file.txt','644'),
        ('file file.txt','file.txt: ASCII text'),
        ('file image.png','image.png: PNG image data, 800 x 600, 8-bit/color RGB'),
        ('file /bin/ls','/bin/ls: ELF 64-bit LSB executable, x86-64'),
        ('file -b file.txt','ASCII text'),
        ('file -i file.txt','file.txt: text/plain; charset=utf-8'),
        ('type ls','ls is aliased to \\u0060ls --color=auto\\u0060'),
        ('type cd','cd is a shell builtin'),
        ('which ls','/bin/ls'),
        ('which python3','/usr/bin/python3'),
        ('which node','/usr/local/bin/node'),
        ('which -a python3','/usr/bin/python3\\n/usr/local/bin/python3'),
        ('whereis ls','ls: /bin/ls /usr/share/man/man1/ls.1.gz'),
        ('whereis python3','python3: /usr/bin/python3 /usr/local/bin/python3 /usr/share/man/man1/python3.1.gz'),
        ('du -sh','2.0G\\t.'),
        ('du -sh *','4.0K\\tDocuments\\n1.5G\\tDownloads\\n500M\\tMusic\\n10M\\tPictures\\n2.0M\\tVideos'),
        ('du -h --max-depth=1','2.0G\\t.\\n1.5G\\t./Downloads\\n500M\\t./Music'),
        ('du -sh /home','15G\\t/home'),
        ('du -sh --apparent-size','1.8G\\t.'),
        ('du -ah','\\u663e\\u793a\\u6240\\u6709\\u6587\\u4ef6\\u5927\\u5c0f'),
        ('df','Filesystem  1K-blocks    Used Available Use% Mounted on\\n/dev/sda2   209715200 41943040 167771776  20% /\\n/dev/sda1      524288   102400    421888  20% /boot'),
        ('df -h','Filesystem  Size  Used Avail Use% Mounted on\\n/dev/sda2   200G   40G  160G  20% /\\n/dev/sda1   512M  100M  412M  20% /boot'),
        ('df -i','Filesystem  Inodes IUsed IFree IUse% Mounted on\\n/dev/sda2   13.1M   256K 12.9M    2% /'),
        ('df -T','Filesystem Type 1K-blocks    Used Available Use% Mounted on\\n/dev/sda2  ext4 209715200 41943040 167771776 20% /'),
        ('df --total','Filesystem  1K-blocks    Used Available Use% Mounted on\\ntotal       210240512 42045440 168193664 20%'),
        ('mount','/dev/sda2 on / type ext4 (rw,relatime)\\n/dev/sda1 on /boot type ext4 (rw,relatime)\\ntmpfs on /tmp type tmpfs (rw,nosuid,nodev)'),
        ('mount -l','/dev/sda2 on / type ext4 (rw,relatime) [root]'),
        ('umount','usage: umount <mountpoint>'),
        ('fdisk -l','Disk /dev/sda: 256 GiB\\nDevice    Boot Start      End  Sectors  Size Id Type\\n/dev/sda1 *     2048  1050623  1048576  512M 83 Linux\\n/dev/sda2     1050624 420618239 419567616 200G 83 Linux\\n/dev/sda3   420618240 536870911 116252672 55.4G 83 Linux'),
    ]
    for kv in fs_cmds:
        entries.append(cmd(kv[0], kv[1]))
    
    # --- Process Management (50 cmds) ---
    entries.append("  /* ── Process Management ── */")
    proc_cmds = [
        ('ps','PID TTY     TIME CMD\\n 567 pts/0 00:00:00 term\\n 890 pts/0 00:00:00 sh'),
        ('ps aux','USER PID %CPU %MEM  VSZ  RSS TTY STAT START  TIME COMMAND\\nuser 567  0.1  0.3 8192 4096 pts/0 Ss 02:00 0:00 term\\nuser 890  0.0  0.1 4096 2048 pts/0 S  02:00 0:00 sh'),
        ('ps -ef','UID  PID PPID  C STIME TTY     TIME CMD\\nuser 567  234  0 02:00 pts/0 00:00:00 term\\nuser 890  567  0 02:00 pts/0 00:00:00 sh'),
        ('ps -e --forest','  PID TTY     TIME CMD\\n  567 pts/0 00:00:00  \\u2514\\u2500 term\\n  890 pts/0 00:00:00      \\u2514\\u2500 sh'),
        ('ps -eo pid,ppid,cmd,%mem,%cpu','PID PPID CMD                         %MEM %CPU\\n 567  234 term                       0.3  0.1\\n 890  567 sh                         0.1  0.0'),
        ('ps -u user','PID TTY     TIME CMD\\n 567 pts/0 00:00:00 term'),
        ('ps -C term','PID TTY     TIME CMD\\n 567 pts/0 00:00:00 term'),
        ('ps --no-headers','567 pts/0 00:00:00 term'),
        ('pstree','systemd\\u2500\\u2500fusion-init\\u2500\\u2500fusion-shell\\u2500\\u2500term\\u2500\\u2500sh'),
        ('pstree -p','systemd(1)\\u2500\\u2500fusion-init(10)\\u2500\\u2500fusion-shell(234)\\u2500\\u2500term(567)\\u2500\\u2500sh(890)'),
        ('pstree -u','systemd\\u2500\\u2500fusion-init\\u2500\\u2500fusion-shell(user)\\u2500\\u2500term(user)\\u2500\\u2500sh(user)'),
        ('kill 567','\\u5df2\\u53d1\\u9001 SIGTERM \\u5230 PID 567'),
        ('kill -9 567','\\u5df2\\u5f3a\\u5236\\u7ec8\\u6b62 PID 567'),
        ('kill -15 567','\\u5df2\\u53d1\\u9001 SIGTERM \\u5230 PID 567'),
        ('kill -l','1) SIGHUP 2) SIGINT 3) SIGQUIT 4) SIGILL 5) SIGTRAP\\n6) SIGABRT 7) SIGBUS 8) SIGFPE 9) SIGKILL 10) SIGUSR1\\n11) SIGSEGV 12) SIGUSR2 13) SIGPIPE 14) SIGALRM 15) SIGTERM'),
        ('kill -HUP 567','\\u5df2\\u53d1\\u9001 SIGHUP \\u5230 PID 567'),
        ('kill -STOP 567','\\u5df2\\u6682\\u505c PID 567'),
        ('kill -CONT 567','\\u5df2\\u7ee7\\u7eed PID 567'),
        ('nice -n 10 command','\\u5df2\\u4ee5\\u4f18\\u5148\\u7ea7 10 \\u8fd0\\u884c command'),
        ('renice 10 -p 567','567 (process ID) old priority 0, new priority 10'),
        ('renice -n 5 -u user','1000 (user ID) old priority 0, new priority 5'),
        ('nohup command &','\\u5df2\\u5728\\u540e\\u53f0\\u8fd0\\u884c command (\\u5ffd\\u7565 SIGHUP)\\n[1] 1234'),
        ('jobs','[1]  Running  nohup command &\\n[2]  Stopped  vim file.txt'),
        ('jobs -l','[1]  1234 Running  nohup command &\\n[2]+ 1235 Stopped  vim file.txt'),
        ('fg','\\u5df2\\u5c06\\u540e\\u53f0\\u4f5c\\u4e1a\\u8c03\\u5230\\u524d\\u53f0'),
        ('fg %1','\\u5df2\\u5c06\\u4f5c\\u4e1a 1 \\u8c03\\u5230\\u524d\\u53f0'),
        ('bg','\\u5df2\\u5c06\\u4f5c\\u4e1a\\u8c03\\u5230\\u540e\\u53f0'),
        ('bg %2','\\u5df2\\u5c06\\u4f5c\\u4e1a 2 \\u8c03\\u5230\\u540e\\u53f0'),
        ('disown','\\u5df2\\u4ece shell \\u4f5c\\u4e1a\\u5217\\u8868\\u79fb\\u9664\\u4f5c\\u4e1a'),
        ('disown %1','\\u5df2\\u79fb\\u9664\\u4f5c\\u4e1a 1'),
        ('wait','\\u7b49\\u5f85\\u6240\\u6709\\u540e\\u53f0\\u4f5c\\u4e1a\\u5b8c\\u6210'),
        ('wait 1234','\\u7b49\\u5f85 PID 1234 \\u5b8c\\u6210'),
        ('time ls','Documents Downloads Music Pictures Videos\\nreal 0m0.003s user 0m0.001s sys 0m0.001s'),
        ('time -v ls','Command being timed: "ls"\\nUser time (seconds): 0.00\\nSystem time (seconds): 0.00\\nPercent of CPU: 80%\\nElapsed (wall clock) time: 0.00'),
        ('/usr/bin/time ls','0.00user 0.00system 0:00.00elapsed 100%CPU'),
        ('exec bash','\\u5df2\\u66ff\\u6362\\u5f53\\u524d shell \\u4e3a bash'),
        ('exec zsh','\\u5df2\\u66ff\\u6362\\u5f53\\u524d shell \\u4e3a zsh'),
        ('source ~/.bashrc','\\u5df2\\u52a0\\u8f7d ~/.bashrc'),
        ('. ~/.bashrc','\\u5df2\\u52a0\\u8f7d ~/.bashrc'),
        ('sleep 1','\\u7b49\\u5f85 1 \\u79d2...'),
        ('sleep 0.5','\\u7b49\\u5f85 0.5 \\u79d2...'),
        ('true',''),
        ('false',''),
        ('yes','y\\ny\\ny\\ny\\ny\\ny\\ny\\ny\\ny\\ny\\n(\\u5df2\\u7ec8\\u6b62)'),
        ('yes hello','hello\\nhello\\nhello\\nhello\\nhello\\n(\\u5df2\\u7ec8\\u6b62)'),
        ('xargs','usage: xargs [options] [command]'),
        ('echo hello | xargs','hello'),
        ('seq 1 5 | xargs','1 2 3 4 5'),
        ('find . -name "*.txt" | xargs rm','\\u5df2\\u5220\\u9664\\u6240\\u6709 .txt \\u6587\\u4ef6'),
    ]
    for kv in proc_cmds:
        entries.append(cmd(kv[0], kv[1]))
    
    # Now for the mass generation, I'll use loop-based generation for each category
    # to quickly reach 1200 commands
    
    # --- Text Processing (100 cmds) ---
    entries.append("  /* ── Text Processing ── */")
    text_cmds = [
        ('cat file.txt','Hello World!\\nThis is a test file.\\nLine 3 of content.\\nEnd of file.'),
        ('cat -n file.txt','     1\\tHello World!\\n     2\\tThis is a test file.\\n     3\\tLine 3 of content.\\n     4\\tEnd of file.'),
        ('cat -b file.txt','     1\\tHello World!\\n     2\\tThis is a test file.\\n     3\\tLine 3 of content.\\n     4\\tEnd of file.'),
        ('cat -s file.txt','\\u538b\\u7f29\\u7a7a\\u884c\\u663e\\u793a'),
        ('cat -E file.txt','Hello World!$\\nThis is a test file.$'),
        ('cat -A file.txt','Hello World!$\\nThis is a test file.$'),
        ('tac file.txt','End of file.\\nLine 3 of content.\\nThis is a test file.\\nHello World!'),
        ('nl file.txt','     1\\tHello World!\\n     2\\tThis is a test file.'),
        ('nl -b a file.txt','     1\\tHello World!\\n     2\\tThis is a test file.\\n     3\\t'),
        ('more file.txt','Hello World!\\nThis is a test file.\\n--More--(66%)'),
        ('less file.txt','Hello World!\\nThis is a test file.\\n(END)'),
        ('head file.txt','Hello World!\\nThis is a test file.\\nLine 3 of content.'),
        ('head -n 2 file.txt','Hello World!\\nThis is a test file.'),
        ('head -c 10 file.txt','Hello Worl'),
        ('head -5 file.txt','\\u524d 5 \\u884c\\u5185\\u5bb9'),
        ('tail file.txt','Line 3 of content.\\nEnd of file.'),
        ('tail -n 2 file.txt','Line 3 of content.\\nEnd of file.'),
        ('tail -f file.log','\\u5b9e\\u65f6\\u8ddf\\u8e2a\\u6587\\u4ef6\\u53d8\\u5316...'),
        ('tail -F file.log','\\u8ddf\\u8e2a\\u6587\\u4ef6(\\u652f\\u6301\\u6587\\u4ef6\\u91cd\\u5efa)...'),
        ('tail -c 10 file.txt','f file.\\n(10 bytes)'),
        ('wc file.txt','4 15 98 file.txt'),
        ('wc -l file.txt','4 file.txt'),
        ('wc -w file.txt','15 file.txt'),
        ('wc -c file.txt','98 file.txt'),
        ('wc -m file.txt','98 file.txt'),
        ('wc -L file.txt','22 file.txt'),
        ('sort file.txt','End of file.\\nHello World!\\nLine 3 of content.\\nThis is a test file.'),
        ('sort -r file.txt','This is a test file.\\nLine 3 of content.\\nHello World!\\nEnd of file.'),
        ('sort -n numbers.txt','1\\n2\\n10\\n20\\n100'),
        ('sort -u file.txt','\\u53bb\\u91cd\\u6392\\u5e8f'),
        ('sort -t , -k2 file.csv','\\u6309\\u7b2c2\\u5217\\u6392\\u5e8f'),
        ('uniq file.txt','Hello World!\\nThis is a test file.\\nLine 3 of content.'),
        ('uniq -c file.txt','      2 Hello World!\\n      1 This is a test file.\\n      1 Line 3 of content.'),
        ('uniq -d file.txt','Hello World!'),
        ('uniq -u file.txt','This is a test file.\\nLine 3 of content.'),
        ('uniq -i file.txt','\\u5ffd\\u7565\\u5927\\u5c0f\\u5199\\u53bb\\u91cd'),
        ('cut -d, -f1 data.csv','Name\\nAlice\\nBob\\nCharlie'),
        ('cut -d, -f2 data.csv','Age\\n25\\n30\\n35'),
        ('cut -c 1-5 file.txt','Hello\\nThis \\nLine \\nEnd o'),
        ('cut -d: -f1,7 /etc/passwd','root:/bin/bash\\nuser:/bin/bash'),
        ('paste file1.txt file2.txt','Hello\\tWorld\\nLine1\\tLine2'),
        ('paste -d, file1.txt file2.txt','Hello,World\\nLine1,Line2'),
        ('paste -s file.txt','Hello World!\\tThis is a test file.\\tLine 3 of content.'),
        ('join file1.txt file2.txt','\\u5173\\u8054\\u5408\\u5e76\\u4e24\\u4e2a\\u6587\\u4ef6'),
        ('join -t, -1 1 -2 1 a.csv b.csv','\\u6309\\u7b2c1\\u5217\\u5173\\u8054'),
        ('tr a-z A-Z < file.txt','HELLO WORLD!\\nTHIS IS A TEST FILE.'),
        ('tr -d "\\n" < file.txt','\\u5220\\u9664\\u6240\\u6709\\u6362\\u884c\\u7b26'),
        ('tr -s " " < file.txt','\\u538b\\u7f29\\u91cd\\u590d\\u7a7a\\u683c'),
        ('tr ":" "," < /etc/passwd','\\u66ff\\u6362\\u5192\\u53f7\\u4e3a\\u9017\\u53f7'),
        ('tee output.txt','Hello World!\\n(\\u8f93\\u5165\\u5df2\\u5199\\u5165 output.txt)'),
        ('tee -a output.txt','\\u8ffd\\u52a0\\u5199\\u5165 output.txt'),
        ('sed \'s/old/new/\' file.txt','\\u66ff\\u6362\\u7b2c\\u4e00\\u4e2a old \\u4e3a new'),
        ("sed 's/old/new/g' file.txt",'\\u5168\\u5c40\\u66ff\\u6362 old \\u4e3a new'),
        ("sed '/pattern/d' file.txt",'\\u5220\\u9664\\u5339\\u914d\\u884c'),
        ("sed -n '5,10p' file.txt",'\\u663e\\u793a 5-10 \\u884c'),
        ("sed -i 's/old/new/' file.txt",'\\u539f\\u5730\\u66ff\\u6362'),
        ("awk '{print $1}' file.txt",'\\u6253\\u5370\\u7b2c1\\u5217'),
        ("awk '{print $NF}' file.txt",'\\u6253\\u5370\\u6700\\u540e\\u4e00\\u5217'),
        ("awk -F, '{print $2}' data.csv",'\\u4ee5\\u9017\\u53f7\\u5206\\u5272\\uff0c\\u6253\\u5370\\u7b2c2\\u5217'),
        ("awk 'NR==2' file.txt",'\\u6253\\u5370\\u7b2c2\\u884c'),
        ("awk '{sum+=$1} END {print sum}' nums.txt",'\\u6c42\\u548c'),
        ("awk 'BEGIN {print \"Start\"} {print} END {print \"End\"}' file.txt",'Start\\nHello World!\\nEnd'),
        ("awk '{if($1>10) print}' data.txt",'\\u7b5b\\u9009\\u7b2c1\\u5217>10\\u7684\\u884c'),
        ('grep "hello" file.txt','Hello World!\\nhello there'),
        ('grep -i "hello" file.txt','Hello World!\\nhello there\\nHELLO EVERYONE'),
        ('grep -v "hello" file.txt','\\u53cd\\u5411\\u5339\\u914d'),
        ('grep -c "hello" file.txt','3'),
        ('grep -n "hello" file.txt','1:Hello World!\\n5:hello there'),
        ('grep -r "TODO" .',"'./src/main.js:  // TODO: implement\\n./README.md:  - TODO list'"),
        ('grep -l "hello" *.txt','file1.txt\\nfile2.txt'),
        ('grep -w "hello" file.txt','\\u5168\\u8bcd\\u5339\\u914d'),
        ('grep -E "hello|world" file.txt','\\u6b63\\u5219\\u8868\\u8fbe\\u5f0f'),
        ('grep -A 2 "hello" file.txt','\\u663e\\u793a\\u5339\\u914d\\u884c\\u53ca\\u540e2\\u884c'),
        ('grep -B 2 "hello" file.txt','\\u663e\\u793a\\u5339\\u914d\\u884c\\u53ca\\u524d2\\u884c'),
        ('grep -C 2 "hello" file.txt','\\u663e\\u793a\\u5339\\u914d\\u884c\\u53ca\\u524d\\u540e\\u5404\\u663e\\u793a2\\u884c'),
        ('grep --color "hello" file.txt','Hello World! (\\u9ad8\\u4eae)'),
        ('egrep "hello|world" file.txt','\\u6269\\u5c55\\u6b63\\u5219\\u5339\\u914d'),
        ('fgrep "hello" file.txt','\\u56fa\\u5b9a\\u5b57\\u7b26\\u4e32\\u5339\\u914d'),
        ('zgrep "error" log.gz','\\u641c\\u7d22\\u538b\\u7f29\\u6587\\u4ef6'),
        ('diff file1.txt file2.txt','1c1\\n< Hello World!\\n---\\n> Hello Universe!'),
        ('diff -u file1.txt file2.txt','--- file1.txt\\n+++ file2.txt\\n@@ -1,4 +1,4 @@\\n-Hello World!\\n+Hello Universe!'),
        ('diff -r dir1 dir2','\\u9012\\u5f52\\u6bd4\\u8f83\\u76ee\\u5f55'),
        ('diff -y file1.txt file2.txt','Hello World!    | Hello Universe!\\nLine 2          Line 2'),
        ('cmp file1.txt file2.txt','file1.txt file2.txt differ: byte 7, line 1'),
        ('comm file1.txt file2.txt','\\u6bd4\\u8f83\\u5df2\\u6392\\u5e8f\\u6587\\u4ef6'),
        ('comm -12 file1.txt file2.txt','\\u663e\\u793a\\u4e24\\u6587\\u4ef6\\u5171\\u6709\\u884c'),
        ('sdiff file1.txt file2.txt','Hello World!    | Hello Universe!'),
        ('patch < diff.patch','\\u5df2\\u5e94\\u7528\\u8865\\u4e01'),
        ('patch -p1 < diff.patch','\\u5df2\\u5e94\\u7528\\u8865\\u4e01(-p1)'),
        ('strings /bin/ls','/lib64/ld-linux-x86-64.so.2\\nlibc.so.6\\n__libc_start_main\\nstdout'),
        ('strings -n 6 /bin/ls','__libc_start_main\\nstdout\\nfprintf'),
        ('od file.txt','0000000 062510 066154 067157 005127 067562 062144 000012'),
        ('od -c file.txt','0000000   H   e   l   l   o       W   o   r   l   d   !  \\n'),
        ('od -x file.txt','0000000 6548 6c6c 206f 6f57 6c72 2164 000a'),
        ('xxd file.txt','00000000: 4865 6c6c 6f20 576f 726c 6421 0a         Hello World!.'),
        ('xxd -p file.txt','48656c6c6f20576f726c64210a'),
        ('hexdump file.txt','0000000 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 0a'),
        ('hexdump -C file.txt','00000000  48 65 6c 6c 6f 20 57 6f  72 6c 64 21 0a           |Hello World!.|'),
        ('base64 file.txt','SGVsbG8gV29ybGQhCg=='),
        ('base64 -d <<< SGVsbG8=','Hello'),
        ('base32 file.txt','JBSWY3DPEBLW64TMMQQQ===='),
    ]
    for kv in text_cmds:
        entries.append(cmd(kv[0], kv[1]))
    
    # --- Network Tools (90 cmds) ---
    entries.append("  /* ── Network Tools ── */")
    net_cmds = [
        ('ping localhost','PING localhost (127.0.0.1): 56 data bytes\\n64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.050 ms\\n64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.045 ms\\n--- localhost ping statistics ---\\n2 packets transmitted, 2 received, 0% loss'),
        ('ping -c 4 8.8.8.8','PING 8.8.8.8: 56 data bytes\\n64 bytes from 8.8.8.8: icmp_seq=0 ttl=118 time=12.3 ms\\n64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=11.8 ms\\n64 bytes from 8.8.8.8: icmp_seq=2 ttl=118 time=12.1 ms\\n64 bytes from 8.8.8.8: icmp_seq=3 ttl=118 time=12.0 ms\\n--- 8.8.8.8 ping statistics ---\\n4 packets transmitted, 4 received, 0% loss'),
        ('ping -i 0.5 localhost','\\u5feb\\u901f ping (0.5s \\u95f4\\u9694)'),
        ('ping -s 100 localhost','\\u6307\\u5b9a\\u5305\\u5927\\u5c0f 100 \\u5b57\\u8282'),
        ('ping -W 2 8.8.8.8','\\u8d85\\u65f6 2 \\u79d2'),
        ('ping6 ::1','PING6(::1) 56 data bytes\\n64 bytes from ::1: icmp_seq=0 hlim=64 time=0.040 ms'),
        ('traceroute 8.8.8.8','traceroute to 8.8.8.8, 30 hops max\\n 1  192.168.1.1  1.234 ms  1.123 ms  1.098 ms\\n 2  10.0.0.1  5.678 ms  5.543 ms  5.432 ms\\n 3  8.8.8.8  12.345 ms  12.234 ms  12.123 ms'),
        ('traceroute -n 8.8.8.8','\\u4e0d\\u89e3\\u6790\\u4e3b\\u673a\\u540d'),
        ('traceroute -m 15 8.8.8.8','\\u6700\\u5927 TTL 15'),
        ('tracepath 8.8.8.8','1: 192.168.1.1  1.234ms\\n2: 10.0.0.1  5.678ms\\n3: 8.8.8.8  12.345ms'),
        ('netstat','Active Internet connections\\nProto Recv-Q Send-Q Local Address    Foreign Address  State\\ntcp        0      0 0.0.0.0:80       0.0.0.0:*        LISTEN'),
        ('netstat -tuln','Proto Local Address    State\\ntcp   0.0.0.0:80       LISTEN\\ntcp   127.0.0.1:3306   LISTEN\\nudp   0.0.0.0:5353'),
        ('netstat -an','\\u663e\\u793a\\u6240\\u6709\\u8fde\\u63a5(\\u4e0d\\u89e3\\u6790)'),
        ('netstat -r','Kernel IP routing table\\nDestination  Gateway      Genmask        Flags MSS Window irtt Iface\\ndefault      192.168.1.1  0.0.0.0        UG    0   0      0    eth0\\n192.168.1.0  0.0.0.0      255.255.255.0  U     0   0      0    eth0'),
        ('netstat -i','Kernel Interface table\\nIface MTU RX-OK RX-ERR TX-OK TX-ERR Flg\\neth0  1500 12345     0  6789     0 BMRU\\nlo   65536   234     0   234     0 LRU'),
        ('netstat -s','Ip: 12345 total packets received\\nTcp: 6789 active connections\\nUdp: 2345 packets received'),
        ('ss','Netid State  Recv-Q Send-Q Local Address:Port Peer Address:Port\\ntcp   LISTEN 0      128    0.0.0.0:80        0.0.0.0:*'),
        ('ss -tuln','\\u663e\\u793a TCP/UDP \\u76d1\\u542c\\u7aef\\u53e3'),
        ('ss -s','Total: 45\\nTCP:   12 (estab 3, closed 5, listening 4)\\nTransport Total IP IPv6\\nRAW       0     0  0\\nUDP       8     5  3\\nTCP       12    8  4'),
        ('ss -p','\\u663e\\u793a\\u8fdb\\u7a0b\\u4fe1\\u606f'),
        ('ss -4','\\u4ec5 IPv4'),
        ('ss -6','\\u4ec5 IPv6'),
        ('ip addr','1: lo: <LOOPBACK,UP> mtu 65536\\n    inet 127.0.0.1/8 scope host lo\\n2: eth0: <BROADCAST,MULTICAST,UP> mtu 1500\\n    inet 192.168.1.100/24 brd 192.168.1.255'),
        ('ip link','1: lo: <LOOPBACK,UP> mtu 65536 qdisc noqueue state UNKNOWN\\n2: eth0: <BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state UP'),
        ('ip route','default via 192.168.1.1 dev eth0\\n192.168.1.0/24 dev eth0 proto kernel scope link'),
        ('ip neigh','192.168.1.1 dev eth0 lladdr 00:11:22:33:44:55 REACHABLE'),
        ('ifconfig','eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\\n    inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255\\n    ether 00:11:22:33:44:55\\n    RX packets 12345  bytes 12345678\\n    TX packets 6789  bytes 6789012\\nlo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536\\n    inet 127.0.0.1  netmask 255.0.0.0'),
        ('ifconfig eth0','eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\\n    inet 192.168.1.100  netmask 255.255.255.0'),
        ('ifconfig -a','\\u663e\\u793a\\u6240\\u6709\\u63a5\\u53e3(\\u542b\\u7981\\u7528\\u63a5\\u53e3)'),
        ('iwconfig','lo   no wireless extensions.\\neth0 no wireless extensions.\\nwlan0 IEEE 802.11 ESSID:"MyWiFi"\\n    Mode:Managed Frequency:2.437 GHz\\n    Bit Rate=144.4 Mb/s Tx-Power=20 dBm\\n    Signal level=-45 dBm'),
        ('arp','Address          HWtype  HWaddress        Flags Mask    Iface\\n192.168.1.1      ether   00:11:22:33:44:55 C            eth0'),
        ('arp -a','? (192.168.1.1) at 00:11:22:33:44:55 [ether] on eth0'),
        ('route','Kernel IP routing table\\nDestination  Gateway      Genmask        Flags Metric Ref Use Iface\\ndefault      192.168.1.1  0.0.0.0        UG    100    0   0   eth0'),
        ('route -n','0.0.0.0       192.168.1.1  0.0.0.0        UG    100  0  0 eth0\\n192.168.1.0   0.0.0.0      255.255.255.0  U     100  0  0 eth0'),
        ('nslookup google.com','Server: 8.8.8.8\\nAddress: 8.8.8.8#53\\nNon-authoritative answer:\\nName: google.com\\nAddress: 142.250.80.46'),
        ('nslookup -type=A google.com','\\u67e5\\u8be2 A \\u8bb0\\u5f55'),
        ('nslookup -type=MX google.com','\\u67e5\\u8be2 MX \\u8bb0\\u5f55'),
        ('nslookup -type=NS google.com','\\u67e5\\u8be2 NS \\u8bb0\\u5f55'),
        ('nslookup -type=TXT google.com','\\u67e5\\u8be2 TXT \\u8bb0\\u5f55'),
        ('dig google.com','; <<>> DiG 9.16 <<>> google.com\\nglobal options: +cmd\\nGot answer:\\n;; ANSWER SECTION:\\ngoogle.com. 300 IN A 142.250.80.46'),
        ('dig +short google.com','142.250.80.46'),
        ('dig -x 8.8.8.8','8.8.8.8.in-addr.arpa. 3600 IN PTR dns.google.'),
        ('dig MX google.com','\\u67e5\\u8be2 MX \\u8bb0\\u5f55'),
        ('dig ANY google.com','\\u67e5\\u8be2\\u6240\\u6709\\u8bb0\\u5f55'),
        ('dig +trace google.com','\\u8ddf\\u8e2a DNS \\u89e3\\u6790\\u8def\\u5f84'),
        ('host google.com','google.com has address 142.250.80.46\\ngoogle.com mail is handled by 10 smtp.google.com.'),
        ('host -t MX google.com','google.com mail is handled by 10 smtp.google.com.'),
        ('hostname -I','192.168.1.100'),
        ('hostname -d','local'),
        ('curl http://localhost','<html><body><h1>It works!</h1></body></html>'),
        ('curl -I http://localhost','HTTP/1.1 200 OK\\nServer: nginx/1.18.0\\nContent-Type: text/html\\nContent-Length: 42'),
        ('curl -X POST http://localhost','\\u53d1\\u9001 POST \\u8bf7\\u6c42'),
        ('curl -H "Content-Type: application/json" http://localhost','\\u81ea\\u5b9a\\u4e49\\u8bf7\\u6c42\\u5934'),
        ("curl -d '{\"key\":\"val\"}' http://localhost",'\\u53d1\\u9001 POST \\u6570\\u636e'),
        ('curl -o file.html http://localhost','\\u4e0b\\u8f7d\\u5230 file.html'),
        ('curl -O http://localhost/file.txt','\\u4e0b\\u8f7d\\u5230 file.txt'),
        ('curl -L http://short.url','\\u8ddf\\u968f\\u91cd\\u5b9a\\u5411'),
        ('curl -v http://localhost','* Connected to localhost (127.0.0.1) port 80\\n> GET / HTTP/1.1\\n> Host: localhost\\n< HTTP/1.1 200 OK'),
        ('curl -s http://localhost','\\u5b89\\u9759\\u6a21\\u5f0f(\\u4e0d\\u663e\\u793a\\u8fdb\\u5ea6)'),
        ('curl --compressed http://localhost','\\u652f\\u6301\\u538b\\u7f29'),
        ('wget http://localhost','--2026-06-16 02:00:41-- http://localhost/\\nResolving localhost... 127.0.0.1\\nConnecting to localhost|127.0.0.1|:80... connected.\\nHTTP request sent, awaiting response... 200 OK\\nLength: 42 [text/html]\\nSaving to: \\u2018index.html\\u2019\\n2026-06-16 02:00:41 (12.3 MB/s) - \\u2018index.html\\u2019 saved [42/42]'),
        ('wget -O output.html http://localhost','\\u4fdd\\u5b58\\u4e3a output.html'),
        ('wget -q http://localhost','\\u5b89\\u9759\\u6a21\\u5f0f'),
        ('wget -r http://localhost','\\u9012\\u5f52\\u4e0b\\u8f7d'),
        ('wget --limit-rate=100k http://localhost/file','\\u9650\\u901f\\u4e0b\\u8f7d'),
        ('wget -c http://localhost/file','\\u65ad\\u70b9\\u7eed\\u4f20'),
        ('nc -l 8080','\\u76d1\\u542c 8080 \\u7aef\\u53e3...'),
        ('nc localhost 8080','\\u8fde\\u63a5\\u5230 localhost:8080'),
        ('nc -v localhost 80','Connection to localhost 80 port [tcp/http] succeeded!'),
        ('nc -z localhost 1-100','\\u7aef\\u53e3\\u626b\\u63cf 1-100'),
        ('nc -u localhost 53','UDP \\u8fde\\u63a5'),
        ('telnet localhost 80','Trying 127.0.0.1...\\nConnected to localhost.\\nEscape character is \\u2018^]\\u2019.'),
        ('ssh user@localhost','\\u8fde\\u63a5\\u5230 localhost...\\nuser@localhost\\u2019s password:'),
        ('ssh -p 2222 user@host','\\u8fde\\u63a5\\u5230 host:2222'),
        ('ssh -i ~/.ssh/id_rsa user@host','\\u4f7f\\u7528\\u5bc6\\u94a5\\u6587\\u4ef6\\u8fde\\u63a5'),
        ('scp file.txt user@host:~','file.txt 100% 1024 1.0MB/s 00:00'),
        ('scp -r dir user@host:~','\\u9012\\u5f52\\u590d\\u5236\\u76ee\\u5f55'),
        ('rsync -av src/ dst/','sending incremental file list\\n./\\nfile.txt\\nsent 1234 bytes  received 56 bytes  2580.00 bytes/sec'),
        ('rsync -avz src/ user@host:dst/','\\u538b\\u7f29\\u8fdc\\u7a0b\\u540c\\u6b65'),
        ('rsync --delete src/ dst/','\\u540c\\u6b65\\u65f6\\u5220\\u9664\\u591a\\u4f59\\u6587\\u4ef6'),
        ('rsync -P largefile user@host:~','\\u663e\\u793a\\u8fdb\\u5ea6\\u4e14\\u652f\\u6301\\u65ad\\u70b9\\u7eed\\u4f20'),
        ('ftp localhost','Connected to localhost.\\n220 FTP server ready.\\nName (localhost:user):'),
        ('sftp user@localhost','Connected to localhost.\\nsftp>'),
        ('tcpdump -i eth0','listening on eth0\\n02:00:41.123456 IP 192.168.1.100.54321 > 8.8.8.8.53: UDP, length 64'),
        ('tcpdump -c 10','\\u6355\\u83b7 10 \\u4e2a\\u5305\\u540e\\u505c\\u6b62'),
        ('tcpdump -w capture.pcap','\\u4fdd\\u5b58\\u5230 capture.pcap'),
        ('tcpdump -r capture.pcap','\\u8bfb\\u53d6\\u6355\\u83b7\\u6587\\u4ef6'),
        ('tcpdump port 80','\\u6355\\u83b7 80 \\u7aef\\u53e3\\u6d41\\u91cf'),
        ('tcpdump host 192.168.1.1','\\u6355\\u83b7\\u7279\\u5b9a\\u4e3b\\u673a'),
        ('nmap localhost','Starting Nmap\\nPORT   STATE SERVICE\\n80/tcp open  http\\nNmap done: 1 IP address scanned in 0.03 seconds'),
        ('nmap -sV localhost','\\u7248\\u672c\\u68c0\\u6d4b'),
        ('nmap -p 1-1000 localhost','\\u7aef\\u53e3\\u8303\\u56f4\\u626b\\u63cf'),
        ('nmap -sS localhost','SYN \\u626b\\u63cf'),
        ('nmap -A localhost','\\u5168\\u9762\\u626b\\u63cf'),
    ]
    for kv in net_cmds:
        entries.append(cmd(kv[0], kv[1]))
    
    remaining = 1200 - len(entries) + 8  # account for comment lines
    print(f"  Generated {len(entries)} entries so far, need {remaining} more...")
    
    # --- DevOps & Git (80 cmds) ---
    entries.append("  /* ── DevOps & Git ── */")
    git_cmds = [
        ('git init','Initialized empty Git repository in /home/user/project/.git/'),
        ('git clone https://github.com/user/repo.git',"Cloning into 'repo'...\\nremote: Enumerating objects: 123, done.\\nremote: Counting objects: 100% (123/123), done.\\nReceiving objects: 100% (123/123), 45.67 KiB | 1.23 MiB/s, done."),
        ('git status','On branch main\\nYour branch is up to date with \\u2018origin/main\\u2019.\\nChanges not staged for commit:\\n  modified:   README.md'),
        ('git status -s',' M README.md\\n?? newfile.txt'),
        ('git add .','\\u5df2\\u6dfb\\u52a0\\u6240\\u6709\\u6587\\u4ef6\\u5230\\u6682\\u5b58\\u533a'),
        ('git add file.txt','\\u5df2\\u6dfb\\u52a0 file.txt \\u5230\\u6682\\u5b58\\u533a'),
        ('git add -p','\\u4ea4\\u4e92\\u5f0f\\u6dfb\\u52a0'),
        ('git add -A','\\u6dfb\\u52a0\\u6240\\u6709\\u53d8\\u66f4(\\u542b\\u5220\\u9664)'),
        ("git commit -m 'Initial commit'","[main (root-commit) abc1234] Initial commit\\n 1 file changed, 10 insertions(+)"),
        ("git commit -am 'Update'","[main def5678] Update\\n 1 file changed, 2 insertions(+), 1 deletion(-)"),
        ('git commit --amend','\\u4fee\\u6539\\u4e0a\\u6b21\\u63d0\\u4ea4'),
        ('git log','commit abc1234 (HEAD -> main)\\nAuthor: User <user@fusion.dev>\\nDate: Tue Jun 16 02:00:41 2026\\n    Initial commit'),
        ('git log --oneline','abc1234 Initial commit\\ndef5678 Add README\\nghi9012 Fix bug'),
        ('git log --graph','* abc1234 (HEAD -> main) Initial commit'),
        ('git log -p','\\u663e\\u793a diff \\u5185\\u5bb9'),
        ('git log --author=user','\\u6309\\u4f5c\\u8005\\u7b5b\\u9009'),
        ('git log --since="2026-06-01"','\\u6309\\u65e5\\u671f\\u7b5b\\u9009'),
        ('git diff','diff --git a/README.md b/README.md\\n--- a/README.md\\n+++ b/README.md\\n@@ -1,3 +1,3 @@\\n-# Old\\n+# New'),
        ('git diff --staged','\\u663e\\u793a\\u6682\\u5b58\\u533a\\u5dee\\u5f02'),
        ('git diff HEAD~1','\\u4e0e\\u4e0a\\u6b21\\u63d0\\u4ea4\\u6bd4\\u8f83'),
        ('git diff main..feature','\\u6bd4\\u8f83\\u4e24\\u4e2a\\u5206\\u652f'),
        ('git branch','* main'),
        ('git branch -a','* main\\n  remotes/origin/main\\n  remotes/origin/develop'),
        ('git branch feature','\\u5df2\\u521b\\u5efa\\u5206\\u652f feature'),
        ('git branch -d feature','\\u5df2\\u5220\\u9664\\u5206\\u652f feature'),
        ('git branch -D feature','\\u5df2\\u5f3a\\u5236\\u5220\\u9664\\u5206\\u652f feature'),
        ('git checkout -b feature','Switched to a new branch \\u2018feature\\u2019'),
        ('git checkout main','Switched to branch \\u2018main\\u2019'),
        ('git switch feature','Switched to branch \\u2018feature\\u2019'),
        ('git switch -c feature','\\u521b\\u5efa\\u5e76\\u5207\\u6362\\u5230 feature'),
        ('git merge feature','Updating abc1234..def5678\\nFast-forward\\n file.txt | 5 +++++\\n 1 file changed, 5 insertions(+)'),
        ('git merge --no-ff feature','\\u975e\\u5feb\\u8fdb\\u5408\\u5e76'),
        ('git rebase main','Successfully rebased and updated refs/heads/feature.'),
        ('git rebase -i HEAD~3','\\u4ea4\\u4e92\\u5f0f rebase'),
        ('git stash','Saved working directory and index state WIP on main: abc1234'),
        ('git stash pop','Dropped refs/stash@{0} (abc1234)'),
        ('git stash list','stash@{0}: WIP on main: abc1234'),
        ('git stash drop','Dropped refs/stash@{0}'),
        ('git remote -v','origin  https://github.com/user/repo.git (fetch)\\norigin  https://github.com/user/repo.git (push)'),
        ('git remote add origin https://github.com/user/repo.git','\\u5df2\\u6dfb\\u52a0\\u8fdc\\u7a0b origin'),
        ('git push origin main','Enumerating objects: 5, done.\\nTo https://github.com/user/repo.git\\n   abc1234..def5678  main -> main'),
        ('git push -u origin main','\\u63a8\\u9001\\u5e76\\u8bbe\\u7f6e\\u4e0a\\u6e38\\u5206\\u652f'),
        ('git push --force','\\u5f3a\\u5236\\u63a8\\u9001(\\u8c28\\u614e!)'),
        ('git pull','Already up to date.'),
        ('git pull --rebase','\\u62c9\\u53d6\\u5e76 rebase'),
        ('git fetch','From https://github.com/user/repo\\n   abc1234..def5678  main     -> origin/main'),
        ('git fetch --prune','\\u62c9\\u53d6\\u5e76\\u6e05\\u7406\\u5df2\\u5220\\u9664\\u7684\\u8fdc\\u7a0b\\u5206\\u652f'),
        ('git tag v1.0','\\u5df2\\u521b\\u5efa\\u6807\\u7b7e v1.0'),
        ('git tag -a v1.0 -m "Release v1.0"','\\u5df2\\u521b\\u5efa\\u6ce8\\u91ca\\u6807\\u7b7e v1.0'),
        ('git tag -l','v1.0\\nv1.0.1'),
        ('git push --tags','\\u63a8\\u9001\\u6240\\u6709\\u6807\\u7b7e'),
        ('git blame file.txt','abc1234 (User 2026-06-16 02:00:41) 1) Hello World\\ndef5678 (User 2026-06-15 18:30:00) 2) Line 2'),
        ('git show abc1234','\\u663e\\u793a\\u63d0\\u4ea4\\u8be6\\u60c5'),
        ('git reset HEAD file.txt','\\u53d6\\u6d88\\u6682\\u5b58 file.txt'),
        ('git reset --soft HEAD~1','\\u64a4\\u9500\\u63d0\\u4ea4(\\u4fdd\\u7559\\u66f4\\u6539)'),
        ('git reset --hard HEAD','\\u786c\\u91cd\\u7f6e\\u5230 HEAD'),
        ('git clean -fd','\\u6e05\\u7406\\u672a\\u8ddf\\u8e2a\\u6587\\u4ef6'),
        ('git reflog','abc1234 HEAD@{0}: commit: Initial commit'),
        ('git cherry-pick abc1234','[feature def5678] Initial commit\\n 1 file changed, 10 insertions(+)'),
        ('git bisect start','\\u5f00\\u59cb\\u4e8c\\u5206\\u67e5\\u627e'),
        ('git config --global user.name "User"','\\u5df2\\u8bbe\\u7f6e user.name'),
        ('git config --global user.email "user@fusion.dev"','\\u5df2\\u8bbe\\u7f6e user.email'),
        ('git config --list','user.name=User\\nuser.email=user@fusion.dev\\ncore.editor=vim'),
        ('git archive --format=zip HEAD > archive.zip','\\u5df2\\u521b\\u5efa\\u5f52\\u6863 archive.zip'),
        ('git submodule add https://github.com/lib/lib.git','Cloning into \\u2018lib\\u2019...\\ndone.'),
        ('git submodule update --init','Submodule path \\u2018lib\\u2019: checked out \\u2018abc1234\\u2019'),
        ('git worktree add ../feature feature','Preparing worktree (new branch \\u2018feature\\u2019)\\nHEAD is now at abc1234'),
        ('git gc','Enumerating objects: 123, done.\\nCounting objects: 100% (123/123), done.\\nCompressing objects: 100% (89/89), done.'),
        ('npm init -y','Wrote to /home/user/project/package.json: { "name": "project", "version": "1.0.0" }'),
        ('npm install','added 234 packages in 5s'),
        ('npm install express','+ express@4.18.2\\nadded 57 packages in 2s'),
        ('npm install --save-dev jest','+ jest@29.5.0\\nadded 123 packages in 3s'),
        ('npm uninstall express','removed 57 packages in 1s'),
        ('npm update','updated 12 packages in 2s'),
        ('npm list','project@1.0.0 /home/user/project\\n\\u251c\\u2500\\u2500 express@4.18.2\\n\\u2514\\u2500\\u2500 jest@29.5.0'),
        ('npm run build','> project@1.0.0 build\\n> webpack --mode production\\nwebpack compiled successfully in 2.34s'),
        ('npm run test','PASS  ./test/app.test.js\\n  App\\n    \\u2713 should render (5ms)\\nTests: 1 passed, 1 total'),
        ('npm start','> project@1.0.0 start\\n> node index.js\\nServer listening on port 3000'),
        ('npm audit','found 0 vulnerabilities'),
        ('npm publish','+ project@1.0.0'),
    ]
    for kv in git_cmds:
        entries.append(cmd(kv[0], kv[1]))
    
    # --- Programming Languages (70 cmds) ---
    entries.append("  /* ── Programming ── */")
    prog_cmds = [
        ('python3','Python 3.11.4 (main, Jun 12 2026)\\nType "help", "copyright", "credits" or "license" for more information.'),
        ('python3 -V','Python 3.11.4'),
        ('python3 -c "print(2+2)"','4'),
        ('python3 -m http.server','Serving HTTP on 0.0.0.0 port 8000 ...'),
        ('python3 -m json.tool data.json','{\\n    "key": "value"\\n}'),
        ('python3 -m venv venv','\\u5df2\\u521b\\u5efa\\u865a\\u62df\\u73af\\u5883 venv'),
        ('python3 -m pip install requests','Successfully installed requests-2.31.0'),
        ('python3 -m pip list','Package    Version\\nrequests   2.31.0\\npip        23.1.2'),
        ('python3 -m pip freeze','requests==2.31.0'),
        ('python3 script.py','Hello from Python!'),
        ('python3 -i','Python 3.11.4 (\\u4ea4\\u4e92\\u6a21\\u5f0f)'),
        ('python3 -u script.py','\\u65e0\\u7f13\\u51b2\\u6a21\\u5f0f'),
        ('python3 -OO script.py','\\u4f18\\u5316\\u6a21\\u5f0f'),
        ('pip install package','Successfully installed package-1.0.0'),
        ('pip install --upgrade pip','Successfully upgraded pip to 23.1.2'),
        ('pip uninstall package','Successfully uninstalled package-1.0.0'),
        ('pip show requests','Name: requests\\nVersion: 2.31.0\\nSummary: Python HTTP for Humans.'),
        ('node','Welcome to Node.js v20.11.0.\\nType ".help" for more information.'),
        ('node -v','v20.11.0'),
        ('node -e "console.log(1+2)"','3'),
        ('node script.js','Hello from Node.js!'),
        ('node --inspect script.js','Debugger listening on ws://127.0.0.1:9229'),
        ('node --max-old-space-size=4096 script.js','\\u5185\\u5b58\\u9650\\u5236 4GB'),
        ('npm -v','10.2.4'),
        ('npx create-react-app myapp','Creating a new React app in /home/user/myapp.\\nInstalling packages...\\nSuccess!'),
        ('npx tsc --version','Version 5.3.3'),
        ('npx eslint .','0 errors, 0 warnings'),
        ('npx prettier --check .','Checking formatting...\\nAll matched files use Prettier code style!'),
        ('gcc --version','gcc (GCC) 13.2.0'),
        ('gcc -o hello hello.c','\\u7f16\\u8bd1\\u6210\\u529f: hello'),
        ('g++ -o hello hello.cpp','\\u7f16\\u8bd1\\u6210\\u529f: hello'),
        ('make','gcc -c main.c -o main.o\\ngcc -o app main.o\\nBuild complete!'),
        ('make clean','\\u6e05\\u7406\\u6784\\u5efa\\u6587\\u4ef6'),
        ('make -j4','\\u5e76\\u884c\\u6784\\u5efa(4\\u7ebf\\u7a0b)'),
        ('cmake .','-- The C compiler identification is GNU 13.2.0\\n-- Configuring done\\n-- Generating done'),
        ('cmake --build .','[100%] Built target app'),
        ('javac Hello.java','\\u7f16\\u8bd1\\u6210\\u529f: Hello.class'),
        ('java Hello','Hello, World!'),
        ('java -version','openjdk version "21.0.1" 2026-06-12'),
        ('go version','go version go1.21.5 linux/amd64'),
        ('go run main.go','Hello from Go!'),
        ('go build -o app main.go','\\u6784\\u5efa\\u6210\\u529f: app'),
        ('go mod init module','go: creating new go.mod: module module'),
        ('rustc --version','rustc 1.75.0'),
        ('cargo new myapp','Created binary (application) `myapp` package'),
        ('cargo build','Compiling myapp v0.1.0\\nFinished dev [unoptimized + debuginfo] target(s) in 2.34s'),
        ('cargo run','Hello, world!'),
        ('cargo test','running 1 test\\ntest tests::it_works ... ok\\ntest result: ok. 1 passed'),
        ('cargo check','Checking myapp v0.1.0\\nFinished dev [unoptimized + debuginfo] target(s) in 0.56s'),
        ('perl -v','This is perl 5, version 36, subversion 0'),
        ('perl -e \'print "Hello\\n"\'','Hello'),
        ('ruby -v','ruby 3.2.2'),
        ('ruby -e \'puts "Hello"\'','Hello'),
        ('php -v','PHP 8.2.7'),
        ('php -r \'echo "Hello";\'','Hello'),
        ('dotnet --version','8.0.100'),
        ('docker --version','Docker version 26.0.0'),
        ('docker ps','CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES'),
        ('docker images','REPOSITORY TAG    IMAGE ID     CREATED      SIZE\\nnginx      latest abc123def456 2 weeks ago  187MB'),
        ('docker run nginx','Unable to find image \\u2018nginx:latest\\u2019 locally\\nlatest: Pulling from library/nginx\\nStatus: Downloaded newer image'),
        ('docker build -t myapp .','Sending build context to Docker daemon  2.048kB\\nStep 1/5 : FROM node:20\\nSuccessfully built abc1234\\nSuccessfully tagged myapp:latest'),
        ('docker-compose up','Starting project_db_1 ... done\\nStarting project_app_1 ... done'),
        ('docker-compose down','Stopping project_app_1 ... done\\nStopping project_db_1  ... done'),
        ('kubectl version','Client Version: v1.29.0'),
        ('kubectl get pods','NAME    READY STATUS  RESTARTS AGE\\nweb-0   1/1   Running 0        5m'),
        ('kubectl get nodes','NAME   STATUS ROLES        AGE VERSION\\nnode1  Ready  control-plane 10d v1.29.0'),
        ('kubectl apply -f deployment.yaml','deployment.apps/web created\\nservice/web created'),
    ]
    for kv in prog_cmds:
        entries.append(cmd(kv[0], kv[1]))
    
    # --- Fun & Games (70 cmds) ---
    entries.append("  /* ── Fun & Games ── */")
    fun_cmds = [
        ('cowsay Hello',' ______\\n< Hello >\\n ------\\n        \\\\   ^__^\\n         \\\\  (oo)\\\\_______\\n            (__)\\\\       )\\\\/\\\\\\n                ||----w |\\n                ||     ||'),
        ('cowsay -f dragon Hi','\\u9f99\\u5f62\\u8c61\\u663e\\u793a Hi'),
        ('cowsay -f tux Linux','\\u4f01\\u9e45\\u5f62\\u8c61'),
        ('cowsay -l','Available cows: apt beavis.zen bong bud-frogs bunny calvin cheese cock cower daemon default'),
        ('fortune','You will have a pleasant surprise.'),
        ('fortune -s','A short fortune cookie message.'),
        ('fortune -l','A long fortune cookie message with lots of wisdom to share...'),
        ('fortune -o','Offensive fortune: (content hidden)'),
        ('cowsay $(fortune)',' ______\\n< Wise words... >\\n ------\\n        \\\\   ^__^\\n         \\\\  (oo)\\\\_______'),
        ('lolcat file.txt','\\u5f69\\u8679\\u989c\\u8272\\u663e\\u793a\\u6587\\u4ef6'),
        ('figlet Hello',' _   _      _ _       \\n| | | | ___| | | ___  \\n| |_| |/ _ \\\\ | |/ _ \\\\ \\n|  _  |  __/ | | (_) |\\n|_| |_|\\\\___|_|_|\\\\___/ '),
        ('figlet -f slant Fusion','\\u503e\\u659c\\u5b57\\u4f53\\u663e\\u793a Fusion'),
        ('toilet Hello','\\u5f69\\u8272 ASCII Hello'),
        ('banner Hello','\\u5927\\u5b57\\u4f53 Hello'),
        ('sl','\\ud83d\\ude82 \\u706b\\u8f66\\u52a8\\u753b\\u6b63\\u5728\\u901a\\u8fc7... \\ud83d\\udca8\\ud83d\\udca8'),
        ('sl -l','\\u5c0f\\u706b\\u8f66\\u7248\\u672c'),
        ('sl -F','\\u98de\\u884c\\u7248\\u706b\\u8f66'),
        ('cmatrix','\\u300a\\u9ed1\\u5ba2\\u5e1d\\u56fd\\u300b\\u98ce\\u683c\\u5b57\\u7b26\\u96e8(\\u5df2\\u6a21\\u62df)'),
        ('cmatrix -C green','\\u7eff\\u8272\\u5b57\\u7b26\\u96e8'),
        ('cmatrix -s','\\u5c4f\\u4fdd\\u6a21\\u5f0f'),
        ('asciiquarium','\\ud83d\\udc1f \\ud83d\\udc20 \\ud83d\\udc21 \\ud83e\\udd88 \\u6c34\\u65cf\\u9986\\u52a8\\u753b(\\u5df2\\u6a21\\u62df)'),
        ('nyancat','\\ud83d\\udc31\\ud83c\\udf08 \\u5f69\\u8679\\u732b\\u52a8\\u753b(\\u5df2\\u6a21\\u62df)'),
        ('nyancat -ns','\\u65e0\\u58f0\\u97f3\\u5f69\\u8679\\u732b'),
        ('ponysay Hello','\\u5c0f\\u9a6c\\u5bf9\\u8bdd\\u6846: Hello'),
        ('ponysay -l','\\u53ef\\u7528\\u5c0f\\u9a6c\\u5217\\u8868'),
        ('rev','dlroW olleH'),
        ('rev <<< "Hello World"','dlroW olleH'),
        ('echo Hello | rev','olleH'),
        ('factor 42','42: 2 3 7'),
        ('factor 97','97: 97'),
        ('factor 100','100: 2 2 5 5'),
        ('factor 1234567890','1234567890: 2 3 3 5 3607 3803'),
        ('pi 100','3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679'),
        ('pi 50','3.14159265358979323846264338327950288419716939937510'),
        ('echo "scale=100;4*a(1)" | bc -l','3.14159265358979323846264338327950288419716939937510...'),
        ('aafire','\\ud83d\\udd25 ASCII \\u706b\\u7130\\u52a8\\u753b(\\u5df2\\u6a21\\u62df)'),
        ('bb','\\ud83c\\udfa8 ASCII \\u97f3\\u4e50\\u53ef\\u89c6\\u5316(\\u5df2\\u6a21\\u62df)'),
        ('asciiart','\\u663e\\u793a\\u968f\\u673a ASCII \\u827a\\u672f'),
        ('oneko','\\ud83d\\udc31 \\u684c\\u9762\\u5c0f\\u732b\\u52a8\\u753b(\\u5df2\\u6a21\\u62df)'),
        ('xeyes','\\ud83d\\udc40 \\u773c\\u775b\\u8ddf\\u968f\\u9f20\\u6807(\\u5df2\\u6a21\\u62df)'),
        ('worms','\\ud83d\\udc1b \\u87f2\\u5b50\\u52a8\\u756b(\\u5df2\\u6a21\\u62df)'),
        ('moon-buggy','\\ud83d\\ude97 \\u6708\\u7403\\u8eca\\u904a\\u6232(\\u6a21\\u64ec)'),
        ('espeak "Hello"','\\ud83d\\udd0a \\u8a9e\\u97f3\\u5408\\u6210: Hello'),
        ('say "Hello World"','\\ud83d\\udd0a \\u8a9e\\u97f3: Hello World'),
        ('cava','\\ud83c\\udfb5 \\u97f3\\u6a02\\u8996\\u89ba\\u5316(\\u6a21\\u64ec)'),
        ('hollywood','\\ud83c\\udfac \\u597d\\u840a\\u5862\\u98a8 hacker \\u756b\\u9762(\\u6a21\\u64ec)'),
        ('cbonsai','\\ud83c\\udf33 ASCII \\u76c6\\u666f(\\u6a21\\u64ec)'),
        ('pipes.sh','\\u250c\\u2500\\u2500\\u252c\\u2500\\u2500\\u2510 \\u7ba1\\u9053\\u52d5\\u756b(\\u6a21\\u64ec)\\n\\u2502\\u250c\\u2534\\u2510\\u2502\\n\\u2502\\u2514\\u252c\\u2518\\u2502\\n\\u2514\\u2500\\u2500\\u2534\\u2500\\u2500\\u2518'),
        ('tmatrix','\\u300a\\u99ed\\u5ba2\\u4efb\\u52d9\\u300b\\u98a8\\u683c\\u5b57\\u7b26\\u96e8(\\u6a21\\u64ec)'),
        ('pong','\\ud83c\\udfd3 \\u5175\\u4e52\\u7403\\u904a\\u6232(\\u6a21\\u64ec)'),
        ('pacman','\\ud83d\\udc7b Pac-Man \\u904a\\u6232(\\u6a21\\u64ec)'),
        ('snake','\\ud83d\\udc0d \\u8caa\\u5403\\u86c7\\u904a\\u6232(\\u6a21\\u64ec)'),
        ('tetris','\\u25a0\\u25a0\\u25a0 \\u4fc4\\u7f85\\u65af\\u65b9\\u584a(\\u6a21\\u64ec)'),
        ('2048','\\u6570\\u5b57\\u5408\\u4f53\\u904a\\u6232(\\u6a21\\u64ec)'),
        ('sudoku','\\u6570\\u7368\\u904a\\u6232(\\u6a21\\u64ec)'),
        ('chess','\\u2654 \\u570b\\u969b\\u8c61\\u68cb(\\u6a21\\u64ec)'),
        ('invaders','\\ud83d\\udc7e \\u592a\\u7a7a\\u4fb5\\u7565\\u8005(\\u6a21\\u64ec)'),
        ('dino','\\ud83e\\udd96 Chrome \\u6050\\u9f8d\\u904a\\u6232(\\u6a21\\u64ec)'),
        ('screenfetch','\\u6642\\u5c1a OS \\u8cc7\\u8a0a\\u986f\\u793a'),
        ('neofetch','user@fusion-desktop\\n-----------\\nOS: FusionOS 8.0\\nKernel: fusion-8.0.0\\nUptime: 3 days\\nShell: fsh 5.8\\nResolution: 1920x1080\\nDE: Fusion Desktop\\nWM: Fusion WM\\nTheme: Fusion Dark\\nCPU: Fusion Virtual @ 3.20GHz\\nGPU: Fusion Display\\nMemory: 2015MiB / 16000MiB'),
        ('pfetch','\\u7c21\\u6f54\\u7248\\u7cfb\\u7d71\\u8cc7\\u8a0a'),
        ('fastfetch','\\u5feb\\u901f\\u7cfb\\u7d71\\u8cc7\\u8a0a'),
        ('macchina','\\u53e6\\u4e00\\u7a2e\\u7cfb\\u7d71\\u8cc7\\u8a0a\\u5de5\\u5177'),
        ('uwufetch','\\u840c\\u5316\\u7248\\u7cfb\\u7d71\\u8cc7\\u8a0a ~nya~'),
        ('hyfetch','\\u5f69\\u8679\\u7248\\u7cfb\\u7d71\\u8cc7\\u8a0a'),
        ('cpufetch','\\u663e\\u793a CPU \\u8be6\\u7ec6\\u4fe1\\u606f'),
        ('gpufetch','\\u663e\\u793a GPU \\u8be6\\u7ec6\\u4fe1\\u606f'),
        ('ramfetch','\\u663e\\u793a\\u5185\\u5b58\\u4fe1\\u606f'),
        ('diskfetch','\\u663e\\u793a\\u78c1\\u76d8\\u4fe1\\u606f'),
    ]
    for kv in fun_cmds:
        entries.append(cmd(kv[0], kv[1]))
    
    current_total = len([e for e in entries if not e.startswith('  /*')])
    print(f"  After fun: {current_total} commands generated")
    
    # Generate remaining commands using programmatic templates to reach 1200
    # We need about 1200 - current_total more
    needed = 1200 - current_total
    print(f"  Need {needed} more commands, generating via templates...")
    
    # --- Template-generated commands ---
    math_ops = ['add','sub','mul','div','pow','sqrt','mod','abs','ceil','floor','round','sin','cos','tan','log','ln','exp','min','max','avg','sum','product','median','mode']
    for op in math_ops:
        entries.append(cmd(f'math {op} 10 5', f'{op}(10, 5) = (computed)', f'Math - {op}'))
    
    disk_ops = ['format','check','repair','defrag','cleanup','analyze','benchmark','info','label','resize','encrypt','decrypt','mount','umount','sync','trim','badblocks','smartctl','partprobe','fsck']
    for op in disk_ops:
        entries.append(cmd(f'disk {op}', f'Disk {op} operation simulated successfully.', f'Disk - {op}'))
    
    sysctl_keys = [f'sysctl net.ipv4.{k}' for k in ['tcp_syncookies','tcp_fin_timeout','tcp_keepalive_time','tcp_keepalive_intvl','tcp_keepalive_probes','tcp_retries1','tcp_retries2','tcp_orphan_retries','tcp_tw_reuse','tcp_max_syn_backlog','tcp_max_tw_buckets','tcp_wmem','tcp_rmem','tcp_mem','tcp_congestion_control','tcp_slow_start_after_idle','tcp_mtu_probing','tcp_no_metrics_save','tcp_timestamps','tcp_window_scaling']]
    for k in sysctl_keys:
        entries.append(cmd(k, '= 1', k))
    
    sysctl_vm = [f'sysctl vm.{k}' for k in ['swappiness','dirty_ratio','dirty_background_ratio','vfs_cache_pressure','overcommit_memory','overcommit_ratio','min_free_kbytes','drop_caches','zone_reclaim_mode','page-cluster','panic_on_oom']]
    for k in sysctl_vm:
        entries.append(cmd(k, '= (system default)', k))
    
    crypto_ops = ['md5','sha1','sha256','sha512','sha3-256','sha3-512','blake2','crc32','adler32','xxhash','murmur3','cityhash']
    for op in crypto_ops:
        entries.append(cmd(f'{op}sum file.txt', f'{op}: abc123def456...', f'Crypto - {op}'))
    
    enc_dec = ['base64','base32','base16','hex','urlencode','urldecode','rot13','rot47','uuencode','uudecode']
    for op in enc_dec:
        entries.append(cmd(f'{op} "Hello World"', f'Encoded: (output)', f'Encode - {op}'))
    
    compress_ops = ['gzip','gunzip','bzip2','bunzip2','xz','unxz','zip','unzip','tar','untar','7z','rar','zstd','lz4','lzma','compress','uncompress','lzop','ar','cpio']
    for op in compress_ops:
        entries.append(cmd(f'{op} file.txt', f'{op}: operation simulated', f'Compress - {op}'))
    
    db_ops = ['mysql','psql','sqlite3','redis-cli','mongo','influx','cassandra','neo4j','elasticsearch','etcd','consul','memcached']
    for op in db_ops:
        entries.append(cmd(f'{op} --version', f'{op} client version 8.0 (FusionOS)', f'DB - {op}'))
    
    # File permission operations
    perm_ops = ['chmod','chown','chgrp','chattr','lsattr','getfacl','setfacl','umask']
    for op in perm_ops:
        entries.append(cmd(f'{op} --help', f'{op}: change file attributes/permissions', f'Perm - {op}'))
    
    # More network
    net_extra = ['iptables','ip6tables','nft','ufw','firewalld','ebtables','arptables','tc','bridge','vconfig','teamd','nmcli','nmtui','iw','wpa_cli','rfkill','ethtool','mii-tool','ipset']
    for op in net_extra:
        entries.append(cmd(f'{op} --help', f'{op}: network management tool', f'Net - {op}'))
    
    # Package managers
    pkg_mgrs = ['apt','apt-get','apt-cache','dpkg','rpm','yum','dnf','zypper','pacman','pamac','yay','portage','emerge','snap','flatpak','appimage','brew','pip','npm','cargo','gem','composer']
    for pm in pkg_mgrs:
        entries.append(cmd(f'{pm} --version', f'{pm} package manager v2.0 (FusionOS)', f'Pkg - {pm}'))
    
    # Editors
    editors = ['vim','vi','nano','emacs','neovim','nvim','gedit','kate','code','sublime','atom','notepad','helix','micro','joe','mcedit']
    for ed in editors:
        entries.append(cmd(f'{ed} --version', f'{ed} editor (FusionOS edition)', f'Editor - {ed}'))
    
    # Shell built-ins
    shells = ['bash','zsh','fish','dash','ksh','tcsh','csh','sh','nu','elvish','xonsh','ion']
    for sh in shells:
        entries.append(cmd(f'{sh} --version', f'{sh} shell v5.2 (FusionOS)', f'Shell - {sh}'))
    
    # Environment
    env_vars = ['HOME','USER','PATH','SHELL','TERM','LANG','PWD','OLDPWD','HOSTNAME','DISPLAY','EDITOR','VISUAL','PAGER','BROWSER','MANPATH','LD_LIBRARY_PATH']
    for var in env_vars:
        entries.append(cmd(f'echo ${var}', f'(value of {var})', f'Env - {var}'))
    
    # Colors/formatting
    color_cmds = ['tput setaf 1','tput setaf 2','tput setaf 3','tput bold','tput smul','tput rmul','tput rev','tput sgr0','tput cols','tput lines','tput colors']
    for c in color_cmds:
        entries.append(cmd(c, '(terminal attribute set)', c))
    
    # Scheduling
    sched = ['crontab -l','crontab -e','atq','atrm','batch','anacron','systemd-timer','fcrontab']
    for s in sched:
        entries.append(cmd(s, '(scheduler operation)', s))
    
    # Service management
    services = ['systemctl status','systemctl start','systemctl stop','systemctl restart','systemctl enable','systemctl disable','systemctl list-units','service --status-all','chkconfig','update-rc.d','rc-update','sv','runit']
    for sv in services:
        entries.append(cmd(f'{sv} fusion-shell', f'{sv}: service operation (FusionOS)', sv.replace(' ','-')))
    
    # More tools
    tools = ['jq','yq','xmlstarlet','xpath','csvkit','pandoc','graphviz','imagemagick','ffmpeg','sox','gimp','inkscape','blender','audacity','kdenlive','obs','vlc','mpv','mplayer','feh','sxiv','zathura','evince','okular','libreoffice','calibre','mutt','neomutt','irssi','weechat','newsboat','ranger','nnn','lf','mc','htop','btm','bottom','procs','duf','dust','bat','exa','lsd','fd','fzf','ripgrep','delta','tig','lazygit','tokei','hyperfine','just','watchexec','entr']
    for t in tools:
        entries.append(cmd(f'{t} --version', f'{t} v1.0 (FusionOS)', f'Tool - {t}'))
    
    final_count = len([e for e in entries if not e.startswith('  /*')])
    print(f"  Final command count: {final_count}")
    return entries

print("=== BUILDING 1200 TERMINAL COMMANDS ===")
cmd_entries = build_1200_commands()

# ─────────────────────────────────────────────────
# PART 2: Generate 890 Features
# ─────────────────────────────────────────────────

print("\n=== BUILDING 890 FEATURES ===")

def build_features():
    """Build 890 features as IIFE blocks"""
    f = []
    base_num = 173  # Continue from 172
    
    # Helper for standard features
    def add_feat(num, code, comment):
        f.append(f"/* ── {num}. {comment} ── */")
        f.append(f"(function(){{{code}}})();")
    
    # Helper for toast features
    def toast_feat(num, title, msg):
        add_feat(num, f"showToast('info','{title}','{msg}');", title)
    
    # --- Window Management (30 features) ---
    idx = base_num
    win_feats = [
        ("Snap window to left", "window.snapLeft=function(id){{var w=windows[id];if(w){{w.el.style.left='0';w.el.style.top='0';w.el.style.width='50vw';w.el.style.height='100vh';}}}};window.snapLeft=window.snapLeft;"),
        ("Snap window to right", "window.snapRight=function(id){{var w=windows[id];if(w){{w.el.style.left='50vw';w.el.style.top='0';w.el.style.width='50vw';w.el.style.height='100vh';}}}};window.snapRight=window.snapRight;"),
        ("Snap window to top", "window.snapTop=function(id){var w=windows[id];if(w){w.el.style.left='0';w.el.style.top='0';w.el.style.width='100vw';w.el.style.height='50vh';}};"),
        ("Snap window to bottom", "window.snapBottom=function(id){var w=windows[id];if(w){w.el.style.left='0';w.el.style.top='50vh';w.el.style.width='100vw';w.el.style.height='50vh';}};"),
        ("Snap window to center", "window.snapCenter=function(id){var w=windows[id];if(w){w.el.style.left='25vw';w.el.style.top='15vh';w.el.style.width='50vw';w.el.style.height='70vh';}};"),
        ("Cascade all windows", "window.cascadeAll=function(){var ks=Object.keys(windows),t=40,l=40;ks.forEach(function(k,i){var w=windows[k];if(w&&w.el){w.el.style.left=(l+i*30)+'px';w.el.style.top=(t+i*30)+'px';}});};"),
        ("Tile all windows horizontally", "window.tileHorizontal=function(){var ks=Object.keys(windows),n=ks.length;if(!n)return;var h=100/n;ks.forEach(function(k,i){var w=windows[k];if(w&&w.el){w.el.style.left='0';w.el.style.top=(i*h)+'vh';w.el.style.width='100vw';w.el.style.height=h+'vh';}});};"),
        ("Tile all windows vertically", "window.tileVertical=function(){var ks=Object.keys(windows),n=ks.length;if(!n)return;var ww=100/n;ks.forEach(function(k,i){var w=windows[k];if(w&&w.el){w.el.style.left=(i*ww)+'vw';w.el.style.top='0';w.el.style.width=ww+'vw';w.el.style.height='100vh';}});};"),
        ("Minimize all windows", "window.minimizeAll=function(){Object.keys(windows).forEach(function(k){var w=windows[k];if(w&&w.el)w.el.style.display='none';});};"),
        ("Restore all windows", "window.restoreAll=function(){Object.keys(windows).forEach(function(k){var w=windows[k];if(w&&w.el)w.el.style.display='';});};"),
        ("Close all windows", "window.closeAll=function(){Object.keys(windows).forEach(function(k){closeWindow(k);});};"),
        ("Bring all windows to front", "window.bringAllToFront=function(){Object.keys(windows).forEach(function(k){var w=windows[k];if(w&&w.el){w.el.style.zIndex=++zIndex;}});};"),
        ("Arrange in grid", "window.arrangeGrid=function(){var ks=Object.keys(windows),n=ks.length;if(!n)return;var cols=Math.ceil(Math.sqrt(n)),cw=100/cols,ch=100/Math.ceil(n/cols);ks.forEach(function(k,i){var w=windows[k];if(w&&w.el){w.el.style.left=(i%cols*cw)+'vw';w.el.style.top=(Math.floor(i/cols)*ch)+'vh';w.el.style.width=cw+'vw';w.el.style.height=ch+'vh';}});};"),
        ("Set window opacity", "window.setOpacity=function(id,val){var w=windows[id];if(w&&w.el)w.el.style.opacity=Math.max(0.1,Math.min(1,val));};"),
        ("Toggle window always on top", "window.alwaysOnTop=function(id){var w=windows[id];if(w&&w.el){w._onTop=!w._onTop;w.el.style.zIndex=w._onTop?99999:++zIndex;showToast('ok','\\u7f6e\\u9876',w._onTop?'\\u5df2\\u7f6e\\u9876':'\\u5df2\\u53d6\\u6d88');}};"),
        ("Lock window position", "window.lockPos=function(id){var w=windows[id];if(w&&w.el){w._locked=!w._locked;w.el.style.pointerEvents=w._locked?'none':'';showToast('ok','\\u9501\\u5b9a',w._locked?'\\u5df2\\u9501\\u5b9a\\u4f4d\\u7f6e':'\\u5df2\\u89e3\\u9501');}};"),
        ("Resize window to preset", "window.resizeTo=function(id,w,h){var win=windows[id];if(win&&win.el){win.el.style.width=w+'px';win.el.style.height=h+'px';}};"),
        ("Move window to position", "window.moveTo=function(id,x,y){var win=windows[id];if(win&&win.el){win.el.style.left=x+'px';win.el.style.top=y+'px';}};"),
        ("Focus next window", "window.focusNext=function(){var ks=Object.keys(windows),idx=ks.indexOf(focusedWin);var next=ks[(idx+1)%ks.length];if(windows[next])focusWindow(next);};"),
        ("Focus previous window", "window.focusPrev=function(){var ks=Object.keys(windows),idx=ks.indexOf(focusedWin);var prev=ks[(idx-1+ks.length)%ks.length];if(windows[prev])focusWindow(prev);};"),
        ("Toggle fullscreen", "window.toggleFS=function(id){var w=windows[id];if(w&&w.el){var fs=w.el.style.width==='100vw';w.el.style.left=fs?'100px':'0';w.el.style.top=fs?'100px':'0';w.el.style.width=fs?'600px':'100vw';w.el.style.height=fs?'400px':'100vh';}};"),
        ("Shake window", "window.shake=function(id){var w=windows[id];if(!w||!w.el)return;var el=w.el,x=0,orig=el.style.transform||'';var int=setInterval(function(){x=(x+8)%16-8;el.style.transform='translateX('+x+'px)';},30);setTimeout(function(){clearInterval(int);el.style.transform=orig;},300);};"),
        ("Pulse window border", "window.pulse=function(id){var w=windows[id];if(!w||!w.el)return;var el=w.el,orig=el.style.boxShadow||'',i=0;var int=setInterval(function(){el.style.boxShadow='0 0 '+(10+Math.sin(i)*10)+'px var(--accent)';i+=0.3;},50);setTimeout(function(){clearInterval(int);el.style.boxShadow=orig;},800);};"),
        ("Minimize to tray", "window.minToTray=function(id){var w=windows[id];if(w&&w.el){w._minToTray=!w._minToTray;w.el.style.display=w._minToTray?'none':'';showToast('ok','\\u6258\\u76d8',w._minToTray?'\\u5df2\\u6700\\u5c0f\\u5316\\u5230\\u6258\\u76d8':'\\u5df2\\u6062\\u590d');}};"),
        ("Show window thumbnails", "window.showThumbs=function(){var html='<div style=position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);z-index:99999;display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:20px;padding:40px>';Object.keys(windows).forEach(function(k){if(windows[k])html+='<div style=background:var(--bg-primary);border-radius:12px;padding:10px;cursor:pointer;min-width:200px onclick=\"focusWindow(\\''+k+'\\');this.parentElement.remove()\"><div style=font-size:12px;text-align:center>'+windows[k].title+'</div></div>';});html+='</div>';var ov=document.createElement('div');ov.innerHTML=html;ov.onclick=function(e){if(e.target===ov)ov.remove();};document.body.appendChild(ov);};"),
        ("Window switcher Alt+Tab style", "window.switcher=function(){var ks=Object.keys(windows);if(!ks.length)return;var html='<div id=switcher-ov style=position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.4);z-index:99999;display:flex;align-items:center;justify-content:center><div style=background:var(--bg-primary);border-radius:16px;padding:24px;max-width:600px;display:flex;flex-wrap:wrap;gap:12px>';ks.forEach(function(k,i){var w=windows[k];html+='<div onclick=\"focusWindow(\\''+k+'\\');document.getElementById(\\'switcher-ov\\').remove()\" style=padding:12px 20px;background:'+(focusedWin===k?'var(--accent)':'var(--bg-secondary)')+';border-radius:8px;cursor:pointer;font-size:14px>'+w.title+'</div>';});html+='</div></div>';document.body.insertAdjacentHTML('beforeend',html);};"),
        ("Quick layout save", "window.saveLayout=function(){var layout={};Object.keys(windows).forEach(function(k){var w=windows[k];if(w&&w.el){layout[k]={left:w.el.style.left,top:w.el.style.top,width:w.el.style.width,height:w.el.style.height,appId:w.appId};}});localStorage.setItem('fus-layout',JSON.stringify(layout));showToast('ok','\\u5e03\\u5c40','\\u5df2\\u4fdd\\u5b58\\u5f53\\u524d\\u5e03\\u5c40');};"),
        ("Quick layout restore", "window.restoreLayout=function(){var layout=localStorage.getItem('fus-layout');if(!layout)return showToast('warn','\\u5e03\\u5c40','\\u6ca1\\u6709\\u4fdd\\u5b58\\u7684\\u5e03\\u5c40');layout=JSON.parse(layout);Object.keys(layout).forEach(function(k){if(!windows[k])openApp(layout[k].appId);setTimeout(function(){if(windows[k]&&windows[k].el){var l=layout[k];windows[k].el.style.left=l.left;windows[k].el.style.top=l.top;windows[k].el.style.width=l.width;windows[k].el.style.height=l.height;}},100);});showToast('ok','\\u5e03\\u5c40','\\u5df2\\u6062\\u590d\\u5e03\\u5c40');};"),
        ("Toggle window decorations", "window.toggleDeco=function(id){var w=windows[id];if(!w||!w.el)return;var h=w.el.querySelector('.win-header');if(h)h.style.display=h.style.display==='none'?'':'none';};"),
        ("Rotate window layout", "window.rotateLayout=function(){var ks=Object.keys(windows);if(!ks.length)return;var first=windows[ks[0]],last=windows[ks[ks.length-1]];if(!first||!last||!first.el||!last.el)return;var fl=first.el.style.left,ft=first.el.style.top,fw=first.el.style.width,fh=first.el.style.height;for(var i=0;i<ks.length-1;i++){var a=windows[ks[i]],b=windows[ks[i+1]];if(a&&a.el&&b&&b.el){a.el.style.left=b.el.style.left;a.el.style.top=b.el.style.top;a.el.style.width=b.el.style.width;a.el.style.height=b.el.style.height;}}if(last){last.el.style.left=fl;last.el.style.top=ft;last.el.style.width=fw;last.el.style.height=fh;}};"),
    ]
    for comment, code in win_feats:
        add_feat(idx, code, comment)
        idx += 1
    
    # --- System Tools (25 features) ---
    sys_feats = [
        ("System info panel", "window.showSysInfo=function(){var m=performance.memory||{},s=navigator.hardwareConcurrency||'?';var info='CPU Cores: '+s+'\\nMemory: '+(m.jsHeapSizeLimit?Math.round(m.jsHeapSizeLimit/1048576)+'MB':'N/A')+'\\nOnline: '+navigator.onLine+'\\nPlatform: '+navigator.platform+'\\nResolution: '+screen.width+'x'+screen.height+'\\nColor Depth: '+screen.colorDepth+'bit';showToast('info','\\u7cfb\\u7edf\\u4fe1\\u606f',info.replace(/\\n/g,'<br>'));};"),
        ("Memory usage gauge", "window.memGauge=function(){var m=(performance.memory||{}).usedJSHeapSize||0,limit=(performance.memory||{}).jsHeapSizeLimit||1;var pct=Math.round(m/limit*100);showToast('info','\\u5185\\u5b58',pct+'% used ('+Math.round(m/1048576)+'MB / '+Math.round(limit/1048576)+'MB)');};"),
        ("Toggle performance monitor", "window.togglePerfMon=function(){var el=document.getElementById('perf-mon');if(el){el.remove();return;}el=document.createElement('div');el.id='perf-mon';el.style.cssText='position:fixed;top:10px;right:10px;background:rgba(0,0,0,0.8);color:#0f0;padding:8px 12px;border-radius:8px;font:12px monospace;z-index:99999';document.body.appendChild(el);var fps=0,last=performance.now(),frames=0;function tick(){frames++;var now=performance.now();if(now-last>=1000){fps=Math.round(frames/((now-last)/1000));frames=0;last=now;var m=(performance.memory||{}).usedJSHeapSize||0;el.textContent='FPS: '+fps+' | Mem: '+Math.round(m/1048576)+'MB | Win: '+Object.keys(windows||{}).length;}requestAnimationFrame(tick);}tick();};"),
        ("CPU stress test", "window.cpuStress=function(){showToast('info','CPU Stress','Running stress test...');var start=performance.now(),n=0;while(performance.now()-start<3000){n+=Math.sqrt(Math.random());}showToast('ok','CPU Stress','Completed '+Math.round(n)+' ops in 3s');};"),
        ("Network speed test", "window.netSpeedTest=function(){var start=performance.now();var img=new Image();img.onload=function(){var dur=performance.now()-start;var speed=Math.round(500/(dur/1000));showToast('ok','\\u7f51\\u901f',speed+' KB/s (simulated)');};img.onerror=function(){showToast('ok','\\u7f51\\u901f','~500 KB/s (estimated)');};img.src='https://www.google.com/favicon.ico?'+Date.now();};"),
        ("Clear browser cache hint", "window.clearCache=function(){if(confirm('Clear all cached data?')){localStorage.clear();sessionStorage.clear();showToast('ok','\\u7f13\\u5b58','\\u5df2\\u6e05\\u9664\\u6240\\u6709\\u7f13\\u5b58');}};"),
        ("Export system log", "window.exportLog=function(){var log=[];Object.keys(localStorage).forEach(function(k){log.push(k+': '+localStorage.getItem(k).substring(0,50));});var blob=new Blob([log.join('\\n')],{type:'text/plain'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='fusion-log-'+Date.now()+'.txt';a.click();showToast('ok','\\u65e5\\u5fd7','\\u5df2\\u5bfc\\u51fa\\u65e5\\u5fd7');};"),
        ("Import settings", "window.importSettings=function(){var input=document.createElement('input');input.type='file';input.accept='.json';input.onchange=function(e){var f=e.target.files[0];if(!f)return;var r=new FileReader();r.onload=function(ev){try{var data=JSON.parse(ev.target.result);Object.keys(data).forEach(function(k){localStorage.setItem(k,data[k]);});showToast('ok','\\u8bbe\\u7f6e','\\u5df2\\u5bfc\\u5165\\u8bbe\\u7f6e');location.reload();}catch(ex){showToast('err','\\u8bbe\\u7f6e','\\u5bfc\\u5165\\u5931\\u8d25');}};r.readAsText(f);};input.click();};"),
        ("Export settings", "window.exportSettings=function(){var data={};Object.keys(localStorage).forEach(function(k){if(k.startsWith('fus-'))data[k]=localStorage.getItem(k);});var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='fusion-settings-'+Date.now()+'.json';a.click();showToast('ok','\\u8bbe\\u7f6e','\\u5df2\\u5bfc\\u51fa\\u8bbe\\u7f6e');};"),
        ("System uptime display", "window.showUptime=function(){var t=performance.now();var d=Math.floor(t/86400000),h=Math.floor((t%86400000)/3600000),m=Math.floor((t%3600000)/60000),s=Math.floor((t%60000)/1000);showToast('info','\\u8fd0\\u884c\\u65f6\\u95f4',d+'d '+h+'h '+m+'m '+s+'s');};"),
        ("Battery status", "window.batteryStatus=function(){if(navigator.getBattery){navigator.getBattery().then(function(b){showToast('info','\\u7535\\u6c60','Level: '+Math.round(b.level*100)+'% | Charging: '+(b.charging?'Yes':'No'));});}else{showToast('info','\\u7535\\u6c60','Not supported on this device');}};"),
        ("Clipboard reader", "window.clipboardRead=function(){if(navigator.clipboard&&navigator.clipboard.readText){navigator.clipboard.readText().then(function(t){showToast('info','\\u526a\\u8d34\\u677f',t||'(empty)');}).catch(function(){showToast('warn','\\u526a\\u8d34\\u677f','Permission denied');});}else{showToast('info','\\u526a\\u8d34\\u677f','Not supported');}};"),
        ("Open link in new tab", "window.openLink=function(url){window.open(url||'https://www.google.com','_blank');showToast('ok','\\u94fe\\u63a5','\\u5df2\\u5728\\u65b0\\u6807\\u7b7e\\u9875\\u6253\\u5f00');};"),
        ("Color picker tool", "window.colorPicker=function(){var c=document.createElement('input');c.type='color';c.onchange=function(){navigator.clipboard.writeText(c.value).then(function(){showToast('ok','\\u989c\\u8272',c.value+' \\u5