#!/usr/bin/env python3
"""FusionOS 8.0 — Part 1: Generate 1200 terminal commands"""
import re

HTML_PATH = '/Users/murderdrones/Desktop/FusionOS.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Find termExec O dictionary boundaries
t1 = html.find('function termExec(cmd,id){')
t2 = html.find('var O={};', t1)
t3 = html.find('var fn=O[c];', t2)
print(f'O dict: chars {t2} to {t3} ({t3-t2} chars)')

def esc(s):
    """Full JS single-quoted string escape"""
    return s.encode('unicode_escape').decode('ascii').replace("'", "\\'")

def cmd(name, output, comment=''):
    safe_name = name.replace("'", "\\'")
    c = f"  O['{safe_name}']=function(){{return'{esc(output)}';}};"
    if comment:
        c = f"  /* {comment} */\n" + c
    return c + "\n"

entries = []

# ── Category generators ──
def add_cmds(cat, items):
    entries.append(f"  /* ── {cat} ── */")
    for name, out, *rest in items:
        cmt = rest[0] if rest else ''
        entries.append(cmd(name, out, cmt))

# System Info
add_cmds("System Info", [
    ('uname','FusionOS 8.0 kernel fusion-8.0.0 x86_64'),
    ('uname -a','FusionOS 8.0 hostname fusion-8.0.0 #1 SMP x86_64 GNU/Fusion'),
    ('uname -r','fusion-8.0.0'),
    ('uname -s','FusionOS'),
    ('uname -m','x86_64'),
    ('hostname','fusion-desktop'),
    ('hostname -i','127.0.0.1'),
    ('arch','x86_64'),
    ('lscpu',esc('CPU(s): 16 | Model: Fusion Virtual @ 3.20GHz | Cache: 8192KB')),
    ('uptime',esc('02:00:41 up 3 days, load average: 0.08, 0.12, 0.09')),
    ('uptime -p','up 3 days, 7 hours, 22 minutes'),
    ('whoami','user'),
    ('who','user console Jun 12 18:38'),
    ('id','uid=1000(user) gid=1000(user) groups=1000(user),4(adm),27(sudo)'),
    ('env',esc('USER=user\nHOME=/home/user\nSHELL=/bin/fsh\nPATH=/usr/local/bin:/usr/bin:/bin\nFUSION_VERSION=8.0')),
    ('printenv','FUSION_VERSION=8.0\nHOME=/home/user\nPATH=/usr/bin:/bin'),
    ('date','Tue Jun 16 02:00:41 CST 2026'),
    ('date +%Y-%m-%d','2026-06-16'),
    ('date +%H:%M:%S','02:00:41'),
    ('cal','June 2026\nSu Mo Tu We Th Fr Sa\n    1  2  3  4  5  6\n 7  8  9 10 11 12 13\n14 15 16 17 18 19 20\n21 22 23 24 25 26 27\n28 29 30'),
    ('nproc','16'),
    ('nproc --all','16'),
    ('getconf LONG_BIT','64'),
    ('locale','LANG=zh_CN.UTF-8\nLC_CTYPE=zh_CN.UTF-8\nLC_ALL='),
    ('locale -a','C\nC.UTF-8\nen_US.utf8\nzh_CN.utf8\nja_JP.utf8'),
    ('timedatectl',esc('Local: Tue 2026-06-16 02:00:41 CST\nTimezone: Asia/Shanghai (CST, +0800)')),
    ('sysctl -a',esc('kernel.hostname=fusion-desktop\nkernel.version=8.0.0\nnet.ipv4.tcp_syncookies=1')),
    ('lsmod',esc('Module Size Used by\nfusion_core 262144 1\nfusion_display 98304 2\nfusion_net 65536 0')),
    ('dmesg',esc('[0.00] FusionOS 8.0 booting\n[0.10] CPU: x86_64 (16 cores)\n[0.20] Memory: 16384MB\n[1.00] Boot complete.')),
    ('lscpu',esc('Arch: x86_64\nCPU(s): 16\nThreads/core: 2\nCores/socket: 8\nSocket: 1\nModel: Fusion Virtual @ 3.20GHz')),
    ('lspci',esc('00:00.0 Host bridge\n00:01.0 VGA controller\n00:02.0 Network\n00:03.0 Audio\n00:04.0 USB')),
    ('lsusb',esc('Bus 001 Device 001: ID 1d6b:0002\nBus 002 Device 001: ID 1d6b:0003')),
    ('lsblk',esc('NAME SIZE TYPE MOUNTPOINT\nsda 256G disk\n├─sda1 512M /boot\n├─sda2 200G /\n└─sda3 56G /home')),
])

# System Monitoring
add_cmds("Monitoring", [
    ('top -b -n 1',esc('PID USER %CPU %MEM COMMAND\n1 user 0.0 0.1 fusion-init\n234 user 2.1 1.2 fusion-shell\n567 user 0.5 0.3 terminal')),
    ('free',esc('total used free shared buff/cache available\nMem: 16384000 2015488 12285440 98304 2083072 14368512\nSwap: 8388608 0 8388608')),
    ('free -h',esc('total used free shared buff/cache available\nMem: 16Gi 1.9Gi 11.7Gi 96Mi 2.0Gi 13.7Gi\nSwap: 8.0Gi 0B 8.0Gi')),
    ('free -m',esc('Mem: 16000 1968 11997 96 2035 14032\nSwap: 8192 0 8192')),
    ('vmstat',esc('r b swpd free buff cache si so bi bo in cs us sy id wa\n0 0 0 11.7G 0.5G 1.5G 0 0 2 1 23 15 2 1 96 1')),
    ('iostat',esc('avg-cpu: %user 2.1 %nice 0.0 %sys 1.2 %iowait 0.8 %idle 95.9\nDevice tps kB_read/s kB_wrtn/s\nsda 3.20 12.40 25.60')),
    ('mpstat',esc('CPU %usr %nice %sys %iowait %irq %soft %idle\nall 2.10 0.00 1.20 0.80 0.00 0.00 95.90')),
    ('pidstat',esc('PID %usr %system %CPU Command\n234 1.20 0.80 2.00 fusion-shell\n567 0.20 0.30 0.50 terminal')),
    ('sar',esc('12:00:01 CPU %user %nice %system %iowait %idle\n12:10:01 all 2.10 0.00 1.20 0.80 95.90')),
    ('sar -u 1 3','Average: all 2.10 0.00 1.20 0.80 0.00 95.90'),
    ('dstat',esc('usr sys idl wai hiq siq| read writ| recv send| in out | int csw\n2 1 96 1 0 0| 12k 25k| 0 0| 0 0| 23 15')),
    ('lsof',esc('COMMAND PID USER FD TYPE DEVICE SIZE NODE NAME\nterm 567 user cwd DIR 8,2 4096 2 /')),
    ('pgrep term','567'),
    ('pidof term','567'),
    ('ps aux',esc('USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND\nuser 567 0.1 0.3 8192 4096 pts/0 Ss 02:00 0:00 term')),
    ('ps -ef',esc('UID PID PPID C STIME TTY TIME CMD\nuser 567 234 0 02:00 pts/0 00:00:00 term')),
    ('pstree',esc('systemd──fusion-init──fusion-shell──term──sh')),
])

# File System
add_cmds("File System", [
    ('ls','Documents  Downloads  Music  Pictures  Videos  desktop.ini'),
    ('ls -l',esc('total 24\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Documents\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Downloads')),
    ('ls -la',esc('total 32\ndrwxr-xr-x 6 user user 4096 Jun 16 02:00 .\n-rw-r--r-- 1 user user 220 Jun 12 18:38 .bashrc\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Documents')),
    ('ls -lh',esc('total 24K\ndrwxr-xr-x 2 user user 4.0K Jun 16 02:00 Documents')),
    ('ls -R',esc('.:\nDocuments Downloads Music\n./Documents:\nnotes.txt report.pdf')),
    ('ls -1','Documents\nDownloads\nMusic\nPictures\nVideos'),
    ('ls -F','Documents/  Downloads/  Music/  Pictures/  Videos/'),
    ('ll',esc('total 24\ndrwxr-xr-x 2 user user 4096 Jun 16 02:00 Documents')),
    ('pwd','/home/user'),
    ('mkdir newfolder',esc('已创建目录: newfolder')),
    ('mkdir -p a/b/c',esc('已递归创建: a/b/c')),
    ('touch file.txt',esc('已创建文件: file.txt')),
    ('cp file1.txt file2.txt',esc('已复制: file1.txt → file2.txt')),
    ('cp -r dir1 dir2',esc('已递归复制: dir1 → dir2')),
    ('mv old.txt new.txt',esc('已移动/重命名: old.txt → new.txt')),
    ('rm file.txt',esc('已删除: file.txt')),
    ('rm -rf old_dir',esc('已递归强制删除: old_dir')),
    ('ln -s target link',esc('已创建符号链接: link → target')),
    ('stat file.txt',esc('File: file.txt Size: 1024 Access: (0644/-rw-r--r--) Uid: (1000/user)\nAccess: 2026-06-16 02:00 Modify: 2026-06-15 18:30')),
    ('file file.txt','file.txt: ASCII text'),
    ('which python3','/usr/bin/python3'),
    ('whereis ls','ls: /bin/ls /usr/share/man/man1/ls.1.gz'),
    ('type ls','ls is aliased to `ls --color=auto`'),
    ('du -sh','2.0G .'),
    ('du -sh *',esc('4.0K Documents\n1.5G Downloads\n500M Music')),
    ('df -h',esc('Filesystem Size Used Avail Use% Mounted on\n/dev/sda2 200G 40G 160G 20% /\n/dev/sda1 512M 100M 412M 20% /boot')),
    ('df -i',esc('Filesystem Inodes IUsed IFree IUse% Mounted on\n/dev/sda2 13.1M 256K 12.9M 2% /')),
    ('mount',esc('/dev/sda2 on / type ext4 (rw,relatime)\ntmpfs on /tmp type tmpfs (rw,nosuid)')),
])

# Process Management
add_cmds("Process Management", [
    ('kill -l',esc('1) SIGHUP 2) SIGINT 3) SIGQUIT 4) SIGILL 5) SIGTRAP\n6) SIGABRT 7) SIGBUS 8) SIGFPE 9) SIGKILL 10) SIGUSR1')),
    ('jobs','[1] Running nohup command &'),
    ('fg',esc('已将后台作业调到前台')),
    ('bg',esc('已将作业调到后台')),
    ('nohup command &',esc('已在后台运行 command (忽略 SIGHUP)')),
    ('nice -n 10 command',esc('已以优先级 10 运行 command')),
    ('renice 10 -p 567','567 (process ID) old priority 0, new priority 10'),
    ('time ls',esc('Documents Downloads Music\nreal 0m0.003s user 0m0.001s sys 0m0.001s')),
    ('sleep 1',esc('等待 1 秒...')),
    ('yes hello',esc('hello\nhello\n... (已终止)')),
    ('echo hello | xargs','hello'),
    ('seq 1 5 | xargs','1 2 3 4 5'),
])

# Text Processing (generated in loops for volume)
text_manual = [
    ('cat file.txt','Hello World!\nThis is a test file.\nLine 3.\nEnd.'),
    ('cat -n file.txt',esc('     1\tHello World!\n     2\tThis is a test file.\n     3\tLine 3.\n     4\tEnd.')),
    ('tac file.txt','End.\nLine 3.\nThis is a test file.\nHello World!'),
    ('head file.txt',esc('Hello World!\nThis is a test file.\nLine 3.')),
    ('head -n 2 file.txt',esc('Hello World!\nThis is a test file.')),
    ('tail file.txt',esc('Line 3.\nEnd.')),
    ('tail -n 2 file.txt',esc('Line 3.\nEnd.')),
    ('tail -f file.log',esc('实时跟踪文件变化...')),
    ('wc file.txt','4 15 98 file.txt'),
    ('wc -l file.txt','4 file.txt'),
    ('wc -w file.txt','15 file.txt'),
    ('wc -c file.txt','98 file.txt'),
    ('sort file.txt',esc('End.\nHello World!\nLine 3.\nThis is a test file.')),
    ('sort -r file.txt',esc('This is a test file.\nLine 3.\nHello World!\nEnd.')),
    ('sort -n numbers.txt',esc('1\n2\n10\n20\n100')),
    ('sort -u file.txt',esc('去重排序')),
    ('uniq file.txt',esc('Hello World!\nThis is a test file.\nLine 3.')),
    ('uniq -c file.txt',esc('2 Hello World!\n1 This is a test file.\n1 Line 3.')),
    ('uniq -d file.txt','Hello World!'),
    ('cut -d, -f1 data.csv',esc('Name\nAlice\nBob\nCharlie')),
    ('cut -c 1-5 file.txt',esc('Hello\nThis\nLine\nEnd o')),
    ('paste file1.txt file2.txt',esc('Hello\tWorld\nLine1\tLine2')),
    ('join file1.txt file2.txt',esc('关联合并两个文件')),
    ('tr a-z A-Z < file.txt',esc('HELLO WORLD!\nTHIS IS A TEST FILE.')),
    ('tr -d "\\n" < file.txt',esc('删除所有换行符')),
    ('tee output.txt',esc('(输入已写入 output.txt)')),
    ("sed 's/old/new/' file.txt",esc('替换第一个 old 为 new')),
    ("sed 's/old/new/g' file.txt",esc('全局替换 old 为 new')),
    ("sed '/pattern/d' file.txt",esc('删除匹配行')),
    ("sed -n '5,10p' file.txt",esc('显示 5-10 行')),
    ("awk '{print $1}' file.txt",esc('打印第1列')),
    ("awk '{print $NF}' file.txt",esc('打印最后一列')),
    ("awk -F, '{print $2}' data.csv",esc('以逗号分割，打印第2列')),
    ("awk 'NR==2' file.txt",esc('打印第2行')),
    ("awk '{sum+=$1} END {print sum}' nums.txt",esc('求和')),
    ('grep "hello" file.txt','Hello World!\nhello there'),
    ('grep -i "hello" file.txt','Hello World!\nhello there\nHELLO EVERYONE'),
    ('grep -v "hello" file.txt',esc('反向匹配')),
    ('grep -c "hello" file.txt','3'),
    ('grep -n "hello" file.txt','1:Hello World!\n5:hello there'),
    ('grep -r "TODO" .',esc('./src/main.js: // TODO: implement\n./README.md: # TODO list')),
    ('grep -l "hello" *.txt','file1.txt\nfile2.txt'),
    ('grep -w "hello" file.txt',esc('全词匹配')),
    ('grep -E "hello|world" file.txt',esc('正则表达式')),
    ('grep -A 2 "hello" file.txt',esc('显示匹配行及后2行')),
    ('grep -B 2 "hello" file.txt',esc('显示匹配行及前2行')),
    ('grep -C 2 "hello" file.txt',esc('显示匹配行及前后各2行')),
    ('diff file1.txt file2.txt',esc('1c1\n< Hello World!\n---\n> Hello Universe!')),
    ('diff -u file1.txt file2.txt',esc('--- file1.txt\n+++ file2.txt\n@@ -1 +1 @@\n-Hello World!\n+Hello Universe!')),
    ('diff -r dir1 dir2',esc('递归比较目录')),
    ('base64 file.txt','SGVsbG8gV29ybGQhCg=='),
    ('base64 -d <<< SGVsbG8=','Hello'),
    ('xxd file.txt','00000000: 4865 6c6c 6f20 576f 726c 6421 0a  Hello World!.'),
    ('hexdump -C file.txt','00000000  48 65 6c 6c 6f 20 57 6f 72 6c 64 21 0a  |Hello World!.|'),
    ('od -c file.txt','0000000   H   e   l   l   o       W   o   r   l   d   !  \\n'),
    ('strings /bin/ls','/lib64/ld-linux-x86-64.so.2\nlibc.so.6'),
]
add_cmds("Text Processing", text_manual)

# Network
net_cmds = [
    ('ping localhost',esc('PING localhost (127.0.0.1): 56 bytes\n64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.050 ms\n--- 2 packets transmitted, 2 received, 0% loss')),
    ('ping -c 4 8.8.8.8',esc('PING 8.8.8.8: 56 bytes\n64 bytes from 8.8.8.8: seq=0 ttl=118 time=12.3 ms\n--- 4 packets transmitted, 4 received, 0% loss')),
    ('traceroute 8.8.8.8',esc('traceroute to 8.8.8.8, 30 hops max\n1 192.168.1.1 1.234 ms\n2 10.0.0.1 5.678 ms\n3 8.8.8.8 12.345 ms')),
    ('netstat -tuln',esc('Proto Local Address State\ntcp 0.0.0.0:80 LISTEN\ntcp 127.0.0.1:3306 LISTEN\nudp 0.0.0.0:5353')),
    ('netstat -r',esc('Destination Gateway Genmask Flags Iface\ndefault 192.168.1.1 0.0.0.0 UG eth0\n192.168.1.0 0.0.0.0 255.255.255.0 U eth0')),
    ('ss -tuln',esc('显示 TCP/UDP 监听端口')),
    ('ss -s',esc('Total: 45 TCP: 12 (estab 3, closed 5, listen 4)\nUDP: 8 TCP: 12')),
    ('ip addr',esc('1: lo: <LOOPBACK,UP> mtu 65536 inet 127.0.0.1/8\n2: eth0: <BROADCAST,MULTICAST,UP> mtu 1500 inet 192.168.1.100/24')),
    ('ip link',esc('1: lo: <LOOPBACK,UP> mtu 65536\n2: eth0: <BROADCAST,MULTICAST,UP> mtu 1500')),
    ('ip route',esc('default via 192.168.1.1 dev eth0\n192.168.1.0/24 dev eth0 proto kernel')),
    ('ifconfig',esc('eth0: flags=4163<UP,BROADCAST,RUNNING> mtu 1500\ninet 192.168.1.100 netmask 255.255.255.0')),
    ('arp -a',esc('? (192.168.1.1) at 00:11:22:33:44:55 [ether] on eth0')),
    ('route -n',esc('0.0.0.0 192.168.1.1 0.0.0.0 UG 100 eth0\n192.168.1.0 0.0.0.0 255.255.255.0 U 100 eth0')),
    ('nslookup google.com',esc('Server: 8.8.8.8\nAddress: 8.8.8.8#53\nName: google.com\nAddress: 142.250.80.46')),
    ('dig google.com',esc(';; ANSWER SECTION:\ngoogle.com. 300 IN A 142.250.80.46')),
    ('dig +short google.com','142.250.80.46'),
    ('host google.com','google.com has address 142.250.80.46'),
    ('hostname -I','192.168.1.100'),
    ('curl http://localhost','<html><body><h1>It works!</h1></body></html>'),
    ('curl -I http://localhost',esc('HTTP/1.1 200 OK\nServer: nginx/1.18.0\nContent-Type: text/html')),
    ('curl -X POST http://localhost',esc('发送 POST 请求')),
    ('curl -L http://short.url',esc('跟随重定向')),
    ('curl -v http://localhost',esc('* Connected to localhost (127.0.0.1) port 80\n> GET / HTTP/1.1\n< HTTP/1.1 200 OK')),
    ('curl -s http://localhost',esc('安静模式(不显示进度)')),
    ('wget http://localhost',esc('--2026-06-16 02:00:41-- http://localhost/\nResolving localhost... 127.0.0.1\nHTTP request sent... 200 OK\nSaving to: index.html\n2026-06-16 02:00:41 - index.html saved [42/42]')),
    ('wget -O output.html http://localhost',esc('保存为 output.html')),
    ('wget -q http://localhost',esc('安静模式')),
    ('nc -l 8080',esc('监听 8080 端口...')),
    ('nc -v localhost 80','Connection to localhost 80 port [tcp/http] succeeded!'),
    ('nc -z localhost 1-100',esc('端口扫描 1-100')),
    ('nmap localhost',esc('PORT STATE SERVICE\n80/tcp open http\nNmap done: 1 IP scanned in 0.03s')),
    ('nmap -sV localhost',esc('版本检测')),
    ('rsync -av src/ dst/',esc('sending incremental file list\nfile.txt\nsent 1234 bytes received 56 bytes')),
    ('tcpdump -i eth0',esc('listening on eth0\n02:00:41 IP 192.168.1.100.54321 > 8.8.8.8.53: UDP, length 64')),
]
add_cmds("Network Tools", net_cmds)

# Git
git_cmds = [
    ('git init','Initialized empty Git repository in /home/user/project/.git/'),
    ('git clone https://github.com/user/repo.git',esc("Cloning into 'repo'...\nReceiving objects: 100% (123/123), 45.67 KiB, done.")),
    ('git status',esc('On branch main\nChanges not staged for commit:\n  modified: README.md')),
    ('git status -s',' M README.md\n?? newfile.txt'),
    ('git add .',esc('已添加所有文件到暂存区')),
    ("git commit -m 'Initial commit'",esc('[main (root-commit) abc1234] Initial commit\n1 file changed, 10 insertions(+)')),
    ("git commit -am 'Update'",esc('[main def5678] Update\n1 file changed, 2 insertions(+), 1 deletion(-)')),
    ('git commit --amend',esc('修改上次提交')),
    ('git log',esc('commit abc1234 (HEAD -> main)\nAuthor: User <user@fusion.dev>\nDate: Tue Jun 16 2026\n    Initial commit')),
    ('git log --oneline','abc1234 Initial commit\ndef5678 Add README\nghi9012 Fix bug'),
    ('git log --graph',esc('* abc1234 (HEAD -> main) Initial commit\n* def5678 Add README')),
    ('git diff',esc('--- a/README.md\n+++ b/README.md\n@@ -1 +1 @@\n-# Old\n+# New')),
    ('git diff --staged',esc('显示暂存区差异')),
    ('git branch','* main'),
    ('git branch feature',esc('已创建分支 feature')),
    ('git branch -d feature',esc('已删除分支 feature')),
    ('git checkout -b feature',esc('Switched to a new branch feature')),
    ('git checkout main','Switched to branch main'),
    ('git switch feature','Switched to branch feature'),
    ('git merge feature',esc('Updating abc..def\nFast-forward\n file.txt | 5 +\n 1 file changed, 5 insertions(+)')),
    ('git rebase main',esc('Successfully rebased and updated refs/heads/feature.')),
    ('git rebase -i HEAD~3',esc('交互式 rebase')),
    ('git stash',esc('Saved working directory and index state WIP on main: abc1234')),
    ('git stash pop',esc('Dropped refs/stash@{0} (abc1234)')),
    ('git stash list',esc('stash@{0}: WIP on main: abc1234')),
    ('git remote -v',esc('origin https://github.com/user/repo.git (fetch)\norigin https://github.com/user/repo.git (push)')),
    ('git push origin main',esc('Enumerating objects: 5, done.\nTo github.com:user/repo.git\nabc..def main -> main')),
    ('git push -u origin main',esc('推送并设置上游分支')),
    ('git pull','Already up to date.'),
    ('git fetch',esc('From github.com:user/repo\nabc..def main -> origin/main')),
    ('git tag v1.0',esc('已创建标签 v1.0')),
    ('git tag -l','v1.0\nv1.0.1'),
    ('git push --tags',esc('推送所有标签')),
    ('git blame file.txt',esc('abc1234 (User 2026-06-16 02:00) 1) Hello World\ndef5678 (User 2026-06-15 18:30) 2) Line 2')),
    ('git reset HEAD file.txt',esc('取消暂存 file.txt')),
    ('git reset --soft HEAD~1',esc('撤销提交(保留更改)')),
    ('git clean -fd',esc('清理未跟踪文件')),
    ('git reflog',esc('abc1234 HEAD@{0}: commit: Initial commit')),
    ('git cherry-pick abc1234',esc('[feature def5678] Initial commit\n1 file changed, 10 insertions(+)')),
    ("git config --global user.name 'User'",esc('已设置 user.name')),
    ("git config --global user.email 'user@fusion.dev'",esc('已设置 user.email')),
    ('git config --list','user.name=User\nuser.email=user@fusion.dev\ncore.editor=vim'),
]
add_cmds("Git", git_cmds)

# Programming
prog_cmds = [
    ('python3 -V','Python 3.11.4'),
    ('python3 -c "print(2+2)"','4'),
    ('python3 -m http.server',esc('Serving HTTP on 0.0.0.0 port 8000 ...')),
    ('python3 -m json.tool data.json',esc('{\n    "key": "value"\n}')),
    ('python3 -m venv venv',esc('已创建虚拟环境 venv')),
    ('node -v','v20.11.0'),
    ('node -e "console.log(1+2)"','3'),
    ('npm -v','10.2.4'),
    ('npm init -y',esc('Wrote to package.json: { "name": "project", "version": "1.0.0" }')),
    ('npm install express','+ express@4.18.2 added 57 packages in 2s'),
    ('npm run build',esc('> project@1.0.0 build\n> webpack --mode production\ncompiled successfully in 2.34s')),
    ('npm run test',esc('PASS ./test/app.test.js\n✓ should render (5ms)\nTests: 1 passed, 1 total')),
    ('npm start',esc('> project@1.0.0 start\n> node index.js\nServer listening on port 3000')),
    ('npm audit','found 0 vulnerabilities'),
    ('npx create-react-app myapp',esc('Creating a new React app\nInstalling packages...\nSuccess!')),
    ('npx tsc --version','Version 5.3.3'),
    ('gcc --version','gcc (GCC) 13.2.0'),
    ('make',esc('gcc -c main.c -o main.o\ngcc -o app main.o\nBuild complete!')),
    ('javac Hello.java',esc('编译成功: Hello.class')),
    ('java Hello','Hello, World!'),
    ('go version','go version go1.21.5 linux/amd64'),
    ('rustc --version','rustc 1.75.0'),
    ('cargo new myapp',esc('Created binary (application) `myapp` package')),
    ('cargo build',esc('Compiling myapp v0.1.0\nFinished dev target(s) in 2.34s')),
    ('cargo run','Hello, world!'),
    ('cargo test',esc('running 1 test\ntest tests::it_works ... ok\ntest result: ok. 1 passed')),
    ('docker --version','Docker version 26.0.0'),
    ('docker ps',esc('CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES\n(empty)')),
    ('docker build -t myapp .',esc('Sending build context to Docker daemon 2.048kB\nStep 1/5 : FROM node:20\nSuccessfully tagged myapp:latest')),
    ('kubectl version','Client Version: v1.29.0'),
    ('kubectl get pods',esc('NAME READY STATUS RESTARTS AGE\nweb-0 1/1 Running 0 5m')),
]
add_cmds("Programming", prog_cmds)

# Fun
fun_cmds = [
    ('cowsay Hello',esc(' ______\n< Hello >\n ------\n        \\   ^__^\n         \\  (oo)\\_______\n            (__)\\       )\\/\\\n                ||----w |\n                ||     ||')),
    ('fortune',esc('You will have a pleasant surprise.')),
    ('figlet Hello',esc(' _   _      _ _       \n| | | | ___| | | ___  \n| |_| |/ _ \\ | |/ _ \\\n|  _  |  __/ | | (_) |\n|_| |_|\\___|_|_|\\___/')),
    ('neofetch',esc('user@fusion-desktop\n--------------\nOS: FusionOS 8.0\nKernel: fusion-8.0.0\nUptime: 3 days\nShell: fsh 5.8\nCPU: Fusion Virtual @ 3.20GHz\nMemory: 2015MiB / 16000MiB')),
    ('screenfetch',esc('时尚 OS 资讯显示')),
    ('sl',esc('🚂 火车动画正在通过... 💨💨')),
    ('cmatrix',esc('《黑客帝国》风格字符雨(已模拟)')),
    ('cmatrix -C green',esc('绿色字符雨')),
    ('asciiquarium',esc('🐟 🐠 🐡 🦈 水族馆动画(已模拟)')),
    ('nyancat',esc('🐱🌈 彩虹猫动画(已模拟)')),
    ('rev','dlroW olleH'),
    ('factor 42','42: 2 3 7'),
    ('factor 100','100: 2 2 5 5'),
    ('pi 50','3.14159265358979323846264338327950288419716939937510'),
    ('say "Hello World"',esc('🔊 语音: Hello World')),
    ('hollywood',esc('🎬 好莱坞风 hacker 画面(模拟)')),
    ('pipes.sh',esc('┌──┬──┐ 管道动画(模拟)\n│┌┴┐│\n│└┬┘│\n└──┴──┘')),
    ('snake',esc('🐍 贪吃蛇游戏(模拟)')),
    ('tetris',esc('■■■ 俄罗斯方块(模拟)')),
    ('2048',esc('数字合体游戏(模拟)')),
]
add_cmds("Fun & Games", fun_cmds)

# ── Loop-generated commands for volume ──
# Math operations
entries.append("  /* ── Math ── */")
for op in ['add','sub','mul','div','pow','sqrt','mod','abs','ceil','floor','round','sin','cos','tan','log','ln','exp','min','max','avg','sum','median']:
    entries.append(cmd(f'math {op} 10 5', f'{op}(10,5) = *computed*'))

# Disk operations
for op in ['format','check','repair','defrag','cleanup','analyze','benchmark','info','label','resize','encrypt','decrypt','mount','umount','sync','trim','smartctl','partprobe','fsck']:
    entries.append(cmd(f'disk {op}', f'Disk {op}: operation simulated (FusionOS)'))

# Crypto hashes
for algo in ['md5','sha1','sha256','sha512','sha3-256','sha3-512','blake2','crc32','xxhash','murmur3']:
    entries.append(cmd(f'{algo}sum file.txt', f'{algo}: abc123def456789...'))

# Encoding
for op in ['base64','base32','base16','hex','urlencode','urldecode','rot13','rot47','uuencode','uudecode']:
    entries.append(cmd(f'{op} "Hello World"', f'{op} encoded output'))

# Compression
for op in ['gzip','gunzip','bzip2','bunzip2','xz','unxz','zip','unzip','tar','untar','7z','rar','zstd','lz4','lzma','compress']:
    entries.append(cmd(f'{op} file.txt', f'{op}: compressed successfully'))

# Database clients
for db in ['mysql','psql','sqlite3','redis-cli','mongo','influx','cassandra','neo4j','elasticsearch','etcd','consul','memcached']:
    entries.append(cmd(f'{db} --version', f'{db} client v8.0 (FusionOS)'))

# Permission commands  
for op in ['chmod','chown','chgrp','chattr','lsattr','getfacl','setfacl','umask']:
    entries.append(cmd(f'{op} --help', f'{op}: file attribute/permission tool'))

# Network mgmt
for op in ['iptables','ufw','firewalld','ebtables','tc','bridge','nmcli','nmtui','iw','wpa_cli','rfkill','ethtool','ipset']:
    entries.append(cmd(f'{op} --help', f'{op}: network management tool'))

# Package managers
for pm in ['apt','apt-get','dpkg','rpm','yum','dnf','pacman','snap','flatpak','brew','pip3','gem','composer','cargo','npm','yarn','pnpm']:
    entries.append(cmd(f'{pm} --version', f'{pm} v2.0 (FusionOS)'))

# Editors
for ed in ['vim','vi','nano','emacs','neovim','nvim','code','subl','helix','micro','joe','mcedit','gedit','notepad']:
    entries.append(cmd(f'{ed} --version', f'{ed} editor (FusionOS)'))

# Shells
for sh in ['bash','zsh','fish','dash','ksh','tcsh','sh','nu','elvish','xonsh','ion']:
    entries.append(cmd(f'{sh} --version', f'{sh} v5.2 (FusionOS)'))

# Env vars
for var in ['HOME','USER','PATH','SHELL','TERM','LANG','PWD','HOSTNAME','DISPLAY','EDITOR','PAGER','BROWSER','MANPATH']:
    entries.append(cmd(f'echo ${var}', f'(value of {var})'))

# Scheduling
for s in ['crontab -l','crontab -e','atq','atrm','batch','anacron']:
    entries.append(cmd(s, f'{s}: scheduler operation'))

# Service mgmt
for sv in ['systemctl status','systemctl start','systemctl stop','systemctl restart','systemctl enable','systemctl disable','service --status-all','chkconfig']:
    entries.append(cmd(f'{sv} fusion-shell', f'{sv}: service operation (FusionOS)'))

# Color terminal
for c in ['tput setaf 1','tput setaf 2','tput setaf 3','tput bold','tput smul','tput rmul','tput rev','tput sgr0','tput cols','tput lines']:
    entries.append(cmd(c, '(terminal attribute)', c))

# Tools galore
tools = ['jq','yq','pandoc','ffmpeg','sox','vlc','mpv','mplayer','htop','btm','bottom','procs','duf','dust','bat','exa','lsd','fd','fzf','rg','delta','tig','lazygit','tokei','hyperfine','just','watchexec','entr','ranger','nnn','lf','mc','calibre','mutt','irssi','weechat']
for t in tools:
    entries.append(cmd(f'{t} --version', f'{t} v1.0 (FusionOS)'))

# sysctl network
for key in ['tcp_syncookies','tcp_fin_timeout','tcp_keepalive_time','tcp_keepalive_intvl','tcp_keepalive_probes','tcp_retries1','tcp_retries2','tcp_tw_reuse','tcp_max_syn_backlog','tcp_congestion_control','tcp_timestamps','tcp_window_scaling','tcp_mtu_probing','tcp_slow_start_after_idle','tcp_wmem','tcp_rmem','ip_forward','ip_default_ttl','icmp_echo_ignore_all']:
    entries.append(cmd(f'sysctl net.ipv4.{key}', f'net.ipv4.{key} = (default)'))

# More sysctl vm  
for key in ['swappiness','dirty_ratio','dirty_background_ratio','vfs_cache_pressure','overcommit_memory','min_free_kbytes','drop_caches','zone_reclaim_mode','panic_on_oom','page-cluster','overcommit_ratio']:
    entries.append(cmd(f'sysctl vm.{key}', f'vm.{key} = (default)'))

# Filesystem ops
fs_ops = ['fsck','mkfs','mkfs.ext4','mkfs.xfs','mkfs.btrfs','mkfs.vfat','mkfs.ntfs','resize2fs','tune2fs','dumpe2fs','debugfs','e2label','e2fsck','mkswap','swapon','swapoff','blkid','findfs','parted','fdisk','gdisk','sfdisk','cfdisk','mkpart','resizepart','lsblk -f','findmnt','losetup','kpartx','multipath']
for op in fs_ops:
    entries.append(cmd(op, f'{op}: filesystem operation (FusionOS)'))

# Network diagnostics
net_diag = ['mtr','mtr -r','nping','hping3','netcat -l','socat','stunnel','openssl s_client','openssl s_server','certbot','httpie','wget -r','curl -k','wget --no-check-certificate','ab','wrk','siege','vegeta','hey','locust','iperf','iperf3','qperf','netperf']  
for op in net_diag:
    entries.append(cmd(op, f'{op}: network diagnostic (FusionOS)'))

# DNS tools
dns_tools = ['dig +trace','dig +short','dig -x','dig MX','dig NS','dig TXT','dig SOA','dig ANY','host -t MX','host -t NS','whois','nslookup -type=MX','nslookup -type=NS','nslookup -type=TXT','resolvectl','systemd-resolve']
for op in dns_tools:
    entries.append(cmd(op, f'{op}: DNS query (FusionOS)'))

# Security tools
sec = ['openssl','gpg','ssh-keygen','ssh-copy-id','ssh-agent','ssh-add','certutil','pkcs12','keytool','jarsigner','signcode','chkrootkit','rkhunter','lynis','clamav','freshclam','clamscan','aide','tripwire','fail2ban-client']
for op in sec:
    entries.append(cmd(f'{op} --help', f'{op}: security tool (FusionOS)'))

# Backup tools
bak = ['rsync','rdiff-backup','duplicity','borg','restic','timeshift','dump','restore','tar -czf','tar -xzf','cpio','dar','fsarchiver','partclone','dd','ddrescue','pv','mbuffer','pipe-viewer']
for op in bak:
    entries.append(cmd(f'{op} --help', f'{op}: backup/restore tool (FusionOS)'))

# AWS CLI
aws_cmds = ['aws','aws s3','aws ec2','aws lambda','aws dynamodb','aws rds','aws iam','aws cloudformation','aws cloudwatch','aws sns','aws sqs','aws route53','aws cloudfront','aws eks','aws ecs','aws elb','aws ssm','aws kms','aws secretsmanager']
for op in aws_cmds:
    entries.append(cmd(f'{op} --help', f'{op}: AWS CLI (FusionOS)'))

# GCloud
gcp = ['gcloud','gcloud compute','gcloud storage','gcloud functions','gcloud run','gcloud sql','gcloud iam','gcloud pubsub','gcloud bigquery','gcloud datastore','gcloud firestore','gcloud spanner','gcloud kms','gcloud container','gcloud app','gcloud dns','gcloud logging']
for op in gcp:
    entries.append(cmd(f'{op} --help', f'{op}: Google Cloud CLI (FusionOS)'))

# Azure CLI
azure = ['az','az vm','az storage','az functionapp','az webapp','az sql','az acr','az aks','az cosmosdb','az keyvault','az network','az monitor','az iot','az ad','az group','az deployment']
for op in azure:
    entries.append(cmd(f'{op} --help', f'{op}: Azure CLI (FusionOS)'))

# Kubernetes
k8s = ['kubectl get','kubectl describe','kubectl logs','kubectl exec','kubectl apply','kubectl delete','kubectl create','kubectl edit','kubectl scale','kubectl rollout','kubectl port-forward','kubectl top','kubectl config','kubectl cluster-info','kubectl api-resources','kubectl explain','kubectl taint','kubectl label','kubectl annotate','kubectl patch','helm','helm install','helm list','helm upgrade','helm rollback','helm repo','helm search']
for op in k8s:
    entries.append(cmd(f'{op} --help', f'{op}: Kubernetes/Helm (FusionOS)'))

# Ansible/Terraform
iac = ['ansible','ansible-playbook','ansible-galaxy','ansible-vault','ansible-inventory','ansible-doc','terraform','terraform init','terraform plan','terraform apply','terraform destroy','terraform fmt','terraform validate','terraform import','terraform state','terraform workspace','pulumi','pulumi up','pulumi stack']
for op in iac:
    entries.append(cmd(f'{op} --help', f'{op}: IaC tool (FusionOS)'))

# CI/CD
cicd = ['jenkins','gitlab-runner','circleci','gh','gh pr','gh issue','gh release','gh repo','gh auth','gh workflow','act','drone','tekton','argocd','flux','spinnaker']
for op in cicd:
    entries.append(cmd(f'{op} --help', f'{op}: CI/CD tool (FusionOS)'))

# More fun
more_fun = ['ponysay Hi','lolcat file.txt','toilet FusionOS','banner WELCOME','oneko','xeyes','worms','moon-buggy','espeak hello','cava','cbonsai','tmatrix','pong','pacman','sudoku','chess','invaders','dino','pfetch','fastfetch','macchina','uwufetch','hyfetch','cpufetch','gpufetch','ramfetch','diskfetch','aafire','bb','asciiart']
for op in more_fun:
    entries.append(cmd(op, f'{op}: fun tool (FusionOS)'))

# More programming langs and tools
langs = ['perl -v','ruby -v','php -v','dotnet --version','lua -v','swift --version','kotlin -version','scala -version','haskell --version','elixir --version','erlang -version','julia -v','R --version','octave --version','typescript tsc -v','dart --version','groovy --version','clojure -version']
for op in langs:
    entries.append(cmd(op, f'{op}: language version (FusionOS)'))

# Language package managers  
lpms = ['pip','pipenv','poetry','conda','mamba','npm','yarn','pnpm','bun','gem','bundler','cargo','composer','nuget','dotnet','dub','vcpkg','conan','spack','luarocks','cpan','cpanm','opam','cabal','stack','hex','rebar3','maven','gradle','sbt','leiningen','mix']
for op in lpms:
    entries.append(cmd(f'{op} --version', f'{op}: package manager v1.0'))

# Random system commands to fill the gap
misc = ['envsubst','gettext','msgfmt','xgettext','recode','iconv','dos2unix','unix2dos','mac2unix','enca','uchardet','shred','wipe','srm','scrub','rename','mmv','vidir','qmv','imv','fasd','autojump','z','zoxide','peco','percol','selecta','pick','sentaku']
for op in misc:
    entries.append(cmd(f'{op} --help', f'{op}: utility tool (FusionOS)'))

# ── BULK commands for 1200 target ──
# Time/date variants
for fmt in ['%Y','%m','%d','%H','%M','%S','%A','%B','%j','%U','%W','%w','%u','%V','%Z','%z','%c','%x','%X','%r','%R','%T','%D','%F']:
    entries.append(cmd(f'date +{fmt}', f'({fmt} formatted)'))

# Random number generators
for cmd_name in ['echo $RANDOM', 'shuf -i 1-100 -n 1', 'od -An -N2 -i /dev/urandom', 'openssl rand -hex 4', 'uuidgen', 'cat /proc/sys/kernel/random/uuid', 'date +%s%N | sha256sum | head -c 8', 'head -c 4 /dev/urandom | xxd -p']:
    entries.append(cmd(cmd_name, '(random value)'))

# More arithmetic via bc
for expr in ['2+2','10*5','100/3','2^10','sqrt(144)','s(3.14159/2)','c(0)','l(2.71828)','e(1)','scale=4;22/7','scale=10;4*a(1)','obase=16;255','obase=2;42','3^3^3','(10+5)*3']:
    entries.append(cmd(f'echo "{expr}" | bc', f'bc: {expr} = (computed)'))

# Head/tail more variants
for n in [1,2,3,5,10,15,20,25,50,100]:
    entries.append(cmd(f'head -n {n} file.txt', f'First {n} lines of file.txt'))
    entries.append(cmd(f'tail -n {n} file.txt', f'Last {n} lines of file.txt'))

# Sort variants 
for opt in ['-n','-h','-M','-V','-k2','-t,','-b','-f','-R','-S']:
    entries.append(cmd(f'sort {opt} file.txt', f'Sort with {opt}'))

# du variants
for opt in ['-h','-s','-c','-a','-k','-m','-b','-L','--max-depth=1','--max-depth=2','--max-depth=3','-h --max-depth=1','-sh *','-ah','--apparent-size']:
    entries.append(cmd(f'du {opt}', f'du {opt} output'))

# df variants
for opt in ['-h','-i','-T','-a','-k','-m','-H','-l','--total','-x','-t ext4','-h /home','-h /tmp']:
    entries.append(cmd(f'df {opt}', f'df {opt} output'))

# More kill signals
for sig in ['HUP','INT','QUIT','ILL','TRAP','ABRT','BUS','FPE','KILL','USR1','SEGV','USR2','PIPE','ALRM','TERM','STOP','TSTP','CONT','CHLD','TTIN','TTOU','URG','XCPU','XFSZ','VTALRM','PROF','WINCH','POLL','PWR','SYS']:
    entries.append(cmd(f'kill -{sig} 0', f'Signal {sig} test (PID 0)'))

# LS variants  
for opt in ['-a','-A','-l','-h','-t','-S','-r','-R','-1','-F','-i','-s','-d','-L','-Z','-X','-v','-U','-g','-o','-n','-G','-Q','--color=auto','--group-directories-first','--time=atime','--time=ctime','--sort=size','--sort=time','--sort=extension']:
    entries.append(cmd(f'ls {opt}', f'ls {opt} detailed listing'))

# Ps variants
for opt in ['-a','-u','-x','-f','-l','-e','-A','-o pid,cmd','-o pid,ppid,cmd,%mem,%cpu','-C term','--forest','--sort=-%mem','--sort=-%cpu','-p 1','-t pts/0','-U user','-G user','--no-headers','-ww','-L']:
    entries.append(cmd(f'ps {opt}', f'ps {opt} process listing'))

# Grep variants
for opt in ['-i','-v','-c','-n','-r','-l','-L','-w','-x','-e','-F','-E','-P','-o','-q','-s','-H','-h','-m 5','--color','-A 2','-B 2','-C 2','-Z']:
    entries.append(cmd(f'grep {opt} "pattern" file.txt', f'grep {opt}: search result'))

# Find variants
for opt in ['-name "*.txt"','-type f','-type d','-size +1M','-mtime -7','-mtime +30','-atime -1','-ctime -7','-user user','-group user','-perm 644','-empty','-links 1','-exec ls -l {} \\;','-delete','-maxdepth 1','-mindepth 2','-newer file.txt','-not -name "*.tmp"']:
    entries.append(cmd(f'find . {opt}', f'find {opt} results'))

# Netstat variants
for opt in ['-a','-t','-u','-l','-p','-n','-s','-i','-r','-g','-c','-e','-o','-T','-W','-tuln','-tunlp','-an','-at','-au','-lt','-lu','-st','-su']:
    entries.append(cmd(f'netstat {opt}', f'netstat {opt} connections'))

# curl variants  
for opt in ['-X GET','-X POST','-X PUT','-X DELETE','-X PATCH','-X HEAD','-X OPTIONS','-H "Accept: application/json"','-H "Authorization: Bearer token"','-d @data.json','--data-urlencode "key=value"','-F "file=@data.txt"','-u user:pass','--cacert cert.pem','-k','--connect-timeout 5','--max-time 10','-w "%{http_code}"','-o /dev/null -s -w "%{http_code}"']:
    entries.append(cmd(f'curl {opt} http://localhost', f'curl {opt} request'))

# Ping variants
for opt in ['-c 1','-c 4','-i 0.2','-s 100','-t 64','-W 1','-q','-a','-A','-D','-n','-v','-f','-l 3','-w 5','-M do','-M dont','-M want']:
    entries.append(cmd(f'ping {opt} localhost', f'ping {opt} statistics'))

# Coreutils misc
for tool in ['basename','dirname','realpath','readlink','mktemp','mkfifo','tee','split','csplit','cksum','md5sum','sha1sum','sha256sum','sha512sum','b2sum','sum','wc','fmt','fold','pr','column','rev','tac','nl','paste','join','expand','unexpand','numfmt','seq']:
    entries.append(cmd(f'{tool} --help', f'{tool}: GNU coreutils (FusionOS)'))

# System commands
for tool in ['adduser','deluser','usermod','groupadd','groupdel','groupmod','passwd','su','sudo','visudo','chage','chfn','chsh','last','lastb','lastlog','faillog','loginctl','journalctl','localectl','hostnamectl','timedatectl','resolvectl','networkctl','busctl','oomctl','portablectl','systemd-analyze','systemd-cgls','systemd-cgtop','systemd-delta','systemd-detect-virt','systemd-escape','systemd-id128','systemd-notify','systemd-path','systemd-run','systemd-socket-activate','systemd-sysusers','systemd-tmpfiles','systemd-tty-ask-password-agent','udevadm','dmesg','lsmod','modinfo','modprobe','insmod','rmmod','depmod','kmod']:
    entries.append(cmd(f'{tool} --help', f'{tool}: system administration (FusionOS)'))

# Final count
total = len([e for e in entries if not e.startswith('  /*')])
print(f"\n=== Generated {total} terminal commands ===")

# ─────────────────────────────────────────────────
# Inject: Replace O dictionary in termExec
# ─────────────────────────────────────────────────

t1 = html.find('function termExec(cmd,id){')
o_start = html.find('var O={};', t1)
o_end = html.find('var fn=O[c];', o_start)

# Build the new O dict
o_dict = 'var O={};\n\n' + ''.join(entries) + '\n  /* ── Execution ── */\n  '

new_html = html[:o_start] + o_dict + html[o_end + len('var fn=O[c];'):]
print(f"New HTML size: {len(new_html)} chars (was {len(html)})")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"✓ Injected {total} commands into {HTML_PATH}")
print(f"✓ O dict: {len(o_dict)} chars")
