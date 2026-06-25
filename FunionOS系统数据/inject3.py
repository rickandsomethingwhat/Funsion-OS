#!/usr/bin/env python3
"""FusionOS 7.0 — Part 3: Terminal 170 Commands + 100 Features"""
FILE = '/Users/murderdrones/WorkBuddy/2026-06-15-12-25-08/vm-os.html'

with open(FILE, 'r', encoding='utf-8') as fh:
    content = fh.read()

lines = content.split('\n')

# ============================================================
# TERMINAL COMMANDS - Replace termExec function entirely
# ============================================================
# Find the termExec function
start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if 'function termExec(cmd,id){' in line:
        start_idx = i
    if start_idx is not None and 'function escHtml' in line:
        end_idx = i
        break

if start_idx and end_idx:
    new_term_parts = lines[:start_idx]
    new_term_parts.append('function termExec(cmd,id){')
    new_term_parts.append('  var tl=document.getElementById(\'tl-\'+id);if(!tl)return;var row=document.createElement(\'div\');row.className=\'line\';row.innerHTML=\'<span class="prompt">❯ </span><span style="color:#c9d1d9">\'+escHtml(cmd)+\'</span>\';tl.appendChild(row);')
    new_term_parts.append('  var out=document.createElement(\'div\');out.className=\'line\';')
    new_term_parts.append('  var parts=cmd.split(/\\s+/),c=parts[0].toLowerCase(),arg=parts.slice(1).join(\' \');')
    
    # Now build the O dictionary with 170+ commands
    cmd_entries = []
    
    # Helper to add a command
    def add_cmd(name, js_code):
        cmd_entries.append(f"  O['{name}']=function(){{{js_code}}};")
    
    # Original commands (keep them)
    add_cmd("help", "return'  <span class=\"cmd\">help</span> 帮助  <span class=\"cmd\">ls</span> 列文件  <span class=\"cmd\">cat</span> 查看  <span class=\"cmd\">pwd</span> 路径<br>  <span class=\"cmd\">clear</span> 清屏  <span class=\"cmd\">mkdir</span> 建目录  <span class=\"cmd\">touch</span> 建文件  <span class=\"cmd\">rm</span> 删除<br>  <span class=\"cmd\">neofetch</span> 系统  <span class=\"cmd\">tree</span> 目录树  <span class=\"cmd\">calc</span> 计算<br>  <span class=\"cmd\">ps</span> 进程  <span class=\"cmd\">free</span> 内存  <span class=\"cmd\">df</span> 磁盘  <span class=\"cmd\">echo</span> 输出  <span class=\"cmd\">date</span> 日期<br>  <span class=\"cmd\">cmds</span> 列出所有'+chr(49)+chr(55)+chr(49)+'+条命令'")  # "170+条命令" but avoid encoding issues
    
    # ---- CORE UNIX COMMANDS (30) ----
    add_cmd("ls", "return'  <span class=\"path\">Documents/</span>  <span class=\"path\">Pictures/</span>  <span class=\"path\">Music/</span>  <span class=\"path\">Desktop/</span><br>  README.txt  todo.txt  kernel.js  boot.log'")
    add_cmd("pwd", "return'  <span class=\"path\">/home/user</span>'")
    add_cmd("cd", "return arg?'  <span class=\"warn\">模拟目录切换: '+arg+'/</span>':'  <span class=\"path\">/home/user</span>'")
    add_cmd("cat", "if(arg.includes('README')){var ct=vfsReadFile('/用户/文档/README.txt');return ct?'  <pre style=\"color:#c9d1d9;white-space:pre-wrap\">'+escHtml(ct)+'</pre>':'  FusionOS 7.0 — 融合桌面系统';}var node=vfsNode(arg);if(node&&node.t==='f')return'  <pre style=\"color:#c9d1d9;white-space:pre-wrap\">'+escHtml(node.d||'(空)')+'</pre>';if(!arg)return'  <span class=\"err\">用法: cat <文件路径></span>';return'  <span class=\"err\">文件未找到: '+arg+'</span>'")
    add_cmd("mkdir", "if(!arg)return'  <span class=\"err\">用法: mkdir <目录名></span>';return vfsMkdir(arg)?'  <span class=\"val\">✓ 已创建目录: '+arg+'</span>':'  <span class=\"err\">创建失败</span>'")
    add_cmd("touch", "if(!arg)return'  <span class=\"err\">用法: touch <文件名></span>';return vfsTouch(arg)?'  <span class=\"val\">✓ 已创建文件: '+arg+'</span>':'  <span class=\"err\">创建失败</span>'")
    add_cmd("rm", "if(!arg)return'  <span class=\"err\">用法: rm <路径></span>';return vfsRm(arg)?'  <span class=\"val\">✓ 已删除: '+arg+'</span>':'  <span class=\"err\">删除失败</span>'")
    add_cmd("rmdir", "if(!arg)return'  <span class=\"err\">用法: rmdir <目录路径></span>';return vfsRm(arg)?'  <span class=\"val\">✓ 已删除目录: '+arg+'</span>':'  <span class=\"err\">删除失败</span>'")
    add_cmd("echo", "return'  '+arg")
    add_cmd("clear", "tl.innerHTML='';return''")
    add_cmd("write", "var p=cmd.split(/\\s+/);if(p.length<3)return'  <span class=\"err\">用法: write <文件路径> <内容></span>';var fp=p[1],ct=p.slice(2).join(' ');return vfsWriteFile(fp,ct)?'  <span class=\"val\">✓ 已写入: '+fp+'</span>':'  <span class=\"err\">写入失败</span>'")
    add_cmd("cp", "return'  <span class=\"warn\">功能暂未实现（VFS限制）</span>'")
    add_cmd("mv", "return'  <span class=\"warn\">功能暂未实现（VFS限制）</span>'")
    add_cmd("ln", "return'  <span class=\"warn\">符号链接不受支持</span>'")
    add_cmd("chmod", "if(!arg)return'  <span class=\"info\">当前权限: rwxr-xr-x</span>';return'  <span class=\"val\">✓ 权限已模拟修改</span>'")
    add_cmd("chown", "return'  <span class=\"val\">✓ 所有者: user:staff</span>'")
    add_cmd("find", "return'  <span class=\"path\">./Documents/README.txt</span><br>  <span class=\"path\">./Documents/todo.txt</span><br>  <span class=\"path\">./System/kernel.js</span>'")
    add_cmd("grep", "return'  <span class=\"warn\">VFS 不支持全文搜索</span>'")
    add_cmd("wc", "return'  <span class=\"val\">'+Math.floor(Math.random()*500+20)+' '+Math.floor(Math.random()*3000+100)+' '+Math.floor(Math.random()*20000+500)+'</span>'")
    add_cmd("sort", "return'  <span class=\"warn\">请在管道中使用</span>'")
    add_cmd("uniq", "return'  <span class=\"warn\">请在管道中使用</span>'")
    add_cmd("head", "return'  line 1<br>  line 2<br>  line 3<br>  <span style=\"color:#8b949e\">... 省略剩余行</span>'")
    add_cmd("tail", "return'  <span style=\"color:#8b949e\">... 省略前几行</span><br>  line 98<br>  line 99<br>  line 100'")
    add_cmd("cut", "return'  <span class=\"warn\">请在管道中使用</span>'")
    add_cmd("diff", "return'  <span class=\"info\">文件相同（模拟）</span>'")
    add_cmd("file", "return'  <span class=\"info\">'+arg+': ASCII text</span>'")
    add_cmd("which", "return'  <span class=\"path\">/usr/bin/'+arg+'</span>'")
    add_cmd("whereis", "return'  <span class=\"path\">/usr/bin/'+arg+'  /usr/share/man/man1/'+arg+'.1</span>'")
    add_cmd("type", "return'  <span class=\"info\">'+arg+' 是内置命令</span>'")
    add_cmd("tee", "return'  <span class=\"val\">✓ 输出已复制</span>'")
    add_cmd("yes", "return'  <span class=\"info\">y y y y y y y y ... (Ctrl+C 停止)</span>'")
    add_cmd("tr", "return'  <span class=\"warn\">请在管道中使用</span>'")

    # ---- SYSTEM INFO (15) ----
    add_cmd("uname", "return'  <span class=\"val\">FusionOS</span> 7.0 fusionos-7.0-generic x86_64'")
    add_cmd("hostname", "return'  <span class=\"val\">fusionos-desktop</span>'")
    add_cmd("whoami", "return'  <span class=\"val\">user</span>'")
    add_cmd("who", "return'  <span class=\"val\">user     pts/0        '+new Date().toLocaleString('zh-CN')+'</span>'")
    add_cmd("id", "return'  <span class=\"val\">uid=1000(user) gid=1000(user) groups=1000(user),998(wheel),997(staff)</span>'")
    add_cmd("groups", "return'  <span class=\"val\">user wheel staff</span>'")
    add_cmd("uptime", "var s=Math.floor((Date.now()-(window._bootTime||Date.now()))/1000);var m=Math.floor(s/60),h=Math.floor(m/60);return'  <span class=\"val\">up '+h+'小时 '+((m%60))+'分</span>,  1 user,  load avg: '+(Math.random()*0.5+0.1).toFixed(2)+' '+(Math.random()*0.3+0.05).toFixed(2)+' '+(Math.random()*0.2+0.02).toFixed(2)")
    add_cmd("arch", "return'  <span class=\"val\">x86_64</span>'")
    add_cmd("dmesg", "return'  <span style=\"color:#8b949e\">[0.000] Kernel booting...<br>[0.012] CPU: FusionOS 7.0 x86_64<br>[0.024] Memory: 16GB available<br>[0.036] VFS mounted<br>[0.048] WM initialized<br>[1.200] Desktop ready</span>'")
    add_cmd("lscpu", "return'  <span class=\"val\">Architecture: x86_64</span><br>  CPU(s): '+Math.floor(Math.random()*4+4)+'<br>  Model: FusionOS Virtual CPU @ 3.2GHz'")
    add_cmd("lsblk", "return'  <span class=\"val\">NAME  MAJ:MIN  SIZE  TYPE  MOUNTPOINT</span><br>  vda   254:0    16G   disk  /'")
    add_cmd("lspci", "return'  <span class=\"val\">00:00.0  Host bridge: FusionOS<br>00:01.0  VGA controller: FusionOS Display<br>00:02.0  Network controller: FusionNet<br>00:03.0  Audio device: FusionAudio</span>'")
    add_cmd("mount", "return'  <span class=\"val\">FusionDisk on / type fusfs (rw)</span>'")
    add_cmd("vmstat", "return'  <span class=\"val\">procs  memory      swap  io  system  cpu<br>r b  free  buff  cache  si  so  bi  bo  in  cs  us sy id</span><br> 0 0  '+Math.floor(Math.random()*8+8)+'G  0  0  0  0  0  0  1  2  2 1 97'")

    # ---- NETWORK COMMANDS (15) ----
    add_cmd("ping", "if(!arg)return'  <span class=\"err\">用法: ping <地址></span>';var ip=arg.replace(/[^a-zA-Z0-9.]/g,'');var ms=Math.floor(Math.random()*30+5);return'  <span class=\"info\">PING '+ip+' 56(84) bytes of data.</span><br>  64 bytes from '+ip+': icmp_seq=1 ttl=64 time='+ms+'.'+Math.floor(Math.random()*100)+' ms<br>  64 bytes from '+ip+': icmp_seq=2 ttl=64 time='+(ms+Math.floor(Math.random()*5))+'.'+Math.floor(Math.random()*100)+' ms<br>  <span class=\"val\">--- '+ip+' ping statistics ---</span><br>  2 packets transmitted, 2 received, 0% packet loss'")
    add_cmd("curl", "return'  <span class=\"info\">模拟 HTTP 请求...</span><br>  <span class=\"val\">HTTP/1.1 200 OK</span><br>  Content-Type: text/html<br>'+'<br>  <span style=\"color:#8b949e\"><html><body>FusionOS 7.0</body></html></span>'")
    add_cmd("wget", "return'  <span class=\"info\">模拟下载: '+arg+'</span><br>  <span class=\"val\">100% [======================] 1.2MB/s   0s</span><br>  ✓ 已保存为 index.html'")
    add_cmd("ifconfig", "return'  <span class=\"val\">eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST></span><br>  inet 192.168.1.100  netmask 255.255.255.0<br>  ether 00:1a:2b:3c:4d:5e'")
    add_cmd("ip", "return'  <span class=\"val\">1: eth0: <BROADCAST,MULTICAST,UP></span><br>  inet 192.168.1.100/24 scope global eth0'")
    add_cmd("netstat", "return'  <span class=\"val\">Proto  Local Address  Foreign Address  State</span><br>  tcp    0.0.0.0:443    0.0.0.0:*       LISTEN<br>  tcp    192.168.1.100:443  151.101.1.69:443  ESTABLISHED'")
    add_cmd("ss", "return'  <span class=\"val\">Netid  State  Recv-Q  Send-Q  Local:Port  Peer:Port</span><br>  tcp    ESTAB  0       0        192.168.1.100:443  151.101.1.69:443'")
    add_cmd("nslookup", "return arg?'<span class=\"info\">Server: 8.8.8.8<br>Address: '+arg+'<br>Non-authoritative answer:<br>Name: '+arg+'<br>Address: 142.250.80.46</span>':'  <span class=\"err\">用法: nslookup <域名></span>'")
    add_cmd("dig", "return'  <span class=\"info\">; <<>> DiG 9.18 <<>> '+arg+'<br>;; ANSWER SECTION:<br>'+arg+'.  300  IN  A  142.250.80.46</span>'")
    add_cmd("traceroute", "return arg?'<span class=\"info\">traceroute to '+arg+', 30 hops max</span><br>  1  _gateway  1.2 ms<br>  2  10.0.0.1  5.4 ms<br>  3  203.0.113.1  12.1 ms<br>  ... (模拟)':'  <span class=\"err\">用法: traceroute <地址></span>'")
    add_cmd("ssh", "return'  <span class=\"warn\">SSH 客户端功能未启用（模拟）</span>'")
    add_cmd("ftp", "return'  <span class=\"warn\">FTP 功能未启用（模拟）</span>'")
    add_cmd("nc", "return'  <span class=\"warn\">netcat 功能未启用（模拟）</span>'")
    add_cmd("wifi", "return'  <span class=\"val\">Wi-Fi 状态: 已连接 (FusionNet)</span><br>  SSID: FusionNet-5G<br>  信号强度: '+Math.floor(Math.random()*30+70)+'%<br>  IP: 192.168.1.100'")
    add_cmd("speedtest", "return'  <span class=\"info\">测速中...</span><br>  <span class=\"val\">下载: '+(Math.random()*500+100).toFixed(1)+' Mbps</span><br>  <span class=\"val\">上传: '+(Math.random()*200+20).toFixed(1)+' Mbps</span><br>  <span class=\"val\">延迟: '+(Math.floor(Math.random()*20+5))+' ms</span>'")

    # ---- SYSTEM MONITORING (10) ----
    add_cmd("ps", "return'  <span class=\"val\">PID  COMMAND</span><br>  1001 fusion-wm<br>  1002 fusion-term<br>  1003 fusion-finder<br>  1004 vfs-daemon<br>  1005 notificationd'")
    add_cmd("top", "return'  <span class=\"val\">PID  USER  PR  NI  VIRT  RES  SHR  S  %CPU  %MEM  TIME+  COMMAND</span><br>  1001 user  20  0   256m  48m  24m  S  '+Math.floor(Math.random()*10+2)+'.'+Math.floor(Math.random()*10)+'  0.'+Math.floor(Math.random()*9)+'  0:05.23  fusion-wm'")
    add_cmd("free", "var u=calcDiskUsed(),f=diskFree();return'  <span class=\"val\">FusionDisk 16 GB</span><br>  已用: '+fmtSize(u)+'  |  可用: '+fmtSize(f)+'<br>  使用率: '+((u/vDisk.total)*100).toFixed(1)+'%'")
    add_cmd("df", "var u=calcDiskUsed(),f=diskFree();return'  <span class=\"val\">文件系统       总大小     已用      可用  使用率</span><br>  FusionDisk   '+fmtSize(vDisk.total)+'    '+fmtSize(u)+'    '+fmtSize(f)+'   '+((u/vDisk.total)*100).toFixed(0)+'%'")
    add_cmd("du", "return'  <span class=\"val\">4.2G  ./Documents</span><br>  <span class=\"val\">2.1G  ./Pictures</span><br>  <span class=\"val\">1.8G  ./Music</span><br>  <span class=\"val\">8.1G  total</span>'")
    add_cmd("iostat", "return'  <span class=\"val\">Device  tps  kB_read/s  kB_wrtn/s</span><br>  vda     '+Math.floor(Math.random()*50+10)+'.'+Math.floor(Math.random()*100)+'  '+Math.floor(Math.random()*100)+'  '+Math.floor(Math.random()*50)+'</span>'")
    add_cmd("iotop", "return'  <span class=\"warn\">iotop 需要 root 权限</span>'")
    add_cmd("mpstat", "return'  <span class=\"val\">CPU  %usr  %sys  %idle</span><br>  all  '+Math.floor(Math.random()*10+2)+'.'+Math.floor(Math.random()*10)+'  '+Math.floor(Math.random()*5+1)+'.'+Math.floor(Math.random()*10)+'  '+(Math.floor(Math.random()*80+10))+'.'+Math.floor(Math.random()*10)+'</span>'")
    add_cmd("sensors", "return'  <span class=\"val\">coretemp-isa-0000</span><br>  Core 0: +'+Math.floor(Math.random()*20+35)+'.'+Math.floor(Math.random()*10)+'°C<br>  Core 1: +'+Math.floor(Math.random()*20+35)+'.'+Math.floor(Math.random()*10)+'°C'")
    add_cmd("hwinfo", "return'  <span class=\"val\">CPU: FusionOS Virtual CPU @ 3.2GHz</span><br>  RAM: 16GB DDR4<br>  GPU: FusionOS Display Adapter<br>  NET: FusionNet Gigabit Ethernet'")

    # ---- TEXT PROCESSING (10) ----
    add_cmd("awk", "return'  <span class=\"warn\">请在管道中使用: echo \"a b c\" | awk \\'{print $1}\\'</span>'")
    add_cmd("sed", "return'  <span class=\"warn\">请在管道中使用</span>'")
    add_cmd("nl", "return'  <span class=\"val\">1  line one</span><br>  <span class=\"val\">2  line two</span><br>  <span class=\"val\">3  line three</span>'")
    add_cmd("fmt", "return arg?'<span class=\"val\">✓ 文本已重新格式化</span>':'<span class=\"err\">用法: fmt <文本></span>'")
    add_cmd("strings", "return'  <span class=\"warn\">VFS 不支持二进制文件</span>'")
    add_cmd("xxd", "return'  <span class=\"warn\">VFS 不支持十六进制转储</span>'")
    add_cmd("column", "return'  <span class=\"warn\">请在管道中使用</span>'")
    add_cmd("sponge", "return'  <span class=\"warn\">请在管道中使用</span>'")
    add_cmd("split", "return'  <span class=\"val\">✓ 模拟分割: 创建了 xaa, xab, xac</span>'")
    add_cmd("csplit", "return'  <span class=\"val\">✓ 模拟分割</span>'")

    # ---- DEV TOOLS (15) ----
    add_cmd("git", "if(!arg)return'  <span class=\"info\">usage: git [--version] [--help] [-C <path>] [-c <name>=<value>] ...</span>';if(arg==='init')return'  <span class=\"val\">Initialized empty Git repository in /home/user/project/.git/</span>';if(arg==='status')return'  <span class=\"val\">On branch main</span><br>  <span class=\"info\">nothing to commit, working tree clean</span>';if(arg==='log')return'  <span class=\"val\">commit abc1234 (HEAD -> main)</span><br>  <span class=\"info\">Author: user <user@fusionos></span><br>  <span class=\"info\">Date: '+new Date().toLocaleDateString()+'</span><br>  <span class=\"info\">    Initial commit</span>';return'  <span class=\"info\">Git 命令已模拟执行</span>'")
    add_cmd("npm", "return'  <span class=\"info\">npm v10.2.0 (模拟)</span><br>  <span class=\"info\">up to date in 1.2s</span>'")
    add_cmd("pip", "return'  <span class=\"info\">pip 24.0 from /usr/lib/python3 (模拟)</span><br>  <span class=\"info\">Requirement already satisfied: '+arg+' in /usr/lib</span>'")
    add_cmd("make", "return'  <span class=\"info\">make[1]: Entering directory \\'/home/user/project\\'</span><br>  <span class=\"val\">gcc -c main.c -o main.o</span><br>  <span class=\"val\">gcc main.o -o main</span><br>  <span class=\"val\">✓ Build complete</span>'")
    add_cmd("gcc", "return arg?'<span class=\"val\">✓ 编译成功: a.out</span>':'<span class=\"err\">用法: gcc <文件.c></span>'")
    add_cmd("python", "return'  <span class=\"info\">Python 3.12.0 (FusionOS)</span><br>  <span class=\"val\">>>> '+arg+'</span>'")
    add_cmd("node", "return'  <span class=\"info\">Node.js v22.0.0 (FusionOS)</span><br>  <span class=\"val\">> '+arg+'</span>'")
    add_cmd("docker", "return'  <span class=\"warn\">Docker 不支持（浏览器环境）</span>'")
    add_cmd("java", "return'  <span class=\"info\">openjdk version \"21.0.2\" 2024-01-16 (模拟)</span>'")
    add_cmd("ruby", "return'  <span class=\"info\">ruby 3.3.0 (2023-12-25) [x86_64-fusionos]</span>'")
    add_cmd("go", "return'  <span class=\"info\">go version go1.22.0 fusionos/amd64 (模拟)</span>'")
    add_cmd("rustc", "return'  <span class=\"info\">rustc 1.77.0 (模拟)</span>'")
    add_cmd("perl", "return'  <span class=\"info\">This is perl 5, version 38 (模拟)</span>'")
    add_cmd("php", "return'  <span class=\"info\">PHP 8.3.0 (cli) (模拟)</span>'")
    add_cmd("lua", "return'  <span class=\"info\">Lua 5.4.6 (模拟)</span>'")

    # ---- FUN COMMANDS (20) ----
    add_cmd("neofetch", "var u=calcDiskUsed(),f=diskFree();return'<pre style=\"color:#8b949e;font-size:11px;line-height:1.3\"> ╔════════════════════════╗\\n ║   █████╗ ██╗   ██╗ ║\\n ║  ██╔═══╝ ██║   ██║ ║\\n ║  █████╗  ██║   ██║ ║\\n ║  ██╔══╝  ██║   ██║ ║\\n ║  ╚█████╗ ╚██████╔╝ ║\\n ║   ╚════╝   ╚═════╝  ║\\n ╠════════════════════════╣\\n ║ OS:   FusionOS 7.0    ║\\n ║ ARCH: hybrid x86+ARM  ║\\n ║ SHL:  fusion-term     ║\\n ║ DSK: '+fmtSize(f)+' / '+fmtSize(vDisk.total)+'  ║\\n ║ VER:  7.0 ('+APPS.length+' apps)  ║\\n ╚════════════════════════╝</pre>'")
    add_cmd("cowsay", "var t=arg||'FusionOS';return'  <pre style=\"color:#c9d1d9\"> _______________\\n< '+t.substring(0, 13)+' >\\n ---------------\\n        \\\\   ^__^\\n         \\\\  (oo)\\\\_______\\n            (__)\\\\       )\\\\/\\\\\\n                ||----w |\\n                ||     ||<\\/pre>'")
    add_cmd("fortune", "var q=['你今天会很幸运！','代码写完了吗？','FusionOS 是最好的桌面系统','休息一下，喝杯茶吧','Bug 是特性，不是缺陷'];return'  <span class=\"info\">'+q[Math.floor(Math.random()*q.length)]+'</span>'")
    add_cmd("banner", "var t=arg||'FUSION';var r='';for(var i=0;i<7;i++){for(var j=0;j<t.length;j++){r+=t[j]+' ';}r+='<br>';}return'  <pre style=\"color:var(--accent);font-size:10px;line-height:1\">'+r+'</pre>'")
    add_cmd("sl", "return'  <pre style=\"color:#c9d1d9\">      ====        _______________<br>  _D _|  |_______/  |__|__|\\__|<br>   (_)===  |  |  \\\\  ||  |  |<br>  |___|   ==  ==    \\\\__________<br>               CHOO CHOO! 🚂</pre>'")
    add_cmd("cmatrix", "return'  <span class="info">⏃ ⏄ ⏅ ⏆ ⏇ — 矩阵模式已激活（视觉模拟）</span>'")
    add_cmd("figlet", "var t=arg||'FUSION';return'  <pre style=\"color:var(--accent);font-size:10px;line-height:1.1\"> _____ _   _ ____ ___ ___  _   _ <br>|  ___| | | / ___|_ _/ _ \\\\| \\\\ | |<br>| |_  | | | \\\\___ \\\\| | | | |  \\\\| |<br>|  _| | |_| |___) | | |_| | |\\\\  |<br>|_|    \\\\___/|____/___\\\\___/|_| \\\\_|<\\/pre>'")
    add_cmd("nyancat", "return'  <pre style=\"color:#ff69b4\">  ／l、     🌈<br>（ﾟ､ ｡ ７    🌈🌈<br>  l  ~ヽ    🌈🌈🌈<br>  じしf_,)ノ  🌈🌈🌈🌈 meow~</pre>'")
    add_cmd("rig", "return'  <span class=\"val\">身份已生成:</span><br>  姓名: 张伟<br>  地址: 北京市朝阳区XX路100号<br>  电话: 138****5678'")
    add_cmd("rev", "return'  <span class=\"val\">'+arg.split('').reverse().join('')+'</span>'")
    add_cmd("yes", "return'  <span class=\"info\">y y y y y y y y ... (Ctrl+C 停止)</span>'")
    add_cmd("factor", "var n=parseInt(arg)||42;var f=[];for(var i=2;i<=n;i++){while(n%i===0){f.push(i);n/=i;}}return'  <span class=\"val\">'+f.join(' ')+'</span>'")
    add_cmd("jot", "return'  <span class=\"val\">1 2 3 4 5 6 7 8 9 10</span>'")
    add_cmd("asciiquarium", "return'  <pre style=\"color:#42a5f5\">   ><(((*>   <°)))><   ><(((*></pre>  <span style=\"color:#8b949e\">🐟🐠🐡 水族馆模式</span>'")
    add_cmd("cowsay-fusion", "return'  <pre style=\"color:#c9d1d9\"> _________________\\n< FusionOS 4ever >\\n -----------------\\n    \\\\   ^__^\\n     \\\\  (oo)_______\\n        (__)       )\\n            ||----w |\\n            ||     ||</pre>'")
    add_cmd("ponysay", "return'  <pre style=\"color:#ff69b4\">🦄  FusionOS is magic!  🦄</pre>'")
    add_cmd("lolcat", "return'  <span style=\"color:#ff6b6b\">R</span><span style=\"color:#ffd93d\">a</span><span style=\"color:#6bcb77\">i</span><span style=\"color:#4d96ff\">n</span><span style=\"color:#ff6b6b\">b</span><span style=\"color:#ffd93d\">o</span><span style=\"color:#6bcb77\">w</span>'")
    add_cmd("espeak", "return'  <span class=\"warn\">TTS 功能不可用（浏览器限制）</span>'")

    # ---- MATH & CALC (10) ----
    add_cmd("calc", "try{var expr=arg.replace(/[^0-9+*/().\\s-]/g,'');if(!expr)return'  <span class=\"err\">用法: calc <表达式></span>';return'  <span class=\"val\">= '+eval(expr)+'</span>'}catch(e){return'  <span class=\"err\">计算错误</span>'}")
    add_cmd("bc", "try{var expr=arg.replace(/[^0-9+*/().\\s-]/g,'');if(!expr)return'  <span class=\"err\">用法: bc <<< \"表达式\"</span>';return'  <span class=\"val\">'+eval(expr)+'</span>'}catch(e){return'  <span class=\"err\">错误</span>'}")
    add_cmd("expr", "try{var r=eval(arg.replace(/[^0-9+*/().\\s-]/g,''));return'  <span class=\"val\">'+r+'</span>'}catch(e){return'  <span class=\"err\">表达式错误</span>'}")
    add_cmd("units", "return'  <span class=\"warn\">请使用\"单位换算\"应用</span>'")
    add_cmd("seq", "return'  <span class=\"val\">1 2 3 4 5 6 7 8 9 10</span>'")
    add_cmd("numfmt", "return'  <span class=\"val\">'+parseInt(arg||1024).toLocaleString()+'</span>'")
    add_cmd("shuf", "return'  <span class=\"val\">7 3 9 1 5 8 2 4 6 10</span>'")
    add_cmd("rand", "return'  <span class=\"val\">'+Math.floor(Math.random()*100)+'</span>'")
    add_cmd("prime", "function isPrime(n){for(var i=2;i*i<=n;i++)if(n%i===0)return false;return n>1;}var n=parseInt(arg)||17;return'  <span class=\"val\">'+(isPrime(n)?'是质数':'不是质数')+'</span>'")
    add_cmd("fib", "var n=parseInt(arg)||10;var a=0,b=1,r=[0];for(var i=1;i<n;i++){var t=b;b=a+b;a=t;r.push(a);}return'  <span class=\"val\">'+r.join(' ')+'</span>'")

    # ---- CRYPTO & SECURITY (10) ----
    add_cmd("md5sum", "return'  <span class=\"val\">d41d8cd98f00b204e9800998ecf8427e  -</span>'")
    add_cmd("sha256sum", "return'  <span class=\"val\">e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -</span>'")
    add_cmd("base64", "return arg?'  <span class=\"val\">'+btoa(unescape(encodeURIComponent(arg)))+'</span>':'<span class=\"err\">用法: base64 <文本></span>'")
    add_cmd("openssl", "return'  <span class=\"warn\">OpenSSL 功能不可用（浏览器限制）</span>'")
    add_cmd("gpg", "return'  <span class=\"warn\">GPG 功能不可用（浏览器限制）</span>'")
    add_cmd("ssh-keygen", "return'  <span class=\"val\">✓ 已生成密钥对:</span><br>  ~/.ssh/id_rsa<br>  ~/.ssh/id_rsa.pub<br>  <span style=\"color:#8b949e\">指纹: SHA256:abc123...</span>'")
    add_cmd("passwd", "return'  <span class=\"info\">更改密码功能已模拟</span><br>  <span class=\"val\">✓ 密码已更新</span>'")
    add_cmd("chroot", "return'  <span class=\"warn\">chroot 需要 root 权限</span>'")
    add_cmd("sudo", "return'  <span class=\"info\">'+arg+' (已以超级用户身份模拟执行)</span>'")
    add_cmd("su", "return'  <span class=\"info\">已切换为 root (模拟)</span>'")

    # ---- FILE OPERATIONS (10) ----
    add_cmd("tar", "return'  <span class=\"val\">✓ 已创建归档: archive.tar</span>'")
    add_cmd("gzip", "return'  <span class=\"val\">✓ 已压缩: '+arg+'.gz</span>'")
    add_cmd("zip", "return'  <span class=\"val\">✓ 已打包: archive.zip</span>'")
    add_cmd("unzip", "return'  <span class=\"val\">✓ 已解压到当前目录</span>'")
    add_cmd("dd", "return'  <span class=\"val\">✓ 模拟写入完成<br>8+0 records in<br>8+0 records out</span>'")
    add_cmd("sync", "return'  <span class=\"val\">✓ 已同步磁盘缓存</span>'")
    add_cmd("stat", "return'  <span class=\"val\">File: '+arg+'<br>Size: '+Math.floor(Math.random()*10000)+'<br>Blocks: '+Math.floor(Math.random()*20)+'<br>Access: (0644/-rw-r--r--)</span>'")
    add_cmd("realpath", "return'  <span class=\"path\">/home/user/'+arg+'</span>'")
    add_cmd("mktemp", "return'  <span class=\"path\">/tmp/tmp.'+Math.random().toString(36).slice(2,10)+'</span>'")
    add_cmd("truncate", "return'  <span class=\"val\">✓ 已截断文件</span>'")

    # ---- DATABASE (5) ----
    add_cmd("sqlite3", "return'  <span class=\"info\">SQLite version 3.45.0 (模拟)</span><br>  <span class=\"val\">sqlite> </span>'")
    add_cmd("redis-cli", "return'  <span class=\"info\">redis 127.0.0.1:6379> PONG</span>'")
    add_cmd("mysql", "return'  <span class=\"info\">MySQL 8.0 (模拟) — 连接本地数据库</span>'")
    add_cmd("mongo", "return'  <span class=\"info\">MongoDB shell 7.0 (模拟)</span>'")
    add_cmd("psql", "return'  <span class=\"info\">psql (PostgreSQL) 16.0 (模拟)</span>'")

    # ---- FUSIONOS SPECIFIC (15) ----
    add_cmd("notify", "if(!arg)return'  <span class=\"err\">用法: notify <消息></span>';addNotif('终端通知',arg,'ic-bell');return'  <span class=\"val\">✓ 通知已发送</span>'")
    add_cmd("open", "if(!arg)return'  <span class=\"err\">用法: open <应用名></span>';var app=APPS.find(function(a){return a.id===arg||a.name.indexOf(arg)===0});if(app){openApp(app.id);return'  <span class=\"val\">✓ 已打开 '+app.name+'</span>';}return'  <span class=\"err\">未找到应用: '+arg+'</span>'")
    add_cmd("wallpaper", "var walls=['','2','3','4','5','6'];setSetting('wallpaper',walls[Math.floor(Math.random()*walls.length)]);applyAllSettings();return'  <span class=\"val\">✓ 壁纸已随机切换</span>'")
    add_cmd("save", "saveState();return'  <span class=\"val\">✓ 系统状态已保存</span>'")
    add_cmd("reset", "if(!confirm('确定要清除所有数据?'))return'  <span class=\"info\">已取消</span>';localStorage.clear();location.reload();return'  <span class=\"val\">✓ 正在重置...</span>'")
    add_cmd("info", "return'  <span class=\"val\">FusionOS 7.0</span><br>  '+APPS.length+' 个应用 | 170+ 终端命令<br>  '+Object.keys(windows).filter(function(k){return windows[k]&&!windows[k].closed}).length+' 个打开窗口<br>  运行时间: '+Math.floor((Date.now()-(window._bootTime||Date.now()))/1000)+'s'")
    add_cmd("debug", "return'  <span class=\"val\">VFS: </span>'+JSON.stringify(Object.keys(VFS))+'<br>  <span class=\"val\">Windows: </span>'+Object.keys(windows).filter(function(k){return windows[k]&&!windows[k].closed}).length+'<br>  <span class=\"val\">Focused: </span>'+focusedWin+'<br>  <span class=\"val\">winZ: </span>'+winZ+'<br>  <span class=\"val\">Notifs: </span>'+notifs.length")
    add_cmd("perf", "return'  <span class=\"val\">性能评分: '+calcPerfScore()+'/10</span>'")
    add_cmd("credits", "return'  <span class=\"val\">FusionOS 7.0 — Credits</span><br>  开发者: Fusion Team<br>  图标: 自定义 SVG<br>  壁纸: FusionOS<br>  技术栈: HTML/CSS/JS (零依赖)'")
    add_cmd("license", "return'  <span class=\"info\">FusionOS 7.0 License</span><br>  MIT License (模拟)<br>  Copyright © 2026 FusionOS'")
    add_cmd("changelog", "return'  <span class=\"val\">v7.0 — 2026-06-15</span><br>  + 15 个新应用<br>  + 3 个游戏（扫雷/俄罗斯方块/打砖块）<br>  + 170+ 终端命令<br>  + 100 个系统功能'")
    add_cmd("update", "return'  <span class=\"val\">✓ 已是最新版本 (7.0)</span>'")
    add_cmd("donate", "return'  <span style=\"color:#ffd700\">⭐ 感谢支持！FusionOS 永远免费。</span>'")
    add_cmd("cmds", "return'  <span class=\"info\">共 170+ 条命令，输入 help-cat <类别> 查看:</span><br>  core · sysinfo · net · monitor · text · dev · fun · math · crypto · file · db · fusion'")
    add_cmd("help-cat", "var cats={core:'ls cd pwd cat mkdir touch rm rmdir echo clear write cp mv ln chmod chown find grep wc sort uniq head tail cut diff file which whereis type tee yes tr',sysinfo:'uname hostname whoami who id groups uptime arch dmesg lscpu lsblk lspci mount vmstat',net:'ping curl wget ifconfig ip netstat ss nslookup dig traceroute ssh ftp nc wifi speedtest',monitor:'ps top free df du iostat iotop mpstat sensors hwinfo',text:'awk sed nl fmt strings xxd column sponge split csplit',dev:'git npm pip make gcc python node docker java ruby go rustc perl php lua',fun:'neofetch cowsay fortune banner sl cmatrix figlet nyancat rig rev factor jot asciiquarium ponysay lolcat espeak',math:'calc bc expr units seq numfmt shuf rand prime fib',crypto:'md5sum sha256sum base64 openssl gpg ssh-keygen passwd chroot sudo su',file_:'tar gzip zip unzip dd sync stat realpath mktemp truncate',db:'sqlite3 redis-cli mysql mongo psql',fusion:'notify open wallpaper save reset info debug perf credits license changelog update donate'};var cat=cats[arg||'core']||cats.core;return'  <span class=\"cmd\">'+cat.split(' ').join('</span>  <span class=\"cmd\">')+'</span>'")

    # ---- MISC (15) ----
    add_cmd("date", "return'  '+new Date().toLocaleString('zh-CN')")
    add_cmd("time", "return'  <span class=\"val\">实际使用: 0.02s user, 0.01s system</span>'")
    add_cmd("watch", "return'  <span class=\"info\">Every 2.0s: '+arg+' (模拟)</span>'")
    add_cmd("xargs", "return'  <span class=\"warn\">请在管道中使用</span>'")
    add_cmd("man", "return arg?'  <span class=\"info\">'+arg.toUpperCase()+'(1)  — 手册页（模拟）</span><br>  <span style=\"color:#8b949e\">手册不可用。尝试: help</span>':'  <span class=\"err\">What manual page do you want?</span>'")
    add_cmd("alias", "return'  <span class=\"val\">alias ll=\\'ls -la\\'<br>alias la=\\'ls -A\\'<br>alias ..=\\'cd ..\\'</span>'")
    add_cmd("unalias", "return'  <span class=\"val\">✓ 已移除别名</span>'")
    add_cmd("export", "return'  <span class=\"val\">HOME=/home/user<br>PATH=/usr/bin:/bin<br>USER=user<br>SHELL=fusion-term<br>TERM=xterm-256color<br>LANG=zh_CN.UTF-8</span>'")
    add_cmd("env", "return'  <span class=\"val\">HOME=/home/user</span><br>  <span class=\"val\">PATH=/usr/bin:/bin</span><br>  <span class=\"val\">USER=user</span><br>  <span class=\"val\">SHELL=fusion-term</span><br>  <span class=\"val\">FUSION_VERSION=7.0</span>'")
    add_cmd("history", "return'  <span class=\"val\">1  ls</span><br>  <span class=\"val\">2  pwd</span><br>  <span class=\"val\">3  neofetch</span><br>  <span class=\"val\">4  '+cmd+'</span>'")
    add_cmd("printenv", "return'  <span class=\"val\">HOME=/home/user<br>USER=user<br>SHELL=fusion-term</span>'")
    add_cmd("logout", "doLogout();return'  <span class=\"val\">正在注销...</span>'")
    add_cmd("shutdown", "doShutdown();return'  <span class=\"val\">正在关机...</span>'")
    add_cmd("reboot", "doRestart();return'  <span class=\"val\">正在重启...</span>'")
    add_cmd("lock", "doLock();return'  <span class=\"val\">✓ 屏幕已锁定</span>'")

    # Add extra ones to reach 170+
    add_cmd("tree", "return'  <span class=\"path\">/</span><br>  ├── <span class=\"path\">用户/</span><br>  │   ├── <span class=\"path\">文档/</span><br>  │   ├── <span class=\"path\">图片/</span><br>  │   ├── <span class=\"path\">音乐/</span><br>  │   └── <span class=\"path\">桌面/</span><br>  ├── <span class=\"path\">系统/</span><br>  └── <span class=\"path\">应用/</span>'")
    add_cmd("version", "return'  <span class=\"val\">FusionOS 7.0</span> — Build '+new Date().toLocaleDateString('zh-CN')+'<br>  Kernel: fusionos-7.0-generic<br>  Shell: fusion-term 7.0<br>  Apps: '+APPS.length+'<br>  Features: 150+'")
    add_cmd("sysinfo", "return'  <span class=\"val\">=== 系统信息 ===</span><br>  OS: FusionOS 7.0<br>  Kernel: fusionos-7.0<br>  CPU: Virtual x86_64 @ 3.2GHz<br>  RAM: 16GB<br>  Disk: FusionDisk 16GB<br>  Apps: '+APPS.length+'<br>  Terminal: 170+ commands'")
    add_cmd("ascii", "return'  <pre style=\"color:var(--accent);font-size:8px;line-height:1\"> ███████╗██╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗<br> ██╔════╝██║   ██║██╔════╝██║██╔═══██╗████╗  ██║<br> █████╗  ██║   ██║███████╗██║██║   ██║██╔██╗ ██║<br> ██╔══╝  ██║   ██║╚════██║██║██║   ██║██║╚██╗██║<br> ██║     ╚██████╔╝███████║██║╚██████╔╝██║ ╚████║<br> ╚═╝      ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝</pre>'")
    add_cmd("fetch", "return'  <span class=\"val\">'+getGreeting()+'！</span><br>  <span class=\"info\">FusionOS 7.0 已就绪</span>'")
    add_cmd("uptime-short", "var s=Math.floor((Date.now()-(window._bootTime||Date.now()))/1000);return'  <span class=\"val\">'+s+'s</span>'")
    add_cmd("quote", "var q=['代码就是诗','少即是多','保持简单，保持优雅','好的软件是迭代出来的'];return'  <span class=\"info\">' + q[Math.floor(Math.random()*q.length)] + '</span>'")
    add_cmd("joke", "var j=['为什么程序员不喜欢户外活动？太多bug了！','0和1走进一家酒吧...','调试就像一场谋杀谜案，而你是侦探'];return'  <span class=\"info\">'+j[Math.floor(Math.random()*j.length)]+'</span>'")
    add_cmd("hack", "return'  <pre style=\"color:#00ff00;font-size:10px;line-height:1\">[+] Initializing hack module...<br>[+] Bypassing firewall... OK<br>[+] Accessing target... 192.168.1.1<br>[+] Decrypting data... 0xDEADBEEF<br>[-] ERROR: This is a simulation<br>[+] Disconnecting... OK</pre>'")
    add_cmd("matrix", "return'  <span style=\"color:#00ff00\">⏃ ⏄ ⏅ ⏆ ⏇ ⏈ ⏉ ⏊ ⏋ ⏌</span><br>  <span style=\"color:#00ff00\">逃离矩阵，进入 FusionOS</span>'")
    add_cmd("rickroll", "return'  <span class=\"warn\">Never gonna give you up 🎵<br>Never gonna let you down 🎵</span>'")
    add_cmd("thanks", "return'  <span class=\"info\">感谢使用 FusionOS 7.0！💙</span>'")

    # Now add the rest of the termExec
    new_term_parts.extend(cmd_entries)
    new_term_parts.append("  var fn=O[c];out.innerHTML=fn?fn():'  <span class=\"err\">'+c+': 命令未找到</span><br>  <span style=\"color:#8b949e\">输入 help 查看命令，输入 cmds 查看所有命令</span>';")
    new_term_parts.append("  tl.appendChild(out);var term=document.getElementById('term-'+id);if(term)term.scrollTop=term.scrollHeight;")
    new_term_parts.append("}")
    
    lines = lines[:start_idx] + new_term_parts[-4:] + lines[end_idx+1:]
    
    print("Terminal replaced with 170+ commands")
else:
    print("ERROR: Could not find termExec function!")

# ============================================================
# Also update the renderTerminal to say 170+ commands
# ============================================================
for i, line in enumerate(lines):
    if 'FusionOS Terminal v6.0' in line:
        lines[i] = lines[i].replace('FusionOS Terminal v6.0', 'FusionOS Terminal 7.0').replace('输入 help 查看命令', '输入 help 查看命令 (170+条)')
    if 'FusionOS 6.0' in line and 'Text' not in line and 'code-editor' not in line and 'neofetch' not in line and i > 1700 and i < 2000:
        lines[i] = lines[i].replace('FusionOS 6.0', 'FusionOS 7.0')

with open(FILE, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines))

print(f"Phase 3 done: Terminal 170+ cmds ({len(lines)} lines)")
