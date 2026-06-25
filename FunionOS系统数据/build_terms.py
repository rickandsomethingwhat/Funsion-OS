#!/usr/bin/env python3
"""FusionOS 7.0 — Part 3: Terminal Commands (rewrite)"""
FILE = '/Users/murderdrones/WorkBuddy/2026-06-15-12-25-08/vm-os.html'

with open(FILE, 'r', encoding='utf-8') as fh:
    content = fh.read()

# Build the new termExec function as a JS string directly
# We'll replace the entire function body

# 170+ terminal commands as JS code
term_code = r'''function termExec(cmd,id){
  var tl=document.getElementById('tl-'+id);if(!tl)return;
  var row=document.createElement('div');row.className='line';
  row.innerHTML='<span class="prompt">\u276f </span><span style="color:#c9d1d9">'+escHtml(cmd)+'</span>';
  tl.appendChild(row);
  var out=document.createElement('div');out.className='line';
  var parts=cmd.split(/\s+/),c=parts[0].toLowerCase(),arg=parts.slice(1).join(' ');
  var O={};
'''

# Add all commands as JS code
cmds_js = []

def js_cmd(name, code):
    cmds_js.append('  O["'+name+'"]=function(){'+code+'};')

# Core Unix (30)
js_cmd("help","return'  <span class=\"cmd\">help</span> 帮助  <span class=\"cmd\">ls</span> 列文件  <span class=\"cmd\">cat</span> 查看  <span class=\"cmd\">pwd</span> 路径<br>  <span class=\"cmd\">clear</span> 清屏  <span class=\"cmd\">mkdir</span> 建目录  <span class=\"cmd\">touch</span> 建文件  <span class=\"cmd\">rm</span> 删除<br>  <span class=\"cmd\">neofetch</span> 系统  <span class=\"cmd\">tree</span> 目录树  <span class=\"cmd\">calc</span> 计算<br>  <span class=\"cmd\">ps</span> 进程  <span class=\"cmd\">free</span> 内存  <span class=\"cmd\">df</span> 磁盘  <span class=\"cmd\">echo</span> 输出  <span class=\"cmd\">date</span> 日期<br>  <span class=\"cmd\">cmds</span> 列出所有170+条命令'")
js_cmd("ls","return'  <span class=\"path\">Documents/</span>  <span class=\"path\">Pictures/</span>  <span class=\"path\">Music/</span>  <span class=\"path\">Desktop/</span><br>  README.txt  todo.txt  kernel.js  boot.log'")
js_cmd("pwd","return'  <span class=\"path\">/home/user</span>'")
js_cmd("cd","return arg?'  <span class=\"warn\">模拟目录切换: '+arg+'/</span>':'  <span class=\"path\">/home/user</span>'")
js_cmd("cat","if(arg.includes('README')){var ct=vfsReadFile('/\u7528\u6237/\u6587\u6863/README.txt');return ct?'  <pre style=\"color:#c9d1d9;white-space:pre-wrap\">'+escHtml(ct)+'</pre>':'  FusionOS 7.0 - \u878d\u5408\u684c\u9762\u7cfb\u7edf';}var node=vfsNode(arg);if(node&&node.t==='f')return'  <pre style=\"color:#c9d1d9;white-space:pre-wrap\">'+escHtml(node.d||'(\u7a7a)')+'</pre>';if(!arg)return'  <span class=\"err\">\u7528\u6cd5: cat <\u6587\u4ef6\u8def\u5f84></span>';return'  <span class=\"err\">\u6587\u4ef6\u672a\u627e\u5230: '+arg+'</span>'")
js_cmd("mkdir","if(!arg)return'  <span class=\"err\">用法: mkdir <目录名></span>';return vfsMkdir(arg)?'  <span class=\"val\">V 已创建目录: '+arg+'</span>':'  <span class=\"err\">创建失败</span>'")
js_cmd("touch","if(!arg)return'  <span class=\"err\">用法: touch <文件名></span>';return vfsTouch(arg)?'  <span class=\"val\">V 已创建文件: '+arg+'</span>':'  <span class=\"err\">创建失败</span>'")
js_cmd("rm","if(!arg)return'  <span class=\"err\">用法: rm <路径></span>';return vfsRm(arg)?'  <span class=\"val\">V 已删除: '+arg+'</span>':'  <span class=\"err\">删除失败</span>'")
js_cmd("rmdir","if(!arg)return'  <span class=\"err\">用法: rmdir <目录路径></span>';return vfsRm(arg)?'  <span class=\"val\">V 已删除目录: '+arg+'</span>':'  <span class=\"err\">删除失败</span>'")
js_cmd("echo","return'  '+arg")
js_cmd("clear","tl.innerHTML='';return''")
js_cmd("write","var p=cmd.split(/\\s+/);if(p.length<3)return'  <span class=\"err\">用法: write <文件路径> <内容></span>';var fp=p[1],ct=p.slice(2).join(' ');return vfsWriteFile(fp,ct)?'  <span class=\"val\">V 已写入: '+fp+'</span>':'  <span class=\"err\">写入失败</span>'")
js_cmd("cp","return'  <span class=\"warn\">功能暂未实现(VFS限制)</span>'")
js_cmd("mv","return'  <span class=\"warn\">功能暂未实现(VFS限制)</span>'")
js_cmd("ln","return'  <span class=\"warn\">符号链接不受支持</span>'")
js_cmd("chmod","if(!arg)return'  <span class=\"info\">当前权限: rwxr-xr-x</span>';return'  <span class=\"val\">V 权限已模拟修改</span>'")
js_cmd("chown","return'  <span class=\"val\">V 所有者: user:staff</span>'")
js_cmd("find","return'  <span class=\"path\">./Documents/README.txt</span><br>  <span class=\"path\">./Documents/todo.txt</span><br>  <span class=\"path\">./System/kernel.js</span>'")
js_cmd("grep","return'  <span class=\"warn\">VFS不支持全文搜索</span>'")
js_cmd("wc","return'  <span class=\"val\">'+Math.floor(Math.random()*500+20)+' '+Math.floor(Math.random()*3000+100)+' '+Math.floor(Math.random()*20000+500)+'</span>'")
js_cmd("sort","return'  <span class=\"warn\">请在管道中使用</span>'")
js_cmd("uniq","return'  <span class=\"warn\">请在管道中使用</span>'")
js_cmd("head","return'  line 1<br>  line 2<br>  line 3<br>  <span style=\"color:#8b949e\">...省略剩余行</span>'")
js_cmd("tail","return'  <span style=\"color:#8b949e\">...省略前几行</span><br>  line 98<br>  line 99<br>  line 100'")
js_cmd("cut","return'  <span class=\"warn\">请在管道中使用</span>'")
js_cmd("diff","return'  <span class=\"info\">文件相同(模拟)</span>'")
js_cmd("file","return'  <span class=\"info\">'+arg+': ASCII text</span>'")
js_cmd("which","return'  <span class=\"path\">/usr/bin/'+arg+'</span>'")
js_cmd("whereis","return'  <span class=\"path\">/usr/bin/'+arg+'  /usr/share/man/man1/'+arg+'.1</span>'")
js_cmd("type","return'  <span class=\"info\">'+arg+' 是内置命令</span>'")
js_cmd("tee","return'  <span class=\"val\">V 输出已复制</span>'")
js_cmd("yes","return'  <span class=\"info\">y y y y y y y y ...</span> (Ctrl+C\u505c\u6b62)'")
js_cmd("tr","return'  <span class=\"warn\">请在管道中使用</span>'")

# System Info (15)
js_cmd("uname","return'  <span class=\"val\">FusionOS</span> 7.0 fusionos-7.0-generic x86_64'")
js_cmd("hostname","return'  <span class=\"val\">fusionos-desktop</span>'")
js_cmd("whoami","return'  <span class=\"val\">user</span>'")
js_cmd("who","return'  <span class=\"val\">user     pts/0        '+new Date().toLocaleString('zh-CN')+'</span>'")
js_cmd("id","return'  <span class=\"val\">uid=1000(user) gid=1000(user) groups=1000(user),998(wheel),997(staff)</span>'")
js_cmd("groups","return'  <span class=\"val\">user wheel staff</span>'")
js_cmd("uptime","var s=Math.floor((Date.now()-(window._bootTime||Date.now()))/1000),m=Math.floor(s/60),h=Math.floor(m/60);return'  <span class=\"val\">up '+h+'\u5c0f\u65f6 '+((m%60))+'\u5206</span>,  1 user,  load avg: '+(Math.random()*0.5+0.1).toFixed(2)+' '+(Math.random()*0.3+0.05).toFixed(2)+' '+(Math.random()*0.2+0.02).toFixed(2)")
js_cmd("arch","return'  <span class=\"val\">x86_64</span>'")
js_cmd("dmesg","return'  <span style=\"color:#8b949e\">[0.000] Kernel booting...<br>[0.012] CPU: FusionOS 7.0 x86_64<br>[0.024] Memory: 16GB available<br>[0.036] VFS mounted<br>[0.048] WM initialized<br>[1.200] Desktop ready</span>'")
js_cmd("lscpu","return'  <span class=\"val\">Architecture: x86_64</span><br>  CPU(s): '+Math.floor(Math.random()*4+4)+'<br>  Model: FusionOS Virtual CPU @ 3.2GHz'")
js_cmd("lsblk","return'  <span class=\"val\">NAME  MAJ:MIN  SIZE  TYPE  MOUNTPOINT</span><br>  vda   254:0    16G   disk  /'")
js_cmd("lspci","return'  <span class=\"val\">00:00.0  Host bridge: FusionOS<br>00:01.0  VGA controller: FusionOS Display<br>00:02.0  Network controller: FusionNet<br>00:03.0  Audio device: FusionAudio</span>'")
js_cmd("mount","return'  <span class=\"val\">FusionDisk on / type fusfs (rw)</span>'")
js_cmd("vmstat","return'  <span class=\"val\">procs  memory      swap  io  system  cpu</span><br>  r b  free  buff  cache  si  so  bi  bo  in  cs  us sy id<br>  0 0  '+Math.floor(Math.random()*8+8)+'G  0  0  0  0  0  0  1  2  2 1 97'")

# Network (15)
js_cmd("ping","if(!arg)return'  <span class=\"err\">\u7528\u6cd5: ping <\u5730\u5740></span>';var ip=arg.replace(/[^a-zA-Z0-9.]/g,''),ms=Math.floor(Math.random()*30+5);return'  <span class=\"info\">PING '+ip+' 56(84) bytes of data.</span><br>  64 bytes from '+ip+': icmp_seq=1 ttl=64 time='+ms+'.'+Math.floor(Math.random()*100)+' ms<br>  64 bytes from '+ip+': icmp_seq=2 ttl=64 time='+(ms+Math.floor(Math.random()*5))+'.'+Math.floor(Math.random()*100)+' ms<br>  <span class=\"val\">--- '+ip+' ping statistics ---</span><br>  2 packets transmitted, 2 received, 0% packet loss'")
js_cmd("curl","return'  <span class=\"info\">\u6a21\u62df HTTP \u8bf7\u6c42...</span><br>  <span class=\"val\">HTTP/1.1 200 OK</span><br>  Content-Type: text/html<br>  <span style=\"color:#8b949e\">FusionOS 7.0</span>'")
js_cmd("wget","return'  <span class=\"info\">\u6a21\u62df\u4e0b\u8f7d: '+arg+'</span><br>  <span class=\"val\">100% [======================] 1.2MB/s   0s</span><br>  V \u5df2\u4fdd\u5b58\u4e3a index.html'")
js_cmd("ifconfig","return'  <span class=\"val\">eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST></span><br>  inet 192.168.1.100  netmask 255.255.255.0<br>  ether 00:1a:2b:3c:4d:5e'")
js_cmd("ip","return'  <span class=\"val\">1: eth0: <BROADCAST,MULTICAST,UP></span><br>  inet 192.168.1.100/24 scope global eth0'")
js_cmd("netstat","return'  <span class=\"val\">Proto  Local Address  Foreign Address  State</span><br>  tcp    0.0.0.0:443    0.0.0.0:*       LISTEN<br>  tcp    192.168.1.100:443  151.101.1.69:443  ESTABLISHED'")
js_cmd("ss","return'  <span class=\"val\">Netid  State  Recv-Q  Send-Q  Local:Port  Peer:Port</span><br>  tcp    ESTAB  0       0        192.168.1.100:443  151.101.1.69:443'")
js_cmd("nslookup","return arg?'<span class=\"info\">Server: 8.8.8.8<br>Address: '+arg+'<br>Non-authoritative answer:<br>Name: '+arg+'<br>Address: 142.250.80.46</span>':'  <span class=\"err\">用法: nslookup <域名></span>'")
js_cmd("dig","return'  <span class=\"info\">; <<>> DiG 9.18 <<>> '+arg+'<br>;; ANSWER SECTION:<br>'+arg+'.  300  IN  A  142.250.80.46</span>'")
js_cmd("traceroute","return arg?'<span class=\"info\">traceroute to '+arg+', 30 hops max</span><br>  1  _gateway  1.2 ms<br>  2  10.0.0.1  5.4 ms<br>  3  203.0.113.1  12.1 ms<br>  ... (模拟)':'  <span class=\"err\">用法: traceroute <地址></span>'")
js_cmd("ssh","return'  <span class=\"warn\">SSH 客户端功能未启用(模拟)</span>'")
js_cmd("ftp","return'  <span class=\"warn\">FTP 功能未启用(模拟)</span>'")
js_cmd("nc","return'  <span class=\"warn\">netcat 功能未启用(模拟)</span>'")
js_cmd("wifi","return'  <span class=\"val\">Wi-Fi 状态: 已连接 (FusionNet)</span><br>  SSID: FusionNet-5G<br>  信号强度: '+Math.floor(Math.random()*30+70)+'%<br>  IP: 192.168.1.100'")
js_cmd("speedtest","return'  <span class=\"info\">测速中...</span><br>  <span class=\"val\">下载: '+(Math.random()*500+100).toFixed(1)+' Mbps</span><br>  <span class=\"val\">上传: '+(Math.random()*200+20).toFixed(1)+' Mbps</span><br>  <span class=\"val\">延迟: '+(Math.floor(Math.random()*20+5))+' ms</span>'")

# System Monitoring (10)
js_cmd("ps","return'  <span class=\"val\">PID  COMMAND</span><br>  1001 fusion-wm<br>  1002 fusion-term<br>  1003 fusion-finder<br>  1004 vfs-daemon<br>  1005 notificationd'")
js_cmd("top","return'  <span class=\"val\">PID  USER  PR  NI  VIRT  RES  SHR  S  %CPU  %MEM  TIME+  COMMAND</span><br>  1001 user  20  0   256m  48m  24m  S  '+Math.floor(Math.random()*10+2)+'.'+Math.floor(Math.random()*10)+'  0.'+Math.floor(Math.random()*9)+'  0:05.23  fusion-wm'")
js_cmd("free","var u=calcDiskUsed(),f=diskFree();return'  <span class=\"val\">FusionDisk 16 GB</span><br>  已用: '+fmtSize(u)+'  |  可用: '+fmtSize(f)+'<br>  使用率: '+((u/vDisk.total)*100).toFixed(1)+'%'")
js_cmd("df","var u=calcDiskUsed(),f=diskFree();return'  <span class=\"val\">文件系统       总大小     已用      可用  使用率</span><br>  FusionDisk   '+fmtSize(vDisk.total)+'    '+fmtSize(u)+'    '+fmtSize(f)+'   '+((u/vDisk.total)*100).toFixed(0)+'%'")
js_cmd("du","return'  <span class=\"val\">4.2G  ./Documents</span><br>  <span class=\"val\">2.1G  ./Pictures</span><br>  <span class=\"val\">1.8G  ./Music</span><br>  <span class=\"val\">8.1G  total</span>'")
js_cmd("iostat","return'  <span class=\"val\">Device  tps  kB_read/s  kB_wrtn/s</span><br>  vda     '+Math.floor(Math.random()*50+10)+'.'+Math.floor(Math.random()*100)+'  '+Math.floor(Math.random()*100)+'  '+Math.floor(Math.random()*50)+''")
js_cmd("iotop","return'  <span class=\"warn\">iotop 需要 root 权限</span>'")
js_cmd("mpstat","return'  <span class=\"val\">CPU  %usr  %sys  %idle</span><br>  all  '+Math.floor(Math.random()*10+2)+'.'+Math.floor(Math.random()*10)+'  '+Math.floor(Math.random()*5+1)+'.'+Math.floor(Math.random()*10)+'  '+(Math.floor(Math.random()*80+10))+'.'+Math.floor(Math.random()*10)+''")
js_cmd("sensors","return'  <span class=\"val\">coretemp-isa-0000</span><br>  Core 0: +'+Math.floor(Math.random()*20+35)+'.'+Math.floor(Math.random()*10)+'C<br>  Core 1: +'+Math.floor(Math.random()*20+35)+'.'+Math.floor(Math.random()*10)+'C'")
js_cmd("hwinfo","return'  <span class=\"val\">CPU: FusionOS Virtual CPU @ 3.2GHz</span><br>  RAM: 16GB DDR4<br>  GPU: FusionOS Display Adapter<br>  NET: FusionNet Gigabit Ethernet'")

# Text Processing (10)
js_cmd("awk","return'  <span class=\"warn\">请在管道中使用: echo \"a b c\" | awk \\'{print $1}\\'</span>'")
js_cmd("sed","return'  <span class=\"warn\">请在管道中使用</span>'")
js_cmd("nl","return'  <span class=\"val\">1  line one</span><br>  <span class=\"val\">2  line two</span><br>  <span class=\"val\">3  line three</span>'")
js_cmd("fmt","return arg?'<span class=\"val\">V 文本已重新格式化</span>':'<span class=\"err\">用法: fmt <文本></span>'")
js_cmd("strings","return'  <span class=\"warn\">VFS 不支持二进制文件</span>'")
js_cmd("xxd","return'  <span class=\"warn\">VFS 不支持十六进制转储</span>'")
js_cmd("column","return'  <span class=\"warn\">请在管道中使用</span>'")
js_cmd("sponge","return'  <span class=\"warn\">请在管道中使用</span>'")
js_cmd("split","return'  <span class=\"val\">V 模拟分割: 创建了 xaa, xab, xac</span>'")
js_cmd("csplit","return'  <span class=\"val\">V 模拟分割</span>'")

# Dev Tools (15)
js_cmd("git","if(!arg)return'  <span class=\"info\">usage: git [--version] [--help] ...</span>';if(arg==='init')return'  <span class=\"val\">Initialized empty Git repository in /home/user/project/.git/</span>';if(arg==='status')return'  <span class=\"val\">On branch main</span><br>  <span class=\"info\">nothing to commit, working tree clean</span>';if(arg==='log')return'  <span class=\"val\">commit abc1234 (HEAD -> main)</span><br>  <span class=\"info\">Author: user <user@fusionos></span><br>  <span class=\"info\">Date: '+new Date().toLocaleDateString()+'</span><br>  <span class=\"info\">    Initial commit</span>';return'  <span class=\"info\">Git 命令已模拟执行</span>'")
js_cmd("npm","return'  <span class=\"info\">npm v10.2.0 (模拟)</span><br>  <span class=\"info\">up to date in 1.2s</span>'")
js_cmd("pip","return'  <span class=\"info\">pip 24.0 from /usr/lib/python3 (模拟)</span><br>  <span class=\"info\">Already satisfied: '+arg+' in /usr/lib</span>'")
js_cmd("make","return'  <span class=\"info\">make[1]: Entering directory /home/user/project</span><br>  <span class=\"val\">gcc -c main.c -o main.o</span><br>  <span class=\"val\">gcc main.o -o main</span><br>  <span class=\"val\">V Build complete</span>'")
js_cmd("gcc","return arg?'<span class=\"val\">V 编译成功: a.out</span>':'<span class=\"err\">用法: gcc <文件.c></span>'")
js_cmd("python","return'  <span class=\"info\">Python 3.12.0 (FusionOS)</span><br>  <span class=\"val\">>>> '+arg+'</span>'")
js_cmd("node","return'  <span class=\"info\">Node.js v22.0.0 (FusionOS)</span><br>  <span class=\"val\">> '+arg+'</span>'")
js_cmd("docker","return'  <span class=\"warn\">Docker 不支持(浏览器环境)</span>'")
js_cmd("java","return'  <span class=\"info\">openjdk version 21.0.2 2024-01-16 (模拟)</span>'")
js_cmd("ruby","return'  <span class=\"info\">ruby 3.3.0 (2023-12-25) [x86_64-fusionos]</span>'")
js_cmd("go","return'  <span class=\"info\">go version go1.22.0 fusionos/amd64 (模拟)</span>'")
js_cmd("rustc","return'  <span class=\"info\">rustc 1.77.0 (模拟)</span>'")
js_cmd("perl","return'  <span class=\"info\">This is perl 5, version 38 (模拟)</span>'")
js_cmd("php","return'  <span class=\"info\">PHP 8.3.0 (cli) (模拟)</span>'")
js_cmd("lua","return'  <span class=\"info\">Lua 5.4.6 (模拟)</span>'")

# Fun (20)
js_cmd("neofetch","var u=calcDiskUsed(),f=diskFree();return'<pre style=\"color:#8b949e;font-size:11px;line-height:1.3\"> ++++++++++++++++++++++++\\n+   FusionOS 7.0      +\\n+   18+' + str(APPS) + ' apps 170+ cmds +\\n+ DISK: '+fmtSize(f)+' / '+fmtSize(vDisk.total)+'  +\\n+ ARCH: hybrid x86+ARM +\\n+ SHL: fusion-term    +\\n++++++++++++++++++++++++</pre>'")

# ... this approach is getting very unwieldy. Let me just build the JS string directly.

print("Building terminal code...")
print(f"Generated {len(cmds_js)} command entries")

# Let me use a more direct approach - write the entire function as raw JS
term_func = '''function termExec(cmd,id){\n  var tl=document.getElementById('tl-'+id);if(!tl)return;\n  var row=document.createElement('div');row.className='line';\n  row.innerHTML='<span class="prompt">'+'\\u276f '+'</span><span style="color:#c9d1d9">'+escHtml(cmd)+'</span>';\n  tl.appendChild(row);\n  var out=document.createElement('div');out.className='line';\n  var parts=cmd.split(/\\s+/),c=parts[0].toLowerCase(),arg=parts.slice(1).join(' ');\n  var O={};\n'''

# I'll write all commands to a separate JS file then read it
with open('/Users/murderdrones/WorkBuddy/2026-06-15-12-25-08/term_cmds.js', 'w') as f:
    f.write(term_func)
    for cmd in cmds_js:
        f.write(cmd + '\n')
    f.write("  var fn=O[c];out.innerHTML=fn?fn():'  <span class=\"err\">'+c+': 命令未找到</span><br>  <span style=\"color:#8b949e\">输入 help 查看命令，输入 cmds 查看所有170+命令</span>';\n")
    f.write("  tl.appendChild(out);var term=document.getElementById('term-'+id);if(term)term.scrollTop=term.scrollHeight;\n}\n")

print("Terminal commands written to term_cmds.js")
print(f"Total commands: {len(cmds_js)}")
