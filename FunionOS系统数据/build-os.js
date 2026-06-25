const fs = require('fs');

// 由于文件极大，用 JS 构建再写入
const CSS = `/* FusionOS 5.0 — Design Tokens */
:root{
  --accent:#0078d4;--accent-hover:#006cbd;--accent-light:rgba(0,120,212,0.18);--accent-glow:0 0 12px rgba(0,120,212,0.45);
  --danger:#e74c3c;--success:#27ae60;--warning:#f39c12;--info:#2980b9;
  --text-primary:rgba(255,255,255,0.93);--text-secondary:rgba(255,255,255,0.62);--text-tertiary:rgba(255,255,255,0.38);
  --surface-0:rgba(0,0,0,0.12);--surface-1:rgba(255,255,255,0.08);--surface-2:rgba(255,255,255,0.13);
  --glass:rgba(255,255,255,0.12);--glass-strong:rgba(255,255,255,0.18);
  --glass-bg:saturate(180%) blur(30px);
  --shadow-1:0 1px 3px rgba(0,0,0,0.12);--shadow-2:0 2px 8px rgba(0,0,0,0.18);
  --shadow-3:0 4px 16px rgba(0,0,0,0.22);--shadow-4:0 8px 32px rgba(0,0,0,0.28);
  --shadow-5:0 16px 48px rgba(0,0,0,0.35);
  --win-shadow:0 8px 32px rgba(0,0,0,0.18),0 2px 8px rgba(0,0,0,0.12);
  --win-shadow-focused:0 12px 48px rgba(0,0,0,0.28),0 0 0 0.5px rgba(255,255,255,0.08),0 0 16px rgba(0,120,212,0.10);
  --r-xs:4px;--r-sm:6px;--r-md:10px;--r-lg:14px;--r-xl:20px;--r-full:9999px;
  --sp-1:4px;--sp-2:8px;--sp-3:12px;--sp-4:16px;--sp-5:24px;--sp-6:32px;--sp-8:48px;
  --ease-out:cubic-bezier(0.16,1,0.3,1);--ease-in-out:cubic-bezier(0.4,0,0.2,1);
  --spring:cubic-bezier(0.34,1.56,0.64,1);
  --dur-fast:0.15s;--dur-normal:0.25s;--dur-slow:0.4s;
  --font-sans:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",Roboto,sans-serif;
  --font-mono:"SF Mono","Fira Code","Cascadia Code",Consolas,monospace;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;overflow:hidden;font-family:var(--font-sans);-webkit-font-smoothing:antialiased}
::selection{background:rgba(0,120,212,0.35);color:#fff}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.18);border-radius:3px}
/* Login */
#login-screen{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0a0a1a 0%,#0d1b2a 40%,#1a1a3e 100%);transition:opacity 0.6s var(--ease-out),visibility 0.6s}
#login-screen.hidden{opacity:0;visibility:hidden;pointer-events:none}
#login-bg-canvas{position:absolute;inset:0;width:100%;height:100%}
.login-card{position:relative;display:flex;flex-direction:column;align-items:center;gap:var(--sp-5);padding:var(--sp-8) var(--sp-6);border-radius:var(--r-xl);background:rgba(255,255,255,0.08);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.12);box-shadow:var(--shadow-5);min-width:340px;animation:cardIn 0.7s var(--spring) both}
@keyframes cardIn{from{opacity:0;transform:translateY(24px) scale(0.95)}to{opacity:1;transform:none}}
.login-avatar{width:88px;height:88px;border-radius:50%;background:linear-gradient(135deg,var(--accent),#6c5ce7);display:flex;align-items:center;justify-content:center;font-size:40px;border:3px solid rgba(255,255,255,0.2);box-shadow:var(--accent-glow);transition:transform var(--dur-normal) var(--spring),box-shadow var(--dur-normal)}
.login-avatar:hover{transform:scale(1.08);box-shadow:0 0 24px rgba(0,120,212,0.6)}
.login-username{color:var(--text-primary);font-size:22px;font-weight:600;letter-spacing:-0.3px}
.login-hint{color:var(--text-secondary);font-size:13px}
.login-input-wrap{position:relative;width:100%}
.login-input{width:100%;padding:12px 16px;padding-left:42px;border-radius:var(--r-md);border:1.5px solid rgba(255,255,255,0.15);background:rgba(255,255,255,0.06);color:var(--text-primary);font-size:15px;outline:none;transition:all var(--dur-fast);font-family:var(--font-sans)}
.login-input:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-light)}
.login-input-icon{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--text-tertiary);font-size:16px;pointer-events:none}
.login-btn{width:100%;padding:12px;border-radius:var(--r-md);border:none;background:linear-gradient(135deg,var(--accent),#006cbd);color:#fff;font-size:15px;font-weight:600;cursor:pointer;transition:all var(--dur-fast);letter-spacing:0.3px}
.login-btn:hover{background:linear-gradient(135deg,var(--accent-hover),#005a9e);box-shadow:var(--accent-glow);transform:translateY(-1px)}
.login-btn:active{transform:translateY(0) scale(0.98)}
.login-progress{width:100%;height:3px;border-radius:2px;background:rgba(255,255,255,0.1);overflow:hidden;margin-top:4px}
.login-progress-bar{height:100%;width:0%;border-radius:2px;background:linear-gradient(90deg,var(--accent),#6c5ce7);transition:width 0.3s var(--ease-out)}
/* Desktop */
#desktop{position:fixed;inset:0;overflow:hidden;background:linear-gradient(135deg,#0d1b2a 0%,#1b2838 30%,#2c3e50 60%,#1a1a3e 100%)}
#desktop.w2{background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460)}
#desktop.w3{background:linear-gradient(135deg,#2d1b69,#11998e,#38ef7d)}
#desktop.w4{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e)}
#desktop.w5{background:linear-gradient(135deg,#1a0000,#8b0000,#ff6b6b)}
#desktop.w6{background:linear-gradient(135deg,#000428,#004e92)}
.wallpaper-particle{position:absolute;border-radius:50%;pointer-events:none;background:radial-gradient(circle,rgba(255,255,255,0.15),transparent 70%);opacity:0;animation:particleFloat 8s infinite var(--ease-in-out)}
@keyframes particleFloat{0%{opacity:0;transform:translateY(0) scale(0.5)}20%{opacity:1}80%{opacity:1}100%{opacity:0;transform:translateY(-120px) scale(1.2)}}
/* Topbar */
#topbar{position:fixed;top:0;left:0;right:0;height:28px;z-index:9000;display:flex;align-items:center;padding:0 var(--sp-3);gap:2px;background:rgba(0,0,0,0.35);backdrop-filter:var(--glass-bg);border-bottom:1px solid rgba(255,255,255,0.06);user-select:none}
.topbar-app{font-size:13.5px;font-weight:600;color:var(--text-primary);padding:2px 10px;border-radius:var(--r-xs);cursor:default;transition:background var(--dur-fast);white-space:nowrap;letter-spacing:-0.1px}
.topbar-app:hover,.topbar-app.active{background:rgba(255,255,255,0.12)}
.topbar-time{font-size:13px;color:var(--text-primary);font-variant-numeric:tabular-nums;cursor:default;padding:2px 8px;border-radius:var(--r-xs);white-space:nowrap;margin-left:auto}
.topbar-icon{width:28px;height:28px;display:flex;align-items:center;justify-content:center;border-radius:var(--r-xs);cursor:pointer;color:var(--text-primary);font-size:14px;transition:background var(--dur-fast);position:relative}
.topbar-icon:hover{background:rgba(255,255,255,0.12)}
.topbar-badge{position:absolute;top:4px;right:4px;width:7px;height:7px;background:var(--danger);border-radius:50%;border:1.5px solid rgba(0,0,0,0.4)}
.topbar-menu{position:absolute;top:28px;min-width:220px;background:rgba(30,30,40,0.92);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.1);border-radius:var(--r-md);box-shadow:var(--shadow-4);padding:var(--sp-1);z-index:9999;animation:menuIn 0.2s var(--spring) both;transform-origin:top left}
@keyframes menuIn{from{opacity:0;transform:scale(0.95) translateY(-4px)}to{opacity:1;transform:none}}
.topbar-menu-item{display:flex;align-items:center;gap:var(--sp-2);padding:6px var(--sp-3);border-radius:var(--r-sm);color:var(--text-primary);font-size:13px;cursor:pointer;transition:background var(--dur-fast)}
.topbar-menu-item:hover{background:var(--accent);color:#fff}
.topbar-menu-sep{height:1px;background:rgba(255,255,255,0.08);margin:4px 8px}
/* Desktop Icons */
#desktop-icons{position:absolute;inset:0;z-index:10;pointer-events:none}
.desktop-icon{position:absolute;width:76px;height:88px;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding-top:8px;gap:4px;cursor:pointer;border-radius:var(--r-md);pointer-events:auto;transition:left 0.22s var(--ease-out),top 0.22s var(--ease-out),background var(--dur-fast),transform var(--dur-fast);user-select:none}
.desktop-icon:hover{background:rgba(255,255,255,0.1)}
.desktop-icon.selected{background:rgba(0,120,212,0.22);outline:2px solid var(--accent);outline-offset:-2px}
.desktop-icon.selected .desktop-icon-label{background:var(--accent);color:#fff;padding:1px 6px;border-radius:3px}
.desktop-icon.dragging{opacity:0.4;transform:scale(0.92);z-index:100}
.desktop-icon.drag-over{outline:2px dashed rgba(0,120,212,0.6);outline-offset:2px;background:rgba(0,120,212,0.1)}
.desktop-icon-inner{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:26px;transition:transform var(--dur-fast);position:relative;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.2)}
.desktop-icon:hover .desktop-icon-inner{transform:scale(1.06)}
.desktop-icon-label{font-size:11px;color:var(--text-primary);text-align:center;text-shadow:0 1px 4px rgba(0,0,0,0.7);line-height:1.3;max-width:70px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;pointer-events:none}
.icon-finder{background:linear-gradient(135deg,#4fc3f7,#0288d1)}
.icon-terminal{background:linear-gradient(135deg,#1a1a2e,#16213e);border:1.5px solid rgba(255,255,255,0.15)}
.icon-notes{background:linear-gradient(135deg,#ffd54f,#ffb300)}
.icon-calc{background:linear-gradient(135deg,#5c6bc0,#3949ab)}
.icon-browser{background:linear-gradient(135deg,#42a5f5,#1565c0)}
.icon-settings{background:linear-gradient(135deg,#78909c,#455a64)}
.icon-music{background:linear-gradient(135deg,#e040fb,#8e24aa)}
.icon-map{background:linear-gradient(135deg,#26a69a,#00695c)}
.icon-weather{background:linear-gradient(135deg,#ff9800,#e65100)}
.icon-paint{background:linear-gradient(135deg,#ec407a,#c2185b)}
/* Dock */
#dock{position:fixed;bottom:6px;left:50%;transform:translateX(-50%);z-index:9500;display:flex;align-items:flex-end;gap:3px;padding:4px 8px;background:rgba(255,255,255,0.08);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.1);border-radius:var(--r-xl);box-shadow:var(--shadow-4);height:56px;user-select:none}
.dock-item{width:42px;height:42px;display:flex;align-items:center;justify-content:center;border-radius:var(--r-md);cursor:pointer;color:var(--text-primary);font-size:20px;transition:all var(--dur-fast) var(--spring);position:relative;background:rgba(255,255,255,0.06)}
.dock-item:hover{background:rgba(255,255,255,0.15);transform:translateY(-3px) scale(1.18)}
.dock-item:active{transform:translateY(0) scale(0.96)}
.dock-item.active::after{content:'';position:absolute;bottom:-2px;left:50%;transform:translateX(-50%);width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,0.7);box-shadow:0 0 6px rgba(255,255,255,0.4)}
.dock-item.running::before{content:'';position:absolute;bottom:2px;left:50%;transform:translateX(-50%);width:3px;height:3px;border-radius:50%;background:var(--accent);box-shadow:0 0 4px var(--accent)}
.dock-separator{width:1px;height:32px;background:rgba(255,255,255,0.12);margin:0 4px}
.dock-tooltip{position:absolute;bottom:52px;left:50%;transform:translateX(-50%) translateY(4px);padding:4px 10px;border-radius:var(--r-sm);background:rgba(30,30,40,0.95);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.1);color:var(--text-primary);font-size:12px;white-space:nowrap;pointer-events:none;opacity:0;transition:all 0.2s var(--spring)}
.dock-item:hover .dock-tooltip{opacity:1;transform:translateX(-50%) translateY(0)}
/* Windows */
.window{position:absolute;border-radius:var(--r-lg);overflow:hidden;background:rgba(30,30,42,0.88);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.1);box-shadow:var(--win-shadow);min-width:320px;min-height:200px;display:flex;flex-direction:column;transition:box-shadow var(--dur-normal),opacity 0.2s,transform 0.2s var(--ease-out);animation:winOpen 0.35s var(--spring) both}
.window.closing{animation:winClose 0.25s var(--ease-in-out) forwards}
@keyframes winOpen{from{opacity:0;transform:scale(0.92) translateY(8px)}to{opacity:1;transform:none}}
@keyframes winClose{to{opacity:0;transform:scale(0.92) translateY(8px);filter:blur(3px)}}
.window.focused{box-shadow:var(--win-shadow-focused);z-index:100!important;border-color:rgba(255,255,255,0.15)}
.window.maximized{border-radius:0;transition:left 0.2s,top 0.2s,width 0.2s,height 0.2s}
.window-titlebar{height:32px;display:flex;align-items:center;padding:0 8px;background:rgba(255,255,255,0.04);border-bottom:1px solid rgba(255,255,255,0.06);cursor:default;flex-shrink:0;user-select:none;gap:6px}
.window-titlebar .traffic-lights{display:flex;gap:6px;padding-right:4px}
.window-titlebar .traffic-lights span{width:12px;height:12px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all var(--dur-fast);position:relative}
.window-titlebar .traffic-lights .close{background:#ff5f57}
.window-titlebar .traffic-lights .min{background:#ffbd2e}
.window-titlebar .traffic-lights .max{background:#28c840}
.window-titlebar .traffic-lights span:hover{filter:brightness(1.2)}
.window-titlebar .traffic-lights span svg{opacity:0;transition:opacity var(--dur-fast)}
.window-titlebar .traffic-lights span:hover svg{opacity:1}
.window-title{font-size:12.5px;color:var(--text-secondary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;text-align:center}
.window-body{flex:1;overflow:auto;position:relative}
/* Start Menu */
#start-menu{position:fixed;bottom:64px;left:12px;width:380px;max-height:520px;background:rgba(30,30,42,0.94);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.1);border-radius:var(--r-xl);box-shadow:var(--shadow-5);z-index:9600;padding:var(--sp-4);display:flex;flex-direction:column;gap:var(--sp-3);transform:scale(0.96) translateY(8px);opacity:0;pointer-events:none;transition:all 0.25s var(--spring)}
#start-menu.show{transform:none;opacity:1;pointer-events:auto}
.start-search{display:flex;align-items:center;gap:var(--sp-2);padding:8px 12px;background:rgba(255,255,255,0.06);border:1.5px solid rgba(255,255,255,0.1);border-radius:var(--r-md);transition:border-color var(--dur-fast),box-shadow var(--dur-fast)}
.start-search:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-light)}
.start-search svg{color:var(--text-tertiary);flex-shrink:0}
.start-search input{flex:1;border:none;background:none;color:var(--text-primary);font-size:14px;outline:none;font-family:var(--font-sans)}
.start-search input::placeholder{color:var(--text-tertiary)}
.start-section-label{font-size:11px;color:var(--text-tertiary);text-transform:uppercase;letter-spacing:0.8px;padding:4px 4px 6px;font-weight:600}
.start-apps{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--sp-1);overflow-y:auto;max-height:300px;padding:2px}
.start-app-item{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 4px;border-radius:var(--r-md);cursor:pointer;transition:background var(--dur-fast)}
.start-app-item:hover{background:rgba(255,255,255,0.1)}
.start-app-item:active{background:var(--accent);transform:scale(0.96)}
.start-app-icon{width:36px;height:36px;border-radius:var(--r-sm);display:flex;align-items:center;justify-content:center;font-size:20px}
.start-app-name{font-size:11px;color:var(--text-secondary);text-align:center}
.start-power{display:flex;align-items:center;justify-content:center;gap:var(--sp-4);padding-top:var(--sp-3);border-top:1px solid rgba(255,255,255,0.06)}
.start-power-btn{padding:6px 16px;border-radius:var(--r-md);border:none;background:rgba(255,255,255,0.08);color:var(--text-primary);font-size:12px;cursor:pointer;transition:all var(--dur-fast)}
.start-power-btn:hover{background:rgba(255,255,255,0.15)}
.start-power-btn.shutdown:hover{background:var(--danger);color:#fff}
/* Context Menu */
.context-menu{position:fixed;z-index:9800;min-width:180px;background:rgba(30,30,42,0.95);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.1);border-radius:var(--r-md);box-shadow:var(--shadow-4);padding:var(--sp-1);animation:ctxIn 0.18s var(--spring) both;transform-origin:top left}
@keyframes ctxIn{from{opacity:0;transform:scale(0.95)}to{opacity:1;transform:none}}
.context-item{display:flex;align-items:center;gap:var(--sp-2);padding:6px var(--sp-3);border-radius:var(--r-sm);color:var(--text-primary);font-size:13px;cursor:pointer;transition:background var(--dur-fast)}
.context-item:hover{background:var(--accent);color:#fff}
.context-sep{height:1px;background:rgba(255,255,255,0.06);margin:3px 6px}
/* Toast */
#toast-container{position:fixed;top:40px;right:16px;z-index:99900;display:flex;flex-direction:column;gap:var(--sp-2);pointer-events:none}
.toast{display:flex;align-items:center;gap:var(--sp-3);padding:12px 16px;background:rgba(30,30,42,0.94);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.1);border-radius:var(--r-md);box-shadow:var(--shadow-3);color:var(--text-primary);font-size:13px;min-width:260px;max-width:360px;pointer-events:auto;animation:toastIn 0.4s var(--spring) both}
.toast.leaving{animation:toastOut 0.3s var(--ease-in-out) forwards}
@keyframes toastIn{from{opacity:0;transform:translateX(40px) scale(0.95)}to{opacity:1;transform:none}}
@keyframes toastOut{to{opacity:0;transform:translateX(40px) scale(0.95)}}
.toast-icon{font-size:20px;flex-shrink:0}
/* Notification Center */
#notif-center{position:fixed;top:0;right:0;width:360px;max-height:100vh;background:rgba(30,30,42,0.94);backdrop-filter:var(--glass-bg);border-left:1px solid rgba(255,255,255,0.08);box-shadow:var(--shadow-5);z-index:9700;transform:translateX(100%);transition:transform 0.3s var(--ease-out);display:flex;flex-direction:column}
#notif-center.show{transform:none}
.notif-header{display:flex;align-items:center;justify-content:space-between;padding:var(--sp-4);border-bottom:1px solid rgba(255,255,255,0.06)}
.notif-header h3{color:var(--text-primary);font-size:16px;font-weight:600}
.notif-clear{background:none;border:none;color:var(--accent);font-size:13px;cursor:pointer;padding:4px 8px;border-radius:var(--r-xs)}
.notif-clear:hover{background:var(--accent-light)}
.notif-list{flex:1;overflow-y:auto;padding:var(--sp-2)}
.notif-item{display:flex;gap:var(--sp-3);padding:10px;margin:2px 0;border-radius:var(--r-md);transition:background var(--dur-fast);cursor:default}
.notif-item:hover{background:rgba(255,255,255,0.06)}
.notif-item-icon{font-size:22px;flex-shrink:0;width:36px;height:36px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,0.06);border-radius:var(--r-sm)}
.notif-item-content{flex:1;min-width:0}
.notif-item-title{color:var(--text-primary);font-size:13px;font-weight:600}
.notif-item-body{color:var(--text-secondary);font-size:12px;margin-top:2px;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.notif-item-time{color:var(--text-tertiary);font-size:11px;margin-top:3px}
/* ===== App Styles ===== */
/* Terminal */
.terminal{background:#0d1117;color:#c9d1d9;font-family:var(--font-mono);font-size:13px;padding:14px;height:100%;overflow:auto;line-height:1.7;white-space:pre-wrap;word-break:break-all;border-radius:0 0 var(--r-lg) var(--r-lg)}
.terminal .line{margin:1px 0}
.terminal .cmd{color:#58a6ff}.terminal .err{color:#f85149}.terminal .info{color:#58a6ff}.terminal .warn{color:#d29922}.terminal .path{color:#a371f7}.terminal .val{color:#79c0ff}.terminal .ascii{color:#8b949e;line-height:1.3;font-size:11px}
.terminal-input-row{display:flex;align-items:center;gap:6px}
.terminal-input-row .prompt{color:#58a6ff;white-space:nowrap}
.terminal-input-row input{flex:1;background:none;border:none;color:#c9d1d9;font-family:var(--font-mono);font-size:13px;outline:none}
/* Notes */
.notes-editor{width:100%;height:100%;background:rgba(255,255,255,0.03);color:var(--text-primary);border:none;padding:16px;font-size:14px;font-family:var(--font-sans);line-height:1.8;resize:none;outline:none}
.notes-toolbar{display:flex;align-items:center;gap:var(--sp-2);padding:6px 12px;background:rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.06)}
/* Calculator */
.calc-body{display:flex;flex-direction:column;height:100%;padding:0;background:rgba(0,0,0,0.15)}
.calc-display{padding:16px 20px 12px;text-align:right;min-height:80px;display:flex;flex-direction:column;justify-content:flex-end}
.calc-expr{font-size:14px;color:var(--text-tertiary);min-height:20px;font-family:var(--font-mono)}
.calc-result{font-size:36px;font-weight:300;color:var(--text-primary);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;transition:font-size var(--dur-fast)}
.calc-result.shrink{font-size:24px}
.calc-keys{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;flex:1;background:rgba(255,255,255,0.04);padding:1px}
.calc-key{display:flex;align-items:center;justify-content:center;font-size:17px;background:rgba(255,255,255,0.06);border:none;color:var(--text-primary);cursor:pointer;transition:all 80ms;font-family:var(--font-sans)}
.calc-key:hover{background:rgba(255,255,255,0.14)}
.calc-key:active{background:var(--accent);transform:scale(0.95)}
.calc-key.op{background:rgba(0,120,212,0.2);color:var(--accent)}
.calc-key.op:hover{background:rgba(0,120,212,0.35)}
.calc-key.eq{background:var(--accent);color:#fff;grid-column:span 2}
.calc-key.eq:hover{background:var(--accent-hover)}
.calc-key.clr{background:rgba(231,76,60,0.2);color:var(--danger)}
.calc-key.clr:hover{background:rgba(231,76,60,0.4)}
/* Finder */
.finder-sidebar{width:180px;flex-shrink:0;background:rgba(255,255,255,0.03);border-right:1px solid rgba(255,255,255,0.06);padding:var(--sp-2);overflow-y:auto}
.finder-sidebar-item{display:flex;align-items:center;gap:var(--sp-2);padding:6px 10px;border-radius:var(--r-sm);color:var(--text-secondary);font-size:13px;cursor:pointer;transition:all var(--dur-fast);white-space:nowrap}
.finder-sidebar-item:hover{background:rgba(255,255,255,0.08)}
.finder-sidebar-item.active{background:var(--accent);color:#fff}
.finder-main{flex:1;padding:var(--sp-4);overflow:auto}
.finder-breadcrumb{display:flex;align-items:center;gap:4px;margin-bottom:var(--sp-4);flex-wrap:wrap}
.finder-breadcrumb span{color:var(--accent);font-size:13px;cursor:pointer;padding:2px 6px;border-radius:var(--r-xs);transition:background var(--dur-fast)}
.finder-breadcrumb span:hover{background:var(--accent-light)}
.finder-breadcrumb .sep{color:var(--text-tertiary);cursor:default;padding:0}
.finder-grid{display:flex;flex-wrap:wrap;gap:var(--sp-3);padding:var(--sp-2)}
.finder-item{width:100px;display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px;border-radius:var(--r-md);cursor:pointer;transition:background var(--dur-fast)}
.finder-item:hover{background:rgba(255,255,255,0.08)}
.finder-item:active{background:var(--accent)}
.finder-item-icon{width:48px;height:48px;border-radius:var(--r-sm);display:flex;align-items:center;justify-content:center;font-size:24px}
.finder-item-name{font-size:11px;color:var(--text-secondary);text-align:center;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:90px}
/* Browser */
.browser-bar{display:flex;align-items:center;gap:var(--sp-2);padding:6px 10px;background:rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.06)}
.browser-bar input{flex:1;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:var(--r-full);padding:6px 14px;color:var(--text-primary);font-size:13px;outline:none;transition:border-color var(--dur-fast)}
.browser-bar input:focus{border-color:var(--accent)}
.browser-frame{flex:1;border:none;background:#fff}
/* Settings */
.settings-sidebar{width:160px;flex-shrink:0;padding:var(--sp-4) 0;border-right:1px solid rgba(255,255,255,0.06)}
.settings-sidebar-item{padding:8px 16px;color:var(--text-secondary);font-size:13px;cursor:pointer;border-radius:0 var(--r-sm) var(--r-sm) 0;transition:all var(--dur-fast)}
.settings-sidebar-item:hover{background:rgba(255,255,255,0.06)}
.settings-sidebar-item.active{background:var(--accent);color:#fff}
.settings-content{flex:1;padding:var(--sp-5);overflow-y:auto}
.settings-card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:var(--r-lg);padding:var(--sp-5);margin-bottom:var(--sp-4)}
.settings-card h3{color:var(--text-primary);font-size:16px;font-weight:600;margin-bottom:var(--sp-4)}
.settings-row{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.04)}
.settings-row:last-child{border-bottom:none}
.settings-row-label{color:var(--text-primary);font-size:13px}
.settings-row-desc{color:var(--text-tertiary);font-size:12px;margin-top:2px}
.wallpaper-grid{display:flex;gap:var(--sp-3);flex-wrap:wrap}
.wallpaper-thumb{width:80px;height:50px;border-radius:var(--r-sm);cursor:pointer;border:2px solid transparent;transition:all var(--dur-fast);overflow:hidden}
.wallpaper-thumb:hover{transform:scale(1.08);border-color:rgba(255,255,255,0.3)}
.wallpaper-thumb.active{border-color:var(--accent);box-shadow:var(--accent-glow)}
.accent-colors{display:flex;gap:var(--sp-2);flex-wrap:wrap}
.accent-dot{width:28px;height:28px;border-radius:50%;cursor:pointer;border:2px solid transparent;transition:all var(--dur-fast)}
.accent-dot:hover{transform:scale(1.15)}
.accent-dot.active{border-color:#fff;box-shadow:0 0 8px rgba(255,255,255,0.3)}
.toggle-switch{width:40px;height:22px;border-radius:11px;background:rgba(255,255,255,0.15);cursor:pointer;position:relative;transition:background var(--dur-fast);border:none;padding:0}
.toggle-switch.on{background:var(--accent)}
.toggle-switch::after{content:'';position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:#fff;transition:transform var(--dur-fast) var(--spring);box-shadow:0 1px 3px rgba(0,0,0,0.2)}
.toggle-switch.on::after{transform:translateX(18px)}
/* Music */
.music-body{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:var(--sp-5);padding:var(--sp-5)}
.music-cover{width:180px;height:180px;border-radius:var(--r-lg);background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;font-size:72px;box-shadow:var(--shadow-4);position:relative;overflow:hidden}
.music-cover.playing::after{content:'';position:absolute;inset:0;border:2px solid rgba(255,255,255,0.2);border-radius:var(--r-lg);animation:pulseRing 2s infinite}
@keyframes pulseRing{0%{transform:scale(1);opacity:0.6}100%{transform:scale(1.08);opacity:0}}
.music-title{font-size:20px;font-weight:600;color:var(--text-primary)}
.music-artist{font-size:14px;color:var(--text-secondary)}
.music-progress{width:100%;max-width:360px}
.music-progress-bar{width:100%;height:4px;border-radius:2px;background:rgba(255,255,255,0.12);cursor:pointer;position:relative}
.music-progress-fill{height:100%;border-radius:2px;background:var(--accent);transition:width 0.3s linear;position:relative}
.music-progress-fill::after{content:'';position:absolute;right:-5px;top:50%;transform:translateY(-50%);width:10px;height:10px;border-radius:50%;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,0.3);opacity:0;transition:opacity var(--dur-fast)}
.music-progress-bar:hover .music-progress-fill::after{opacity:1}
.music-controls{display:flex;align-items:center;gap:var(--sp-4)}
.music-btn{width:44px;height:44px;border-radius:50%;border:none;background:rgba(255,255,255,0.08);color:var(--text-primary);font-size:18px;cursor:pointer;transition:all var(--dur-fast);display:flex;align-items:center;justify-content:center}
.music-btn:hover{background:rgba(255,255,255,0.18);transform:scale(1.08)}
.music-btn.play-btn{width:52px;height:52px;background:var(--accent);color:#fff;font-size:22px}
.music-btn.play-btn:hover{background:var(--accent-hover);box-shadow:var(--accent-glow)}
.music-list{width:100%;max-width:360px;max-height:160px;overflow-y:auto}
.music-list-item{display:flex;align-items:center;gap:var(--sp-3);padding:8px 12px;border-radius:var(--r-sm);cursor:pointer;transition:background var(--dur-fast)}
.music-list-item:hover{background:rgba(255,255,255,0.06)}
.music-list-item.active{background:var(--accent-light);color:var(--accent)}
/* MAP */
.map-body{position:relative;width:100%;height:100%;overflow:hidden;background:#1a1a2e}
.map-canvas{width:100%;height:100%;cursor:grab}
.map-canvas:active{cursor:grabbing}
.map-controls{position:absolute;top:10px;left:10px;display:flex;flex-direction:column;gap:var(--sp-2);z-index:10}
.map-btn{width:36px;height:36px;border-radius:var(--r-sm);border:1px solid rgba(255,255,255,0.15);background:rgba(30,30,42,0.9);backdrop-filter:var(--glass-bg);color:var(--text-primary);font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background var(--dur-fast);box-shadow:var(--shadow-2)}
.map-btn:hover{background:rgba(255,255,255,0.15)}
.map-search{position:absolute;top:10px;left:56px;z-index:10;background:rgba(30,30,42,0.92);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.12);border-radius:var(--r-md);padding:6px 12px;color:var(--text-primary);font-size:13px;width:260px;outline:none;transition:border-color var(--dur-fast)}
.map-search:focus{border-color:var(--accent)}
.map-coords{position:absolute;bottom:10px;left:10px;z-index:10;background:rgba(30,30,42,0.9);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.1);border-radius:var(--r-sm);padding:4px 10px;color:var(--text-tertiary);font-size:11px;font-family:var(--font-mono)}
.map-scale{position:absolute;bottom:10px;right:10px;z-index:10;background:rgba(30,30,42,0.9);backdrop-filter:var(--glass-bg);border:1px solid rgba(255,255,255,0.1);border-radius:var(--r-sm);padding:4px 10px;color:var(--text-tertiary);font-size:11px}
.map-poi{position:absolute;width:28px;height:28px;border-radius:50% 50% 50% 0;background:var(--accent);display:flex;align-items:center;justify-content:center;font-size:14px;color:#fff;cursor:pointer;transform:rotate(-45deg);box-shadow:0 2px 8px rgba(0,0,0,0.3);transition:transform var(--dur-fast)}
.map-poi span{transform:rotate(45deg)}
.map-poi:hover{transform:rotate(-45deg) scale(1.15)}
/* WEATHER */
.weather-body{display:flex;flex-direction:column;height:100%;overflow-y:auto;padding:0}
.weather-current{display:flex;flex-direction:column;align-items:center;padding:var(--sp-6) var(--sp-4);background:linear-gradient(135deg,rgba(0,120,212,0.2),rgba(108,92,231,0.15));border-bottom:1px solid rgba(255,255,255,0.06)}
.weather-icon-big{font-size:72px;margin-bottom:var(--sp-3)}
.weather-temp{font-size:56px;font-weight:200;color:var(--text-primary);letter-spacing:-2px;line-height:1}
.weather-temp sup{font-size:24px;font-weight:300;color:var(--text-secondary)}
.weather-desc{font-size:16px;color:var(--text-secondary);margin-top:2px}
.weather-city{font-size:14px;color:var(--text-tertiary);margin-top:4px}
.weather-details{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,0.04);padding:1px;margin-top:var(--sp-4)}
.weather-detail{display:flex;flex-direction:column;align-items:center;padding:var(--sp-4);background:rgba(30,30,42,0.6);gap:4px}
.weather-detail-icon{font-size:20px}
.weather-detail-val{font-size:18px;font-weight:600;color:var(--text-primary)}
.weather-detail-label{font-size:11px;color:var(--text-tertiary)}
.weather-forecast{padding:var(--sp-4)}
.weather-forecast h4{color:var(--text-secondary);font-size:13px;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:var(--sp-3)}
.weather-forecast-list{display:flex;gap:var(--sp-2);overflow-x:auto;padding-bottom:var(--sp-2)}
.weather-forecast-item{min-width:90px;display:flex;flex-direction:column;align-items:center;gap:6px;padding:12px 8px;border-radius:var(--r-md);background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06)}
.weather-forecast-item .day{font-size:12px;color:var(--text-tertiary)}
.weather-forecast-item .wi{font-size:24px}
.weather-forecast-item .t{font-size:14px;color:var(--text-primary)}
.weather-forecast-item .t-low{font-size:12px;color:var(--text-tertiary)}
.weather-search-bar{display:flex;gap:var(--sp-2);padding:var(--sp-4);border-bottom:1px solid rgba(255,255,255,0.06);flex-wrap:wrap}
.weather-city-btn{padding:6px 12px;border-radius:var(--r-sm);border:1px solid rgba(255,255,255,0.12);background:rgba(255,255,255,0.06);color:var(--text-secondary);font-size:12px;cursor:pointer;transition:all var(--dur-fast)}
.weather-city-btn:hover,.weather-city-btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
/* PAINT */
.paint-body{display:flex;flex-direction:column;height:100%;overflow:hidden}
.paint-toolbar{display:flex;align-items:center;gap:var(--sp-1);padding:4px 8px;background:rgba(255,255,255,0.04);border-bottom:1px solid rgba(255,255,255,0.06);flex-wrap:wrap}
.paint-tool{padding:6px 10px;border-radius:var(--r-sm);border:none;background:rgba(255,255,255,0.06);color:var(--text-secondary);font-size:13px;cursor:pointer;transition:all var(--dur-fast);display:flex;align-items:center;gap:4px}
.paint-tool:hover{background:rgba(255,255,255,0.12)}
.paint-tool.active{background:var(--accent);color:#fff}
.paint-tool-sep{width:1px;height:24px;background:rgba(255,255,255,0.1);margin:0 4px}
.paint-color-picker{width:24px;height:24px;border-radius:50%;border:2px solid rgba(255,255,255,0.3);cursor:pointer;padding:0;transition:transform var(--dur-fast)}
.paint-color-picker:hover{transform:scale(1.15)}
.paint-size-slider{width:80px;accent-color:var(--accent);cursor:pointer}
.paint-canvas-wrap{flex:1;overflow:hidden;position:relative;background:#1a1a2e;display:flex;align-items:center;justify-content:center}
.paint-canvas{border:1px solid rgba(255,255,255,0.1);cursor:crosshair;background:#fff}
.paint-status{display:flex;align-items:center;justify-content:space-between;padding:4px 12px;background:rgba(0,0,0,0.2);font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono)}
.paint-layer-panel{width:160px;flex-shrink:0;background:rgba(255,255,255,0.03);border-left:1px solid rgba(255,255,255,0.06);padding:var(--sp-2);overflow-y:auto}
.paint-layer-item{display:flex;align-items:center;gap:var(--sp-2);padding:6px 8px;border-radius:var(--r-sm);cursor:pointer;font-size:12px;color:var(--text-secondary);transition:background var(--dur-fast)}
.paint-layer-item:hover{background:rgba(255,255,255,0.06)}
.paint-layer-item.active{background:var(--accent-light);color:var(--accent)}
/* Task Manager */
.taskmgr-table{width:100%;border-collapse:collapse}
.taskmgr-table th{text-align:left;padding:8px 12px;color:var(--text-tertiary);font-size:11px;text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid rgba(255,255,255,0.08);font-weight:600}
.taskmgr-table td{padding:8px 12px;color:var(--text-secondary);font-size:13px;border-bottom:1px solid rgba(255,255,255,0.03)}
.taskmgr-table tr:hover td{background:rgba(255,255,255,0.04)}
.status-dot{width:8px;height:8px;border-radius:50%;background:var(--success);display:inline-block;margin-right:6px}
.kill-btn{background:var(--danger);color:#fff;border:none;padding:3px 10px;border-radius:var(--r-xs);font-size:11px;cursor:pointer;transition:background var(--dur-fast)}
.kill-btn:hover{background:var(--danger-hover)}`;

// HTML structure
const HTML_HEAD = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>FusionOS 5.0</title>
<style>${CSS}</style>
</head>
<body>
<!-- Login -->
<div id="login-screen">
  <canvas id="login-bg-canvas"></canvas>
  <div class="login-card">
    <div class="login-avatar">👤</div>
    <div class="login-username">FusionOS 用户</div>
    <div class="login-hint">点击登录或按 Enter</div>
    <div class="login-input-wrap">
      <span class="login-input-icon">🔒</span>
      <input class="login-input" id="login-pwd" type="password" placeholder="密码（可选，默认免密）" onkeydown="if(event.key==='Enter')doLogin()">
    </div>
    <button class="login-btn" onclick="doLogin()">登 录</button>
    <div class="login-progress"><div class="login-progress-bar" id="login-prog"></div></div>
  </div>
</div>
<!-- Desktop -->
<div id="desktop">
  <div id="wallpaper-particles"></div>
  <div id="desktop-icons"></div>
  <div id="windows-container"></div>
</div>
<!-- Topbar -->
<div id="topbar">
  <div class="topbar-app" onclick="toggleTopbarMenu('apple')">🍎</div>
  <div class="topbar-app" onclick="toggleTopbarMenu('file')">文件</div>
  <div class="topbar-app" onclick="toggleTopbarMenu('edit')">编辑</div>
  <div class="topbar-app" onclick="toggleTopbarMenu('view')">显示</div>
  <div class="topbar-app" onclick="toggleTopbarMenu('window')">窗口</div>
  <div class="topbar-app" onclick="toggleTopbarMenu('help')">帮助</div>
  <div class="topbar-time" id="topbar-time"></div>
  <div class="topbar-icon" onclick="toggleNotifCenter()" title="通知">🔔<span class="topbar-badge" id="notif-badge" style="display:none"></span></div>
  <div class="topbar-icon" onclick="showToast('info','FusionOS','系统运行正常')" title="系统状态">⚡</div>
</div>
<!-- Topbar menus -->
<div id="topbar-apple-menu" class="topbar-menu" style="display:none">
  <div class="topbar-menu-item" onclick="openApp('finder');closeTopbarMenus()">关于 FusionOS</div>
  <div class="topbar-menu-sep"></div>
  <div class="topbar-menu-item" onclick="openApp('settings');closeTopbarMenus()">系统设置…</div>
  <div class="topbar-menu-sep"></div>
  <div class="topbar-menu-item" onclick="doSleep()">睡眠</div>
  <div class="topbar-menu-item" onclick="doRestart()">重新启动…</div>
  <div class="topbar-menu-item" onclick="doShutdown()">关机…</div>
</div>
<div id="topbar-file-menu" class="topbar-menu" style="display:none"><div class="topbar-menu-item">新建窗口</div><div class="topbar-menu-item">新建文件夹</div><div class="topbar-menu-sep"></div><div class="topbar-menu-item">关闭窗口</div></div>
<div id="topbar-edit-menu" class="topbar-menu" style="display:none"><div class="topbar-menu-item">撤销</div><div class="topbar-menu-item">重做</div><div class="topbar-menu-sep"></div><div class="topbar-menu-item">复制</div><div class="topbar-menu-item">粘贴</div></div>
<div id="topbar-view-menu" class="topbar-menu" style="display:none"><div class="topbar-menu-item">实际大小</div><div class="topbar-menu-item">缩放</div><div class="topbar-menu-sep"></div><div class="topbar-menu-item">显示隐藏文件</div></div>
<div id="topbar-window-menu" class="topbar-menu" style="display:none"><div class="topbar-menu-item">最小化所有</div><div class="topbar-menu-item">平铺窗口</div></div>
<div id="topbar-help-menu" class="topbar-menu" style="display:none"><div class="topbar-menu-item">FusionOS 帮助</div><div class="topbar-menu-item">报告问题</div></div>
<!-- Dock -->
<div id="dock"></div>
<!-- Start Menu -->
<div id="start-menu">
  <div class="start-search">
    <svg width="16" height="16" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2"><circle cx="7" cy="7" r="5"/><line x1="11" y1="11" x2="14" y2="14"/></svg>
    <input placeholder="搜索应用、文件、设置…" id="start-search-input">
  </div>
  <div class="start-section-label">常用应用</div>
  <div class="start-apps" id="start-apps"></div>
  <div class="start-section-label">所有应用</div>
  <div class="start-apps" id="start-apps-all"></div>
  <div class="start-power">
    <button class="start-power-btn" onclick="doRestart()">🔄 重启</button>
    <button class="start-power-btn shutdown" onclick="doShutdown()">⏻ 关机</button>
  </div>
</div>
<!-- Context Menu -->
<div class="context-menu" id="desktop-context" style="display:none">
  <div class="context-item" onclick="openApp('finder');closeContextMenu()">📁 打开此电脑</div>
  <div class="context-item" onclick="openApp('terminal');closeContextMenu()">⚡ 打开终端</div>
  <div class="context-sep"></div>
  <div class="context-item" onclick="openApp('settings');closeContextMenu()">⚙ 显示设置</div>
  <div class="context-item" onclick="refreshWallpaperParticles();closeContextMenu()">✨ 刷新壁纸特效</div>
  <div class="context-sep"></div>
  <div class="context-item" onclick="doShutdown()">⏻ 关机</div>
</div>
<!-- Notification Center -->
<div id="notif-center">
  <div class="notif-header">
    <h3>🔔 通知中心</h3>
    <button class="notif-clear" onclick="clearNotifs()">全部清除</button>
  </div>
  <div class="notif-list" id="notif-list"></div>
</div>
<!-- Toast Container -->
<div id="toast-container"></div>
<!-- Loading overlay -->
<div id="loading-overlay" style="position:fixed;inset:0;z-index:999999;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.7);backdrop-filter:blur(10px);transition:opacity 0.5s">
  <div style="text-align:center;color:#fff">
    <div style="font-size:48px;margin-bottom:16px">💻</div>
    <div style="font-size:18px;font-weight:600;margin-bottom:8px">FusionOS 5.0</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.5)">正在启动...</div>
  </div>
</div>
<script>`;

const JS_CODE = buildJS();
const HTML_TAIL = `</script></body></html>`;

fs.writeFileSync('vm-os.html', HTML_HEAD + JS_CODE + HTML_TAIL);
console.log('Build complete! Size:', fs.statSync('vm-os.html').size, 'bytes');

// Syntax check
try {
  const html = fs.readFileSync('vm-os.html', 'utf8');
  const m = html.match(/<script>([\s\S]*?)<\/script>/);
  if (!m) { console.log('ERROR: No script tag found!'); process.exit(1); }
  new Function(m[1]);
  console.log('JS syntax OK!');
} catch(e) {
  console.log('JS SYNTAX ERROR:', e.message);
  process.exit(1);
}

function buildJS() {
  return `/* FusionOS 5.0 — Core JS */
const APPS=[{id:'finder',name:'此电脑',icon:'😊'},{id:'terminal',name:'终端',icon:'>_'},
{id:'notes',name:'记事本',icon:'📝'},{id:'calc',name:'计算器',icon:'🔢'},
{id:'browser',name:'浏览器',icon:'🌐'},{id:'settings',name:'设置',icon:'⚙'},
{id:'music',name:'音乐',icon:'🎵'},{id:'map',name:'地图',icon:'🗺'},
{id:'weather',name:'天气',icon:'🌤'},{id:'paint',name:'绘图',icon:'🎨'}];
let windows={},winOrder=0,winZ=100,focusedWin=null,notifs=[],notifId=0;

/* ═══════════════════════════════════════
   Login
   ═══════════════════════════════════════ */
(function(){
  const c=document.getElementById('login-bg-canvas');
  if(!c)return;
  c.width=window.innerWidth;c.height=window.innerHeight;
  const ctx=c.getContext('2d');
  const pts=Array.from({length:40},()=>({x:Math.random()*c.width,y:Math.random()*c.height,
    r:Math.random()*2+1,dx:(Math.random()-0.5)*0.3,dy:(Math.random()-0.5)*0.3,o:Math.random()*0.4+0.1}));
  (function draw(){ctx.clearRect(0,0,c.width,c.height);pts.forEach(p=>{
    p.x+=p.dx;p.y+=p.dy;
    if(p.x<0)p.x=c.width;if(p.x>c.width)p.x=0;
    if(p.y<0)p.y=c.height;if(p.y>c.height)p.y=0;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle='rgba(255,255,255,'+p.o+')';ctx.fill();
  });requestAnimationFrame(draw)}());
})();
function doLogin(){
  const pwd=document.getElementById('login-pwd').value;
  const bar=document.getElementById('login-prog');
  bar.style.width='30%';
  setTimeout(function(){bar.style.width='70%'},400);
  setTimeout(function(){
    bar.style.width='100%';
    if(pwd&&pwd!=='123456'){showToast('err','登录失败','密码错误');bar.style.width='0%';return;}
    document.getElementById('login-screen').classList.add('hidden');
    document.getElementById('loading-overlay').style.opacity='0';
    setTimeout(function(){document.getElementById('loading-overlay').style.display='none'},500);
    initDesktop();
    showToast('info','欢迎回来','FusionOS 已就绪');
    addNotif('系统','FusionOS 桌面环境已加载','ℹ');
    startClock();refreshWallpaperParticles();
  },800);
}

/* ═══════════════════════════════════════
   Desktop Init
   ═══════════════════════════════════════ */
function initDesktop(){
  buildDesktopIcons();buildDock();renderStartMenu();initDesktopGrid();
  document.addEventListener('click',onGlobalClick);
  document.addEventListener('contextmenu',onContextMenu);
  document.addEventListener('keydown',onKeyDown);
}
function buildDesktopIcons(){
  const c=document.getElementById('desktop-icons');
  c.innerHTML=APPS.map(function(a,i){return '<div class="desktop-icon" data-app="'+a.id+'" ondblclick="openApp(\''+a.id+'\')" onclick="selectDesktopIcon(this)" onmousedown="startIconDrag(event,this)">'+
    '<div class="desktop-icon-inner icon-'+a.id+'">'+a.icon+'</div>'+
    '<span class="desktop-icon-label">'+a.name+'</span></div>';
  }).join('');
}
function buildDock(){
  const c=document.getElementById('dock');
  c.innerHTML=APPS.map(function(a){
    return '<div class="dock-item" data-app="'+a.id+'" onclick="openApp(\''+a.id+'\')">'+
      '<span class="dock-tooltip">'+a.name+'</span>'+a.icon+'</div>';
  }).join('<div class="dock-separator"></div>');
}

/* ═══════════════════════════════════════
   Clock
   ═══════════════════════════════════════ */
function startClock(){updateClock();setInterval(updateClock,1000)}
function updateClock(){
  var d=new Date(),h=d.getHours().toString().padStart(2,'0'),m=d.getMinutes().toString().padStart(2,'0');
  var el=document.getElementById('topbar-time');if(el)el.textContent=h+':'+m;
}

/* ═══════════════════════════════════════
   Wallpaper Particles
   ═══════════════════════════════════════ */
function refreshWallpaperParticles(){
  var c=document.getElementById('wallpaper-particles');if(!c)return;c.innerHTML='';
  for(var i=0;i<12;i++){
    var p=document.createElement('div');p.className='wallpaper-particle';
    var s=Math.random()*80+40;p.style.width=s+'px';p.style.height=s+'px';
    p.style.left=Math.random()*100+'%';p.style.top=Math.random()*100+'%';
    p.style.animationDelay=Math.random()*8+'s';p.style.animationDuration=(6+Math.random()*6)+'s';
    c.appendChild(p);
  }
}

/* ═══════════════════════════════════════
   Desktop Icon Drag
   ═══════════════════════════════════════ */
var GRID={colW:92,rowH:96,padX:16,padY:16},selectedIcon=null,iconDrag=null;
function getGridPos(col,row){return{x:GRID.padX+col*GRID.colW,y:GRID.padY+row*GRID.rowH}}
function getNearestGrid(px,py){
  var mc=Math.max(1,Math.floor((window.innerWidth-GRID.padX*2)/GRID.colW));
  var c=Math.round((px-GRID.padX)/GRID.colW),r=Math.round((py-GRID.padY)/GRID.rowH);
  return{col:Math.max(0,Math.min(c,mc-1)),row:Math.max(0,r)};
}
function getAllIcons(){return[].slice.call(document.querySelectorAll('#desktop-icons .desktop-icon'))}
function setIconPos(el,col,row,animate){
  el.dataset.col=col;el.dataset.row=row;
  var p=getGridPos(col,row);el.style.left=p.x+'px';el.style.top=p.y+'px';
  if(animate){el.style.transition='left 0.22s cubic-bezier(0.16,1,0.3,1),top 0.22s cubic-bezier(0.16,1,0.3,1)';
    setTimeout(function(){el.style.transition='background 0.15s,transform 0.15s'},240);}
}
function autoSortIcons(){
  var icons=getAllIcons().map(function(el){return{el:el,c:parseInt(el.dataset.col)||0,r:parseInt(el.dataset.row)||0}});
  icons.sort(function(a,b){return a.r-b.r||a.c-b.c});
  var mc=Math.max(1,Math.floor((window.innerWidth-GRID.padX*2)/GRID.colW));
  icons.forEach(function(item,i){setIconPos(item.el,i%mc,Math.floor(i/mc),true)});
}
function selectDesktopIcon(el){
  if(selectedIcon)selectedIcon.classList.remove('selected');selectedIcon=el;el.classList.add('selected');
}
function startIconDrag(e,el){
  if(e.button!==0)return;e.preventDefault();
  var rect=el.getBoundingClientRect(),desk=document.getElementById('desktop').getBoundingClientRect();
  iconDrag={el:el,offX:e.clientX-rect.left,offY:e.clientY-rect.top,
    origCol:parseInt(el.dataset.col)||0,origRow:parseInt(el.dataset.row)||0,
    startX:e.clientX,startY:e.clientY,moved:false,deskTop:desk.top,deskLeft:desk.left};
  el.classList.add('dragging');document.addEventListener('mousemove',onIconDrag);document.addEventListener('mouseup',stopIconDrag);
  selectDesktopIcon(el);
}
function onIconDrag(e){
  if(!iconDrag)return;
  if(!iconDrag.moved){var dx=Math.abs(e.clientX-iconDrag.startX),dy=Math.abs(e.clientY-iconDrag.startY);if(dx<5&&dy<5)return;iconDrag.moved=true;}
  var el=iconDrag.el;el.style.transition='none';
  el.style.left=(e.clientX-iconDrag.deskLeft-iconDrag.offX)+'px';el.style.top=(e.clientY-iconDrag.deskTop-iconDrag.offY)+'px';
  getAllIcons().forEach(function(other){if(other===el)return;other.classList.remove('drag-over');
    var r=other.getBoundingClientRect();
    if(Math.abs(e.clientX-iconDrag.deskLeft-parseInt(other.style.left||0)-38)<50&&Math.abs(e.clientY-iconDrag.deskTop-parseInt(other.style.top||0)-41)<50)other.classList.add('drag-over');
  });
}
function stopIconDrag(e){
  document.removeEventListener('mousemove',onIconDrag);document.removeEventListener('mouseup',stopIconDrag);
  if(!iconDrag)return;var el=iconDrag.el;el.classList.remove('dragging');
  getAllIcons().forEach(function(o){o.classList.remove('drag-over')});
  el.style.transition='left 0.22s cubic-bezier(0.16,1,0.3,1),top 0.22s cubic-bezier(0.16,1,0.3,1)';
  if(iconDrag.moved){
    var cx=parseFloat(el.style.left)+38,cy=parseFloat(el.style.top)+41;var g=getNearestGrid(cx,cy);
    var occ=getAllIcons().find(function(o){return o!==el&&parseInt(o.dataset.col)===g.col&&parseInt(o.dataset.row)===g.row});
    if(occ){setIconPos(occ,iconDrag.origCol,iconDrag.origRow,true);}
    setIconPos(el,g.col,g.row,true);setTimeout(autoSortIcons,250);
  }else{setIconPos(el,iconDrag.origCol,iconDrag.origRow,true);}
  iconDrag=null;
}
function initDesktopGrid(){
  var icons=getAllIcons();var mc=Math.max(1,Math.floor((window.innerWidth-GRID.padX*2)/GRID.colW));
  icons.forEach(function(el,i){var col=i%mc,row=Math.floor(i/mc);el.dataset.col=col;el.dataset.row=row;
    var p=getGridPos(col,row);el.style.left=p.x+'px';el.style.top=p.y+'px';el.style.transition='';
  });
}
window.addEventListener('resize',initDesktopGrid);

/* ═══════════════════════════════════════
   Window Management
   ═══════════════════════════════════════ */
function openApp(appId,ev){
  if(ev)ev.stopPropagation();
  var existing=Object.keys(windows).map(function(k){return windows[k]}).find(function(w){return w.appId===appId&&!w.closed});
  if(existing){
    if(focusedWin===existing.id){minimizeWindow(existing.id);return;}
    focusWindow(existing.id);return;
  }
  winOrder++;var id='win-'+winOrder;var app=APPS.find(function(a){return a.id===appId})||APPS[0];
  var w=window.innerWidth*0.55,h=window.innerHeight*0.6;
  var x=(window.innerWidth-w)/2+(Math.random()*40-20),y=(window.innerHeight-h)/2+(Math.random()*30-15);
  var win=document.createElement('div');win.className='window';win.id=id;
  win.style.left=x+'px';win.style.top=y+'px';win.style.width=w+'px';win.style.height=h+'px';
  win.innerHTML='<div class="window-titlebar"><div class="traffic-lights">'+
    '<span class="close" onclick="closeWindow(\''+id+'\')"><svg width="8" height="8" viewBox="0 0 8 8"><path d="M2 2l4 4M6 2l-4 4" stroke="#4a0000" stroke-width="1.2" fill="none"/></svg></span>'+
    '<span class="min" onclick="minimizeWindow(\''+id+'\')"><svg width="8" height="8" viewBox="0 0 8 8"><path d="M2 4h4" stroke="#6a5300" stroke-width="1.2"/></svg></span>'+
    '<span class="max" onclick="toggleMaximize(\''+id+'\')"><svg width="8" height="8" viewBox="0 0 8 8"><rect x="1.5" y="1.5" width="5" height="5" rx="1" stroke="#006000" stroke-width="1" fill="none"/></svg></span>'+
    '</div><div class="window-title">'+app.name+'</div></div>'+
    '<div class="window-body" id="body-'+id+'"></div>';
  document.getElementById('windows-container').appendChild(win);
  windows[id]={appId:appId,el:win,closed:false,minimized:false,maximized:false};
  focusWindow(id);renderAppContent(id,appId);makeDraggable(win);updateDock();
}
function closeWindow(id){
  var win=windows[id];if(!win)return;win.el.classList.add('closing');
  setTimeout(function(){win.el.remove();delete windows[id];if(focusedWin===id)focusedWin=null;updateDock();},260);
}
function minimizeWindow(id){var win=windows[id];if(!win)return;win.minimized=true;win.el.style.display='none';if(focusedWin===id)focusedWin=null;updateDock();}
function toggleMaximize(id){
  var win=windows[id];if(!win)return;
  if(win.maximized){win.el.classList.remove('maximized');win.el.style.left=win._prevLeft;win.el.style.top=win._prevTop;win.el.style.width=win._prevW;win.el.style.height=win._prevH;win.maximized=false;}
  else{win._prevLeft=win.el.style.left;win._prevTop=win.el.style.top;win._prevW=win.el.style.width;win._prevH=win.el.style.height;win.el.classList.add('maximized');win.el.style.left='0';win.el.style.top='28px';win.el.style.width='100%';win.el.style.height='calc(100vh - 28px - 56px)';win.maximized=true;}
}
function focusWindow(id){
  var win=windows[id];if(!win||win.closed)return;
  win.el.style.zIndex=++winZ;win.el.classList.add('focused');
  if(focusedWin&&focusedWin!==id){var pw=windows[focusedWin];if(pw)pw.el.classList.remove('focused');}
  focusedWin=id;win.el.style.display='';win.minimized=false;updateDock();
}
function makeDraggable(el){
  var bar=el.querySelector('.window-titlebar');if(!bar)return;var ox,oy,dragging=false;
  bar.addEventListener('mousedown',function(e){
    if(e.target.closest('.traffic-lights'))return;dragging=true;
    var r=el.getBoundingClientRect();ox=e.clientX-r.left;oy=e.clientY-r.top;el.style.transition='none';focusWindow(el.id);
    function onMove(e2){if(!dragging)return;var w=el.getBoundingClientRect().width;
      var nx=e2.clientX-ox,ny=e2.clientY-oy;nx=Math.max(-w+80,Math.min(nx,window.innerWidth-80));ny=Math.max(28,Math.min(ny,window.innerHeight-56));
      el.style.left=nx+'px';el.style.top=ny+'px';}
    function onUp(){dragging=false;el.style.transition='';document.removeEventListener('mousemove',onMove);document.removeEventListener('mouseup',onUp);}
    document.addEventListener('mousemove',onMove);document.addEventListener('mouseup',onUp);
  });
  var rh=document.createElement('div');rh.style.cssText='position:absolute;right:0;bottom:0;width:16px;height:16px;cursor:se-resize';el.appendChild(rh);
  rh.addEventListener('mousedown',function(e){e.stopPropagation();var r=el.getBoundingClientRect();var sx=e.clientX,sy=e.clientY,sw=r.width,sh=r.height;
    function onMove(e2){el.style.width=Math.max(280,sw+e2.clientX-sx)+'px';el.style.height=Math.max(200,sh+e2.clientY-sy)+'px';}
    function onUp(){document.removeEventListener('mousemove',onMove);document.removeEventListener('mouseup',onUp);}
    document.addEventListener('mousemove',onMove);document.addEventListener('mouseup',onUp);
  });
}
function updateDock(){document.querySelectorAll('#dock .dock-item').forEach(function(el){var appId=el.dataset.app;
  var isOpen=Object.keys(windows).map(function(k){return windows[k]}).some(function(w){return w.appId===appId&&!w.closed});
  var isFocused=isOpen&&focusedWin&&windows[focusedWin]&&windows[focusedWin].appId===appId;
  el.classList.toggle('running',!!isOpen);el.classList.toggle('active',!!isFocused);
});}

/* ═══════════════════════════════════════
   Start Menu
   ═══════════════════════════════════════ */
function renderStartMenu(){
  var c=document.getElementById('start-apps'),c2=document.getElementById('start-apps-all');if(!c)return;
  var common=['finder','terminal','notes','calc','browser','settings'];
  c.innerHTML=common.map(function(a){var app=APPS.find(function(x){return x.id===a});return '<div class="start-app-item" onclick="openApp(\''+a+'\');toggleStartMenu()"><div class="start-app-icon icon-'+a+'">'+app.icon+'</div><div class="start-app-name">'+app.name+'</div></div>';}).join('');
  c2.innerHTML=APPS.map(function(a){return '<div class="start-app-item" onclick="openApp(\''+a.id+'\');toggleStartMenu()"><div class="start-app-icon icon-'+a.id+'">'+a.icon+'</div><div class="start-app-name">'+a.name+'</div></div>';}).join('');
}
function toggleStartMenu(){document.getElementById('start-menu').classList.toggle('show');}

/* ═══════════════════════════════════════
   Menus & Context
   ═══════════════════════════════════════ */
var activeTopbarMenu=null;
function toggleTopbarMenu(name){
  var map={apple:'topbar-apple-menu',file:'topbar-file-menu',edit:'topbar-edit-menu',view:'topbar-view-menu',window:'topbar-window-menu',help:'topbar-help-menu'};
  var mid=map[name];if(!mid)return;var el=document.getElementById(mid);if(!el)return;
  if(activeTopbarMenu&&activeTopbarMenu!==mid){document.getElementById(activeTopbarMenu).style.display='none';}
  el.style.display=el.style.display==='none'?'':'none';activeTopbarMenu=el.style.display===''?'':mid;
}
function closeTopbarMenus(){document.querySelectorAll('.topbar-menu').forEach(function(m){m.style.display='none';});activeTopbarMenu=null;}
function onContextMenu(e){e.preventDefault();closeContextMenu();var menu=document.getElementById('desktop-context');menu.style.display='';menu.style.left=e.clientX+'px';menu.style.top=e.clientY+'px';}
function closeContextMenu(){var m=document.getElementById('desktop-context');if(m)m.style.display='none';closeTopbarMenus();}
function onGlobalClick(e){
  if(!e.target.closest('#start-menu')&&!e.target.closest('#start-btn'))document.getElementById('start-menu').classList.remove('show');
  if(!e.target.closest('.context-menu'))closeContextMenu();
  if(e.target.closest('.window'))focusWindow(e.target.closest('.window').id);
  if(!e.target.closest('.desktop-icon')){if(selectedIcon)selectedIcon.classList.remove('selected');selectedIcon=null;}
}

/* ═══════════════════════════════════════
   Keyboard Shortcuts
   ═══════════════════════════════════════ */
function onKeyDown(e){
  if(e.key==='Escape'){if(document.getElementById('start-menu').classList.contains('show'))toggleStartMenu();else if(document.getElementById('notif-center').classList.contains('show'))toggleNotifCenter();}
  if((e.metaKey||e.ctrlKey)&&e.key==='t'){e.preventDefault();openApp('terminal')}
  if((e.metaKey||e.ctrlKey)&&e.key==='n'){e.preventDefault();openApp('notes')}
  if((e.metaKey||e.ctrlKey)&&e.key==='f'){e.preventDefault();openApp('finder')}
  if((e.metaKey||e.ctrlKey)&&e.key==='b'){e.preventDefault();openApp('browser')}
  if((e.metaKey||e.ctrlKey)&&e.key==='m'){e.preventDefault();openApp('music')}
}

/* ═══════════════════════════════════════
   Toast & Notifications
   ═══════════════════════════════════════ */
function showToast(type,title,body){
  var c=document.getElementById('toast-container');var t=document.createElement('div');t.className='toast';
  var icons={info:'ℹ️',err:'❌',ok:'✅'};
  t.innerHTML='<span class="toast-icon">'+(icons[type]||'ℹ️')+'</span><div><div style="font-weight:600">'+title+'</div><div style="font-size:12px;color:var(--text-secondary)">'+(body||'')+'</div></div>';
  c.appendChild(t);setTimeout(function(){t.classList.add('leaving');setTimeout(function(){t.remove()},300)},3000);
}
function toggleNotifCenter(){document.getElementById('notif-center').classList.toggle('show');}
function addNotif(title,body,icon){
  notifs.unshift({id:++notifId,title:title,body:body,icon:icon||'ℹ',t:new Date()});if(notifs.length>20)notifs.length=20;renderNotifs();
  var badge=document.getElementById('notif-badge');badge.style.display='';badge.textContent=notifs.length;
}
function clearNotifs(){notifs=[];renderNotifs();document.getElementById('notif-badge').style.display='none';}
function renderNotifs(){
  var c=document.getElementById('notif-list');
  c.innerHTML=notifs.map(function(n){var ts=n.t.getHours().toString().padStart(2,'0')+':'+n.t.getMinutes().toString().padStart(2,'0');
    return '<div class="notif-item"><div class="notif-item-icon">'+(n.icon||'ℹ')+'</div><div class="notif-item-content"><div class="notif-item-title">'+n.title+'</div><div class="notif-item-body">'+(n.body||'')+'</div><div class="notif-item-time">'+ts+'</div></div></div>';
  }).join('');
}

/* ═══════════════════════════════════════
   Shutdown / Restart
   ═══════════════════════════════════════ */
function doShutdown(){closeContextMenu();showToast('info','正在关机','FusionOS 正在关闭…');setTimeout(function(){document.getElementById('desktop').style.opacity='0';document.getElementById('topbar').style.opacity='0';document.getElementById('dock').style.opacity='0';setTimeout(function(){document.getElementById('login-screen').classList.remove('hidden');document.getElementById('desktop').style.opacity='';document.getElementById('topbar').style.opacity='';document.getElementById('dock').style.opacity='';},1500);},800);}
function doRestart(){showToast('info','正在重启…','FusionOS 正在重新启动');setTimeout(doShutdown,1000);}
function doSleep(){showToast('info','睡眠','系统已睡眠（模拟）')}

/* ═══════════════════════════════════════
   App Content Rendering
   ═══════════════════════════════════════ */
function renderAppContent(winId,appId){
  var body=document.getElementById('body-'+winId);if(!body)return;
  switch(appId){
    case'finder':renderFinder(body,winId);break;
    case'terminal':renderTerminal(body,winId);break;
    case'notes':renderNotes(body,winId);break;
    case'calc':renderCalc(body,winId);break;
    case'browser':renderBrowser(body,winId);break;
    case'settings':renderSettings(body,winId);break;
    case'music':renderMusic(body,winId);break;
    case'map':renderMap(body,winId);break;
    case'weather':renderWeather(body,winId);break;
    case'paint':renderPaint(body,winId);break;
  }
}`;
}

process.exit(0);
