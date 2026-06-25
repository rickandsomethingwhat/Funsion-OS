#!/usr/bin/env python3
"""Build terminal commands JS directly using a text template approach"""
# Write the complete termExec function directly as JS
with open('/Users/murderdrones/WorkBuddy/2026-06-15-12-25-08/term_cmds.js', 'w') as f:
    f.write('''function termExec(cmd,id){
  var tl=document.getElementById('tl-'+id);if(!tl)return;
  var row=document.createElement('div');row.className='line';
  row.innerHTML='<span class="prompt">\\u276f </span><span style="color:#c9d1d9">'+escHtml(cmd)+'</span>';
  tl.appendChild(row);
  var out=document.createElement('div');out.className='line';
  var parts=cmd.split(/\\s+/),c=parts[0].toLowerCase(),arg=parts.slice(1).join(' ');
  var O={};

  /* ── help ── */
  O['help']=function(){return'  <span class="cmd">help</span> \\u5e2e\\u52a9  <span class="cmd">ls</span> \\u5217\\u6587\\u4ef6  <span class="cmd">cat</span> \\u67e5\\u770b  <span class="cmd">pwd</span> \\u8def\\u5f84<br>  <span class="cmd">clear</span> \\u6e05\\u5c4f  <span class="cmd">mkdir</span> \\u5efa\\u76ee\\u5f55  <span class="cmd">touch</span> \\u5efa\\u6587\\u4ef6  <span class="cmd">rm</span> \\u5220\\u9664<br>  <span class="cmd">neofetch</span> \\u7cfb\\u7edf  <span class="cmd">tree</span> \\u76ee\\u5f55\\u6811  <span class="cmd">calc</span> \\u8ba1\\u7b97<br>  <span class="cmd">ps</span> \\u8fdb\\u7a0b  <span class="cmd">free</span> \\u5185\\u5b58  <span class="cmd">df</span> \\u78c1\\u76d8  <span class="cmd">echo</span> \\u8f93\\u51fa  <span class="cmd">date</span> \\u65e5\\u671f<br>  \\u8f93\\u5165 <span class="cmd">cmds</span> \\u67e5\\u770b172\\u6761\\u547d\\u4ee4';};
  O['cmds']=function(){return'  <span class="info">\\u5171 172 \\u6761\\u547d\\u4ee4\\uff0c\\u8f93\\u5165 help-cat <\\u7c7b\\u522b> \\u67e5\\u770b:</span><br>  core \\u00b7 sysinfo \\u00b7 net \\u00b7 monitor \\u00b7 text \\u00b7 dev \\u00b7 fun \\u00b7 math \\u00b7 crypto \\u00b7 file \\u00b7 db \\u00b7 fusion';};

  /* ── Core Unix (30) ── */
  O['ls']=function(){return'  <span class="path">Documents/</span>  <span class="path">Pictures/</span>  <span class="path">Music/</span>  <span class="path">Desktop/</span><br>  README.txt  todo.txt  kernel.js  boot.log';};
  O['pwd']=function(){return'  <span class="path">/home/user</span>';};
  O['cd']=function(){return arg?'  <span class="warn">\\u6a21\\u62df\\u76ee\\u5f55\\u5207\\u6362: '+arg+'/</span>':'  <span class="path">/home/user</span>';};
  O['cat']=function(){if(arg.includes('README')){var ct=vfsReadFile('/\\u7528\\u6237/\\u6587\\u6863/README.txt');return ct?'  <pre style="color:#c9d1d9;white-space:pre-wrap">'+escHtml(ct)+'</pre>':'  FusionOS 7.0';}var node=vfsNode(arg);if(node&&node.t==='f')return'  <pre style="color:#c9d1d9;white-space:pre-wrap">'+escHtml(node.d||'(空)')+'</pre>';if(!arg)return'  <span class="err">用法: cat <文件路径></span>';return'  <span class="err">文件未找到: '+arg+'</span>';};
  O['mkdir']=function(){if(!arg)return'  <span class="err">用法: mkdir <目录名></span>';return vfsMkdir(arg)?'  <span class="val">V 已创建: '+arg+'</span>':'  <span class="err">创建失败</span>';};
  O['touch']=function(){if(!arg)return'  <span class="err">用法: touch <文件名></span>';return vfsTouch(arg)?'  <span class="val">V 已创建: '+arg+'</span>':'  <span class="err">创建失败</span>';};
  O['rm']=function(){if(!arg)return'  <span class="err">用法: rm <路径></span>';return vfsRm(arg)?'  <span class="val">V 已删除: '+arg+'</span>':'  <span class="err">删除失败</span>';};
  O['rmdir']=function(){if(!arg)return'  <span class="err">用法: rmdir <目录></span>';return vfsRm(arg)?'  <span class="val">V 已删除: '+arg+'</span>':'  <span class="err">删除失败</span>';};
  O['echo']=function(){return'  '+arg;};
  O['clear']=function(){tl.innerHTML='';return'';};
  O['write']=function(){var p=cmd.split(/\\s+/);if(p.length<3)return'  <span class="err">用法: write <路径> <内容></span>';var fp=p[1],ct=p.slice(2).join(' ');return vfsWriteFile(fp,ct)?'  <span class="val">V 已写入: '+fp+'</span>':'  <span class="err">写入失败</span>';};
  O['cp']=function(){return'  <span class="warn">功能暂未实现(VFS限制)</span>';};
  O['mv']=function(){return'  <span class="warn">功能暂未实现(VFS限制)</span>';};
  O['ln']=function(){return'  <span class="warn">符号链接不受支持</span>';};
  O['chmod']=function(){return'  <span class="val">V 权限已模拟修改</span>';};
  O['chown']=function(){return'  <span class="val">V 所有者: user:staff</span>';};
  O['find']=function(){return'  <span class="path">./Documents/README.txt</span><br>  <span class="path">./Documents/todo.txt</span><br>  <span class="path">./System/kernel.js</span>';};
  O['grep']=function(){return'  <span class="warn">VFS 不支持全文搜索</span>';};
  O['wc']=function(){return'  <span class="val">42 256 2048</span>';};
  O['sort']=function(){return'  <span class="warn">请在管道中使用</span>';};
  O['uniq']=function(){return'  <span class="warn">请在管道中使用</span>';};
  O['head']=function(){return'  line 1<br>  line 2<br>  line 3<br>  <span style="color:#8b949e">...省略</span>';};
  O['tail']=function(){return'  <span style="color:#8b949e">...省略</span><br>  line 98<br>  line 99<br>  line 100';};
  O['cut']=function(){return'  <span class="warn">请在管道中使用</span>';};
  O['diff']=function(){return'  <span class="info">文件相同(模拟)</span>';};
  O['file']=function(){return'  <span class="info">\\u6587\\u4ef6: ASCII text</span>';};
  O['which']=function(){return'  <span class="path">/usr/bin/'+arg+'</span>';};
  O['whereis']=function(){return'  <span class="path">/usr/bin/'+arg+'  /usr/share/man/man1/'+arg+'.1</span>';};
  O['type']=function(){return'  <span class="info">'+arg+' 是内置命令</span>';};
  O['tee']=function(){return'  <span class="val">V 输出已复制</span>';};
  O['yes']=function(){return'  <span class="info">y y y y y y ... (Ctrl+C 停止)</span>';};
  O['tr']=function(){return'  <span class="warn">请在管道中使用</span>';};

  /* ── System Info (17) ── */
  O['uname']=function(){return'  <span class="val">FusionOS</span> 7.0 fusionos-7.0-generic x86_64';};
  O['hostname']=function(){return'  <span class="val">fusionos-desktop</span>';};
  O['whoami']=function(){return'  <span class="val">user</span>';};
  O['who']=function(){return'  <span class="val">user     pts/0        '+new Date().toLocaleString('zh-CN')+'</span>';};
  O['id']=function(){return'  <span class="val">uid=1000(user) gid=1000(user) groups=user,wheel,staff</span>';};
  O['groups']=function(){return'  <span class="val">user wheel staff</span>';};
  O['uptime']=function(){return'  <span class="val">up 2小时35分</span>, 1 user, load avg: 0.15 0.05 0.01';};
  O['arch']=function(){return'  <span class="val">x86_64</span>';};
  O['dmesg']=function(){return'  <span style="color:#8b949e">[0000] Kernel booting...<br>[0.012] CPU: FusionOS 7.0 x86_64<br>[0.024] Memory: 16GB available<br>[0.036] VFS mounted<br>[0.048] WM initialized<br>[1.200] Desktop ready</span>';};
  O['lscpu']=function(){return'  <span class="val">Architecture: x86_64</span><br>  CPU(s): 8<br>  Model: FusionOS Virtual CPU @ 3.2GHz';};
  O['lsblk']=function(){return'  <span class="val">NAME  MAJ:MIN  SIZE  TYPE  MOUNTPOINT</span><br>  vda   254:0    16G   disk  /';};
  O['lspci']=function(){return'  <span class="val">00:00.0  Host bridge: FusionOS<br>00:01.0  VGA controller: Fusion Display<br>00:02.0  Network controller: FusionNet<br>00:03.0  Audio device: FusionAudio</span>';};
  O['mount']=function(){return'  <span class="val">FusionDisk on / type fusfs (rw)</span>';};
  O['vmstat']=function(){return'  <span class="val">procs  memory      swap  io  system  cpu</span><br>  r b  free  buff  cache  si  so  bi  bo  in  cs  us sy id<br>  0 0  12G  0  0  0  0  0  0  1  2  2 1 97';};
  O['umount']=function(){return'  <span class="val">V 已卸载(模拟)</span>';};
  O['sysinfo']=function(){return'  <span class="val">=== 系统信息 ===</span><br>  OS: FusionOS 7.0<br>  Kernel: fusionos-7.0<br>  CPU: Virtual x86_64 @ 3.2GHz<br>  RAM: 16GB<br>  Disk: FusionDisk 16GB<br>  Apps: '+APPS.length+'<br>  Commands: 172';};
  O['version']=function(){return'  <span class="val">FusionOS 7.0</span> Build 2026-06-15<br>  Kernel: fusionos-7.0<br>  Shell: fusion-term 7.0<br>  Apps: '+APPS.length+'<br>  Features: 100+';};

  /* ── Network (20) ── */
  O['ping']=function(){if(!arg)return'  <span class="err">用法: ping <地址></span>';var ip=arg.replace(/[^a-zA-Z0-9.]/g,''),ms=Math.floor(Math.random()*30+5);return'  <span class="info">PING '+ip+'</span><br>  64 bytes from '+ip+': icmp_seq=1 ttl=64 time='+ms+'.'+Math.floor(Math.random()*100)+' ms<br>  64 bytes from '+ip+': icmp_seq=2 ttl=64 time='+(ms+Math.floor(Math.random()*5))+'.'+Math.floor(Math.random()*100)+' ms<br>  <span class="val">2 packets transmitted, 2 received, 0% loss</span>';};
  O['curl']=function(){return'  <span class="info">模拟HTTP请求...</span><br>  <span class="val">HTTP/1.1 200 OK</span><br>  Content-Type: text/html<br>  <span style="color:#8b949e"><html>FusionOS 7.0</html></span>';};
  O['wget']=function(){return'  <span class="info">模拟下载: '+arg+'</span><br>  <span class="val">100% [====================] 1.2MB/s   0s</span><br>  V 已保存为 index.html';};
  O['ifconfig']=function(){return'  <span class="val">eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST></span><br>  inet 192.168.1.100  netmask 255.255.255.0<br>  ether 00:1a:2b:3c:4d:5e';};
  O['ip']=function(){return'  <span class="val">1: eth0: <BROADCAST,MULTICAST,UP></span><br>  inet 192.168.1.100/24 scope global eth0';};
  O['netstat']=function(){return'  <span class="val">Proto  Local Address        Foreign Address     State</span><br>  tcp    0.0.0.0:443          0.0.0.0:*          LISTEN<br>  tcp    192.168.1.100:443    151.101.1.69:443   ESTABLISHED';};
  O['ss']=function(){return'  <span class="val">Netid  State  Recv-Q  Send-Q  Local:Port  Peer:Port</span><br>  tcp    ESTAB  0       0        192.168.1.100:443  151.101.1.69:443';};
  O['nslookup']=function(){return arg?'<span class="info">Server: 8.8.8.8<br>Address: '+arg+'<br>Non-authoritative:<br>Name: '+arg+'<br>Address: 142.250.80.46</span>':'  <span class="err">用法: nslookup <域名></span>';};
  O['dig']=function(){return'  <span class="info">;; <<>> DiG 9.18 <<>> '+arg+'<br>;; ANSWER SECTION:<br>'+arg+'.  300  IN  A  142.250.80.46</span>';};
  O['traceroute']=function(){return arg?'<span class="info">traceroute to '+arg+', 30 hops max</span><br>  1  _gateway  1.2 ms<br>  2  10.0.0.1  5.4 ms<br>  ... (模拟)':'  <span class="err">用法: traceroute <地址></span>';};
  O['ssh']=function(){return'  <span class="warn">SSH 客户端功能未启用(模拟)</span>';};
  O['ftp']=function(){return'  <span class="warn">FTP 功能未启用(模拟)</span>';};
  O['nc']=function(){return'  <span class="warn">netcat 功能未启用(模拟)</span>';};
  O['scp']=function(){return'  <span class="warn">SCP 功能未启用(模拟)</span>';};
  O['telnet']=function(){return'  <span class="warn">Telnet 功能未启用(模拟)</span>';};
  O['tcpdump']=function(){return'  <span class="warn">tcpdump 需要 root 权限</span>';};
  O['wifi']=function(){return'  <span class="val">Wi-Fi 状态: 已连接 (FusionNet)</span><br>  SSID: FusionNet-5G<br>  信号强度: 92%<br>  IP: 192.168.1.100';};
  O['speedtest']=function(){return'  <span class="info">测速中...</span><br>  <span class="val">下载: 352.1 Mbps</span><br>  <span class="val">上传: 124.5 Mbps</span><br>  <span class="val">延迟: 12 ms</span>';};
  O['route']=function(){return'  <span class="val">Kernel IP routing table</span><br>  Destination  Gateway      Genmask        Iface<br>  0.0.0.0      192.168.1.1  0.0.0.0        eth0';};
  O['arp']=function(){return'  <span class="val">Address        HWaddress</span><br>  192.168.1.1    00:11:22:33:44:55';};

  /* ── Monitoring (12) ── */
  O['ps']=function(){return'  <span class="val">PID  COMMAND</span><br>  1001 fusion-wm<br>  1002 fusion-term<br>  1003 fusion-finder<br>  1004 vfs-daemon<br>  1005 notificationd';};
  O['top']=function(){return'  <span class="val">PID  USER  %CPU  %MEM  COMMAND</span><br>  1001 user  2.3   0.5   fusion-wm<br>  1002 user  0.1   0.2   fusion-term';};
  O['free']=function(){return'  <span class="val">FusionDisk 16 GB</span><br>  \\u5df2\\u7528: 4.2 GB  |  \\u53ef\\u7528: 11.8 GB<br>  \\u4f7f\\u7528\\u7387: 26.3%';};
  O['df']=function(){return'  <span class="val">\\u6587\\u4ef6\\u7cfb\\u7edf       总大小     已用      可用  使用率</span><br>  FusionDisk   16.0GB    4.2GB    11.8GB    26%';};
  O['du']=function(){return'  <span class="val">4.2G  ./Documents</span><br>  <span class="val">2.1G  ./Pictures</span><br>  <span class="val">1.8G  ./Music</span><br>  <span class="val">8.1G  total</span>';};
  O['iostat']=function(){return'  <span class="val">Device  tps  kB_read/s  kB_wrtn/s</span><br>  vda     15.2  120         45';};
  O['iotop']=function(){return'  <span class="warn">iotop 需要 root 权限</span>';};
  O['mpstat']=function(){return'  <span class="val">CPU  %usr  %sys  %idle</span><br>  all  3.2   1.1   95.7';};
  O['sensors']=function(){return'  <span class="val">coretemp-isa-0000</span><br>  Core 0: +42.5C<br>  Core 1: +41.0C';};
  O['hwinfo']=function(){return'  <span class="val">CPU: FusionOS Virtual CPU @ 3.2GHz</span><br>  RAM: 16GB DDR4<br>  GPU: FusionOS Display Adapter<br>  NET: FusionNet Gigabit Ethernet';};
  O['perf']=function(){return'  <span class="val">\\u6027\\u80fd\\u8bc4\\u5206: '+calcPerfScore()+'/10</span>';};

  /* ── Text Processing (10) ── */
  O['awk']=function(){return'  <span class="warn">请在管道中使用</span>';};
  O['sed']=function(){return'  <span class="warn">请在管道中使用</span>';};
  O['nl']=function(){return'  <span class="val">1  line one</span><br>  <span class="val">2  line two</span><br>  <span class="val">3  line three</span>';};
  O['fmt']=function(){return'  <span class="val">V 文本已重新格式化</span>';};
  O['strings']=function(){return'  <span class="warn">VFS 不支持二进制文件</span>';};
  O['xxd']=function(){return'  <span class="warn">VFS 不支持十六进制转储</span>';};
  O['column']=function(){return'  <span class="warn">请在管道中使用</span>';};
  O['split']=function(){return'  <span class="val">V 模拟分割: 创建了 xaa, xab, xac</span>';};
  O['csplit']=function(){return'  <span class="val">V 模拟分割</span>';};
  O['sponge']=function(){return'  <span class="warn">请在管道中使用</span>';};

  /* ── Dev Tools (15) ── */
  O['git']=function(){return'  <span class="info">usage: git [--version] [--help] [-C path] [-c name=value]</span>';};
  O['npm']=function(){return'  <span class="info">npm v10.2.0 (模拟)</span><br>  <span class="info">up to date in 1.2s</span>';};
  O['pip']=function(){return'  <span class="info">pip 24.0 from /usr/lib/python3 (模拟)</span>';};
  O['make']=function(){return'  <span class="info">make[1]: Entering directory /home/user/project</span><br>  <span class="val">gcc main.o -o main</span><br>  <span class="val">V Build complete</span>';};
  O['gcc']=function(){return'  <span class="val">V 编译成功: a.out</span>';};
  O['python']=function(){return'  <span class="info">Python 3.12.0 (FusionOS)</span>';};
  O['node']=function(){return'  <span class="info">Node.js v22.0.0 (FusionOS)</span>';};
  O['docker']=function(){return'  <span class="warn">Docker 不支持(浏览器环境)</span>';};
  O['java']=function(){return'  <span class="info">openjdk version 21.0.2 (模拟)</span>';};
  O['ruby']=function(){return'  <span class="info">ruby 3.3.0 [x86_64-fusionos]</span>';};
  O['go']=function(){return'  <span class="info">go version go1.22.0 fusionos/amd64 (模拟)</span>';};
  O['rustc']=function(){return'  <span class="info">rustc 1.77.0 (模拟)</span>';};
  O['perl']=function(){return'  <span class="info">This is perl 5, version 38 (模拟)</span>';};
  O['php']=function(){return'  <span class="info">PHP 8.3.0 (cli) (模拟)</span>';};
  O['lua']=function(){return'  <span class="info">Lua 5.4.6 (模拟)</span>';};

  /* ── Fun (20) ── */
  O['neofetch']=function(){var u=calcDiskUsed(),f=diskFree();return'<pre style="color:#8b949e;font-size:10px;line-height:1.2"> \\u250c\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2510\\n \\u2502   FusionOS 7.0    \\u2502\\n \\u2502   '+APPS.length+' Apps  172 Cmds   \\u2502\\n \\u2502   DISK: '+f.toFixed(1)+'/'+vDisk.total+' GB \\u2502\\n \\u2502   ARCH: x86+ARM       \\u2502\\n \\u2502   SHL: fusion-term    \\u2502\\n \\u2514\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2518</pre>';};
  O['date']=function(){return'  '+new Date().toLocaleString('zh-CN');};
  O['tree']=function(){return'  <span class="path">/</span><br>  \\u251c\\u2500\\u2500 <span class="path">\\u7528\\u6237/</span><br>  \\u2502   \\u251c\\u2500\\u2500 <span class="path">\\u6587\\u6863/</span><br>  \\u2502   \\u2502   \\u251c\\u2500\\u2500 README.txt<br>  \\u2502   \\u2502   \\u2514\\u2500\\u2500 todo.txt<br>  \\u2502   \\u251c\\u2500\\u2500 <span class="path">\\u56fe\\u7247/</span><br>  \\u2502   \\u2514\\u2500\\u2500 <span class="path">\\u97f3\\u4e50/</span><br>  \\u251c\\u2500\\u2500 <span class="path">\\u7cfb\\u7edf/</span><br>  \\u2502   \\u251c\\u2500\\u2500 kernel.js<br>  \\u2502   \\u2514\\u2500\\u2500 boot.log<br>  \\u2514\\u2500\\u2500 <span class="path">\\u5e94\\u7528/</span>';};
  O['cowsay']=function(){var t=arg||'FusionOS';return'  <pre style="color:#c9d1d9"> _______________<br>< '+t.slice(0,13)+' ><br> ---------------<br>        \\\\   ^__^<br>         \\\\  (oo)\\\\_______<br>            (__)\\\\       )\\\\/\\\\<br>                ||----w |<br>                ||     ||</pre>';};
  O['fortune']=function(){var q=['你今天会很幸运！','代码写完了吗？','FusionOS是最好的桌面系统','休息一下，喝杯茶吧'];return'  <span class="info">'+q[Math.floor(Math.random()*q.length)]+'</span>';};
  O['banner']=function(){return'  <pre style="color:var(--accent)">FUSION</pre>';};
  O['sl']=function(){return'  <pre style="color:#c9d1d9">CHOO CHOO! ==== _______<br>  _D _|  |_____/  |__[_]<br>   (_)===  |  |  \\\\  ||<br>  |___|   ==  ==   \\\\_|</pre>';};
  O['cmatrix']=function(){return'  <span style="color:#00ff00">Matrix mode activated...</span>';};
  O['figlet']=function(){return'  <pre style="color:var(--accent);font-size:9px;line-height:1.1"> _____ _   _ ____ ___ ___  _   _<br>|  ___| | | / ___|_ _/ _ \\\\| \\\\ | |<br>| |_  | | | \\\\___ \\\\| | | | |  \\\\| |<br>|  _| | |_| |___) | | |_| | |\\\\  |<br>|_|    \\\\___/|____/___\\\\___/|_| \\\\_|</pre>';};
  O['nyancat']=function(){return'  <pre style="color:#ff69b4">  /l,     Nyan~<br> (., )7    Nyan~<br>  l  ~_    Nyan~<br>   "_,)    Nyan~</pre>';};
  O['rig']=function(){return'  <span class="val">身份已生成:</span><br>  姓名: 张伟<br>  地址: 北京市朝阳区100号<br>  电话: 138****5678';};
  O['rev']=function(){return'  <span class="val">'+arg.split('').reverse().join('')+'</span>';};
  O['factor']=function(){return'  <span class="val">2 3 7</span>';};
  O['jot']=function(){return'  <span class="val">1 2 3 4 5 6 7 8 9 10</span>';};
  O['asciiquarium']=function(){return'  <pre style="color:#42a5f5">   ><(((*>   <..)))><   ><(((*></pre>';};
  O['ponysay']=function(){return'  <pre style="color:#ff69b4">Unicorn: FusionOS is magic!</pre>';};
  O['lolcat']=function(){return'  <span style="color:#ff6b6b">R</span><span style="color:#ffd93d">a</span><span style="color:#6bcb77">i</span><span style="color:#4d96ff">n</span><span style="color:#ff6b6b">b</span><span style="color:#ffd93d">o</span><span style="color:#6bcb77">w</span>';};
  O['espeak']=function(){return'  <span class="warn">TTS 功能不可用(浏览器限制)</span>';};
  O['matrix']=function(){return'  <span style="color:#00ff00">Escape the Matrix. Enter FusionOS.</span>';};
  O['rickroll']=function(){return'  <span class="warn">Never gonna give you up!</span>';};
  O['hack']=function(){return'  <pre style="color:#00ff00;font-size:10px">[+] Initializing hack module...<br>[+] Bypassing firewall... OK<br>[+] Accessing target... 192.168.1.1<br>[-] ERROR: This is a simulation</pre>';};

  /* ── Math (10) ── */
  O['calc']=function(){try{var e=arg.replace(/[^0-9+*/()\\s.-]/g,'');if(!e)return'  <span class="err">用法: calc <表达式></span>';return'  <span class="val">= '+eval(e)+'</span>'}catch(e){return'  <span class="err">计算错误</span>'};};
  O['bc']=function(){try{var e=arg.replace(/[^0-9+*/()\\s.-]/g,'');return'  <span class="val">'+eval(e||0)+'</span>'}catch(e){return'  <span class="err">错误</span>'};};
  O['expr']=function(){try{return'  <span class="val">'+eval(arg.replace(/[^0-9+*/()\\s.-]/g,'')||0)+'</span>'}catch(e){return'  <span class="err">错误</span>'};};
  O['units']=function(){return'  <span class="warn">请使用"单位换算"应用</span>';};
  O['seq']=function(){return'  <span class="val">1 2 3 4 5 6 7 8 9 10</span>';};
  O['numfmt']=function(){return'  <span class="val">1,024</span>';};
  O['shuf']=function(){return'  <span class="val">7 3 9 1 5 8 2 4 6 10</span>';};
  O['rand']=function(){return'  <span class="val">42</span>';};
  O['prime']=function(){var n=parseInt(arg)||17;function ip(n){for(var i=2;i*i<=n;i++)if(n%i===0)return false;return n>1;}return'  <span class="val">'+(ip(n)?'是质数':'不是质数')+'</span>';};
  O['fib']=function(){var n=parseInt(arg)||10,a=0,b=1,r=[0];for(var i=1;i<n;i++){var t=b;b=a+b;a=t;r.push(a);}return'  <span class="val">'+r.join(' ')+'</span>';};

  /* ── Crypto (10) ── */
  O['md5sum']=function(){return'  <span class="val">d41d8cd98f00b204e9800998ecf8427e  -</span>';};
  O['sha256sum']=function(){return'  <span class="val">e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -</span>';};
  O['base64']=function(){return'  <span class="val">'+btoa(unescape(encodeURIComponent(arg||'FusionOS')))+'</span>';};
  O['openssl']=function(){return'  <span class="warn">OpenSSL 不可用(浏览器限制)</span>';};
  O['gpg']=function(){return'  <span class="warn">GPG 不可用(浏览器限制)</span>';};
  O['ssh-keygen']=function(){return'  <span class="val">V 已生成密钥对:</span><br>  ~/.ssh/id_rsa<br>  ~/.ssh/id_rsa.pub';};
  O['passwd']=function(){return'  <span class="val">V 密码已更新(模拟)</span>';};
  O['chroot']=function(){return'  <span class="warn">chroot 需要 root 权限</span>';};
  O['sudo']=function(){return'  <span class="info">'+arg+' (已以超级用户身份模拟执行)</span>';};
  O['su']=function(){return'  <span class="info">已切换为 root (模拟)</span>';};

  /* ── File Ops (10) ── */
  O['tar']=function(){return'  <span class="val">V 已创建归档: archive.tar</span>';};
  O['gzip']=function(){return'  <span class="val">V 已压缩</span>';};
  O['bzip2']=function(){return'  <span class="val">V 已压缩</span>';};
  O['zip']=function(){return'  <span class="val">V 已打包: archive.zip</span>';};
  O['unzip']=function(){return'  <span class="val">V 已解压</span>';};
  O['dd']=function(){return'  <span class="val">V 模拟写入完成<br>8+0 records in<br>8+0 records out</span>';};
  O['sync']=function(){return'  <span class="val">V 已同步缓存</span>';};
  O['stat']=function(){return'  <span class="val">File: '+arg+'<br>Size: 4096<br>Access: (0644/-rw-r--r--)</span>';};
  O['realpath']=function(){return'  <span class="path">/home/user/'+arg+'</span>';};
  O['mktemp']=function(){return'  <span class="path">/tmp/tmp.x9Kf3z</span>';};

  /* ── Database (5) ── */
  O['sqlite3']=function(){return'  <span class="info">SQLite version 3.45.0 (模拟)</span>';};
  O['redis-cli']=function(){return'  <span class="info">redis 127.0.0.1:6379> PONG</span>';};
  O['mysql']=function(){return'  <span class="info">MySQL 8.0 (模拟) 连接本地数据库</span>';};
  O['mongo']=function(){return'  <span class="info">MongoDB shell 7.0 (模拟)</span>';};
  O['psql']=function(){return'  <span class="info">psql (PostgreSQL) 16.0 (模拟)</span>';};

  /* ── FusionOS (18) ── */
  O['notify']=function(){addNotif('终端通知',arg||'来自终端的通知','ic-bell');return'  <span class="val">V 通知已发送</span>';};
  O['open']=function(){if(!arg)return'  <span class="err">用法: open <应用名></span>';var app=APPS.find(function(a){return a.id===arg||a.name.indexOf(arg)===0});if(app){openApp(app.id);return'  <span class="val">V 已打开 '+app.name+'</span>';}return'  <span class="err">未找到: '+arg+'</span>';};
  O['wallpaper']=function(){var walls=['','2','3','4','5','6'];setSetting('wallpaper',walls[Math.floor(Math.random()*walls.length)]);applyAllSettings();return'  <span class="val">V 壁纸已切换</span>';};
  O['save']=function(){saveState();return'  <span class="val">V 已保存</span>';};
  O['reset']=function(){return'  <span class="warn">警告: reset destroy 不可逆!</span>';};
  O['info']=function(){return'  <span class="val">FusionOS 7.0</span><br>  '+APPS.length+' Apps | 172 Commands';};
  O['debug']=function(){return'  <span class="val">VFS: </span>'+JSON.stringify(Object.keys(VFS))+'<br>  <span class="val">Windows: </span>'+Object.keys(windows).filter(function(k){return windows[k]&&!windows[k].closed}).length+'<br>  <span class="val">winZ: </span>'+winZ+'<br>  <span class="val">Notifs: </span>'+notifs.length;};
  O['credits']=function(){return'  <span class="val">FusionOS 7.0</span><br>  \\u5f00\\u53d1\\u8005: Fusion Team<br>  \\u56fe\\u6807: \\u81ea\\u5b9a\\u4e49 SVG<br>  \\u6280\\u672f\\u6808: HTML/CSS/JS (\\u96f6\\u4f9d\\u8d56)';};
  O['license']=function(){return'  <span class="info">FusionOS 7.0 License</span><br>  MIT License (\\u6a21\\u62df)<br>  Copyright 2026 FusionOS';};
  O['changelog']=function(){return'  <span class="val">v7.0 - 2026-06-15</span><br>  + 15 \\u4e2a\\u65b0\\u5e94\\u7528<br>  + 3 \\u4e2a\\u6e38\\u620f<br>  + 172 \\u6761\\u7ec8\\u7aef\\u547d\\u4ee4<br>  + 100 \\u4e2a\\u7cfb\\u7edf\\u529f\\u80fd';};
  O['update']=function(){return'  <span class="val">V 已是最新版本 (7.0)</span>';};
  O['donate']=function(){return'  <span style="color:#ffd700">Star \\u611f\\u8c22\\u652f\\u6301\\uff01FusionOS \\u6c38\\u8fdc\\u514d\\u8d39\\u3002</span>';};
  O['fetch']=function(){return'  <span class="val">'+getGreeting()+'\\uff01FusionOS 7.0 \\u5df2\\u5c31\\u7eea</span>';};
  O['quote']=function(){var q=['代码就是诗','少即是多','保持简单'];return'  <span class="info">"'+q[Math.floor(Math.random()*q.length)]+'"</span>';};
  O['joke']=function(){var j=['程序员出门看到阳光说: null pointer!','0和1走进酒吧... 0说: 我什么都没有'];return'  <span class="info">'+j[Math.floor(Math.random()*j.length)]+'</span>';};
  O['thanks']=function(){return'  <span class="info">感谢使用 FusionOS 7.0! </span>';};
  O['help-cat']=function(){var cats={core:'ls cd pwd cat mkdir touch rm rmdir echo clear write cp mv ln chmod chown find grep wc sort uniq head tail cut diff file which whereis type tee yes tr',sysinfo:'uname hostname whoami who id groups uptime arch dmesg lscpu lsblk lspci mount vmstat umount sysinfo version',net:'ping curl wget ifconfig ip netstat ss nslookup dig traceroute ssh ftp nc scp telnet tcpdump wifi speedtest route arp',monitor:'ps top free df du iostat iotop mpstat sensors hwinfo perf',text:'awk sed nl fmt strings xxd column split csplit sponge',dev:'git npm pip make gcc python node docker java ruby go rustc perl php lua',fun:'neofetch cowsay fortune banner sl cmatrix figlet nyancat rig rev factor jot asciiquarium ponysay lolcat espeak matrix rickroll hack',math:'calc bc expr units seq numfmt shuf rand prime fib',crypto:'md5sum sha256sum base64 openssl gpg ssh-keygen passwd chroot sudo su',file_:'tar gzip bzip2 zip unzip dd sync stat realpath mktemp',db:'sqlite3 redis-cli mysql mongo psql',fusion:'notify open wallpaper save reset info debug credits license changelog update donate fetch quote joke thanks help-cat'};var cat=cats[arg||'core']||cats.core;return'  <span class="cmd">'+cat.split(' ').join('</span>  <span class="cmd">')+'</span>';};

  /* ── Misc (6) ── */
  O['man']=function(){return'  <span class="info">'+arg.toUpperCase()+'(1)</span><br>  <span style="color:#8b949e">手册不可用。试试: help</span>';};
  O['alias']=function(){return'  <span class="val">alias ll="ls -la"<br>alias la="ls -A"<br>alias ..="cd .."</span>';};
  O['export']=function(){return'  <span class="val">HOME=/home/user<br>PATH=/usr/bin:/bin<br>USER=user<br>SHELL=fusion-term</span>';};
  O['env']=function(){return'  <span class="val">HOME=/home/user<br>PATH=/usr/bin:/bin<br>USER=user<br>FUSION_VERSION=7.0</span>';};
  O['history']=function(){return'  <span class="val">1  ls</span><br>  <span class="val">2  pwd</span><br>  <span class="val">3  neofetch</span>';};
  O['printenv']=function(){return'  <span class="val">HOME=/home/user<br>USER=user</span>';};

  /* ── System Actions (5) ── */
  O['logout']=function(){doLogout();return'  <span class="val">正在注销...</span>';};
  O['shutdown']=function(){doShutdown();return'  <span class="val">正在关机...</span>';};
  O['reboot']=function(){doRestart();return'  <span class="val">正在重启...</span>';};
  O['lock']=function(){doLock();return'  <span class="val">V 屏幕已锁定</span>';};
  O['exit']=function(){return'  <span class="val">再见！</span>';};

  var fn=O[c];
  out.innerHTML=fn?fn():'  <span class="err">'+c+': \\u547d\\u4ee4\\u672a\\u627e\\u5230</span><br>  <span style="color:#8b949e">\\u8f93\\u5165 help \\u67e5\\u770b\\u547d\\u4ee4\\uff0c\\u8f93\\u5165 cmds \\u67e5\\u770b172\\u6761\\u547d\\u4ee4</span>';
  tl.appendChild(out);var term=document.getElementById('term-'+id);if(term)term.scrollTop=term.scrollHeight;
}
''')

print("term_cmds.js written with 172 commands")
