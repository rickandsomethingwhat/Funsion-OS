#!/usr/bin/env python3
"""Inject all 15 missing render functions into FusionOS 7.0"""

import sys

# Read the file
with open('/Users/murderdrones/Desktop/FusionOS.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Build all 15 render functions as JS code
new_fns = r'''

/* ════════════════════════════════
   15 NEW APP RENDER FUNCTIONS
   ════════════════════════════════ */

/* ── Minesweeper ── */
var mineState = {};
function renderMinesweeper(body, winId) {
  if (!mineState[winId]) {
    var rows = 9, cols = 9, mines = 10;
    var board = []; for (var r = 0; r < rows; r++) { board[r] = []; for (var c = 0; c < cols; c++) board[r][c] = 0; }
    var placed = 0; while (placed < mines) { var rr = Math.floor(Math.random() * rows); var cc = Math.floor(Math.random() * cols); if (board[rr][cc] !== -1) { board[rr][cc] = -1; placed++; } }
    for (var r = 0; r < rows; r++) { for (var c = 0; c < cols; c++) { if (board[r][c] === -1) continue; var cnt = 0; for (var dr = -1; dr <= 1; dr++) { for (var dc = -1; dc <= 1; dc++) { var nr = r + dr; var nc = c + dc; if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && board[nr][nc] === -1) cnt++; } } board[r][c] = cnt; } }
    mineState[winId] = { board: board, revealed: {}, flagged: {}, gameOver: false, won: false, rows: rows, cols: cols, mines: mines, started: false, timer: 0, timerId: null, firstClick: true };
  }
  var ms = mineState[winId];
  body.innerHTML = '<div class="mine-wrap">' +
    '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:rgba(0,0,0,0.2);border-radius:6px;margin-bottom:8px">' +
    '<span style="color:#ff6b6b">\u{1F4A3} ' + (ms.mines - Object.keys(ms.flagged).filter(function(k) { return ms.flagged[k]; }).length) + '</span>' +
    '<span style="color:var(--accent);font-size:18px;font-weight:600" id="mine-timer-' + winId + '">' + String(ms.timer).padStart(3, '0') + '</span>' +
    '<button onclick="mineRestart(\'' + winId + '\')" style="font-size:18px;background:none;border:none;cursor:pointer;color:#fff">\u{1F504}</button>' +
    '</div>' +
    '<div class="mine-board" id="mine-board-' + winId + '" style="display:grid;grid-template-columns:repeat(' + ms.cols + ',32px);gap:2px;justify-content:center">';
  for (var r = 0; r < ms.rows; r++) {
    for (var c = 0; c < ms.cols; c++) {
      var key = r + ',' + c;
      var revealed = ms.revealed[key];
      var flagged = ms.flagged[key];
      var cls = 'mine-cell';
      if (revealed) { cls += ' revealed'; if (ms.board[r][c] === -1) cls += ' mine'; else cls += ' n' + ms.board[r][c]; }
      if (flagged) cls += ' flagged';
      body.innerHTML += '<div class="' + cls + '" onclick="mineClick(\'' + winId + '\',' + r + ',' + c + ')" oncontextmenu="mineFlag(\'' + winId + '\',' + r + ',' + c + ');return false">' + (revealed ? (ms.board[r][c] === -1 ? '\u{1F4A3}' : (ms.board[r][c] || '')) : (flagged ? '\u{1F6A9}' : '')) + '</div>';
    }
  }
  body.innerHTML += '</div>';
  if (ms.gameOver) body.innerHTML += '<div style="text-align:center;padding:10px;color:#ff6b6b;font-size:14px;font-weight:600">\u{1F4A5} \u6E38\u620F\u7ED3\u675F</div>';
  if (ms.won) body.innerHTML += '<div style="text-align:center;padding:10px;color:#51cf66;font-size:14px;font-weight:600">\u{1F389} \u4F60\u8D62\u4E86!</div>';
  body.innerHTML += '</div>';
}

function mineClick(winId, r, c) {
  var ms = mineState[winId]; if (!ms || ms.gameOver || ms.won) return;
  var key = r + ',' + c;
  if (ms.flagged[key]) return;
  if (ms.firstClick) { ms.firstClick = false; ms.started = true; ms.timerId = setInterval(function() { ms.timer++; var el = document.getElementById('mine-timer-' + winId); if (el) el.textContent = String(ms.timer).padStart(3, '0'); }, 1000); }
  if (ms.board[r][c] === -1) {
    ms.revealed[key] = true; ms.gameOver = true;
    for (var rr = 0; rr < ms.rows; rr++) for (var cc = 0; cc < ms.cols; cc++) if (ms.board[rr][cc] === -1) ms.revealed[rr + ',' + cc] = true;
    if (ms.timerId) clearInterval(ms.timerId);
  } else {
    var stack = [{ r: r, c: c }];
    while (stack.length) {
      var p = stack.pop(); var k = p.r + ',' + p.c;
      if (ms.revealed[k] || ms.flagged[k]) continue;
      ms.revealed[k] = true;
      if (ms.board[p.r][p.c] === 0) {
        for (var dr = -1; dr <= 1; dr++) { for (var dc = -1; dc <= 1; dc++) { var nr = p.r + dr; var nc = p.c + dc; if (nr >= 0 && nr < ms.rows && nc >= 0 && nc < ms.cols) stack.push({ r: nr, c: nc }); } }
      }
    }
  }
  var revealed = 0; for (var rr = 0; rr < ms.rows; rr++) for (var cc = 0; cc < ms.cols; cc++) if (ms.revealed[rr + ',' + cc]) revealed++;
  if (revealed === ms.rows * ms.cols - ms.mines && !ms.gameOver) { ms.won = true; if (ms.timerId) clearInterval(ms.timerId); }
  var b = document.getElementById('body-' + winId); if (b) renderMinesweeper(b, winId);
}

function mineFlag(winId, r, c) {
  var ms = mineState[winId]; if (!ms || ms.gameOver || ms.won) return;
  var key = r + ',' + c;
  if (ms.revealed[key]) return;
  ms.flagged[key] = !ms.flagged[key];
  var b = document.getElementById('body-' + winId); if (b) renderMinesweeper(b, winId);
}

function mineRestart(winId) {
  var ms = mineState[winId]; if (!ms) return;
  if (ms.timerId) clearInterval(ms.timerId);
  delete mineState[winId];
  var b = document.getElementById('body-' + winId); if (b) renderMinesweeper(b, winId);
}

/* ── Tetris ── */
var tetrisState = {};
var TETRIS_PIECES = [
  { shape: [[1,1,1,1]], color: '#00f5ff' },
  { shape: [[1,1],[1,1]], color: '#ffd700' },
  { shape: [[0,1,0],[1,1,1]], color: '#ab47bc' },
  { shape: [[1,0,0],[1,1,1]], color: '#42a5f5' },
  { shape: [[0,0,1],[1,1,1]], color: '#ffa726' },
  { shape: [[0,1,1],[1,1,0]], color: '#66bb6a' },
  { shape: [[1,1,0],[0,1,1]], color: '#ef5350' }
];
function renderTetris(body, winId) {
  if (!tetrisState[winId]) {
    tetrisState[winId] = { board: [], piece: null, pieceX: 0, pieceY: 0, score: 0, gameOver: false, paused: false, dropId: null, cols: 10, rows: 20 };
    var ts = tetrisState[winId];
    for (var r = 0; r < ts.rows; r++) { ts.board[r] = []; for (var c = 0; c < ts.cols; c++) ts.board[r][c] = 0; }
    tetrisSpawn(winId);
  }
  var ts = tetrisState[winId];
  body.innerHTML = '<div class="tetris-wrap" style="display:flex;gap:16px;justify-content:center;padding:12px">' +
    '<canvas id="tetris-canvas-' + winId + '" width="' + (ts.cols * 28) + '" height="' + (ts.rows * 28) + '" style="border:2px solid rgba(255,255,255,0.2);border-radius:4px;background:rgba(0,0,0,0.3)"></canvas>' +
    '<div style="display:flex;flex-direction:column;gap:12px;min-width:100px">' +
    '<div style="background:rgba(0,0,0,0.2);padding:10px;border-radius:6px;text-align:center"><div style="font-size:11px;color:var(--text-tertiary)">分数</div><div style="font-size:22px;font-weight:700;color:var(--accent)">' + ts.score + '</div></div>' +
    '<div style="background:rgba(0,0,0,0.2);padding:10px;border-radius:6px;text-align:center"><div style="font-size:11px;color:var(--text-tertiary)">下一个</div><canvas id="tetris-next-' + winId + '" width="112" height="84" style="margin-top:4px"></canvas></div>' +
    '<button onclick="tetrisMove(\'' + winId + '\',\'left\')" style="padding:6px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:4px;color:#fff;cursor:pointer">\u25C0</button>' +
    '<button onclick="tetrisMove(\'' + winId + '\',\'right\')" style="padding:6px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:4px;color:#fff;cursor:pointer">\u25B6</button>' +
    '<button onclick="tetrisMove(\'' + winId + '\',\'rotate\')" style="padding:6px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:4px;color:#fff;cursor:pointer">\u{1F504}</button>' +
    '<button onclick="tetrisMove(\'' + winId + '\',\'drop\')" style="padding:6px;background:var(--accent);border:none;border-radius:4px;color:#fff;cursor:pointer;font-weight:600">\u{2B07} 硬降</button>' +
    '<button onclick="tetrisRestart(\'' + winId + '\')" style="padding:6px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:4px;color:#fff;cursor:pointer">重新开始</button>' +
    '</div></div>';
  tetrisDraw(winId);
  if (!ts.dropId && !ts.gameOver) ts.dropId = setInterval(function() { tetrisMove(winId, 'down'); }, 800);
  if (ts.gameOver) body.innerHTML += '<div style="text-align:center;color:#ff6b6b;font-size:14px;font-weight:600;padding:10px">\u{1F4A5} \u6E38\u620F\u7ED3\u675F - \u5F97\u5206: ' + ts.score + '</div>';
}

function tetrisSpawn(winId) {
  var ts = tetrisState[winId]; if (!ts) return;
  var p = TETRIS_PIECES[Math.floor(Math.random() * TETRIS_PIECES.length)];
  ts.piece = p.shape.map(function(r) { return r.slice(); });
  ts.pieceColor = p.color;
  ts.pieceX = Math.floor((ts.cols - ts.piece[0].length) / 2);
  ts.pieceY = 0;
  if (!tetrisValid(winId, ts.piece, ts.pieceX, ts.pieceY)) { ts.gameOver = true; if (ts.dropId) { clearInterval(ts.dropId); ts.dropId = null; } }
}

function tetrisValid(winId, piece, px, py) {
  var ts = tetrisState[winId];
  for (var r = 0; r < piece.length; r++) {
    for (var c = 0; c < piece[r].length; c++) {
      if (piece[r][c]) { var x = px + c; var y = py + r; if (x < 0 || x >= ts.cols || y >= ts.rows) return false; if (y >= 0 && ts.board[y][x]) return false; }
    }
  }
  return true;
}

function tetrisMove(winId, dir) {
  var ts = tetrisState[winId]; if (!ts || ts.gameOver || ts.paused) return;
  var nx = ts.pieceX, ny = ts.pieceY, piece = ts.piece;
  if (dir === 'left') nx--;
  else if (dir === 'right') nx++;
  else if (dir === 'down') ny++;
  else if (dir === 'rotate') { var rot = piece[0].map(function(_, i) { return piece.map(function(r) { return r[i]; }).reverse(); }); if (tetrisValid(winId, rot, ts.pieceX, ts.pieceY)) ts.piece = rot; }
  else if (dir === 'drop') { while (tetrisValid(winId, ts.piece, ts.pieceX, ts.pieceY + 1)) ts.pieceY++; tetrisPlace(winId); }

  if (dir !== 'rotate' && dir !== 'drop') {
    if (tetrisValid(winId, piece, nx, ny)) { ts.pieceX = nx; ts.pieceY = ny; }
    else if (dir === 'down') tetrisPlace(winId);
  }
  var b = document.getElementById('body-' + winId); if (b && ts.gameOver) { renderTetris(b, winId); return; }
  tetrisDraw(winId);
}

function tetrisPlace(winId) {
  var ts = tetrisState[winId];
  for (var r = 0; r < ts.piece.length; r++) {
    for (var c = 0; c < ts.piece[r].length; c++) {
      if (ts.piece[r][c]) { var y = ts.pieceY + r; var x = ts.pieceX + c; if (y >= 0 && y < ts.rows && x >= 0 && x < ts.cols) ts.board[y][x] = ts.pieceColor; }
    }
  }
  var cleared = 0;
  for (var r = ts.rows - 1; r >= 0; r--) {
    if (ts.board[r].every(function(c) { return c; })) { ts.board.splice(r, 1); ts.board.unshift(new Array(ts.cols).fill(0)); cleared++; r++; }
  }
  if (cleared) ts.score += cleared * cleared * 100;
  tetrisSpawn(winId);
}

function tetrisDraw(winId) {
  var ts = tetrisState[winId]; if (!ts) return;
  var cvs = document.getElementById('tetris-canvas-' + winId); if (!cvs) return;
  var ctx = cvs.getContext('2d');
  var cs = 28;
  ctx.fillStyle = 'rgba(0,0,0,0.3)'; ctx.fillRect(0, 0, ts.cols * cs, ts.rows * cs);
  for (var r = 0; r < ts.rows; r++) {
    for (var c = 0; c < ts.cols; c++) {
      if (ts.board[r][c]) { ctx.fillStyle = ts.board[r][c]; ctx.fillRect(c * cs + 1, r * cs + 1, cs - 2, cs - 2); ctx.fillStyle = 'rgba(255,255,255,0.2)'; ctx.fillRect(c * cs + 1, r * cs + 1, cs - 2, 3); }
    }
  }
  if (ts.piece && !ts.gameOver) {
    ctx.fillStyle = ts.pieceColor;
    for (var r = 0; r < ts.piece.length; r++) {
      for (var c = 0; c < ts.piece[r].length; c++) {
        if (ts.piece[r][c]) { var y = ts.pieceY + r; if (y >= 0) { ctx.fillRect((ts.pieceX + c) * cs + 1, y * cs + 1, cs - 2, cs - 2); ctx.fillStyle = 'rgba(255,255,255,0.3)'; ctx.fillRect((ts.pieceX + c) * cs + 1, y * cs + 1, cs - 2, 3); ctx.fillStyle = ts.pieceColor; } }
      }
    }
  }
  var ncv = document.getElementById('tetris-next-' + winId);
  if (ncv && ts._nextPiece) {
    var nctx = ncv.getContext('2d'); nctx.clearRect(0, 0, 112, 84);
  }
}

function tetrisRestart(winId) {
  var ts = tetrisState[winId]; if (!ts) return;
  if (ts.dropId) clearInterval(ts.dropId);
  delete tetrisState[winId];
  var b = document.getElementById('body-' + winId); if (b) renderTetris(b, winId);
}

/* ── Breakout ── */
var breakoutState = {};
function renderBreakout(body, winId) {
  if (!breakoutState[winId]) {
    var rows = 5, cols = 8;
    var bricks = []; for (var r = 0; r < rows; r++) { bricks[r] = []; for (var c = 0; c < cols; c++) bricks[r][c] = 1; }
    breakoutState[winId] = {
      bricks: bricks, paddleX: 150, ballX: 200, ballY: 250, ballDX: 3, ballDY: -3,
      score: 0, lives: 3, gameOver: false, won: false, running: false, loopId: null,
      rows: rows, cols: cols, canvasW: 400, canvasH: 350
    };
  }
  var bs = breakoutState[winId];
  body.innerHTML = '<div class="breakout-wrap" style="display:flex;flex-direction:column;align-items:center;gap:10px;padding:12px">' +
    '<div style="display:flex;gap:20px;font-size:14px"><span style="color:var(--accent)">\u{2B50} ' + bs.score + '</span><span style="color:#ff6b6b">\u{2764} ' + bs.lives + '</span></div>' +
    '<canvas id="breakout-canvas-' + winId + '" width="' + bs.canvasW + '" height="' + bs.canvasH + '" style="border:2px solid rgba(255,255,255,0.2);border-radius:4px;background:rgba(0,0,0,0.3);cursor:none"></canvas>' +
    '<div style="display:flex;gap:8px">' +
    '<button onclick="breakoutAction(\'' + winId + '\',\'start\')" style="padding:6px 16px;background:var(--accent);border:none;border-radius:4px;color:#fff;cursor:pointer;font-weight:600">' + (bs.running ? '\u23F8 \u6682\u505C' : '\u25B6 \u5F00\u59CB') + '</button>' +
    '<button onclick="breakoutAction(\'' + winId + '\',\'restart\')" style="padding:6px 16px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:4px;color:#fff;cursor:pointer">\u{1F504} \u91CD\u65B0\u5F00\u59CB</button></div>' +
    '</div>';
  breakoutDraw(winId);
  if (bs.running && !bs.loopId) bs.loopId = setInterval(function() { breakoutUpdate(winId); }, 16);
}

function breakoutDraw(winId) {
  var bs = breakoutState[winId]; if (!bs) return;
  var cvs = document.getElementById('breakout-canvas-' + winId); if (!cvs) return;
  var ctx = cvs.getContext('2d');
  ctx.fillStyle = 'rgba(0,0,0,0.3)'; ctx.fillRect(0, 0, bs.canvasW, bs.canvasH);
  var colors = ['#ff6b6b', '#ffa726', '#ffd700', '#66bb6a', '#42a5f5'];
  var bw = bs.canvasW / bs.cols - 4, bh = 16;
  for (var r = 0; r < bs.rows; r++) {
    for (var c = 0; c < bs.cols; c++) {
      if (bs.bricks[r][c]) { ctx.fillStyle = colors[r % colors.length]; ctx.fillRect(c * (bw + 4) + 2, r * (bh + 4) + 20, bw, bh); }
    }
  }
  ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(bs.ballX, bs.ballY, 6, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = 'var(--accent)'; ctx.fillRect(bs.paddleX, bs.canvasH - 25, 100, 12);
  if (!bs.running && !bs.gameOver && !bs.won) { ctx.fillStyle = 'rgba(255,255,255,0.6)'; ctx.font = '16px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('\u70B9\u51FB\u5F00\u59CB\u6E38\u620F', bs.canvasW / 2, bs.canvasH / 2); }
  if (bs.gameOver) { ctx.fillStyle = '#ff6b6b'; ctx.font = '20px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('\u6E38\u620F\u7ED3\u675F', bs.canvasW / 2, bs.canvasH / 2); }
  if (bs.won) { ctx.fillStyle = '#51cf66'; ctx.font = '20px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('\u{1F389} \u4F60\u8D62\u4E86!', bs.canvasW / 2, bs.canvasH / 2); }
}

function breakoutUpdate(winId) {
  var bs = breakoutState[winId]; if (!bs || !bs.running || bs.gameOver || bs.won) return;
  bs.ballX += bs.ballDX; bs.ballY += bs.ballDY;
  if (bs.ballX - 6 <= 0 || bs.ballX + 6 >= bs.canvasW) bs.ballDX = -bs.ballDX;
  if (bs.ballY - 6 <= 0) bs.ballDY = -bs.ballDY;
  if (bs.ballY + 6 >= bs.canvasH) { bs.lives--; bs.ballX = 200; bs.ballY = 250; bs.ballDX = 3; bs.ballDY = -3; bs.running = false; if (bs.lives <= 0) { bs.gameOver = true; if (bs.loopId) { clearInterval(bs.loopId); bs.loopId = null; } } }
  if (bs.ballY + 6 >= bs.canvasH - 25 && bs.ballX > bs.paddleX && bs.ballX < bs.paddleX + 100) { bs.ballDY = -Math.abs(bs.ballDY); bs.ballDX += (bs.ballX - bs.paddleX - 50) / 10; }
  var bw = bs.canvasW / bs.cols - 4, bh = 16;
  for (var r = 0; r < bs.rows; r++) {
    for (var c = 0; c < bs.cols; c++) {
      if (!bs.bricks[r][c]) continue;
      var bx = c * (bw + 4) + 2, by = r * (bh + 4) + 20;
      if (bs.ballX + 6 > bx && bs.ballX - 6 < bx + bw && bs.ballY + 6 > by && bs.ballY - 6 < by + bh) {
        bs.bricks[r][c] = 0; bs.ballDY = -bs.ballDY; bs.score += 10;
        var left = false; for (var rr = 0; rr < bs.rows; rr++) for (var cc = 0; cc < bs.cols; cc++) if (bs.bricks[rr][cc]) left = true;
        if (!left) { bs.won = true; if (bs.loopId) { clearInterval(bs.loopId); bs.loopId = null; } }
      }
    }
  }
  breakoutDraw(winId);
  if (!bs.running || bs.gameOver || bs.won) { if (bs.loopId) { clearInterval(bs.loopId); bs.loopId = null; } var b = document.getElementById('body-' + winId); if (b) renderBreakout(b, winId); }
}

function breakoutAction(winId, action) {
  var bs = breakoutState[winId]; if (!bs) return;
  if (action === 'start') { if (!bs.gameOver && !bs.won) { bs.running = !bs.running; if (bs.running && !bs.loopId) bs.loopId = setInterval(function() { breakoutUpdate(winId); }, 16); } else { breakoutRestart(winId); } }
  else if (action === 'restart') breakoutRestart(winId);
  var b = document.getElementById('body-' + winId); if (b) renderBreakout(b, winId);
}

function breakoutRestart(winId) { var bs = breakoutState[winId]; if (!bs) return; if (bs.loopId) clearInterval(bs.loopId); delete breakoutState[winId]; var b = document.getElementById('body-' + winId); if (b) renderBreakout(b, winId); }

/* ── Code Editor ── */
var codeState = {};
function renderCodeEditor(body, winId) {
  if (!codeState[winId]) codeState[winId] = { code: '// \u6B22\u8FCE\u4F7F\u7528 FusionOS \u4EE3\u7801\u7F16\u8F91\u5668\\nconsole.log("Hello, FusionOS!");\\n', lang: 'js', theme: 'dark' };
  var cs = codeState[winId];
  body.innerHTML = '<div class="code-editor-wrap" style="display:flex;flex-direction:column;height:100%">' +
    '<div style="display:flex;gap:4px;padding:8px;background:rgba(0,0,0,0.2);border-radius:6px 6px 0 0">' +
    '<select onchange="codeSwitchLang(\'' + winId + '\',this.value)" style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:4px 8px;font-size:12px"><option value="js"' + (cs.lang === 'js' ? ' selected' : '') + '>JavaScript</option><option value="py"' + (cs.lang === 'py' ? ' selected' : '') + '>Python</option><option value="html"' + (cs.lang === 'html' ? ' selected' : '') + '>HTML</option></select>' +
    '<button onclick="codeRun(\'' + winId + '\')" style="background:var(--accent);border:none;color:#fff;padding:4px 12px;border-radius:4px;font-size:12px;cursor:pointer;font-weight:600">\u25B6 \u8FD0\u884C</button>' +
    '<span style="flex:1"></span><button onclick="codeClear(\'' + winId + '\')" style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;padding:4px 10px;border-radius:4px;font-size:12px;cursor:pointer">\u6E05\u7A7A</button></div>' +
    '<textarea id="code-input-' + winId + '" style="flex:1;background:#1e1e2e;color:#d4d4d4;border:none;padding:12px;font-family:\'Courier New\',monospace;font-size:13px;resize:none;outline:none;line-height:1.6;border-radius:0 0 6px 6px" spellcheck="false">' + escHtml(cs.code) + '</textarea>' +
    '<div id="code-output-' + winId + '" style="max-height:120px;overflow:auto;background:#12121a;color:#51cf66;padding:8px 12px;font-family:\'Courier New\',monospace;font-size:12px;margin-top:4px;border-radius:4px;display:none"></div>' +
    '</div>';
}

function codeRun(winId) {
  var inp = document.getElementById('code-input-' + winId); var out = document.getElementById('code-output-' + winId); if (!inp || !out) return;
  var cs = codeState[winId]; if (!cs) codeState[winId] = { code: '' }; cs = codeState[winId];
  cs.code = inp.value; out.style.display = 'block'; out.textContent = '';
  try {
    var result;
    if (cs.lang === 'js') { result = eval(inp.value); }
    else if (cs.lang === 'py') { out.textContent = '[Python \u6A21\u62DF] \u8F93\u5165: ' + inp.value.substring(0, 100); }
    else { out.textContent = '[HTML \u9884\u89C8] \u5C06\u5728\u65B0\u7A97\u53E3\u6253\u5F00'; return; }
    out.textContent = '> ' + (result !== undefined ? String(result) : '\u6267\u884C\u5B8C\u6210');
  } catch(e) { out.textContent = 'Error: ' + e.message; }
}

function codeSwitchLang(winId, lang) { var cs = codeState[winId]; if (cs) cs.lang = lang; }
function codeClear(winId) { var inp = document.getElementById('code-input-' + winId); if (inp) inp.value = ''; var out = document.getElementById('code-output-' + winId); if (out) out.style.display = 'none'; var cs = codeState[winId]; if (cs) cs.code = ''; }

/* ── Stopwatch ── */
var swState = {};
function renderStopwatchApp(body, winId) {
  if (!swState[winId]) swState[winId] = { time: 0, running: false, laps: [], intervalId: null };
  var sw = swState[winId];
  var t = sw.time; var ms = t % 100; t = Math.floor(t / 100); var s = t % 60; var m = Math.floor(t / 60);
  body.innerHTML = '<div class="sw-body" style="display:flex;flex-direction:column;align-items:center;gap:16px;padding:20px">' +
    '<div style="font-size:48px;font-weight:300;font-family:\'Courier New\',monospace;color:#fff;font-variant-numeric:tabular-nums">' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0') + '.' + String(ms).padStart(2, '0') + '</div>' +
    '<div style="display:flex;gap:8px">' +
    '<button onclick="swAction(\'' + winId + '\',\'' + (sw.running ? 'stop' : 'start') + '\')" style="padding:8px 20px;background:' + (sw.running ? '#ff6b6b' : 'var(--accent)') + ';border:none;border-radius:6px;color:#fff;font-size:14px;cursor:pointer;font-weight:600">' + (sw.running ? '\u23F9 \u505C\u6B62' : '\u25B6 \u5F00\u59CB') + '</button>' +
    '<button onclick="swAction(\'' + winId + '\',\'lap\')" style="padding:8px 16px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:6px;color:#fff;font-size:14px;cursor:pointer">\u{1F3C1} \u5206\u6BB5</button>' +
    '<button onclick="swAction(\'' + winId + '\',\'reset\')" style="padding:8px 16px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:6px;color:#fff;font-size:14px;cursor:pointer">\u{1F504} \u91CD\u7F6E</button></div>';
  if (sw.laps.length) {
    body.innerHTML += '<div style="width:100%;max-height:150px;overflow:auto"><table style="width:100%;font-size:12px;color:var(--text-secondary)">';
    for (var i = 0; i < sw.laps.length; i++) {
      var lt = sw.laps[i]; var lms = lt % 100; lt = Math.floor(lt / 100); var ls = lt % 60; var lm = Math.floor(lt / 60);
      body.innerHTML += '<tr><td style="padding:4px;color:var(--text-tertiary)">#' + (i + 1) + '</td><td style="padding:4px;text-align:right;font-family:monospace">' + String(lm).padStart(2, '0') + ':' + String(ls).padStart(2, '0') + '.' + String(lms).padStart(2, '0') + '</td></tr>';
    }
    body.innerHTML += '</table></div>';
  }
  body.innerHTML += '</div>';
}

function swAction(winId, action) {
  var sw = swState[winId]; if (!sw) return;
  if (action === 'start') { sw.running = true; sw.intervalId = setInterval(function() { sw.time++; var b = document.getElementById('body-' + winId); if (b) renderStopwatchApp(b, winId); }, 10); }
  else if (action === 'stop') { sw.running = false; if (sw.intervalId) { clearInterval(sw.intervalId); sw.intervalId = null; } }
  else if (action === 'lap') { if (sw.running) sw.laps.push(sw.time); }
  else if (action === 'reset') { sw.running = false; sw.time = 0; sw.laps = []; if (sw.intervalId) { clearInterval(sw.intervalId); sw.intervalId = null; } }
  var b = document.getElementById('body-' + winId); if (b) renderStopwatchApp(b, winId);
}

/* ── Unit Converter ── */
function renderConverter(body, winId) {
  body.innerHTML = '<div class="conv-body" style="padding:16px">' +
    '<div style="margin-bottom:12px"><select id="conv-cat-' + winId + '" onchange="convUpdate(\'' + winId + '\')" style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:6px 10px;font-size:13px;width:100%">' +
    '<option value="length">\u957F\u5EA6 (Length)</option><option value="weight">\u91CD\u91CF (Weight)</option><option value="temp">\u6E29\u5EA6 (Temperature)</option><option value="area">\u9762\u79EF (Area)</option></select></div>' +
    '<div style="display:flex;gap:8px;align-items:center;margin-bottom:8px">' +
    '<input id="conv-from-' + winId + '" type="number" value="1" oninput="convCalc(\'' + winId + '\')" style="flex:1;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:6px 10px;font-size:14px;outline:none">' +
    '<select id="conv-unit1-' + winId + '" onchange="convCalc(\'' + winId + '\')" style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:6px 8px;font-size:12px"></select></div>' +
    '<div style="text-align:center;font-size:20px;margin:4px 0">=</div>' +
    '<div style="display:flex;gap:8px;align-items:center">' +
    '<input id="conv-to-' + winId + '" type="text" readonly style="flex:1;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.2);color:var(--accent);border-radius:4px;padding:6px 10px;font-size:14px;font-weight:600">' +
    '<select id="conv-unit2-' + winId + '" onchange="convCalc(\'' + winId + '\')" style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:6px 8px;font-size:12px"></select></div>' +
    '</div>';
  convUpdate(winId);
}

function convUpdate(winId) {
  var cat = document.getElementById('conv-cat-' + winId); if (!cat) return;
  var units = { length: ['\u7C73 (m)', '\u5343\u7C73 (km)', '\u5398\u7C73 (cm)', '\u6BEB\u7C73 (mm)', '\u82F1\u91CC (mi)', '\u82F1\u5C3A (ft)', '\u82F1\u5BF8 (in)'], weight: ['\u5343\u514B (kg)', '\u514B (g)', '\u6BEB\u514B (mg)', '\u5428 (t)', '\u78C5 (lb)', '\u76CE\u53F8 (oz)'], temp: ['\u6444\u6C0F\u5EA6 (\u00B0C)', '\u534E\u6C0F\u5EA6 (\u00B0F)', '\u5F00\u5C14\u6587 (K)'], area: ['\u5E73\u65B9\u7C73 (m\u00B2)', '\u5E73\u65B9\u5343\u7C73 (km\u00B2)', '\u516C\u9877 (ha)', '\u82F1\u4EA9 (ac)'] };
  var u = units[cat.value] || units.length;
  var s1 = document.getElementById('conv-unit1-' + winId); var s2 = document.getElementById('conv-unit2-' + winId);
  if (s1) { s1.innerHTML = ''; u.forEach(function(un, i) { s1.innerHTML += '<option value="' + i + '"' + (i === 0 ? ' selected' : '') + '>' + un + '</option>'; }); }
  if (s2) { s2.innerHTML = ''; u.forEach(function(un, i) { s2.innerHTML += '<option value="' + i + '"' + (i === 1 ? ' selected' : '') + '>' + un + '</option>'; }); }
  convCalc(winId);
}

function convCalc(winId) {
  var cat = document.getElementById('conv-cat-' + winId); var val = parseFloat(document.getElementById('conv-from-' + winId).value); var u1 = parseInt(document.getElementById('conv-unit1-' + winId).value); var u2 = parseInt(document.getElementById('conv-unit2-' + winId).value); var out = document.getElementById('conv-to-' + winId);
  if (!cat || isNaN(val) || !out) return;
  var conv = {
    length: [1, 1000, 0.01, 0.001, 1609.34, 0.3048, 0.0254],
    weight: [1, 0.001, 0.000001, 1000, 0.453592, 0.0283495],
    temp: null,
    area: [1, 1000000, 10000, 4046.86]
  };
  if (cat.value === 'temp') {
    var c; if (u1 === 0) c = val; else if (u1 === 1) c = (val - 32) * 5 / 9; else c = val - 273.15;
    var result; if (u2 === 0) result = c; else if (u2 === 1) result = c * 9 / 5 + 32; else result = c + 273.15;
    out.value = result.toFixed(2);
  } else {
    var tbl = conv[cat.value]; if (!tbl) { out.value = 'N/A'; return; }
    var meters = val * tbl[u1];
    out.value = (meters / tbl[u2]).toFixed(4);
  }
}

/* ── Document Reader ── */
function renderReader(body, winId) {
  body.innerHTML = '<div class="reader-body" style="padding:20px">' +
    '<div style="font-size:48px;text-align:center;margin-bottom:12px">\u{1F4D6}</div>' +
    '<div style="text-align:center;color:var(--text-tertiary);font-size:13px;margin-bottom:16px">\u6587\u6863\u67E5\u770B\u5668</div>' +
    '<div style="background:rgba(0,0,0,0.15);border-radius:8px;padding:16px;margin-bottom:12px;border:1px solid rgba(255,255,255,0.08)">' +
    '<div style="font-size:14px;font-weight:600;margin-bottom:8px;color:var(--accent)">\u{1F4C4} README.md</div>' +
    '<div style="font-size:12px;line-height:1.8;color:var(--text-secondary)">\u6B22\u8FCE\u4F7F\u7528 <b>FusionOS 7.0</b>\uFF01<br><br>\u8FD9\u662F\u4E00\u4E2A\u5355\u9875 HTML \u684C\u9762\u64CD\u4F5C\u7CFB\u7EDF\u6A21\u62DF\u5668\u3002<br><br>\u{2705} 33 \u4E2A\u5E94\u7528<br>\u{2705} 3 \u6B3E\u6E38\u620F<br>\u{2705} 172 \u6761\u7EC8\u7AEF\u547D\u4EE4<br>\u{2705} 170+ \u7CFB\u7EDF\u529F\u80FD</div></div>' +
    '<div style="background:rgba(0,0,0,0.15);border-radius:8px;padding:12px 16px;border:1px solid rgba(255,255,255,0.08)">' +
    '<div style="font-size:12px;color:var(--text-tertiary)">\u{1F4C1} \u6587\u4EF6\u5217\u8868</div>' +
    '<div style="font-size:12px;color:var(--text-secondary);margin-top:6px">\u{1F4C4} README.md<br>\u{1F4C4} CHANGELOG.txt<br>\u{1F4C4} LICENSE</div></div>' +
    '</div>';
}

/* ── Password Generator ── */
var passState = {};
function renderPassword(body, winId) {
  if (!passState[winId]) passState[winId] = { length: 16, upper: true, lower: true, nums: true, syms: true, lastPass: '' };
  var ps = passState[winId];
  body.innerHTML = '<div class="pw-body" style="padding:16px">' +
    '<div style="font-size:36px;text-align:center;margin-bottom:12px">\u{1F511}</div>' +
    '<div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.15);border-radius:6px;padding:12px;margin-bottom:12px;display:flex;align-items:center;gap:8px">' +
    '<input id="pass-output-' + winId + '" type="text" readonly value="' + escHtml(ps.lastPass) + '" style="flex:1;background:none;border:none;color:var(--accent);font-family:\'Courier New\',monospace;font-size:16px;outline:none">' +
    '<button onclick="passCopy(\'' + winId + '\')" style="background:rgba(255,255,255,0.1);border:none;color:#fff;padding:6px 10px;border-radius:4px;cursor:pointer;font-size:12px">\u{1F4CB} \u590D\u5236</button></div>' +
    '<div style="margin-bottom:12px"><label style="font-size:12px;color:var(--text-tertiary)">\u957F\u5EA6: <span id="pass-len-label-' + winId + '">' + ps.length + '</span></label>' +
    '<input id="pass-len-' + winId + '" type="range" min="4" max="32" value="' + ps.length + '" oninput="document.getElementById(\'pass-len-label-' + winId + '\').textContent=this.value;passState[\'' + winId + '\'].length=parseInt(this.value)" style="width:100%"></div>' +
    '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px">' +
    '<label style="font-size:12px;color:var(--text-secondary);display:flex;align-items:center;gap:4px"><input type="checkbox" ' + (ps.upper ? 'checked' : '') + ' onchange="passState[\'' + winId + '\'].upper=this.checked"> A-Z</label>' +
    '<label style="font-size:12px;color:var(--text-secondary);display:flex;align-items:center;gap:4px"><input type="checkbox" ' + (ps.lower ? 'checked' : '') + ' onchange="passState[\'' + winId + '\'].lower=this.checked"> a-z</label>' +
    '<label style="font-size:12px;color:var(--text-secondary);display:flex;align-items:center;gap:4px"><input type="checkbox" ' + (ps.nums ? 'checked' : '') + ' onchange="passState[\'' + winId + '\'].nums=this.checked"> 0-9</label>' +
    '<label style="font-size:12px;color:var(--text-secondary);display:flex;align-items:center;gap:4px"><input type="checkbox" ' + (ps.syms ? 'checked' : '') + ' onchange="passState[\'' + winId + '\'].syms=this.checked"> !@#$</label></div>' +
    '<button onclick="passGenerate(\'' + winId + '\')" style="width:100%;padding:10px;background:var(--accent);border:none;border-radius:6px;color:#fff;font-size:14px;cursor:pointer;font-weight:600">\u{1F3B2} \u751F\u6210\u5BC6\u7801</button>' +
    '</div>';
}

function passGenerate(winId) {
  var ps = passState[winId]; if (!ps) return;
  var chars = '';
  if (ps.upper) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  if (ps.lower) chars += 'abcdefghijklmnopqrstuvwxyz';
  if (ps.nums) chars += '0123456789';
  if (ps.syms) chars += '!@#$%^&*()_+-=[]{}|;:,.<>?';
  if (!chars) chars = 'abcdefghijklmnopqrstuvwxyz';
  var pass = '';
  for (var i = 0; i < ps.length; i++) pass += chars[Math.floor(Math.random() * chars.length)];
  ps.lastPass = pass;
  var out = document.getElementById('pass-output-' + winId); if (out) out.value = pass;
}

function passCopy(winId) {
  var out = document.getElementById('pass-output-' + winId); if (!out || !out.value) return;
  navigator.clipboard.writeText(out.value).then(function() { showToast('ok', '\u5BC6\u7801\u751F\u6210\u5668', '\u5DF2\u590D\u5236\u5230\u526A\u8D34\u677F'); }).catch(function() {});
}

/* ── QR Code Display ── */
function renderQRCode(body, winId) {
  var qrText = 'https://fusionos.dev';
  body.innerHTML = '<div class="qr-body" style="padding:20px;display:flex;flex-direction:column;align-items:center;gap:16px">' +
    '<div style="font-size:28px">\u{1F4F1}</div>' +
    '<div style="font-size:13px;color:var(--text-tertiary);text-align:center">\u4E8C\u7EF4\u7801\u751F\u6210\u5668</div>' +
    '<input id="qr-text-' + winId + '" type="text" value="' + escHtml(qrText) + '" placeholder="\u8F93\u5165\u6587\u672C\u6216 URL..." style="width:100%;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:8px 12px;font-size:13px;outline:none">' +
    '<canvas id="qr-canvas-' + winId + '" width="180" height="180" style="background:#fff;border-radius:6px;padding:8px"></canvas>' +
    '<div style="font-size:11px;color:var(--text-tertiary)">\u{1F4A1} \u8F93\u5165\u6587\u672C\u540E\u81EA\u52A8\u751F\u6210 QR \u7801</div>' +
    '</div>';
  setTimeout(function() {
    var cvs = document.getElementById('qr-canvas-' + winId); if (cvs) { var ctx = cvs.getContext('2d'); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 164, 164); for (var i = 0; i < 164; i += 8) { for (var j = 0; j < 164; j += 8) { if (Math.random() > 0.5) { ctx.fillStyle = '#fff'; ctx.fillRect(i + 1, j + 1, 6, 6); } } } }
  }, 100);
}

/* ── Voice Recorder (simulated) ── */
var recState = {};
function renderRecorder(body, winId) {
  if (!recState[winId]) recState[winId] = { recording: false, duration: 0, records: [], intervalId: null };
  var rs = recState[winId];
  var d = rs.duration; var s = d % 60; var m = Math.floor(d / 60);
  body.innerHTML = '<div class="rec-body" style="padding:20px;display:flex;flex-direction:column;align-items:center;gap:16px">' +
    '<div style="font-size:48px">\u{1F3A4}</div>' +
    '<div style="font-size:28px;font-family:\'Courier New\',monospace;color:' + (rs.recording ? '#ff6b6b' : '#fff') + '">' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0') + '</div>' +
    '<div style="width:80%;height:40px;background:rgba(0,0,0,0.2);border-radius:4px;overflow:hidden"><div style="height:100%;background:var(--accent);width:' + Math.min(100, (d % 10) * 10) + '%;border-radius:4px;transition:width 0.1s"></div></div>' +
    '<div style="display:flex;gap:8px">' +
    '<button onclick="recAction(\'' + winId + '\',\'' + (rs.recording ? 'stop' : 'start') + '\')" style="padding:10px 24px;background:' + (rs.recording ? '#ff6b6b' : 'var(--accent)') + ';border:none;border-radius:50px;color:#fff;font-size:14px;cursor:pointer;font-weight:600">' + (rs.recording ? '\u23F9 \u505C\u6B62' : '\u23FA \u5F55\u5236') + '</button></div>';
  if (rs.records.length) {
    body.innerHTML += '<div style="width:100%"><div style="font-size:12px;color:var(--text-tertiary);margin-bottom:6px">\u5F55\u97F3\u8BB0\u5F55</div>';
    rs.records.forEach(function(r, i) {
      var ds = r % 60; var dm = Math.floor(r / 60);
      body.innerHTML += '<div style="display:flex;justify-content:space-between;padding:6px 10px;background:rgba(255,255,255,0.05);border-radius:4px;margin-bottom:4px;font-size:12px"><span>\u5F55\u97F3 #' + (i + 1) + '</span><span style="color:var(--text-tertiary);font-family:monospace">' + String(dm).padStart(2, '0') + ':' + String(ds).padStart(2, '0') + '</span></div>';
    });
    body.innerHTML += '</div>';
  }
  body.innerHTML += '</div>';
  if (rs.recording && !rs.intervalId) rs.intervalId = setInterval(function() { rs.duration++; var b = document.getElementById('body-' + winId); if (b) renderRecorder(b, winId); }, 1000);
}

function recAction(winId, action) {
  var rs = recState[winId]; if (!rs) return;
  if (action === 'start') { rs.recording = true; rs.duration = 0; }
  else if (action === 'stop') { rs.recording = false; if (rs.intervalId) { clearInterval(rs.intervalId); rs.intervalId = null; } if (rs.duration > 0) rs.records.push(rs.duration); rs.duration = 0; }
  var b = document.getElementById('body-' + winId); if (b) renderRecorder(b, winId);
}

/* ── Charts ── */
function renderCharts(body, winId) {
  body.innerHTML = '<div class="charts-body" style="padding:16px">' +
    '<div style="text-align:center;font-size:24px;margin-bottom:12px">\u{1F4CA}</div>' +
    '<div style="margin-bottom:16px"><select onchange="chartRender(\'' + winId + '\',this.value)" style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:6px 10px;font-size:13px;width:100%">' +
    '<option value="bar">\u67F1\u72B6\u56FE</option><option value="line">\u6298\u7EBF\u56FE</option><option value="pie">\u997C\u56FE</option></select></div>' +
    '<canvas id="chart-canvas-' + winId + '" width="350" height="200" style="width:100%;background:rgba(0,0,0,0.2);border-radius:6px"></canvas>' +
    '</div>';
  setTimeout(function() { chartRender(winId, 'bar'); }, 50);
}

function chartRender(winId, type) {
  var cvs = document.getElementById('chart-canvas-' + winId); if (!cvs) return;
  var ctx = cvs.getContext('2d'); ctx.clearRect(0, 0, 350, 200);
  var data = [45, 72, 38, 90, 55, 68, 30]; var colors = ['#42a5f5', '#66bb6a', '#ffa726', '#ef5350', '#ab47bc', '#ffd700', '#26c6da'];
  var labels = ['\u5468\u4E00', '\u5468\u4E8C', '\u5468\u4E09', '\u5468\u56DB', '\u5468\u4E94', '\u5468\u516D', '\u5468\u65E5'];
  if (type === 'bar') {
    var bw = 30, gap = 15, maxV = 100, baseY = 170;
    data.forEach(function(v, i) {
      var h = (v / maxV) * 140;
      ctx.fillStyle = colors[i % colors.length];
      ctx.fillRect(30 + i * (bw + gap), baseY - h, bw, h);
      ctx.fillStyle = '#fff'; ctx.font = '10px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(v, 30 + i * (bw + gap) + bw / 2, baseY - h - 6);
      ctx.fillText(labels[i], 30 + i * (bw + gap) + bw / 2, baseY + 14);
    });
  } else if (type === 'line') {
    ctx.strokeStyle = 'var(--accent)'; ctx.lineWidth = 2; ctx.beginPath();
    data.forEach(function(v, i) { var x = 40 + i * 45; var y = 170 - (v / 100) * 150; if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); });
    ctx.stroke();
    data.forEach(function(v, i) { var x = 40 + i * 45; var y = 170 - (v / 100) * 150; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, 4, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = '#fff'; ctx.font = '10px sans-serif'; ctx.textAlign = 'center'; ctx.fillText(v, x, y - 10); ctx.fillText(labels[i], x, 190); });
  } else if (type === 'pie') {
    var total = data.reduce(function(a, b) { return a + b; }, 0);
    var angle = -Math.PI / 2;
    data.forEach(function(v, i) {
      var slice = (v / total) * Math.PI * 2;
      ctx.fillStyle = colors[i % colors.length]; ctx.beginPath(); ctx.moveTo(175, 90); ctx.arc(175, 90, 70, angle, angle + slice); ctx.fill();
      var mid = angle + slice / 2; ctx.fillStyle = '#fff'; ctx.font = '10px sans-serif'; ctx.textAlign = 'center'; ctx.fillText(v, 175 + Math.cos(mid) * 40, 90 + Math.sin(mid) * 40);
      angle += slice;
    });
  }
}

/* ── RSS Reader ── */
function renderRSS(body, winId) {
  var articles = [
    { title: '\u{1F4E2} FusionOS 7.0 \u53D1\u5E03', desc: '\u5168\u65B0\u7248\u672C\u5E26\u6765 15 \u4E2A\u65B0\u5E94\u7528\u548C 170+ \u529F\u80FD', date: '2026-06-15' },
    { title: '\u{1F3AE} \u4E09\u6B3E\u65B0\u6E38\u620F\u4E0A\u7EBF', desc: '\u626B\u96F7\u3001\u4FC4\u7F57\u65AF\u65B9\u5757\u3001\u6253\u7816\u5757\u73B0\u5DF2\u53EF\u73A9', date: '2026-06-14' },
    { title: '\u{1F4BB} \u4EE3\u7801\u7F16\u8F91\u5668\u4E0A\u7EBF', desc: '\u652F\u6301 JS/Python/HTML \u5B9E\u65F6\u8FD0\u884C', date: '2026-06-13' }
  ];
  body.innerHTML = '<div class="rss-body" style="padding:16px"><div style="font-size:20px;font-weight:600;margin-bottom:12px;color:var(--accent)">\u{1F4F0} RSS \u9605\u8BFB\u5668</div>';
  articles.forEach(function(a) {
    body.innerHTML += '<div style="background:rgba(0,0,0,0.15);border:1px solid rgba(255,255,255,0.08);border-radius:6px;padding:12px;margin-bottom:8px;cursor:pointer"><div style="font-size:14px;font-weight:500;margin-bottom:4px">' + a.title + '</div><div style="font-size:12px;color:var(--text-secondary);margin-bottom:4px">' + a.desc + '</div><div style="font-size:10px;color:var(--text-tertiary)">' + a.date + '</div></div>';
  });
  body.innerHTML += '<div style="text-align:center;padding:12px;color:var(--text-tertiary);font-size:12px">\u{1F4A1} \u8FD9\u662F\u6A21\u62DF RSS \u6E90</div></div>';
}

/* ── Diary ── */
var diaryState = {};
function renderDiary(body, winId) {
  if (!diaryState[winId]) diaryState[winId] = { entries: [], editing: false };
  var ds = diaryState[winId];
  var today = new Date().toISOString().split('T')[0];
  body.innerHTML = '<div class="diary-body" style="padding:16px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><span style="font-size:18px;font-weight:600;color:var(--accent)">\u{1F4D3} \u65E5\u8BB0</span><span style="font-size:12px;color:var(--text-tertiary)">' + today + '</span></div>';
  if (ds.editing) {
    body.innerHTML += '<textarea id="diary-input-' + winId + '" style="width:100%;height:100px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:10px;font-size:13px;resize:none;outline:none;box-sizing:border-box" placeholder="\u4ECA\u5929\u53D1\u751F\u4E86\u4EC0\u4E48..."></textarea>' +
    '<div style="display:flex;gap:8px;margin-top:8px">' +
    '<button onclick="diarySave(\'' + winId + '\')" style="padding:6px 16px;background:var(--accent);border:none;border-radius:4px;color:#fff;font-size:13px;cursor:pointer;font-weight:600">\u4FDD\u5B58</button>' +
    '<button onclick="diaryState[\'' + winId + '\'].editing=false;renderDiary(document.getElementById(\'body-' + winId + '\'),\'' + winId + '\')" style="padding:6px 12px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:4px;color:#fff;font-size:13px;cursor:pointer">\u53D6\u6D88</button></div>';
  } else {
    body.innerHTML += '<button onclick="diaryState[\'' + winId + '\'].editing=true;renderDiary(document.getElementById(\'body-' + winId + '\'),\'' + winId + '\')" style="width:100%;padding:10px;background:rgba(255,255,255,0.1);border:1px dashed rgba(255,255,255,0.2);border-radius:6px;color:var(--accent);font-size:14px;cursor:pointer">+ \u5199\u65E5\u8BB0</button>';
  }
  if (ds.entries.length) {
    body.innerHTML += '<div style="margin-top:16px">';
    ds.entries.forEach(function(e, i) {
      body.innerHTML += '<div style="background:rgba(0,0,0,0.15);border:1px solid rgba(255,255,255,0.08);border-radius:6px;padding:10px 12px;margin-bottom:6px"><div style="display:flex;justify-content:space-between;font-size:12px;color:var(--text-tertiary);margin-bottom:4px"><span>' + e.date + '</span><button onclick="diaryState[\'' + winId + '\'].entries.splice(' + i + ',1);renderDiary(document.getElementById(\'body-' + winId + '\'),\'' + winId + '\')" style="background:none;border:none;color:#ff6b6b;cursor:pointer;font-size:12px">\u2715</button></div><div style="font-size:13px;color:var(--text-secondary);white-space:pre-wrap">' + escHtml(e.text) + '</div></div>';
    });
    body.innerHTML += '</div>';
  }
  body.innerHTML += '</div>';
}

function diarySave(winId) {
  var inp = document.getElementById('diary-input-' + winId); if (!inp || !inp.value.trim()) return;
  var ds = diaryState[winId]; if (!ds) diaryState[winId] = { entries: [], editing: false }; ds = diaryState[winId];
  ds.entries.unshift({ text: inp.value.trim(), date: new Date().toISOString().split('T')[0] });
  ds.editing = false;
  var b = document.getElementById('body-' + winId); if (b) renderDiary(b, winId);
}

/* ── Translator ── */
function renderTranslator(body, winId) {
  body.innerHTML = '<div class="trans-body" style="padding:16px">' +
    '<div style="font-size:32px;text-align:center;margin-bottom:12px">\u{1F310}</div>' +
    '<div style="display:flex;gap:8px;align-items:center;margin-bottom:8px">' +
    '<select id="trans-from-' + winId + '" style="flex:1;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:6px 8px;font-size:12px">' +
    '<option value="zh">\u{1F1E8}\u{1F1F3} \u4E2D\u6587</option><option value="en">\u{1F1FA}\u{1F1F8} English</option><option value="ja">\u{1F1EF}\u{1F1F5} \u65E5\u672C\u8A9E</option><option value="ko">\u{1F1F0}\u{1F1F7} \uD55C\uAD6D\uC5B4</option></select>' +
    '<span style="color:var(--text-tertiary)">\u2192</span>' +
    '<select id="trans-to-' + winId + '" style="flex:1;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:6px 8px;font-size:12px">' +
    '<option value="en">\u{1F1FA}\u{1F1F8} English</option><option value="zh">\u{1F1E8}\u{1F1F3} \u4E2D\u6587</option><option value="ja">\u{1F1EF}\u{1F1F5} \u65E5\u672C\u8A9E</option><option value="ko">\u{1F1F0}\u{1F1F7} \uD55C\uAD6D\uC5B4</option></select></div>' +
    '<textarea id="trans-input-' + winId + '" placeholder="\u8F93\u5165\u8981\u7FFB\u8BD1\u7684\u6587\u672C..." style="width:100%;height:80px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:4px;padding:10px;font-size:13px;resize:none;outline:none;box-sizing:border-box;margin-bottom:8px"></textarea>' +
    '<button onclick="transDo(\'' + winId + '\')" style="width:100%;padding:10px;background:var(--accent);border:none;border-radius:6px;color:#fff;font-size:14px;cursor:pointer;font-weight:600">\u{1F500} \u7FFB\u8BD1</button>' +
    '<textarea id="trans-output-' + winId + '" readonly placeholder="\u7FFB\u8BD1\u7ED3\u679C\u5C06\u663E\u793A\u5728\u8FD9\u91CC..." style="width:100%;height:80px;background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.15);color:var(--accent);border-radius:4px;padding:10px;font-size:13px;resize:none;outline:none;box-sizing:border-box;margin-top:8px"></textarea>' +
    '</div>';
}

function transDo(winId) {
  var inp = document.getElementById('trans-input-' + winId); var out = document.getElementById('trans-output-' + winId); if (!inp || !out || !inp.value.trim()) return;
  var from = document.getElementById('trans-from-' + winId).value; var to = document.getElementById('trans-to-' + winId).value;
  if (from === to) { out.value = inp.value; return; }
  var dict = {
    'zh-en': { '\u4F60\u597D': 'Hello', '\u8C22\u8C22': 'Thank you', '\u4E16\u754C': 'World' },
    'en-zh': { 'Hello': '\u4F60\u597D', 'Thank you': '\u8C22\u8C22', 'World': '\u4E16\u754C' }
  };
  var key = from + '-' + to;
  out.value = (dict[key] && dict[key][inp.value.trim()]) ? dict[key][inp.value.trim()] : '[\u6A21\u62DF\u7FFB\u8BD1] ' + inp.value;
}

/* ── Stocks ── */
function renderStocks(body, winId) {
  var stocks = [
    { symbol: 'AAPL', name: 'Apple Inc.', price: 218.45, change: 2.3, color: '#ff4444' },
    { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 185.32, change: -1.2, color: '#44ff44' },
    { symbol: 'TSLA', name: 'Tesla Inc.', price: 248.70, change: 5.8, color: '#ff4444' },
    { symbol: 'MSFT', name: 'Microsoft', price: 445.12, change: 0.5, color: '#ff4444' },
    { symbol: 'NVDA', name: 'NVIDIA Corp', price: 128.90, change: -3.2, color: '#44ff44' }
  ];
  body.innerHTML = '<div class="stocks-body" style="padding:16px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><span style="font-size:18px;font-weight:600;color:var(--accent)">\u{1F4C8} \u80A1\u7968\u5E02\u573A</span><span style="font-size:10px;color:var(--text-tertiary)">\u6A21\u62DF\u6570\u636E</span></div>';
  stocks.forEach(function(s) {
    body.innerHTML += '<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:rgba(0,0,0,0.15);border:1px solid rgba(255,255,255,0.08);border-radius:6px;margin-bottom:6px">' +
      '<div><div style="font-size:13px;font-weight:600">' + s.symbol + '</div><div style="font-size:10px;color:var(--text-tertiary)">' + s.name + '</div></div>' +
      '<div style="text-align:right"><div style="font-size:14px;font-weight:600">\u00A5' + s.price.toFixed(2) + '</div><div style="font-size:12px;color:' + s.color + '">' + (s.change >= 0 ? '+' : '') + s.change.toFixed(2) + '%</div></div></div>';
  });
  body.innerHTML += '<div style="text-align:center;padding:12px;color:var(--text-tertiary);font-size:11px">\u{1F4A1} \u6570\u636E\u4EC5\u4E3A\u6A21\u62DF\uFF0C\u4E0D\u4EE3\u8868\u5B9E\u9645\u5E02\u573A</div></div>';
}

/* ════════════════════════════════ */
'''

# Find injection point: after "function taskFilter..." and before "/* ══ 50+ SYSTEM FEATURES"
inject_marker = '/* ════════════════════════════════\n   50+ SYSTEM FEATURES\n   ════════════════════════════════ */'

if inject_marker in html:
    html = html.replace(inject_marker, new_fns + '\n' + inject_marker)
    with open('/Users/murderdrones/Desktop/FusionOS.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('OK: injected at marker')
else:
    print('ERROR: marker not found')
