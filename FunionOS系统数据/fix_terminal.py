#!/usr/bin/env python3
"""Fix all terminal issues: help/cmds commands, tab completion, Ctrl+L"""

with open('/Users/murderdrones/Desktop/FusionOS.html', 'r') as f:
    html = f.read()

fixes = 0

# 1. Add help and cmds commands to the O dictionary (before the Execution section)
old_exec = '\n  /* \u2500\u2500 Execution \u2500\u2500 */'
insert_help = '''
  /* \u2500\u2500 Help & Discovery \u2500\u2500 */
  O['help']=function(){var c='\\u2714 \u53ef\u7528\u547d\u4ee4\u2014\u2014\u8f93\u5165 \u547d\u4ee4\u540d \u6216 \u547d\u4ee4\u540d --help \u67e5\u770b\u8be6\u60c5\\n';c+='\u7cfb\u7edf: uname,hostname,arch,lscpu,uptime,whoami,who,id,env,date,cal\\n';c+='\u76d1\u63a7: top,free,vmstat,iostat,mpstat,pidstat,sar,dstat,lsof,ps\\n';c+='\u6587\u4ef6: ls,cd,pwd,mkdir,rmdir,touch,cp,mv,rm,cat,head,tail,find\\n';c+='\u7f51\u7edc: ping,curl,wget,ifconfig,ip,netstat,ss,ssh,traceroute\\n';c+='Git: git,git-init,git-clone,git-add,git-commit,git-push,git-pull\\n';c+='\u5f00\u53d1: gcc,g++,python,node,npm,cargo,tree,jq,yq,sed,awk\\n';c+='\u5b89\u5168: openssl,base64,md5sum,sha256sum,gpg,ssh-keygen\\n';c+='\u5a31\u4e50: cowsay,fortune,lolcat,cmatrix,sl,figlet,toilet\\n';c+='\u6570\u636e\u5e93: mysql,psql,sqlite3,redis-cli,mongosh\\n';c+='\u4e91: aws,gcloud,az,kubectl,helm,terraform,ansible,docker\\n';c+='\u5176\u4ed6: version,sysinfo,clear,cls,date,history,exit\\n';c+='\u8f93\u5165 cmds \u67e5\u770b\u6240\u6709 1,200+ \u6761\u547d\u4ee4';return c;};
  O['cmds']=function(){var k=Object.keys(O).filter(function(x){return x!=='help'&&x!=='cmds';}).sort();var p='\u2500\u2500 \u6240\u6709\u547d\u4ee4 ('+k.length+') \u2500\u2500\\n';for(var i=0;i<k.length;i++){p+=k[i];if((i+1)%4===0)p+='\\n';else p+='  ';}return p;};
'''
html = html.replace(old_exec, insert_help + old_exec, 1)
fixes += 1
print(f"Fix {fixes}: Added help + cmds commands to O dictionary")

# 2. Enhance termKey to support Tab completion and Ctrl+L
old_termKey = """function termKey(e,id){
  if(e.key==='Enter'){var inp=document.getElementById('ti-'+id),v=inp.value.trim();
    if(!termHist[id])termHist[id]=[];termHist[id].push(v);termIdx[id]=termHist[id].length;
    termExec(v,id);inp.value='';}
  if(e.key==='ArrowUp'){if(termHist[id]&&termIdx[id]>0){termIdx[id]--;document.getElementById('ti-'+id).value=termHist[id][termIdx[id]];}}
  if(e.key==='ArrowDown'){if(termHist[id]&&termIdx[id]<termHist[id].length-1){termIdx[id]++;document.getElementById('ti-'+id).value=termHist[id][termIdx[id]];}else{termIdx[id]=termHist[id]?termHist[id].length:0;document.getElementById('ti-'+id).value='';}}
}"""

new_termKey = """function termKey(e,id){
  if(e.key==='Enter'){var inp=document.getElementById('ti-'+id),v=inp.value.trim();
    if(!termHist[id])termHist[id]=[];termHist[id].push(v);termIdx[id]=termHist[id].length;
    termExec(v,id);inp.value='';return;}
  if(e.key==='ArrowUp'){if(termHist[id]&&termIdx[id]>0){termIdx[id]--;document.getElementById('ti-'+id).value=termHist[id][termIdx[id]];}e.preventDefault();return;}
  if(e.key==='ArrowDown'){if(termHist[id]&&termIdx[id]<termHist[id].length-1){termIdx[id]++;document.getElementById('ti-'+id).value=termHist[id][termIdx[id]];}else{termIdx[id]=termHist[id]?termHist[id].length:0;document.getElementById('ti-'+id).value='';}e.preventDefault();return;}
  if(e.key==='Tab'){e.preventDefault();var inp=document.getElementById('ti-'+id);if(!inp)return;var v=inp.value.trim();var cmdParts=v.split(/\s+/);var prefix=(cmdParts[0]||'').toLowerCase();var matches=[];if(typeof _termExecOrig==='function'){var fakeO={};var origExec=new Function('var O=fakeO;'+_termExecOrig.toString().match(/\\{([\\s\\S]*)\\}/)[1]);try{origExec();}catch(err){}var allCmds=Object.keys(fakeO);for(var i=0;i<allCmds.length;i++){if(allCmds[i].indexOf(prefix)===0)matches.push(allCmds[i]);}}if(matches.length===1){inp.value=matches[0];}else if(matches.length>1){var commonPrefix=matches[0];for(var i=1;i<matches.length;i++){var j=0;while(j<commonPrefix.length&&j<matches[i].length&&commonPrefix[j]===matches[i][j])j++;commonPrefix=commonPrefix.substring(0,j);}if(commonPrefix.length>prefix.length){inp.value=commonPrefix;}else{terminalOut(id,'Tab','<span style="color:#d29922">'+matches.join('  ')+'</span>');}}return;}
  if(e.ctrlKey&&e.key==='l'){e.preventDefault();var tl=document.getElementById('tl-'+id);if(tl)tl.innerHTML='';return;}
}"""

html = html.replace(old_termKey, new_termKey, 1)
fixes += 1
print(f"Fix {fixes}: Enhanced termKey with Tab completion + Ctrl+L + preventDefault")

# 3. Fix Tab completion - use a simpler approach that doesn't break
# The tab completion above tries to execute termExecOrig which won't work.
# Let me fix it to use a pre-built command list instead.

# We'll store all commands in a global variable when termExec runs first
old_var_O = '  var O={};'
new_var_O = '  var O={};if(!window._allCmds){window._allCmds=[];}'
html = html.replace(old_var_O, new_var_O, 1)

# Add command collection after each O['...']=function... entry
# Actually, let's do this at the end of the function after all O entries are populated
old_exec_block = '  /* ── Execution ── */\n  var fn=O[c];'
new_exec_block = '  /* ── Cache all commands for Tab completion ── */\n  if(!window._allCmds||window._allCmds.length<100){window._allCmds=Object.keys(O);}\n  /* ── Execution ── */\n  var fn=O[c];'
html = html.replace(old_exec_block, new_exec_block, 1)
fixes += 1
print(f"Fix {fixes}: Cache command list for Tab completion")

# 4. Simplify the Tab completion to use the cached list
old_tab_match = """var matches=[];if(typeof _termExecOrig==='function'){var fakeO={};var origExec=new Function('var O=fakeO;'+_termExecOrig.toString().match(/\\{([\\s\\S]*)\\}/)[1]);try{origExec();}catch(err){}var allCmds=Object.keys(fakeO);for(var i=0;i<allCmds.length;i++){if(allCmds[i].indexOf(prefix)===0)matches.push(allCmds[i]);}}"""
new_tab_match = """var allCmds=window._allCmds||[];var matches=[];for(var i=0;i<allCmds.length;i++){if(allCmds[i].indexOf(prefix)===0)matches.push(allCmds[i]);}"""

html = html.replace(old_tab_match, new_tab_match, 1)
fixes += 1
print(f"Fix {fixes}: Simplified Tab completion to use cached commands")

# 5. Sync to work dir and write
with open('/Users/murderdrones/Desktop/FusionOS.html', 'w') as f:
    f.write(html)

import shutil
shutil.copy('/Users/murderdrones/Desktop/FusionOS.html',
            '/Users/murderdrones/WorkBuddy/2026-06-15-12-25-08/vm-os.html')

print(f"\nTotal fixes: {fixes}")
print("Desktop and workdir synced")
