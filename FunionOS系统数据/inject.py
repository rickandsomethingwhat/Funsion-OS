#!/usr/bin/env python3
"""FusionOS 7.0 Mega-Upgrade Injector — 15 Apps + 100 Features + 170 Terminal Cmds"""
import re, os

FILE = '/Users/murderdrones/WorkBuddy/2026-06-15-12-25-08/vm-os.html'

with open(FILE, 'r', encoding='utf-8') as fh:
    content = fh.read()

lines = content.split('\n')

# ============================================================
# 1. NEW SVG ICONS (before </svg> at line 1267)
# ============================================================
svg_icons = '''
  <symbol id="ic-minesweeper" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="3" fill="currentColor"/><line x1="12" y1="2" x2="12" y2="6" stroke="currentColor" stroke-width="2"/><line x1="12" y1="18" x2="12" y2="22" stroke="currentColor" stroke-width="2"/><line x1="2" y1="12" x2="6" y2="12" stroke="currentColor" stroke-width="2"/><line x1="18" y1="12" x2="22" y2="12" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="ic-tetris" viewBox="0 0 24 24"><rect x="2" y="2" width="6" height="6" rx="1" fill="currentColor"/><rect x="10" y="2" width="5" height="6" rx="1" fill="currentColor" opacity="0.6"/><rect x="17" y="2" width="5" height="6" rx="1" fill="currentColor" opacity="0.3"/><rect x="2" y="10" width="6" height="5" rx="1" fill="currentColor" opacity="0.8"/><rect x="10" y="10" width="6" height="5" rx="1" fill="currentColor" opacity="0.5"/><rect x="2" y="17" width="6" height="5" rx="1" fill="currentColor" opacity="0.4"/><rect x="10" y="17" width="5" height="5" rx="1" fill="currentColor" opacity="0.7"/></symbol>
  <symbol id="ic-breakout" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="3" rx="1.5" fill="currentColor"/><rect x="5" y="8" width="4" height="2" rx="0.5" fill="currentColor" opacity="0.8"/><rect x="11" y="8" width="4" height="2" rx="0.5" fill="currentColor" opacity="0.6"/><rect x="17" y="8" width="3" height="2" rx="0.5" fill="currentColor" opacity="0.4"/><rect x="8" y="12" width="4" height="2" rx="0.5" fill="currentColor" opacity="0.3"/><rect x="8" y="20" width="7" height="2" rx="1" fill="currentColor"/><circle cx="11" cy="17" r="1.2" fill="currentColor"/></symbol>
  <symbol id="ic-code-editor" viewBox="0 0 24 24"><polyline points="7 8 3 12 7 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><polyline points="17 8 21 12 17 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="14" y1="5" x2="10" y2="19" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
  <symbol id="ic-stopwatch-app" viewBox="0 0 24 24"><circle cx="12" cy="13" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="12" y1="13" x2="16" y2="10" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="4" x2="12" y2="6" stroke="currentColor" stroke-width="2"/><line x1="9" y1="2" x2="15" y2="2" stroke="currentColor" stroke-width="1.8"/></symbol>
  <symbol id="ic-converter" viewBox="0 0 24 24"><path d="M7 3L3 8h8L7 3z" fill="currentColor"/><path d="M17 21l4-5h-8l4 5z" fill="currentColor" opacity="0.6"/><line x1="12" y1="5" x2="12" y2="19" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 2"/></symbol>
  <symbol id="ic-reader" viewBox="0 0 24 24"><rect x="3" y="2" width="18" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="7" y1="7" x2="17" y2="7" stroke="currentColor" stroke-width="1.2"/><line x1="7" y1="11" x2="17" y2="11" stroke="currentColor" stroke-width="1.2"/><line x1="7" y1="15" x2="13" y2="15" stroke="currentColor" stroke-width="1.2"/></symbol>
  <symbol id="ic-password" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="16.5" r="2.5" fill="currentColor"/><path d="M8 11V7a4 4 0 118 0v4" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
  <symbol id="ic-qrcode" viewBox="0 0 24 24"><rect x="2" y="2" width="8" height="8" rx="1" fill="currentColor"/><rect x="3" y="3" width="2" height="2" rx="0.3" fill="#fff"/><rect x="7" y="3" width="2" height="2" rx="0.3" fill="#fff"/><rect x="3" y="7" width="2" height="2" rx="0.3" fill="#fff"/><rect x="14" y="2" width="8" height="8" rx="1" fill="currentColor" opacity="0.3"/><rect x="2" y="14" width="8" height="8" rx="1" fill="currentColor" opacity="0.6"/><rect x="14" y="14" width="2" height="2" fill="currentColor"/><rect x="18" y="14" width="2" height="2" fill="currentColor"/></symbol>
  <symbol id="ic-recorder" viewBox="0 0 24 24"><circle cx="12" cy="12" r="6" fill="currentColor"/><circle cx="12" cy="12" r="2" fill="#fff"/><path d="M12 2v3M12 19v3M4 12H1M23 12h-3" stroke="currentColor" stroke-width="1.5"/></symbol>
  <symbol id="ic-charts" viewBox="0 0 24 24"><rect x="3" y="14" width="4" height="7" rx="1" fill="currentColor"/><rect x="10" y="8" width="4" height="13" rx="1" fill="currentColor" opacity="0.7"/><rect x="17" y="5" width="4" height="16" rx="1" fill="currentColor" opacity="0.4"/></symbol>
  <symbol id="ic-rss" viewBox="0 0 24 24"><circle cx="6" cy="18" r="3" fill="currentColor"/><path d="M4 4a16 16 0 0116 16h-4A12 12 0 004 8z" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M4 10a10 10 0 0110 10" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.5"/></symbol>
  <symbol id="ic-diary" viewBox="0 0 24 24"><rect x="5" y="2" width="15" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="10" y1="2" x2="10" y2="22" stroke="currentColor" stroke-width="0.8" opacity="0.4"/><line x1="5" y1="8" x2="10" y2="8" stroke="currentColor" stroke-width="0.8"/><line x1="5" y1="14" x2="10" y2="14" stroke="currentColor" stroke-width="0.8"/></symbol>
  <symbol id="ic-translator" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="2" y1="12" x2="22" y2="12" stroke="currentColor" stroke-width="1.2"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10A15.3 15.3 0 018 12 15.3 15.3 0 0112 2z" fill="none" stroke="currentColor" stroke-width="1.2"/></symbol>
  <symbol id="ic-stocks" viewBox="0 0 24 24"><polyline points="3 18 8 13 12 16 16 10 21 14" fill="none" stroke="currentColor" stroke-width="1.8"/><rect x="1" y="3" width="22" height="17" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/></symbol>
  <symbol id="ic-dice" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="8" cy="8" r="1.5" fill="currentColor"/><circle cx="16" cy="16" r="1.5" fill="currentColor"/></symbol>
  <symbol id="ic-flag" viewBox="0 0 24 24"><line x1="4" y1="3" x2="4" y2="22" stroke="currentColor" stroke-width="2"/><path d="M4 4h14l-3 5 3 5H4z" fill="currentColor"/></symbol>
  <symbol id="ic-target" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="2" fill="currentColor"/></symbol>
  <symbol id="ic-clipboard" viewBox="0 0 24 24"><rect x="8" y="2" width="8" height="4" rx="1" fill="currentColor" opacity="0.3"/><rect x="6" y="4" width="12" height="17" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
  <symbol id="ic-book" viewBox="0 0 24 24"><path d="M4 4h7v16H4a2 2 0 01-2-2V6a2 2 0 012-2z" fill="currentColor" opacity="0.4"/><path d="M13 4h7a2 2 0 012 2v12a2 2 0 01-2 2h-7z" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="8" y1="8" x2="11" y2="8" stroke="#fff" stroke-width="1"/><line x1="8" y1="12" x2="11" y2="12" stroke="#fff" stroke-width="1"/></symbol>
  <symbol id="ic-terminal-new" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><polyline points="6 9 9 12 6 15" stroke="currentColor" stroke-width="1.5"/><line x1="11" y1="15" x2="16" y2="15" stroke="currentColor" stroke-width="1.5"/></symbol>
  <symbol id="ic-fork" viewBox="0 0 24 24"><circle cx="6" cy="6" r="2.5" fill="currentColor"/><circle cx="18" cy="6" r="2.5" fill="currentColor" opacity="0.5"/><circle cx="12" cy="18" r="2.5" fill="currentColor" opacity="0.3"/><path d="M6 8.5V18h3" stroke="currentColor" stroke-width="1.5"/></symbol>
  <symbol id="ic-bug" viewBox="0 0 24 24"><ellipse cx="12" cy="14" rx="8" ry="6" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="8" y1="8" x2="3" y2="3" stroke="currentColor" stroke-width="1.5"/><line x1="16" y1="8" x2="21" y2="3" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="20" x2="12" y2="23" stroke="currentColor" stroke-width="1.5"/></symbol>
  <symbol id="ic-crown" viewBox="0 0 24 24"><path d="M3 18l3-12 6 9 6-9 3 12H3z" fill="none" stroke="currentColor" stroke-width="1.8"/><rect x="6" y="18" width="12" height="3" rx="1" fill="currentColor"/></symbol>
  <symbol id="ic-bomb" viewBox="0 0 24 24"><circle cx="12" cy="13" r="8" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="12" y1="5" x2="12" y2="6" stroke="currentColor" stroke-width="1.5"/><line x1="8" y1="7" x2="9" y2="8" stroke="currentColor" stroke-width="1.5"/></symbol>
  <symbol id="ic-pacman" viewBox="0 0 24 24"><path d="M12 2a10 10 0 110 20 10 10 0 010-20zM12 12l5-5-5 5 5 5z" fill="currentColor"/><circle cx="18" cy="6" r="1.2" fill="#fff"/><circle cx="18" cy="14" r="1.2" fill="#fff"/></symbol>
  <symbol id="ic-printer" viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="6" rx="1" fill="currentColor" opacity="0.3"/><rect x="5" y="12" width="14" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="8" y1="16" x2="16" y2="16" stroke="currentColor" stroke-width="1.2"/></symbol>
  <symbol id="ic-sliders" viewBox="0 0 24 24"><line x1="4" y1="21" x2="4" y2="14" stroke="currentColor" stroke-width="2"/><line x1="4" y1="10" x2="4" y2="3" stroke="currentColor" stroke-width="2"/><line x1="12" y1="21" x2="12" y2="12" stroke="currentColor" stroke-width="2"/><line x1="12" y1="8" x2="12" y2="3" stroke="currentColor" stroke-width="2"/><line x1="20" y1="21" x2="20" y2="16" stroke="currentColor" stroke-width="2"/><line x1="20" y1="12" x2="20" y2="3" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="ic-layers" viewBox="0 0 24 24"><polygon points="12 3 2 9 12 15 22 9" fill="currentColor" opacity="0.4"/><polygon points="12 8 2 14 12 20 22 14" fill="none" stroke="currentColor" stroke-width="1.5"/></symbol>
  <symbol id="ic-grid-3x3" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1" fill="currentColor" opacity="0.6"/><rect x="14" y="3" width="7" height="7" rx="1" fill="currentColor" opacity="0.4"/><rect x="3" y="14" width="7" height="7" rx="1" fill="currentColor" opacity="0.8"/><rect x="14" y="14" width="7" height="7" rx="1" fill="currentColor" opacity="0.3"/></symbol>
  <symbol id="ic-link" viewBox="0 0 24 24"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
  <symbol id="ic-palette" viewBox="0 0 24 24"><path d="M12 2a10 10 0 1010 10c0-5.5-4-10-8-10z" fill="currentColor"/><circle cx="8" cy="10" r="1.5" fill="#fff"/><circle cx="12" cy="8" r="1.5" fill="#fff"/><circle cx="16" cy="10" r="1.5" fill="#fff"/><circle cx="10" cy="15" r="1.5" fill="#fff"/><circle cx="14" cy="15" r="1.5" fill="#fff"/></symbol>
  <symbol id="ic-trophy" viewBox="0 0 24 24"><path d="M6 4h12v4a6 6 0 01-12 0V4z" fill="none" stroke="currentColor" stroke-width="1.8"/><rect x="8" y="16" width="8" height="5" rx="1" fill="currentColor" opacity="0.4"/><rect x="9" y="21" width="6" height="2" rx="0.5" fill="currentColor"/></symbol>
  <symbol id="ic-command" viewBox="0 0 24 24"><path d="M18 3a3 3 0 00-3 3v3H9V6a3 3 0 10-3 3h3v6H6a3 3 0 103 3v-3h6v3a3 3 0 103-3h-3V9h3a3 3 0 003-6z" fill="currentColor"/></symbol>
  <symbol id="ic-rocket" viewBox="0 0 24 24"><path d="M12 2L9 12l3 4 3-4z" fill="currentColor"/><circle cx="12" cy="12" r="2" fill="#fff"/><path d="M7 22c-1-3 2-6 5-7M17 22c1-3-2-6-5-7" stroke="currentColor" stroke-width="1.5"/></symbol>
  <symbol id="ic-shield" viewBox="0 0 24 24"><path d="M12 2L3 7v5c0 5.5 3.8 10.7 9 12 5.2-1.3 9-6.5 9-12V7z" fill="none" stroke="currentColor" stroke-width="1.8"/><polyline points="8 12 11 15 16 9" stroke="currentColor" stroke-width="1.8"/></symbol>
  <symbol id="ic-database" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3" fill="currentColor" opacity="0.5"/><path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M3 12c0 1.66 4.03 3 9 3s9-1.34 9-3" fill="none" stroke="currentColor" stroke-width="1.2"/></symbol>
  <symbol id="ic-pin" viewBox="0 0 24 24"><path d="M16 2l4 4-2 2-6-6z" fill="currentColor" opacity="0.5"/><path d="M8 14a15 15 0 01-6 8h20a15 15 0 01-6-8V8H8z" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
  <symbol id="ic-color-picker" viewBox="0 0 24 24"><path d="M4 20l6-6M4 4l16 16" stroke="currentColor" stroke-width="1.5"/><circle cx="14" cy="14" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
  <symbol id="ic-presentation" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" stroke-width="1.5"/><line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" stroke-width="1.5"/></symbol>
</svg>
'''

# Find </svg> line
for i, line in enumerate(lines):
    if line.strip() == '</svg>':
        lines.insert(i, svg_icons)
        break

# ============================================================
# 2. NEW APP ICON CSS GRADIENTS (before /* Dock */)
# ============================================================
app_css = '''
.icon-minesweeper{background:linear-gradient(135deg,#f44336,#c62828)}
.icon-tetris{background:linear-gradient(135deg,#9c27b0,#6a1b9a)}
.icon-breakout{background:linear-gradient(135deg,#ff9800,#e65100)}
.icon-code-editor{background:linear-gradient(135deg,#2196f3,#0d47a1)}
.icon-stopwatch-app{background:linear-gradient(135deg,#00bcd4,#006064)}
.icon-converter{background:linear-gradient(135deg,#4caf50,#1b5e20)}
.icon-reader{background:linear-gradient(135deg,#795548,#3e2723)}
.icon-password{background:linear-gradient(135deg,#607d8b,#263238)}
.icon-qrcode{background:linear-gradient(135deg,#212121,#000)}
.icon-recorder{background:linear-gradient(135deg,#e91e63,#880e4f)}
.icon-charts{background:linear-gradient(135deg,#3f51b5,#1a237e)}
.icon-rss{background:linear-gradient(135deg,#ff5722,#bf360c)}
.icon-diary{background:linear-gradient(135deg,#8d6e63,#4e342e)}
.icon-translator{background:linear-gradient(135deg,#009688,#004d40)}
.icon-stocks{background:linear-gradient(135deg,#d32f2f,#b71c1c)}
'''

for i, line in enumerate(lines):
    if '/* Dock */' in line:
        lines.insert(i, app_css)
        break

# ============================================================
# 3. NEW APP CSS STYLES
# ============================================================
new_app_styles = '''
/* ── Minesweeper ── */
.mine-board{display:inline-grid;gap:1px;background:rgba(255,255,255,0.06);border:2px solid rgba(255,255,255,0.1);border-radius:4px;user-select:none}
.mine-cell{width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;cursor:pointer;background:rgba(255,255,255,0.08);border-radius:2px;transition:background 0.1s;color:var(--text-primary)}
.mine-cell:hover{background:rgba(255,255,255,0.16)}
.mine-cell.revealed{background:rgba(255,255,255,0.04);cursor:default}
.mine-cell.flagged{background:rgba(255,100,100,0.15)}
.mine-cell.mine{background:rgba(255,0,0,0.3)}
.mine-cell .n1{color:#42a5f5}.mine-cell .n2{color:#66bb6a}.mine-cell .n3{color:#ef5350}.mine-cell .n4{color:#ab47bc}.mine-cell .n5{color:#ff7043}.mine-cell .n6{color:#26c6da}.mine-cell .n7{color:#333}.mine-cell .n8{color:#78909c}
/* ── Tetris ── */
.tetris-board{display:inline-grid;gap:1px;background:rgba(255,255,255,0.04);border:2px solid rgba(255,255,255,0.1);border-radius:4px;padding:1px}
.tetris-cell{width:28px;height:28px;border-radius:2px;background:rgba(255,255,255,0.03)}
.tetris-cell.filled{box-shadow:inset 0 0 6px rgba(0,0,0,0.3),inset 2px 2px 6px rgba(255,255,255,0.15)}
/* ── Breakout ── */
.breakout-canvas{border-radius:6px;border:2px solid rgba(255,255,255,0.1)}
/* ── Code Editor ── */
.code-editor-wrap{display:flex;flex-direction:column;height:100%}
.code-editor-textarea{flex:1;background:#1e1e2e;color:#cdd6f4;font-family:var(--font-mono);font-size:13px;border:none;outline:none;resize:none;padding:16px;line-height:1.6;tab-size:2;border-radius:0 0 var(--r-lg) var(--r-lg)}
.code-editor-stats{display:flex;align-items:center;justify-content:space-between;padding:6px 14px;background:rgba(0,0,0,0.3);color:var(--text-secondary);font-size:11px;font-family:var(--font-mono)}
/* ── Stopwatch ── */
.sw-body{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:20px}
.sw-time{font-size:64px;font-family:var(--font-mono);color:var(--text-primary);font-weight:200;letter-spacing:2px}
.sw-btns{display:flex;gap:12px}
.sw-lap-list{max-height:150px;overflow-y:auto;width:200px;font-family:var(--font-mono);font-size:12px;color:var(--text-secondary)}
.sw-lap-item{display:flex;justify-content:space-between;padding:4px 8px;border-bottom:1px solid rgba(255,255,255,0.05)}
/* ── Converter ── */
.conv-body{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:16px;padding:20px}
.conv-row{display:flex;align-items:center;gap:10px;width:100%;max-width:400px}
.conv-input{flex:1;padding:10px 14px;background:rgba(255,255,255,0.08);border:1.5px solid rgba(255,255,255,0.12);border-radius:8px;color:var(--text-primary);font-size:16px;outline:none;text-align:center}
.conv-input:focus{border-color:var(--accent)}
.conv-select{padding:10px;background:rgba(255,255,255,0.08);border:1.5px solid rgba(255,255,255,0.12);border-radius:8px;color:var(--text-primary);font-size:14px;outline:none;cursor:pointer}
.conv-eq{font-size:24px;color:var(--text-tertiary)}
/* ── Password Generator ── */
.pw-body{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:20px;padding:20px}
.pw-display{font-size:24px;font-family:var(--font-mono);color:var(--accent);background:rgba(0,120,212,0.1);padding:14px 28px;border-radius:10px;border:1.5px solid rgba(0,120,212,0.3);letter-spacing:2px;word-break:break-all;text-align:center;min-width:280px}
.pw-controls{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.pw-option{display:flex;align-items:center;gap:6px;color:var(--text-secondary);font-size:13px;cursor:pointer}
.pw-option input[type=checkbox]{accent-color:var(--accent)}
/* ── QR Code ── */
.qr-body{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:16px;padding:20px}
.qr-input{width:300px;padding:10px 14px;background:rgba(255,255,255,0.08);border:1.5px solid rgba(255,255,255,0.12);border-radius:8px;color:var(--text-primary);font-size:14px;outline:none}
.qr-code-box{padding:24px;background:#fff;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.3)}
/* ── Stocks ── */
.stocks-body{padding:16px;display:flex;flex-direction:column;gap:12px;overflow-y:auto}
.stock-card{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;background:rgba(255,255,255,0.06);border-radius:10px;border:1px solid rgba(255,255,255,0.06);transition:background 0.15s}
.stock-card:hover{background:rgba(255,255,255,0.1)}
.stock-name{font-size:15px;font-weight:600;color:var(--text-primary)}
.stock-code{font-size:11px;color:var(--text-tertiary)}
.stock-price{font-size:18px;font-weight:700;font-family:var(--font-mono)}
.stock-change{font-size:13px;font-weight:600;padding:3px 8px;border-radius:4px}
.stock-up{color:#ff5252}.stock-down{color:#69f0ae}
.stock-up-bg{background:rgba(255,82,82,0.1)}.stock-down-bg{background:rgba(105,240,174,0.1)}
/* ── Diary ── */
.diary-body{display:flex;flex-direction:column;height:100%}
.diary-header{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid rgba(255,255,255,0.06)}
.diary-date{font-size:18px;font-weight:600;color:var(--text-primary)}
.diary-textarea{flex:1;background:transparent;color:var(--text-primary);font-size:14px;border:none;outline:none;resize:none;padding:16px;line-height:1.8}
/* ── Translator ── */
.trans-body{display:flex;flex-direction:column;height:100%;padding:16px;gap:12px}
.trans-row{display:flex;gap:10px;align-items:center}
.trans-lang{padding:8px 12px;background:rgba(255,255,255,0.08);border:1.5px solid rgba(255,255,255,0.12);border-radius:8px;color:var(--text-primary);font-size:13px;outline:none;cursor:pointer}
.trans-input-area{flex:1;padding:14px;background:rgba(255,255,255,0.06);border:1.5px solid rgba(255,255,255,0.12);border-radius:10px;color:var(--text-primary);font-size:14px;outline:none;resize:none;min-height:80px}
.trans-output-area{flex:1;padding:14px;background:rgba(30,30,50,0.6);border:1.5px solid rgba(255,255,255,0.08);border-radius:10px;color:var(--text-primary);font-size:14px;min-height:80px;white-space:pre-wrap;overflow-y:auto}
'''

for i, line in enumerate(lines):
    if '/* ── Video Player Controls ── */' in line:
        lines.insert(i, new_app_styles)
        break

# ============================================================
# 4. APPS ARRAY — ADD 15 NEW APPS
# ============================================================
new_apps_entries = '''
  {id:'minesweeper',name:'扫雷',ico:'ic-minesweeper'},
  {id:'tetris',name:'俄罗斯方块',ico:'ic-tetris'},
  {id:'breakout',name:'打砖块',ico:'ic-breakout'},
  {id:'code-editor',name:'代码编辑器',ico:'ic-code-editor'},
  {id:'stopwatch-app',name:'秒表',ico:'ic-stopwatch-app'},
  {id:'converter',name:'单位换算',ico:'ic-converter'},
  {id:'reader',name:'文档查看器',ico:'ic-reader'},
  {id:'password',name:'密码生成器',ico:'ic-password'},
  {id:'qrcode',name:'二维码',ico:'ic-qrcode'},
  {id:'recorder',name:'录音机',ico:'ic-recorder'},
  {id:'charts',name:'图表',ico:'ic-charts'},
  {id:'rss',name:'RSS 阅读',ico:'ic-rss'},
  {id:'diary',name:'日记',ico:'ic-diary'},
  {id:'translator',name:'翻译',ico:'ic-translator'},
  {id:'stocks',name:'股票',ico:'ic-stocks'}
'''

# Insert before ]; in APPS array
for i, line in enumerate(lines):
    if line.strip() == '];' and i > 1300:  # APPS array end
        # Check it's the APPS array end
        if any('id:' in l.strip() for l in lines[i-3:i]):
            lines.insert(i, new_apps_entries)
            break

# ============================================================
# 5. RENDER APP CONTENT SWITCH — ADD 15 CASES
# ============================================================
new_switch_cases = '''    case'minesweeper':renderMinesweeper(body,winId);break;
    case'tetris':renderTetris(body,winId);break;
    case'breakout':renderBreakout(body,winId);break;
    case'code-editor':renderCodeEditor(body,winId);break;
    case'stopwatch-app':renderStopwatchApp(body,winId);break;
    case'converter':renderConverter(body,winId);break;
    case'reader':renderReader(body,winId);break;
    case'password':renderPassword(body,winId);break;
    case'qrcode':renderQRCode(body,winId);break;
    case'recorder':renderRecorder(body,winId);break;
    case'charts':renderCharts(body,winId);break;
    case'rss':renderRSS(body,winId);break;
    case'diary':renderDiary(body,winId);break;
    case'translator':renderTranslator(body,winId);break;
    case'stocks':renderStocks(body,winId);break;
'''

for i, line in enumerate(lines):
    if "case'tasks':renderTasks(body,winId);break;" in line:
        lines.insert(i+1, new_switch_cases)
        break

print("Phase 1 done: SVG, CSS, APPS, renderAppContent injected")

# Write intermediate
with open(FILE, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines))

print(f"Written {len(lines)} lines to {FILE}")
