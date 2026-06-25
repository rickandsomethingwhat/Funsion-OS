#!/usr/bin/env python3
"""FusionOS 7.0 — Part 2: App Implementations"""
FILE = '/Users/murderdrones/WorkBuddy/2026-06-15-12-25-08/vm-os.html'

with open(FILE, 'r', encoding='utf-8') as fh:
    content = fh.read()

lines = content.split('\n')

# ============================================================
# APP IMPLEMENTATIONS (15 new apps)
# ============================================================

app_impls = '''
/* ── Minesweeper ── */
var mineState={};
function renderMinesweeper(body,winId){
  var s=mineState[winId]||{rows:9,cols:9,mines:10,board:null,revealed:null,flagged:null,over:false,started:false};
  mineState[winId]=s;
  if(!s.board){s.board=[];s.revealed=[];s.flagged=[];
    for(var r=0;r<s.rows;r++){s.board[r]=[];s.revealed[r]=[];s.flagged[r]=[];
      for(var c=0;c<s.cols;c++){s.board[r][c]=0;s.revealed[r][c]=false;s.flagged[r][c]=false;}}
  }
  var h='<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:12px">';
  h+='<div style="display:flex;gap:20px;font-family:var(--font-mono);color:var(--text-secondary);font-size:14px">';
  h+='<span>💣 '+s.mines+'</span><span>⏱ <span id="ms-timer-'+winId+'">0</span>s</span>';
  h+='<button class="btn btn-ghost" onclick="mState[\\''+winId+'\\']={};var b=document.getElementById(\\'body-'+winId+'\\');if(b)renderMinesweeper(b,\\''+winId+'\\')" style="padding:2px 10px;font-size:11px">新游戏</button></div>';
  h+='<div class="mine-board" style="grid-template-columns:repeat('+s.cols+',32px)">';
  for(var r=0;r<s.rows;r++)for(var c=0;c<s.cols;c++){var cls='mine-cell';var txt='';if(s.revealed[r][c]){cls+=' revealed';if(s.board[r][c]===-1){cls+=' mine';txt='💣';}else{txt=s.board[r][c]||'';cls+=' n'+s.board[r][c];}}else if(s.flagged[r][c]){cls+=' flagged';txt='🚩';}
    h+='<div class="'+cls+'" id="mc-'+winId+'-'+r+'-'+c+'" onmousedown="mineClick(event,\\''+winId+'\\','+r+','+c+')">'+txt+'</div>';}
  h+='</div></div>';
  body.innerHTML=h;
}
function mineInitBoard(winId,r0,c0){
  var s=mineState[winId];
  // Place mines
  var placed=0;
  while(placed<s.mines){
    var rr=Math.floor(Math.random()*s.rows),cc=Math.floor(Math.random()*s.cols);
    if((Math.abs(rr-r0)<=1&&Math.abs(cc-c0)<=1)||s.board[rr][cc]===-1)continue;
    s.board[rr][cc]=-1;placed++;
  }
  // Calc numbers
  for(var r=0;r<s.rows;r++)for(var c=0;c<s.cols;c++){
    if(s.board[r][c]===-1)continue;var cnt=0;
    for(var dr=-1;dr<=1;dr++)for(var dc=-1;dc<=1;dc++){var nr=r+dr,nc=c+dc;if(nr>=0&&nr<s.rows&&nc>=0&&nc<s.cols&&s.board[nr][nc]===-1)cnt++;}
    s.board[r][c]=cnt;
  }
  s.started=true;s._startTime=Date.now();
  s._timer=setInterval(function(){if(s.over)return;var el=document.getElementById('ms-timer-'+winId);if(el)el.textContent=Math.floor((Date.now()-s._startTime)/1000);},1000);
}
function mineReveal(winId,r,c){
  var s=mineState[winId];if(s.over||s.revealed[r][c]||s.flagged[r][c])return;
  s.revealed[r][c]=true;
  if(s.board[r][c]===-1){s.over=true;showToast('err','游戏结束','你踩到地雷了！');clearInterval(s._timer);
    for(var rr=0;rr<s.rows;rr++)for(var cc=0;cc<s.cols;cc++)s.revealed[rr][cc]=true;
  var b=document.getElementById('body-'+winId);if(b)renderMinesweeper(b,winId);return;}
  if(s.board[r][c]===0){for(var dr=-1;dr<=1;dr++)for(var dc=-1;dc<=1;dc++){var nr=r+dr,nc=c+dc;if(nr>=0&&nr<s.rows&&nc>=0&&nc<s.cols)mineReveal(winId,nr,nc);}}
  // Check win
  var allSafe=true;
  for(var rr=0;rr<s.rows;rr++)for(var cc=0;cc<s.cols;cc++){if(s.board[rr][cc]!==-1&&!s.revealed[rr][cc])allSafe=false;}
  if(allSafe){s.over=true;clearInterval(s._timer);showToast('ok','恭喜！','你赢了！');}
  var b=document.getElementById('body-'+winId);if(b)renderMinesweeper(b,winId);
}
function mineClick(e,winId,r,c){
  e.preventDefault();var s=mineState[winId];if(s.over)return;
  if(e.button===2){s.flagged[r][c]=!s.flagged[r][c];var b=document.getElementById('body-'+winId);if(b)renderMinesweeper(b,winId);return;}
  if(!s.started)mineInitBoard(winId,r,c);
  mineReveal(winId,r,c);
}

/* ── Tetris ── */
var tetrisState={};
function renderTetris(body,winId){
  var s=tetrisState[winId]||{board:[],piece:null,pos:{x:0,y:0},score:0,over:false,paused:false,_int:null};
  tetrisState[winId]=s;
  if(!s.board.length){for(var r=0;r<20;r++){s.board[r]=[];for(var c=0;c<10;c++)s.board[r][c]=0;}}
  if(!s._int&&!s.over){s._int=setInterval(function(){if(!s.paused&&!s.over)tetrisTick(winId);},400);}
  var COLS=10,ROWS=20;
  var pieces=[[[1,1,1,1]],[[1,1],[1,1]],[[0,1,0],[1,1,1]],[[1,1,0],[0,1,1]],[[0,1,1],[1,1,0]],[[1,0,0],[1,1,1]],[[0,0,1],[1,1,1]]];
  var colors=['#00bcd4','#ffeb3b','#9c27b0','#4caf50','#f44336','#2196f3','#ff9800'];
  if(!s.piece){var pi=Math.floor(Math.random()*pieces.length);s.piece=pieces[pi];s._color=colors[pi];s.pos={x:Math.floor((COLS-s.piece[0].length)/2),y:0};}
  // Check collision
  function collides(px,py,piece){for(var r=0;r<piece.length;r++)for(var c=0;c<piece[r].length;c++){if(piece[r][c]){var nx=px+c,ny=py+r;if(nx<0||nx>=COLS||ny>=ROWS||(ny>=0&&s.board[ny][nx]))return true;}}return false;}
  // Lock piece
  function lock(){for(var r=0;r<s.piece.length;r++)for(var c=0;c<s.piece[r].length;c++){if(s.piece[r][c]){var nx=s.pos.x+c,ny=s.pos.y+r;if(ny<0){s.over=true;clearInterval(s._int);showToast('err','游戏结束','得分:'+s.score);return;}s.board[ny][nx]=s._color;}}
    var cleared=0;
    for(var r=ROWS-1;r>=0;r--){if(s.board[r].every(function(v){return v!==0})){s.board.splice(r,1);s.board.unshift(new Array(COLS).fill(0));cleared++;r++;}}
    if(cleared){s.score+=[0,100,300,500,800][cleared];}
    var pi=Math.floor(Math.random()*pieces.length);s.piece=pieces[pi];s._color=colors[pi];s.pos={x:Math.floor((COLS-s.piece[0].length)/2),y:0};
    if(collides(s.pos.x,s.pos.y,s.piece)){s.over=true;clearInterval(s._int);showToast('err','游戏结束','得分:'+s.score);}
  }
  s._lock=lock;s._collides=collides;
  // Build display
  var boardCopy=s.board.map(function(r){return r.slice();});
  if(!s.over&&s.piece)for(var r=0;r<s.piece.length;r++)for(var c=0;c<s.piece[r].length;c++){if(s.piece[r][c]){var ny=s.pos.y+r,nx=s.pos.x+c;if(ny>=0)boardCopy[ny][nx]=s._color;}}
  var h='<div style="display:flex;align-items:center;justify-content:center;height:100%;gap:20px">';
  h+='<div class="tetris-board" style="grid-template-columns:repeat(10,28px)">';
  for(var r=0;r<20;r++)for(var c=0;c<10;c++)h+='<div class="tetris-cell'+(boardCopy[r][c]?' filled':'')+'" style="'+(boardCopy[r][c]?'background:'+boardCopy[r][c]:'')+'"></div>';
  h+='</div><div style="display:flex;flex-direction:column;gap:8px;align-items:center;color:var(--text-primary)">';
  h+='<div style="font-size:24px;font-weight:700;font-family:var(--font-mono)">'+s.score+'</div>';
  h+='<button class="btn btn-ghost" onclick="tetrisState[\\''+winId+'\\']={};var b=document.getElementById(\\'body-'+winId+'\\');if(b)renderTetris(b,\\''+winId+'\\')" style="padding:6px 14px;font-size:12px">新游戏</button>';
  h+='<div style="font-size:11px;color:var(--text-tertiary)">← → 移动 | ↑ 旋转 | ↓ 加速 | P 暂停</div></div></div>';
  body.innerHTML=h;
  body.onkeydown=function(e){var s=tetrisState[winId];if(!s||s.over)return;
    if(e.key==='ArrowLeft'&&!s._collides(s.pos.x-1,s.pos.y,s.piece))s.pos.x--;
    if(e.key==='ArrowRight'&&!s._collides(s.pos.x+1,s.pos.y,s.piece))s.pos.x++;
    if(e.key==='ArrowDown'){if(!s._collides(s.pos.x,s.pos.y+1,s.piece))s.pos.y++;}
    if(e.key==='ArrowUp'){var rot=[];for(var c=0;c<s.piece[0].length;c++){rot.push([]);for(var r=s.piece.length-1;r>=0;r--)rot[c].push(s.piece[r][c]);}if(!s._collides(s.pos.x,s.pos.y,rot))s.piece=rot;}
    if(e.key==='p')s.paused=!s.paused;
    if(e.key===' '){while(!s._collides(s.pos.x,s.pos.y+1,s.piece))s.pos.y++;s._lock();}
    var b=document.getElementById('body-'+winId);if(b)renderTetris(b,winId);
  };
}
function tetrisTick(winId){var s=tetrisState[winId];if(!s||s.over||s.paused)return;
  if(!s._collides(s.pos.x,s.pos.y+1,s.piece)){s.pos.y++;}
  else{s._lock();}
  var b=document.getElementById('body-'+winId);if(b)renderTetris(b,winId);
}

/* ── Breakout ── */
var breakoutState={};
function renderBreakout(body,winId){
  var s=breakoutState[winId]||{paddle:200,ball:{x:300,y:300,vx:3,vy:-3},bricks:[],score:0,lives:3,over:false,started:false,_int:null};
  breakoutState[winId]=s;
  var w=440,h=380,brickRows=5,brickCols=8,brickW=48,brickH=18,brickPad=4,paddleW=80,paddleH=12,ballR=7;
  if(!s.bricks.length){for(var r=0;r<brickRows;r++){for(var c=0;c<brickCols;c++){s.bricks.push({x:c*(brickW+brickPad)+20,y:r*(brickH+brickPad)+20,w:brickW,h:brickH,alive:true,color:'hsl('+(r*50+200)+',60%,50%)'});}}}
  if(!s._int){s._int=setInterval(function(){if(!s.over&&s.started)breakoutTick(winId);},16);}
  var html='<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:10px">';
  html+='<div style="display:flex;gap:20px;color:var(--text-primary);font-size:14px"><span>🎯 '+s.score+'</span><span>❤ '+s.lives+'</span>';
  html+='<button class="btn btn-ghost" onclick="breakoutState[\\''+winId+'\\']={};var b=document.getElementById(\\'body-'+winId+'\\');if(b)renderBreakout(b,\\''+winId+'\\')" style="padding:2px 10px;font-size:11px">新游戏</button></div>';
  html+='<canvas id="bo-cvs-'+winId+'" class="breakout-canvas" width="'+w+'" height="'+h+'"></canvas>';
  html+='<div style="color:var(--text-tertiary);font-size:11px">← → 移动 | 空格 开始/发射</div></div>';
  body.innerHTML=h;
  setTimeout(function(){
    var cv=document.getElementById('bo-cvs-'+winId);if(!cv)return;
    s._canvas=cv;
    body.onkeydown=function(e){
      if(e.key==='ArrowLeft')s.paddle=Math.max(0,s.paddle-20);
      if(e.key==='ArrowRight')s.paddle=Math.min(w-paddleW,s.paddle+20);
      if(e.key===' '){s.started=true;if(s.over){breakoutState[winId]={};var b=document.getElementById('body-'+winId);if(b)renderBreakout(b,winId);}}
      breakoutDraw(winId);
    };
    cv.addEventListener('mousemove',function(e){var rect=cv.getBoundingClientRect();s.paddle=Math.max(0,Math.min(w-paddleW,e.clientX-rect.left-paddleW/2));breakoutDraw(winId);});
    breakoutDraw(winId);
  },50);
}
function breakoutTick(winId){
  var s=breakoutState[winId];if(!s||s.over)return;
  var w=440,h=380,paddleW=80,ballR=7;
  s.ball.x+=s.ball.vx;s.ball.y+=s.ball.vy;
  if(s.ball.x<=ballR||s.ball.x>=w-ballR)s.ball.vx*=-1;
  if(s.ball.y<=ballR)s.ball.vy*=-1;
  if(s.ball.y>=h-ballR-12){if(s.ball.x>=s.paddle&&s.ball.x<=s.paddle+paddleW){var hit=(s.ball.x-s.paddle)/paddleW;s.ball.vx=6*(hit-0.5);s.ball.vy=-Math.abs(s.ball.vy);}else{s.lives--;if(s.lives<=0){s.over=true;showToast('err','游戏结束','得分:'+s.score);}else{s.started=false;s.ball={x:220,y:300,vx:3,vy:-3};}}}
  s.bricks.forEach(function(br){if(br.alive&&s.ball.x+ballR>br.x&&s.ball.x-ballR<br.x+br.w&&s.ball.y+ballR>br.y&&s.ball.y-ballR<br.y+br.h){br.alive=false;s.ball.vy*=-1;s.score+=10;}});
  breakoutDraw(winId);
}
function breakoutDraw(winId){
  var s=breakoutState[winId];if(!s||!s._canvas)return;
  var cv=s._canvas,ctx=cv.getContext('2d'),w=440,h=380;
  ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,w,h);
  s.bricks.forEach(function(br){if(br.alive){ctx.fillStyle=br.color;ctx.fillRect(br.x,br.y,br.w,br.h);ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.strokeRect(br.x,br.y,br.w,br.h);}});
  ctx.fillStyle='#42a5f5';ctx.fillRect(s.paddle,h-20,80,10);
  ctx.beginPath();ctx.arc(s.ball.x,s.ball.y,7,0,Math.PI*2);ctx.fillStyle='#fff';ctx.fill();
  if(!s.started&&!s.over){ctx.fillStyle='rgba(255,255,255,0.5)';ctx.font='20px sans-serif';ctx.textAlign='center';ctx.fillText('按空格开始',w/2,h/2);}
}

/* ── Code Editor ── */
var codeState={};
function renderCodeEditor(body,winId){
  var s=codeState[winId]||{code:'// FusionOS Code Editor\\nconsole.log("Hello, World!");\\n',lang:'javascript'};
  codeState[winId]=s;
  body.innerHTML='<div class="code-editor-wrap"><textarea class="code-editor-textarea" id="ce-ta-'+winId+'" spellcheck="false">'+escHtml(s.code)+'</textarea><div class="code-editor-stats"><span id="ce-ln-'+winId+'">行: '+s.code.split('\\n').length+' | 字符: '+s.code.length+'</span><div><button class="btn btn-ghost" onclick="codeRun(\\''+winId+'\\')" style="padding:2px 10px;font-size:11px">▶ 运行</button><button class="btn btn-ghost" onclick="codeSave(\\''+winId+'\\')" style="padding:2px 10px;font-size:11px">💾 保存</button></div></div></div>';
  var ta=document.getElementById('ce-ta-'+winId);
  ta.addEventListener('input',function(){var st=codeState[winId];st.code=ta.value;var ln=document.getElementById('ce-ln-'+winId);if(ln)ln.textContent='行: '+st.code.split('\\n').length+' | 字符: '+st.code.length;});
}
function codeRun(winId){
  var s=codeState[winId];
  try{var result=eval(s.code);showToast('ok','运行结果',String(result).slice(0,50));}catch(e){showToast('err','错误',e.message);}
}
function codeSave(winId){
  var s=codeState[winId];localStorage.setItem('fus-code-'+winId,s.code);
  showToast('ok','已保存','代码已保存到本地存储');
}

/* ── Stopwatch App ── */
var swState={};
function renderStopwatchApp(body,winId){
  var s=swState[winId]||{running:false,time:0,laps:[],_int:null};
  swState[winId]=s;
  function fmt(ms){var m=Math.floor(ms/60000),sec=Math.floor((ms%60000)/1000),cs=Math.floor((ms%1000)/10);return ('0'+m).slice(-2)+':'+('0'+sec).slice(-2)+'.'+('0'+cs).slice(-2);}
  var h='<div class="sw-body"><div class="sw-time">'+fmt(s.time)+'</div><div class="sw-btns">';
  h+='<button class="btn btn-primary" onclick="swToggle(\\''+winId+'\\')">'+(s.running?'⏸ 暂停':'▶ 开始')+'</button>';
  h+='<button class="btn btn-ghost" onclick="swLap(\\''+winId+'\\')" '+(s.running?'':'disabled')+'>🏁 计圈</button>';
  h+='<button class="btn btn-ghost" onclick="swState[\\''+winId+'\\']={};var b=document.getElementById(\\'body-'+winId+'\\');if(b)renderStopwatchApp(b,\\''+winId+'\\')">↺ 重置</button></div>';
  if(s.laps.length){h+='<div class="sw-lap-list">';s.laps.forEach(function(l,i){h+='<div class="sw-lap-item"><span>圈 '+(i+1)+'</span><span>'+fmt(l)+'</span></div>';});h+='</div>';}
  h+='</div>';body.innerHTML=h;
}
function swToggle(winId){var s=swState[winId];if(!s.running){s.running=true;s._start=Date.now()-s.time;s._int=setInterval(function(){s.time=Date.now()-s._start;var b=document.getElementById('body-'+winId);if(b)renderStopwatchApp(b,winId);},30);}else{s.running=false;clearInterval(s._int);}var b=document.getElementById('body-'+winId);if(b)renderStopwatchApp(b,winId);}
function swLap(winId){var s=swState[winId];s.laps.push(s.time);var b=document.getElementById('body-'+winId);if(b)renderStopwatchApp(b,winId);}

/* ── Unit Converter ── */
function renderConverter(body,winId){
  var cats={length:{m:1,km:1000,cm:0.01,mm:0.001,inch:0.0254,ft:0.3048,yd:0.9144,mi:1609.34},weight:{kg:1,g:0.001,mg:0.000001,lb:0.4536,oz:0.02835},temp:['temp']};
  // Temp is special
  function convert(val,from,to){
    if(from===to)return val;
    if(from==='C'&&to==='F')return val*9/5+32;
    if(from==='F'&&to==='C')return (val-32)*5/9;
    if(from==='C'&&to==='K')return val+273.15;
    if(from==='K'&&to==='C')return val-273.15;
    if(from==='F'&&to==='K')return (val-32)*5/9+273.15;
    if(from==='K'&&to==='F')return (val-273.15)*9/5+32;
    return val;
  }
  body.innerHTML='<div class="conv-body"><div class="conv-row"><input class="conv-input" id="cv-in-'+winId+'" type="number" value="1" oninput="cvDo(\\''+winId+'\\')"><select class="conv-select" id="cv-unit-'+winId+'" onchange="cvDo(\\''+winId+'\\')"><option value="m">米 (m)</option><option value="km">千米 (km)</option><option value="cm">厘米 (cm)</option><option value="mm">毫米 (mm)</option><option value="inch">英寸</option><option value="ft">英尺</option><option value="yd">码</option><option value="mi">英里</option><option value="kg">千克 (kg)</option><option value="g">克 (g)</option><option value="lb">磅</option><option value="oz">盎司</option><option value="C">摄氏 (°C)</option><option value="F">华氏 (°F)</option><option value="K">开尔文 (K)</option></select></div><div class="conv-eq">=</div><div class="conv-row"><div id="cv-out-'+winId+'" class="conv-input" style="background:rgba(30,30,50,0.6);cursor:default">3.281</div><select class="conv-select" id="cv-to-'+winId+'" onchange="cvDo(\\''+winId+'\\')"><option value="m">米 (m)</option><option value="km">千米 (km)</option><option value="cm">厘米 (cm)</option><option value="mm">毫米 (mm)</option><option value="inch">英寸</option><option value="ft" selected>英尺</option><option value="yd">码</option><option value="mi">英里</option><option value="kg">千克 (kg)</option><option value="g">克 (g)</option><option value="lb">磅</option><option value="oz">盎司</option><option value="C">摄氏 (°C)</option><option value="F">华氏 (°F)</option><option value="K">开尔文 (K)</option></select></div></div>';
  setTimeout(function(){cvDo(winId);},50);
}
function cvDo(winId){
  var v=parseFloat(document.getElementById('cv-in-'+winId).value)||0;
  var from=document.getElementById('cv-unit-'+winId).value,to=document.getElementById('cv-to-'+winId).value;
  var lengths={m:1,km:1000,cm:0.01,mm:0.001,inch:0.0254,ft:0.3048,yd:0.9144,mi:1609.34};
  var weights={kg:1,g:0.001,mg:0.000001,lb:0.4536,oz:0.02835};
  var res;
  if(lengths[from]!==undefined&&lengths[to]!==undefined)res=(v*lengths[from])/lengths[to];
  else if(weights[from]!==undefined&&weights[to]!==undefined)res=(v*weights[from])/weights[to];
  else{if(from==='C'&&to==='F')res=v*9/5+32;else if(from==='F'&&to==='C')res=(v-32)*5/9;else if(from==='C'&&to==='K')res=v+273.15;else if(from==='K'&&to==='C')res=v-273.15;else if(from==='F'&&to==='K')res=(v-32)*5/9+273.15;else if(from==='K'&&to==='F')res=(v-273.15)*9/5+32;else res=v;}
  document.getElementById('cv-out-'+winId).textContent=parseFloat(res.toFixed(4));
}

/* ── Reader ── */
function renderReader(body,winId){
  body.innerHTML='<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:12px;color:var(--text-secondary);text-align:center;padding:20px">'
    +'<div style="font-size:48px">📖</div><div style="font-size:18px;font-weight:600;color:var(--text-primary)">文档查看器</div>'
    +'<p>支持 .txt .md .js .css .html .json 文件预览</p>'
    +'<textarea id="rd-in-'+winId+'" style="width:80%;height:200px;background:rgba(255,255,255,0.06);border:1.5px solid rgba(255,255,255,0.12);border-radius:10px;color:var(--text-primary);padding:16px;font-family:var(--font-mono);font-size:13px;resize:none;outline:none" placeholder="粘贴文本内容…"></textarea>'
    +'<button class="btn btn-primary" onclick="readerPreview(\\''+winId+'\\')">预览</button>'
    +'<div id="rd-prev-'+winId+'" style="width:80%;max-height:200px;overflow:auto;background:rgba(30,30,50,0.6);border-radius:10px;padding:16px;text-align:left;white-space:pre-wrap;font-size:13px;line-height:1.6;display:none"></div>'
    +'</div>';
}
function readerPreview(winId){
  var txt=document.getElementById('rd-in-'+winId).value;
  var prev=document.getElementById('rd-prev-'+winId);
  if(txt){prev.style.display='block';prev.textContent=txt;}else{prev.style.display='none';}
}

/* ── Password Generator ── */
function renderPassword(body,winId){
  var s=passState||{len:16,upper:true,lower:true,num:true,sym:true};window._pwWin=winId;
  function gen(){var chars='';var up='ABCDEFGHJKLMNPQRSTUVWXYZ',lo='abcdefghjkmnpqrstuvwxyz',n='23456789',sy='!@#$%^&*()_+-=[]{}|;:,.<>?';
    if(s.upper)chars+=up;if(s.lower)chars+=lo;if(s.num)chars+=n;if(s.sym)chars+=sy;if(!chars)chars=lo;
    var pw='';for(var i=0;i<s.len;i++)pw+=chars[Math.floor(Math.random()*chars.length)];return pw;}
  body.innerHTML='<div class="pw-body"><div class="pw-display" id="pw-d-'+winId+'">'+gen()+'</div>'
    +'<div class="pw-controls">'
    +'<label class="pw-option"><input type="checkbox" checked onchange="passState.upper=this.checked;pwRefresh(\\''+winId+'\\')"> 大写字母</label>'
    +'<label class="pw-option"><input type="checkbox" checked onchange="passState.lower=this.checked;pwRefresh(\\''+winId+'\\')"> 小写字母</label>'
    +'<label class="pw-option"><input type="checkbox" checked onchange="passState.num=this.checked;pwRefresh(\\''+winId+'\\')"> 数字</label>'
    +'<label class="pw-option"><input type="checkbox" checked onchange="passState.sym=this.checked;pwRefresh(\\''+winId+'\\')"> 符号</label></div>'
    +'<div style="display:flex;gap:8px;align-items:center"><span style="color:var(--text-secondary);font-size:13px">长度: </span>'
    +'<input type="range" min="8" max="64" value="16" style="width:200px" oninput="passState.len=parseInt(this.value);pwRefresh(\\''+winId+'\\');this.nextElementSibling.textContent=this.value"><span style="color:var(--text-primary);font-size:14px;width:30px">16</span></div>'
    +'<button class="btn btn-primary" onclick="pwRefresh(\\''+winId+'\\')">🔄 生成新密码</button>'
    +'<button class="btn btn-ghost" onclick="navigator.clipboard.writeText(document.getElementById(\\'pw-d-'+winId+'\\').textContent);showToast(\\'ok\\',\\'已复制\\',\\'密码已复制到剪贴板\\')">📋 复制</button></div>';
}
var passState={len:16,upper:true,lower:true,num:true,sym:true};
function pwRefresh(winId){
  var chars='';var s=passState;
  var up='ABCDEFGHJKLMNPQRSTUVWXYZ',lo='abcdefghjkmnpqrstuvwxyz',n='23456789',sy='!@#$%^&*()_+-=[]{}|;:,.<>?';
  if(s.upper)chars+=up;if(s.lower)chars+=lo;if(s.num)chars+=n;if(s.sym)chars+=sy;if(!chars)chars=lo;
  var pw='';for(var i=0;i<s.len;i++)pw+=chars[Math.floor(Math.random()*chars.length)];
  var d=document.getElementById('pw-d-'+winId);if(d)d.textContent=pw;
}

/* ── QR Code ── */
function renderQRCode(body,winId){
  body.innerHTML='<div class="qr-body"><div>输入文本生成二维码:</div><input class="qr-input" id="qr-in-'+winId+'" placeholder="输入网址或文本…" oninput="qrGen(\\''+winId+'\\')" value="https://fusionos.dev"><div class="qr-code-box" id="qr-box-'+winId+'"></div></div>';
  setTimeout(function(){qrGen(winId)},100);
}
function qrGen(winId){
  var txt=document.getElementById('qr-in-'+winId).value;
  var box=document.getElementById('qr-box-'+winId);
  if(!txt){box.innerHTML='';return;}
  // Simple QR-like pattern
  var canvas=document.createElement('canvas');canvas.width=180;canvas.height=180;
  var ctx=canvas.getContext('2d');
  ctx.fillStyle='#fff';ctx.fillRect(0,0,180,180);
  ctx.fillStyle='#000';
  // Generate a hash-based pattern
  var hash=0;for(var i=0;i<txt.length;i++){hash=((hash<<5)-hash)+txt.charCodeAt(i);hash|=0;}
  var size=12,bs=15;
  // Corner patterns
  var corners=[[0,0],[7,0],[0,7]];
  corners.forEach(function(c){var x=c[0]*bs,y=c[1]*bs;ctx.fillRect(x,y,bs*3,bs*3);ctx.fillStyle='#fff';ctx.fillRect(x+bs*0.5,y+bs*0.5,bs*2,bs*2);ctx.fillStyle='#000';ctx.fillRect(x+bs,y+bs,bs,bs);ctx.fillStyle='#000';});
  // Data pattern
  for(var r=0;r<size;r++)for(var c=0;c<size;c++){
    if(r<3&&c<3)continue;if(r<3&&c>=size-3)continue;if(r>=size-3&&c<3)continue;
    var seed=Math.abs(hash+r*31+c*17)%100;
    if(seed<40){ctx.fillRect(c*bs,r*bs,bs,bs);}
  }
  box.innerHTML='';box.appendChild(canvas);
}

/* ── Voice Recorder (Simulated) ── */
function renderRecorder(body,winId){
  var s=recState[winId]||{recording:false,recorded:[]};
  recState[winId]=s;
  body.innerHTML='<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:16px;color:var(--text-primary)">'
    +'<div style="width:80px;height:80px;border-radius:50%;background:'+(s.recording?'#e74c3c':'rgba(255,255,255,0.1)')+';display:flex;align-items:center;justify-content:center;transition:all 0.3s;cursor:pointer" onclick="recToggle(\\''+winId+'\\')">'
    +'<div style="font-size:32px">'+(s.recording?'⏹':'⏺')+'</div></div>'
    +'<div>'+s.recorded.length+' 条录音</div>'
    +'<div style="max-height:150px;overflow-y:auto;width:250px">'
    +s.recorded.map(function(r,i){return'<div style="display:flex;justify-content:space-between;padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.05);font-size:12px;color:var(--text-secondary)"><span>录音 '+(i+1)+'</span><span>'+r+'</span></div>';}).join('')
    +'</div></div>';
}
var recState={};
function recToggle(winId){
  var s=recState[winId]||{recording:false,recorded:[]};
  if(!s.recording){s.recording=true;showToast('info','录音','模拟录音已开始（2秒后停止）');
    setTimeout(function(){s.recording=false;var d=new Date();s.recorded.push(d.toLocaleTimeString('zh-CN'));var b=document.getElementById('body-'+winId);if(b)renderRecorder(b,winId);showToast('ok','完成','录音已保存');},2000);
  }else{s.recording=false;}
  var b=document.getElementById('body-'+winId);if(b)renderRecorder(b,winId);
}

/* ── Charts ── */
function renderCharts(body,winId){
  body.innerHTML='<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:12px;padding:16px">'
    +'<canvas id="ch-cvs-'+winId+'" width="400" height="280" style="background:rgba(30,30,50,0.6);border-radius:10px"></canvas>'
    +'<button class="btn btn-primary" onclick="renderCharts(document.getElementById(\\'body-'+winId+'\\'),\\''+winId+'\\')">🔄 刷新数据</button></div>';
  setTimeout(function(){
    var cv=document.getElementById('ch-cvs-'+winId);if(!cv)return;
    var ctx=cv.getContext('2d'),w=400,h=280;
    var data=[],labels=[];for(var i=0;i<7;i++){data.push(Math.floor(20+Math.random()*80));labels.push('周'+(i+1));}
    ctx.fillStyle='rgba(30,30,50,0.9)';ctx.fillRect(0,0,w,h);
    ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.lineWidth=1;
    for(var i=0;i<=4;i++){var y=30+i*55;ctx.beginPath();ctx.moveTo(40,y);ctx.lineTo(w-20,y);ctx.stroke();}
    var barW=30,gap=(w-100)/data.length;
    var maxVal=Math.max.apply(null,data);
    data.forEach(function(v,i){
      var barH=(v/maxVal)*180,x=50+i*gap,y=h-40-barH;
      ctx.fillStyle='hsl('+(200+i*25)+',60%,55%)';ctx.fillRect(x,y,barW,barH);
      ctx.fillStyle='rgba(255,255,255,0.6)';ctx.font='11px sans-serif';ctx.textAlign='center';ctx.fillText(labels[i],x+barW/2,h-22);
      ctx.fillText(v,x+barW/2,y-6);
    });
  },50);
}

/* ── RSS Reader ── */
function renderRSS(body,winId){
  var feeds=[{title:'FusionOS Blog',items:[{title:'FusionOS 7.0 发布！',date:'2026-06-15',desc:'100+新功能、15个新应用'},{title:'性能优化指南',date:'2026-06-10',desc:'提升系统响应速度的技巧'},{title:'开发者工具上线',date:'2026-06-08',desc:'代码编辑器和终端增强'}],url:'https://fusionos.dev/blog'}];
  var h='<div style="display:flex;flex-direction:column;height:100%;overflow-y:auto;padding:16px;gap:8px">';
  feeds.forEach(function(f){h+='<div style="font-size:16px;font-weight:600;color:var(--accent);margin-bottom:4px">'+f.title+'</div>';
    f.items.forEach(function(item){h+='<div style="background:rgba(255,255,255,0.06);border-radius:8px;padding:12px;cursor:pointer" onclick="showToast(\\'info\\',\\''+item.title+'\\',\\''+item.desc+'\\')"><div style="font-weight:600;color:var(--text-primary);font-size:14px">'+item.title+'</div><div style="font-size:11px;color:var(--text-tertiary);margin:4px 0">'+item.date+'</div><div style="font-size:12px;color:var(--text-secondary)">'+item.desc+'</div></div>';});
  });
  h+='</div>';body.innerHTML=h;
}

/* ── Diary ── */
var diaryState={};
function renderDiary(body,winId){
  var s=diaryState[winId]||{date:new Date().toLocaleDateString('zh-CN'),entry:localStorage.getItem('fus-diary-'+winId)||''};
  diaryState[winId]=s;
  body.innerHTML='<div class="diary-body"><div class="diary-header"><div class="diary-date">📅 '+s.date+'</div><button class="btn btn-ghost" onclick="diarySave(\\''+winId+'\\')" style="padding:4px 12px;font-size:12px">💾 保存</button></div><textarea class="diary-textarea" id="diary-ta-'+winId+'" placeholder="今天发生了什么…">'+escHtml(s.entry)+'</textarea></div>';
}
function diarySave(winId){
  var ta=document.getElementById('diary-ta-'+winId);if(!ta)return;
  var s=diaryState[winId];s.entry=ta.value;
  localStorage.setItem('fus-diary-'+winId,ta.value);
  showToast('ok','已保存','日记已保存到本地');
}

/* ── Translator ── */
function renderTranslator(body,winId){
  body.innerHTML='<div class="trans-body"><div class="trans-row"><select class="trans-lang" id="tr-from-'+winId+'"><option value="zh">中文</option><option value="en">英语</option><option value="ja">日语</option><option value="ko">韩语</option><option value="fr">法语</option><option value="de">德语</option><option value="es">西班牙语</option><option value="ru">俄语</option></select><span style="color:var(--text-tertiary);font-size:18px">→</span><select class="trans-lang" id="tr-to-'+winId+'"><option value="zh">中文</option><option value="en" selected>英语</option><option value="ja">日语</option><option value="ko">韩语</option><option value="fr">法语</option><option value="de">德语</option><option value="es">西班牙语</option><option value="ru">俄语</option></select></div><textarea class="trans-input-area" id="tr-in-'+winId+'" placeholder="输入要翻译的文本…"></textarea><button class="btn btn-primary" onclick="trDo(\\''+winId+'\\')">翻译</button><div class="trans-output-area" id="tr-out-'+winId+'">翻译结果将显示在这里</div></div>';
}
function trDo(winId){
  var inp=document.getElementById('tr-in-'+winId).value,from=document.getElementById('tr-from-'+winId).value,to=document.getElementById('tr-to-'+winId).value;
  var out=document.getElementById('tr-out-'+winId);
  if(!inp){out.textContent='请输入文本';return;}
  var demo={zh:{en:'Hello World',ja:'こんにちは世界',ko:'안녕하세요 세계',fr:'Bonjour le monde',de:'Hallo Welt',es:'Hola Mundo',ru:'Привет мир'},en:{zh:'你好世界',ja:'こんにちは世界',ko:'안녕하세요 세계',fr:'Bonjour le monde',de:'Hallo Welt',es:'Hola Mundo',ru:'Привет мир'}};
  if(from===to){out.textContent=inp;return;}
  if(inp==='你好'||inp==='Hello'||inp==='hello'){
    var map={zh:{en:'Hello',ja:'こんにちは',ko:'안녕하세요',fr:'Bonjour',de:'Hallo',es:'Hola',ru:'Здравствуйте'},en:{zh:'你好',ja:'こんにちは',ko:'안녕하세요',fr:'Bonjour',de:'Hallo',es:'Hola',ru:'Здравствуйте'}};
    out.textContent=(map[from]&&map[from][to])||'[翻译: '+inp+']';return;
  }
  out.textContent='[模拟翻译] '+inp+' → ('+to+')';
}

/* ── Stocks ── */
var stockState={stocks:[{code:'600519',name:'贵州茅台',price:1680.50,change:2.35},{code:'000858',name:'五粮液',price:142.30,change:-1.20},{code:'601318',name:'中国平安',price:48.60,change:0.85},{code:'600036',name:'招商银行',price:38.90,change:-0.45},{code:'000333',name:'美的集团',price:62.80,change:1.55},{code:'002415',name:'海康威视',price:35.20,change:-2.10},{code:'300750',name:'宁德时代',price:198.00,change:3.20}],_int:null};
function renderStocks(body,winId){
  var s=stockState;
  if(!s._int){s._int=setInterval(function(){s.stocks.forEach(function(st){st.change+=(Math.random()-0.5)*0.4;st.price+=st.change;if(st.price<5)st.price=5;});var b=document.getElementById('body-'+winId);if(b)renderStocks(b,winId);},5000);}
  var h='<div class="stocks-body">';
  s.stocks.forEach(function(st){var up=st.change>=0,clr=up?'stock-up':'stock-down',bg=up?'stock-up-bg':'stock-down-bg';
    h+='<div class="stock-card"><div><div class="stock-name">'+st.name+'</div><div class="stock-code">'+st.code+'</div></div><div style="text-align:right"><div class="stock-price">¥'+st.price.toFixed(2)+'</div><div class="stock-change '+clr+' '+bg+'">'+(up?'+':'')+st.change.toFixed(2)+'%</div></div></div>';});
  h+='</div>';body.innerHTML=h;
}

'''

# Insert before the "═══ App Implementations ═══" section divider
for i, line in enumerate(lines):
    if 'App Implementations' in line and '/* ═' in line:
        lines.insert(i+2, app_impls)
        break

with open(FILE, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines))

print(f"Phase 2 done: App implementations written ({len(lines)} lines)")
