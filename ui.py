"""Editor UI for the dashboard server (single page, no build step).

Layout: one interactive treemap on the left, a candidate pool on the right.
There is no separate "selected list" — tiles in the map are the selection, and
they are dragged/clicked directly. Group assignment happens by dropping a tile
onto a group bucket, or onto another tile that already belongs to that group.
"""

UI_HTML = r"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard 编辑器</title>
<style>
@font-face{font-family:"SmileySans";src:url('/assets/font/SmileySans-Oblique.otf.woff2') format('woff2');font-display:swap}
:root{
  color-scheme:dark;
  --bg:#07090d;--panel:#0c1017;--panel2:#0f141c;--line:#1b2331;--line2:#252f3f;
  --ink:#dde5ee;--dim:#8d99a9;--faint:#5b6675;
  --accent:#9fb8cf;--warm:#dfa08a;--ok:#93bcab;--r:12px;
  /* one bar height shared by the editor and the preview, so toggling views
     never shifts the content below it */
  --bar-h:52px;
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"SmileySans","Segoe UI",system-ui,sans-serif;font-size:14px;
  display:grid;grid-template-rows:auto auto 1fr;overflow:hidden}

/* ---------- top bar ---------- */
/* Fixed height shared with the preview bar, so toggling views never shifts
   anything. Vertical padding is 0 — flex centring handles it and keeps the
   computed height exactly var(--bar-h). */
.bar{display:flex;align-items:center;gap:12px;padding:0 18px;
  height:var(--bar-h);box-sizing:border-box;
  border-bottom:1px solid var(--line);background:linear-gradient(#0b0f16,#07090d);
  flex-wrap:nowrap;overflow:hidden}
.bar h1{font-size:16px;font-weight:400;margin:0;letter-spacing:.2px}
.spacer{flex:1 1 auto;min-width:0}
.bar button{flex:0 0 auto}
/* new-group input sits right after the title, before the action buttons */
.bar-group{display:flex;align-items:center;gap:6px;flex:0 0 auto;
  margin-left:6px;padding-left:14px;border-left:1px solid var(--line)}
.bar-group input{font:inherit;font-size:12.5px;color:var(--ink);
  background:#0a0e14;border:1px solid var(--line2);border-radius:8px;
  padding:5px 9px;width:112px}
.bar-group input::placeholder{color:#4a5567}
.bar-group input:focus{outline:none;border-color:var(--accent)}
.bar-group button{padding:5px 10px;font-size:13px;line-height:1}

button{font:inherit;color:var(--ink);background:var(--panel2);
  border:1px solid var(--line2);border-radius:9px;padding:7px 13px;cursor:pointer;
  transition:background .15s,border-color .15s,transform .08s}
button:hover{background:#151c26;border-color:#35435a}
button:active{transform:translateY(1px)}
button:disabled{opacity:.45;cursor:not-allowed;transform:none}
button.primary{background:#1d2b3c;border-color:#33506e;color:#dbe8f6}
button.primary:hover{background:#24384e}
button.danger{color:var(--warm);border-color:#4a3230}
button.danger:hover{background:#1c1413}
button.sm{padding:4px 9px;font-size:12px;border-radius:7px}
button.on{background:#24384e;border-color:var(--accent);color:#e6f0fa}

/* ================= GitHub profile preview (true to github.com) ================= */
/* Geometry and colours measured off a live github.com profile page:
     canvas bg   rgb(33,40,48)      border     rgb(61,68,77)
     text        rgb(209,215,224)   muted      rgb(145,152,161)
     layout     1216px wide, 296px sidebar, 24px gutter, 896px main column
     README box 896px with 24px padding  ->  846px of usable content width
   That 846px is the number that matters: GitHub caps README images at
   max-width:100%. Our SVG is built at exactly that width, so it renders 1:1
   with no scaling; the preview shows it at the size the profile really uses. */
.pv{display:none;position:fixed;inset:0;z-index:70;background:#212830;
  overflow:auto;color:#d1d7e0;
  opacity:0;transform:translateY(10px) scale(.995);
  transition:opacity .26s ease, transform .26s cubic-bezier(.2,.8,.3,1)}
.pv.on{display:block;opacity:1;transform:none}
.pv.closing{display:block;opacity:0;transform:translateY(8px) scale(.997)}

/* same height as the editor bar so the switch doesn't jump */
.pv-top{position:sticky;top:0;z-index:3;display:flex;align-items:center;gap:12px;
  padding:0 18px;height:var(--bar-h);box-sizing:border-box;
  background:#252d38;border-bottom:1px solid #3d444d}
.pv-top .mark{display:grid;place-items:center;width:26px;height:26px;
  border-radius:50%;background:#d1d7e0;color:#212830;font-size:14px;flex:0 0 auto}
.pv-top .ttl{font-size:13px;color:#9198a1}
.pv-top .sz{font-size:11.5px;color:#9198a1;padding:2px 8px;
  border:1px solid #3d444d;border-radius:6px;font-variant-numeric:tabular-nums}
.pv-top .spacer{flex:1}
.pv-top button{background:#2d333b;border-color:#3d444d;color:#d1d7e0}
.pv-top button:hover{background:#3d444d;border-color:#4f5862}

/* GitHub's own profile layout: 296 + 24 + 896 = 1216px of content, centred.
   The main column is a hard 896px (not minmax) so the README lands on exactly
   846px of usable width — same as the real page — instead of shrinking with
   the viewport. Narrow screens collapse to one column instead. */
.pv-body{max-width:1216px;margin:0 auto;padding:24px 0 80px;
  display:grid;grid-template-columns:296px 896px;gap:24px;
  justify-content:center;align-items:start;box-sizing:content-box}
@media (max-width:1256px){
  .pv-body{padding:24px 16px 80px;box-sizing:border-box;
    grid-template-columns:296px minmax(0,896px)}
}
@media (max-width:1012px){
  .pv-body{grid-template-columns:minmax(0,1fr);padding:18px 14px 60px}
  .gh-side{display:none}
}

/* ---- left sidebar: avatar, name, bio, followers, links ---- */
.gh-side{display:flex;flex-direction:column;gap:16px;position:sticky;
  top:calc(var(--bar-h) + 16px);align-items:flex-start;min-width:0}
.gh-avatar{width:100%;aspect-ratio:1;border-radius:50%;flex:0 0 auto;
  background:linear-gradient(135deg,#1f6feb33,#8957e533);
  border:1px solid #3d444d;display:grid;place-items:center;
  font-size:84px;color:#d1d7e0;letter-spacing:1px;font-weight:300}
.gh-name-wrap{display:flex;flex-direction:column;gap:0;min-width:0}
.gh-name{font-size:24px;font-weight:600;line-height:1.25;margin:0;color:#d1d7e0}
.gh-login{font-size:20px;color:#9198a1;font-weight:300;margin:0;line-height:1.3}
.gh-bio{font-size:16px;line-height:1.5;color:#d1d7e0;margin:0}
.gh-follow{display:flex;gap:6px;align-items:center;font-size:14px;color:#9198a1;
  flex-wrap:wrap}
.gh-follow b{color:#d1d7e0;font-weight:600}
.gh-follow .dot{color:#6e7681}
/* measured off github.com: 296x32, bg rgb(42,49,60), 6px radius */
.gh-edit{display:block;width:100%;box-sizing:border-box;text-align:center;
  font-size:14px;color:#d1d7e0;background:#2a313c;
  border:1px solid #3d444d;border-radius:6px;padding:5px 16px;line-height:1.5;
  margin-top:2px}
.gh-list{display:flex;flex-direction:column;gap:7px;width:100%;
  padding-top:14px;border-top:1px solid #3d444d}
.gh-list .item{display:flex;gap:8px;align-items:center;font-size:14px;
  color:#9198a1;line-height:1.4}
.gh-list .item b{color:#d1d7e0;font-weight:400}
.gh-pins{margin-top:2px}
.gh-pins .lbl{font-size:16px;color:#d1d7e0;margin-bottom:8px}
.gh-pins .pin{display:flex;gap:7px;align-items:center;font-size:13px;
  color:#4493f8;text-decoration:none;line-height:1.4}
.gh-pins .pin .repo{color:#4493f8;font-weight:600}
.gh-pins .pin .desc{color:#9198a1;font-size:12px;display:block;font-weight:400}

/* ---- README column ---- */
.gh-readme{min-width:0}
.gh-readme-hd{display:flex;align-items:center;gap:8px;font-size:14px;
  color:#9198a1;margin-bottom:8px;padding-bottom:8px;
  border-bottom:1px solid #3d444d;flex-wrap:wrap}
.gh-readme-hd .mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
.gh-readme-hd .tag{font-size:11px;color:#9198a1;border:1px solid #3d444d;
  border-radius:2em;padding:0 7px;line-height:18px}
/* The README card: 896px outer, 24px padding -> 846px content, exactly like
   GitHub. The inner box is that content width, so the SVG is clamped to it the
   same way github.com does (max-width:100%). */
.gh-box{border:1px solid #3d444d;border-radius:6px;background:#212830;
  padding:24px;box-sizing:border-box;width:100%}
.gh-box .inner{width:100%;display:flex;justify-content:flex-start}
/* 846px content box — the exact width GitHub gives README images. The SVG is
   generated at that width, so width:100% resolves to 846 and nothing scales. */
.pv .stage{position:relative;border:0;border-radius:0;background:transparent;
  width:100%;max-width:846px}
.pv .stage>svg{display:block;width:100%;height:auto;max-width:100%;border-radius:0}
/* keep editing available in preview: same hit boxes, GitHub-blue affordance */
.pv .hit{border-radius:8px;cursor:pointer}
.pv .hit:hover{border-color:rgba(68,147,248,.8);background:rgba(68,147,248,.1)}
.pv .hit.sel{border-color:#4493f8;background:rgba(68,147,248,.14);
  box-shadow:0 0 0 1px #4493f8 inset}
.pv-hint{font-size:12px;color:#9198a1;margin:14px 0 0;line-height:1.6}
.pv-hint b{color:#d1d7e0;font-weight:400}
.pv-hint .warn{color:#e3b341}

/* The linked list that ships under the image. Rendered with GitHub's own
   markdown typography so it reads exactly like it will on the profile:
   bold group headings, a real <ul> with 16px body text, links in #4493f8. */
.gh-projects{margin-top:20px;font-size:16px;line-height:1.6;color:#d1d7e0}
.gh-projects h3{font-size:16px;font-weight:600;margin:22px 0 8px;color:#d1d7e0;
  line-height:1.25}
.gh-projects h3:first-child{margin-top:0}
.gh-projects ul{margin:0 0 8px;padding-left:2em;list-style:disc}
.gh-projects li{margin:4px 0}
.gh-projects li::marker{color:#9198a1}
.gh-projects a{color:#4493f8;text-decoration:none;font-weight:600}
.gh-projects a:hover{text-decoration:underline}
.gh-projects .meta{color:#9198a1;font-weight:400}
.gh-projects .kp{color:#d1d7e0;font-weight:400}

/* ---------- main split: candidate pool on the left, map on the right ---------- */
.main{display:grid;grid-template-columns:340px minmax(0,1fr);min-height:0}
.pool{border-right:1px solid var(--line);display:grid;
  grid-template-rows:auto auto minmax(0,1fr);min-height:0;background:var(--panel)}
/* map column never scrolls: the stage is sized to fit the viewport height */
.left{padding:14px 20px 18px;min-width:0;overflow:hidden;
  display:flex;flex-direction:column;justify-content:center}

/* ---------- treemap stage ---------- */
/* Size is computed in JS (fitStage) so the map fills the available height
   without ever changing its native aspect ratio — distortion would desync the SVG
   from the HTML hit-boxes sitting on top of it. */
.stage{position:relative;flex:0 1 auto;margin:0 auto;
  border:1px solid var(--line);border-radius:var(--r);
  overflow:hidden;background:#0b0e13}
.stage>svg{width:100%;height:100%;display:block}
/* The editor draws its own interactive group headers (.ghead) on top of the
   map, so hide the baked-in SVG labels — they'd show through as a ghost copy.
   Scoped to the editor stage: the 1:1 preview keeps the SVG's own labels,
   because that's what the profile will really show. The exported
   dashboard.svg is untouched. */
#stage svg .glabel{display:none}
.stage.drop-hot{outline:2px dashed #33506e;outline-offset:-6px}
.overlay{position:absolute;inset:0}
.hit{position:absolute;border-radius:10px;cursor:grab;
  border:1px solid transparent;transition:background .12s,border-color .12s}
.hit:hover{border-color:rgba(159,184,207,.55);background:rgba(159,184,207,.07)}
.hit.sel{border-color:var(--accent);background:rgba(159,184,207,.1);
  box-shadow:0 0 0 1px var(--accent) inset}
.hit.drag{opacity:.3}
.hit.ins-before::after,.hit.ins-after::after{content:"";position:absolute;top:0;bottom:0;
  width:3px;background:var(--warm);border-radius:2px}
.hit.ins-before::after{left:-2px}
.hit.ins-after::after{right:-2px}
/* Drop target over an empty group's region. The SVG already draws a dashed
   placeholder; this adds the hover affordance and captures the drop. */
.dropzone{position:absolute;border-radius:12px;cursor:copy;
  border:1px dashed transparent;transition:background .12s,border-color .12s}
.dropzone:hover{border-color:rgba(159,184,207,.45);background:rgba(159,184,207,.05)}
.dropzone.over{border-color:var(--accent);background:rgba(159,184,207,.14);
  border-style:solid}
.empty-stage{position:absolute;inset:0;display:grid;place-content:center;gap:8px;
  text-align:center;color:var(--faint);font-size:13px;line-height:1.7;pointer-events:none}
.stage-note{color:var(--faint);font-size:12px;line-height:1.65;margin:10px 0 0}
.stage-note b{color:var(--dim);font-weight:400}

/* ---------- tile editor popover ---------- */
/* Above the preview layer (70) so it stays usable while previewing. */
.editor{position:fixed;z-index:90;width:310px;background:#0e131b;
  border:1px solid var(--line2);border-radius:12px;padding:12px;
  box-shadow:0 18px 40px rgba(0,0,0,.55);display:none}
.editor.show{display:block}
.editor .hd{display:flex;align-items:baseline;gap:8px;margin-bottom:9px}
.editor .hd .rp{font-size:13.5px;word-break:break-all;line-height:1.3}
.editor .hd .rp .o{color:var(--faint)}
.editor .hd .x{margin-left:auto;cursor:pointer;color:var(--faint);padding:0 4px;line-height:1}
.editor .hd .x:hover{color:var(--warm)}
.editor .stats{display:flex;gap:10px;flex-wrap:wrap;font-size:11.5px;color:var(--dim);
  font-variant-numeric:tabular-nums;margin-bottom:10px;padding-bottom:9px;
  border-bottom:1px solid var(--line)}
.editor .stats i{color:var(--faint);font-style:normal}
.editor label{display:block;font-size:11px;color:var(--faint);margin:9px 0 4px}
.editor select,.editor input[type=number]{font:inherit;font-size:12.5px;color:var(--ink);
  background:#090d13;border:1px solid var(--line2);border-radius:7px;padding:6px 8px;width:100%}
.editor input[type=number]{font-variant-numeric:tabular-nums}
.editor .kp{display:flex;flex-direction:column;gap:5px}
.editor .kp input{font:inherit;font-size:12px;color:var(--ink);background:#090d13;
  border:1px solid var(--line2);border-radius:7px;padding:6px 8px;width:100%}
.editor .kp input::placeholder{color:#3d4756}
.editor .row{display:flex;gap:7px;align-items:center;margin-top:11px}
.editor .row .boost{flex:1}
.editor .hintx{font-size:11px;color:var(--faint);margin-top:8px;line-height:1.5}
select:focus,input:focus{outline:none;border-color:var(--accent)!important}

/* ---------- group headers on the map ---------- */
/* The editor's interactive replacement for the SVG's baked-in group label
   (that one is hidden via `#stage svg .glabel`). Everything scales with
   --map-scale, published by fitStage(): the stage is usually wider than its
   846px design width, so fixed px sizes would look shrunken next to SVG text.

   Split in two: .gdrop is the full-width invisible drop strip, .ghead is the
   compact pill that carries the label and buttons. Keeping them separate lets
   the pill hug its text instead of highlighting the entire region width. */
.gdrop{position:absolute;z-index:2;border-radius:calc(6px * var(--map-scale, 1));
  border:1px solid transparent;transition:background .12s,border-color .12s}
.gdrop.over{border-color:var(--accent);background:rgba(159,184,207,.16)}

.ghead{position:absolute;z-index:3;display:inline-flex;align-items:center;
  gap:calc(1px * var(--map-scale, 1));
  height:calc(18px * var(--map-scale, 1));
  padding:0 calc(3px * var(--map-scale, 1));
  border-radius:calc(5px * var(--map-scale, 1));
  border:1px solid transparent;
  transition:background .12s,border-color .12s}
.ghead:hover{background:rgba(255,255,255,.07);border-color:var(--line2)}
.ghead .gt{font-size:calc(10.5px * var(--map-scale, 1));color:var(--dim);
  line-height:1;cursor:text;
  padding:calc(1px * var(--map-scale, 1)) calc(2px * var(--map-scale, 1));
  border-radius:calc(3px * var(--map-scale, 1));white-space:nowrap;
  max-width:calc(190px * var(--map-scale, 1));
  overflow:hidden;text-overflow:ellipsis;
  transition:color .12s,background .12s}
.ghead .gt:hover{color:var(--ink);background:rgba(159,184,207,.14)}
.ghead .gx{font-size:calc(9.5px * var(--map-scale, 1));color:var(--faint);
  cursor:pointer;line-height:1;opacity:0;
  padding:calc(1px * var(--map-scale, 1)) calc(3px * var(--map-scale, 1));
  border-radius:calc(3px * var(--map-scale, 1));
  transition:opacity .12s,color .12s,background .12s}
.ghead:hover .gx{opacity:1}
.ghead .gx:hover{color:var(--ink);background:rgba(255,255,255,.1)}
.ghead .gx.del:hover{color:var(--warm);background:#1c1413}
.grename{font:inherit;font-size:calc(10.5px * var(--map-scale, 1));color:var(--ink);
  background:#0a0e14;border:1px solid var(--accent);
  border-radius:calc(4px * var(--map-scale, 1));
  padding:calc(1px * var(--map-scale, 1)) calc(4px * var(--map-scale, 1));
  width:calc(130px * var(--map-scale, 1));}
/* ---------- candidate pool ---------- */
.pool-head{display:flex;align-items:center;gap:7px;padding:12px 13px;
  border-bottom:1px solid var(--line);flex-wrap:wrap}
.pool-head input{font:inherit;font-size:12.5px;color:var(--ink);background:#0a0e14;
  border:1px solid var(--line2);border-radius:8px;padding:6px 10px;flex:1;min-width:90px}
.pool-head .refresh{display:grid;place-items:center;padding:6px 8px;line-height:0}
.pool-head .refresh svg{display:block}
.pool-head .refresh.busy svg{animation:spin .9s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.pool-head .refresh:disabled{opacity:.55;cursor:progress}

/* owner filter: takes whatever height its wrapped chips need — never scrolls */
.pool-owner{padding:9px 13px 4px;display:flex;gap:5px;align-items:center;flex-wrap:wrap;
  flex:0 0 auto;border-bottom:1px solid var(--line)}
.pool-owner .lbl{font-size:11px;color:var(--faint);flex:0 0 auto;margin-right:1px}
.fchip{font-size:11.5px;color:var(--dim);border:1px solid var(--line2);border-radius:999px;
  padding:3px 7px 3px 10px;cursor:pointer;user-select:none;white-space:nowrap;line-height:1.5;
  display:inline-flex;align-items:center;gap:1px}
.fchip:hover{border-color:#35435a}
.fchip.on{background:#16202c;border-color:#33506e;color:#cfe0f0}
.fchip .c{color:var(--faint);font-size:10px;margin:0 3px}
/* per-source refresh inside the chip */
.fchip .orefresh{display:grid;place-items:center;background:transparent;border:0;
  color:inherit;font:inherit;font-size:11px;line-height:1;padding:2px 4px;
  border-radius:50%;cursor:pointer;opacity:.55;transition:opacity .12s,background .12s}
.fchip:hover .orefresh{opacity:.9}
.fchip .orefresh:hover{background:#223042;opacity:1}
.fchip .orefresh:disabled{opacity:.5;cursor:progress}
.fchip .orefresh.busy{opacity:1}
.fchip .orefresh.busy svg{animation:spin .9s linear infinite}
.pool-list{overflow:auto;min-height:0;padding:6px 8px 20px}
.prow{display:grid;grid-template-columns:minmax(0,1fr) auto auto auto;gap:8px;align-items:center;
  padding:7px 8px;border-radius:8px;cursor:grab;
  border:1px solid transparent;transition:background .12s,border-color .12s}
.prow:hover{background:#111823;border-color:#1e2a3a}
.prow.drag{opacity:.35}
.prow .nm{font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.prow .nm .o{color:var(--faint)}
.prow .stats{font-size:10.5px;color:var(--dim);font-variant-numeric:tabular-nums;
  white-space:nowrap;opacity:.85}
.prow .meta{font-size:10.5px;color:var(--faint);font-variant-numeric:tabular-nums;
  white-space:nowrap;min-width:34px;text-align:right}
.prow .add{opacity:0;padding:2px 7px;font-size:12px;border-radius:6px}
.prow:hover .add{opacity:1}
.prow .org{font-size:9.5px;color:var(--ok);border:1px solid #2f5344;border-radius:4px;
  padding:0 4px;margin-left:5px}
.pool-empty{color:var(--faint);font-size:12px;padding:24px 14px;text-align:center;line-height:1.7}

/* ---------- toast ---------- */
.toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,20px);
  background:#141b25;border:1px solid var(--line2);border-radius:10px;
  padding:9px 16px;font-size:12.5px;color:var(--ink);opacity:0;pointer-events:none;
  transition:opacity .2s,transform .2s;z-index:95;max-width:80vw}
.toast.show{opacity:1;transform:translate(-50%,0)}
.toast.err{border-color:#4a3230;color:#f0c4bb}
.toast.ok{border-color:#2f5344;color:#bfe3d3}

@media (max-width:1100px){
  .main{grid-template-columns:minmax(0,1fr)}
  .pool{border-right:0;border-bottom:1px solid var(--line);max-height:44vh}
}
</style></head><body>

<div class="bar">
  <h1>Dashboard 编辑器</h1>
  <div class="bar-group">
    <input id="new-group" maxlength="16" placeholder="新分组…">
    <button id="btn-add-group" title="新建分组">+</button>
  </div>
  <div class="spacer"></div>
  <button id="btn-export" class="primary" title="写 dashboard.svg / preview.html / dashboard.md">导出 SVG</button>
  <button id="btn-save" title="保存到 projects.json (Ctrl+S)">保存配置</button>
  <button id="btn-preview" title="以真实尺寸查看 GitHub profile 中的效果（可继续编辑）">Preview</button>
</div>

<div class="main">
  <aside class="pool">
    <div class="pool-head">
      <input id="pool-search" placeholder="搜索候选仓库…">
      <button class="sm" id="btn-pool-sort" title="切换排序">权重 ↓</button>
    </div>
    <div class="pool-owner" id="pool-filter"></div>
    <div class="pool-list" id="pool-list"></div>
  </aside>

  <div class="left">
    <div class="stage" id="stage">
      <div class="overlay" id="overlay"></div>
    </div>
  </div>
</div>

<div class="editor" id="editor"></div>
<div class="toast" id="toast"></div>

<div class="pv" id="pv">
  <div class="pv-top">
    <span class="mark">⌂</span>
    <span class="ttl">GitHub profile · 1:1 预览</span>
    <span class="sz" id="pv-size">—</span>
    <div class="spacer"></div>
    <span class="ttl" id="pv-note">点击方块仍可编辑</span>
    <button id="btn-preview-close">返回编辑器</button>
  </div>
  <div class="pv-body">
    <aside class="gh-side">
      <div class="gh-avatar" id="pv-avatar">W</div>
      <div class="gh-name-wrap">
        <h1 class="gh-name" id="pv-name">Weidows</h1>
        <p class="gh-login" id="pv-login">Weidows</p>
      </div>
      <p class="gh-bio" id="pv-bio">Learning by building. Go / Python / 前端小工具。</p>
      <div class="gh-follow">
        <span><b id="pv-repos">0</b> repositories</span>
        <span class="dot">·</span>
        <span><b id="pv-stars">0</b> stars</span>
      </div>
      <div class="gh-edit">Edit profile</div>
      <div class="gh-list">
        <div class="item">📍 <b>Earth</b></div>
        <div class="item">🔗 <b id="pv-link">github.com/Weidows</b></div>
      </div>
      <div class="gh-pins">
        <div class="lbl">Pinned</div>
        <a class="pin" href="#">
          <span class="repo">Featured Projects</span>
          <span class="desc">按 ★·fork·新鲜度加权的项目热力图</span>
        </a>
      </div>
    </aside>
    <div class="gh-readme">
      <div class="gh-readme-hd">
        <span class="mono" id="pv-readme-name">Weidows / README.md</span>
        <span class="tag">Profile</span>
      </div>
      <div class="gh-box">
        <div class="inner">
          <div class="stage" id="pv-stage">
            <div class="overlay" id="pv-overlay"></div>
          </div>
        </div>
        <div class="gh-projects" id="pv-projects"></div>
        <p class="pv-hint">
          README 内容宽 <b>846px</b>（896 减去两侧 24px padding），GitHub 对图片施加
          <code style="font-family:ui-monospace,monospace">max-width:100%</code>。
          地图原生 <b id="pv-dims">—</b>
          <span id="pv-scale-note"></span>
        </p>
      </div>
    </div>
  </div>
</div>

<script>
const S = {
  config:null, pool:[], layout:null, meta:{},
  selected:null,        // repo whose editor is open
  poolSort:'weight',
  poolOwner:null,       // null until config arrives, then defaults to the user
  dragRepo:null, dragFromPool:false,
};

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g,
  (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const shortName = (repo) => repo.split('/')[1] || repo;
const ownerOf = (repo) => repo.split('/')[0] || '';

let toastTimer = null;
function toast(msg, kind) {
  const el = $('toast');
  el.textContent = msg;
  el.className = 'toast show' + (kind ? ' ' + kind : '');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.className = 'toast'; }, 3400);
}

async function api(path, body) {
  const opt = body === undefined ? {} : {
    method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body),
  };
  const r = await fetch(path, opt);
  const data = await r.json().catch(() => ({error:'invalid JSON response'}));
  if (!r.ok) throw new Error(data.error || ('HTTP ' + r.status));
  return data;
}

/* ================= stage sizing ================= */

/* The exported SVG grows taller as tiles are added (fixed 846 width). In the
   editor we still fit it inside the column so the layout stays put and the left
   side never scrolls — the real output size is shown in the top bar instead.
   Done in JS because the container's available height isn't known to CSS until
   layout, and any width/height mismatch would distort the map and desync the
   hit-boxes sitting on top of it. */
function fitStage() {
  const left = document.querySelector('.left');
  const stage = $('stage');
  if (!left || !stage) return;
  const cs = getComputedStyle(left);
  const availW = left.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
  const availH = left.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
  if (availW <= 0 || availH <= 0) return;
  const L = S.layout || {w: 846, h: 580};
  const ratio = (L.w || 846) / (L.h || 580);
  const w = Math.min(availW, availH * ratio);
  stage.style.width = Math.floor(w) + 'px';
  stage.style.height = Math.floor(w / ratio) + 'px';
  // The map is usually drawn larger than its 846px design width. The SVG text
  // scales with it, but HTML overlays (group headers) would stay at their CSS
  // size and end up looking undersized — expose the factor so they can match.
  const scale = w / (L.w || 846);
  stage.style.setProperty('--map-scale', scale.toFixed(4));
  S.mapScale = scale;
}

let fitTimer = null;
function scheduleFit() {
  clearTimeout(fitTimer);
  fitTimer = setTimeout(fitStage, 60);
}
window.addEventListener('resize', scheduleFit);

/* ================= state ================= */

function applyState(st, opts) {
  opts = opts || {};
  if (st.config) S.config = st.config;
  if (st.pool) S.pool = st.pool;
  if (st.layout) S.layout = st.layout;
  if (S.layout && S.layout.date) S.renderedDate = S.layout.date;
  if (st.markdown) S.markdown = st.markdown;
  if (st.meta) {
    if (st.meta.items) { S.meta = {}; for (const it of st.meta.items) S.meta[it.repo] = it; }
    if (st.meta.note) {
      const err = /失败|error/i.test(st.meta.note);
      toast(st.meta.note, err ? 'err' : 'ok');
    }
  }
  if (st.svg) {
    const stage = $('stage');
    const old = stage.querySelector('svg');
    if (old) old.remove();
    stage.insertAdjacentHTML('afterbegin', st.svg);
  }
  if (S.selected && !S.config.projects.some(p => p.repo === S.selected)) {
    S.selected = null; closeEditor();
  }
  renderAll();
  if (S.selected) openEditor(S.selected, true);
  scheduleFit();
}

function renderAll() {
  renderOverlay();
  renderPool();
}

/* ================= group helpers ================= */

/* Groups are manipulated entirely on the map now: the region header is the
   drag target, and clicking it turns into an inline rename box. The old
   horizontal chip bar is gone, so this only renders the "new group" affordance
   into the stage's overlay (see renderGroupChrome). */

function addGroup(name) {
  name = (name || '').trim();
  if (!name) return false;
  if (S.config.groups.some(g => g.name === name)) { toast('分组已存在', 'err'); return false; }
  S.config.groups.push({ name });
  renderAll(); preview();
  return true;
}

function renameGroup(oldName, newName) {
  newName = (newName || '').trim();
  if (!newName || newName === oldName) return;
  if (S.config.groups.some(g => g.name === newName)) {
    toast('分组已存在', 'err');
    return;
  }
  const g = S.config.groups.find(x => x.name === oldName);
  if (!g) return;
  g.name = newName;
  // every project in that group must follow the rename
  S.config.projects.forEach(p => { if (p.group === oldName) p.group = newName; });
  if (S.selected && (S.config.projects.find(p => p.repo === S.selected) || {}).group === newName) {
    closeEditor();           // its group label changed; reopen cleanly
  }
  toast(`已重命名为「${newName}」`, 'ok');
  renderAll(); preview();
}

function deleteGroup(name) {
  S.config.groups = S.config.groups.filter(g => g.name !== name);
  S.config.projects.forEach(p => { if (p.group === name) p.group = ''; });
  renderAll(); preview();
}

/* Swap the group title for an input in place. Enter/blur commits, Escape
   cancels — the surrounding header keeps its size so the map doesn't jump. */
function startRename(headEl, oldName) {
  if (!headEl || headEl.classList.contains('renaming')) return;
  headEl.classList.add('renaming');
  const label = headEl.querySelector('.gt');
  const input = document.createElement('input');
  input.className = 'grename';
  input.value = oldName;
  input.maxLength = 16;
  label.replaceWith(input);
  input.focus();
  input.select();

  let done = false;
  const finish = (commit) => {
    if (done) return;
    done = true;
    const v = input.value.trim();
    if (commit && v && v !== oldName) renameGroup(oldName, v);
    else { renderOverlay(); }
  };
  input.onkeydown = (e) => {
    e.stopPropagation();
    if (e.key === 'Enter') finish(true);
    else if (e.key === 'Escape') finish(false);
  };
  input.onblur = () => finish(true);
  input.onmousedown = (e) => e.stopPropagation();
}

/* ================= treemap overlay ================= */

/* Builds the transparent hit-boxes that sit on top of the rendered SVG. Called
   for the editor stage and for the 1:1 GitHub preview, so editing keeps working
   in both. The boxes are positioned in the SVG's own coordinate space (percent
   of layout width/height), so they line up in either container as long as that
   container has the SVG's aspect ratio. */
function renderOverlayInto(ov, opts) {
  opts = opts || {};
  const L = S.layout;
  if (!ov) return;
  if (!L || !L.tiles) { ov.innerHTML = ''; return; }

  const { w: SW, h: SH } = L;
  const pct = (v, total) => (v / total * 100).toFixed(3) + '%';
  const order = S.config.projects.map(p => p.repo);
  const readonly = !!opts.readonly;
  const emptyMsg = opts.emptyMsg;

  let html = '';
  for (const [repo, t] of Object.entries(L.tiles)) {
    const p = S.config.projects.find(x => x.repo === repo);
    const m = S.meta[repo] || {};
    const tip = `${repo}\n★${m.stars ?? '?'} · fork ${m.forks ?? '?'}`
      + (m.lang ? ` · ${m.lang}` : '') + (p && p.group ? `\n分组：${p.group}` : '')
      + '\n点击编辑 · 拖动换位';
    html += `<div class="hit${repo === S.selected ? ' sel' : ''}"`
      + `${readonly ? '' : ' draggable="true"'} data-repo="${esc(repo)}"`
      + ` title="${esc(tip)}"`
      + ` style="left:${pct(t.x, SW)};top:${pct(t.y, SH)};`
      + `width:${pct(t.w, SW)};height:${pct(t.h, SH)}"></div>`;
  }

  // Empty groups have a region in the layout but no tiles, so give that region
  // an invisible drop zone: it's the target that makes a new group usable by
  // drag alone (no group dropdown in the editor).
  if (!readonly) {
    const filled = new Set(S.config.projects.map(p => p.group || ''));
    for (const r of (L.regions || [])) {
      if (!r.group || filled.has(r.group)) continue;
      html += `<div class="dropzone" data-drop-group="${esc(r.group)}"`
        + ` title="拖入项目加入「${esc(r.group)}」"`
        + ` style="left:${pct(r.x, SW)};top:${pct(r.y, SH)};`
        + `width:${pct(r.w, SW)};height:${pct(r.h, SH)}"></div>`;
    }
  }

  // Group headers live on the map: each region gets a clickable title bar that
  // also acts as a drop target. The SVG draws the label too, so hide the SVG
  // text under it (it's there for the exported file, not the editor overlay).
  if (!readonly) {
    for (const r of (L.regions || [])) {
      if (!r.group) continue;
      // Two elements per group: a full-width invisible strip that captures drops
      // across the whole header band, and a compact pill on top of it that holds
      // the label and the rename/delete buttons. Splitting them keeps the hover
      // highlight tight around the text instead of lighting up the full width.
      html += `<div class="gdrop" data-ghead="${esc(r.group)}"`
        + ` style="left:${pct(r.x, SW)};top:${pct(r.y, SH)};`
        + `width:${pct(r.w, SW)};height:${pct(20, SH)}"`
        + ` title="拖项目到这里加入「${esc(r.group)}」"></div>`
        + `<div class="ghead" data-ghead-pill="${esc(r.group)}"`
        + ` style="left:${pct(r.x + 6, SW)};top:${pct(r.y, SH)}">`
        + `<span class="gt" title="点击重命名">${esc(r.group)}</span>`
        + `<span class="gx" data-rename="${esc(r.group)}" title="重命名">✎</span>`
        + `<span class="gx del" data-del="${esc(r.group)}" title="删除分组">×</span>`
        + `</div>`;
    }
  }

  if (!order.length && emptyMsg) {
    html += `<div class="empty-stage">${emptyMsg}</div>`;
  }
  ov.innerHTML = html;

  // group header interactions: drag-to-join lives on the full-width strip,
  // rename/delete live on the compact pill above it
  ov.querySelectorAll('.gdrop').forEach((el) => {
    const group = el.dataset.ghead;
    el.addEventListener('dragover', (e) => {
      if (!S.dragRepo) return;
      e.preventDefault();
      e.dataTransfer.dropEffect = dragEffect();
      el.classList.add('over');
    });
    el.addEventListener('dragleave', () => el.classList.remove('over'));
    el.addEventListener('drop', (e) => {
      e.preventDefault();
      e.stopPropagation();
      el.classList.remove('over');
      const src = S.dragRepo;
      if (!src) return;
      assignGroup(src, group, true);
      clearDropMarks();
      S.dragRepo = null;
      $('stage').classList.remove('drop-hot');
    });
  });
  ov.querySelectorAll('[data-ghead-pill]').forEach((pill) => {
    const group = pill.dataset.gheadPill;
    pill.querySelector('.gt').addEventListener('click', (e) => {
      e.stopPropagation();
      startRename(pill, group);
    });
  });
  ov.querySelectorAll('[data-del]').forEach((b) => {
    b.onclick = (e) => { e.stopPropagation(); deleteGroup(b.dataset.del); };
  });
  ov.querySelectorAll('[data-rename]').forEach((b) => {
    b.onclick = (e) => {
      e.stopPropagation();
      startRename(b.closest('.ghead'), b.dataset.rename);
    };
  });
  // wire the empty-group zones: dropping a tile here moves it into that group
  ov.querySelectorAll('[data-drop-group]').forEach((el) => {
    const group = el.dataset.dropGroup;
    el.addEventListener('dragover', (e) => {
      if (!S.dragRepo) return;
      e.preventDefault();
      e.dataTransfer.dropEffect = dragEffect();
      el.classList.add('over');
    });
    el.addEventListener('dragleave', () => el.classList.remove('over'));
    el.addEventListener('drop', (e) => {
      e.preventDefault();
      e.stopPropagation();
      el.classList.remove('over');
      const src = S.dragRepo;
      if (!src) return;
      assignGroup(src, group, true);
      clearDropMarks();
      S.dragRepo = null;
      $('stage').classList.remove('drop-hot');
    });
  });

  ov.querySelectorAll('.hit').forEach((el) => {
    const repo = el.dataset.repo;

    el.addEventListener('click', () => { S.selected = repo; renderOverlay(); openEditor(repo); });

    if (readonly) return;

    el.addEventListener('dragstart', (e) => {
      S.dragRepo = repo; S.dragFromPool = false;
      el.classList.add('drag');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', repo);
      $('stage').classList.add('drop-hot');
    });
    el.addEventListener('dragend', () => {
      el.classList.remove('drag');
      S.dragRepo = null;
      clearDropMarks();
      $('stage').classList.remove('drop-hot');
    });

    // dropping another tile onto this one: reorder + adopt its group
    el.addEventListener('dragover', (e) => {
      if (!S.dragRepo || S.dragRepo === repo) return;
      e.preventDefault();
      e.dataTransfer.dropEffect = dragEffect();
      const r = el.getBoundingClientRect();
      const after = (e.clientX - r.left) > r.width / 2;
      clearDropMarks();
      el.classList.add(after ? 'ins-after' : 'ins-before');
    });
    el.addEventListener('dragleave', () => {
      el.classList.remove('ins-before', 'ins-after');
    });
    el.addEventListener('drop', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const src = S.dragRepo;
      if (!src || src === repo) return;
      const r = el.getBoundingClientRect();
      const after = (e.clientX - r.left) > r.width / 2;
      const targetGroup = (S.config.projects.find(x => x.repo === repo) || {}).group || '';
      moveBeforeAfter(src, repo, after, targetGroup);
      clearDropMarks();
      S.dragRepo = null;
      $('stage').classList.remove('drop-hot');
    });
  });
}

function renderOverlay() {
  renderOverlayInto($('overlay'), {
    emptyMsg: '<div>画面还是空的</div><div>从右侧候选池把仓库拖进来</div>',
  });
  // every overlay refresh also pumps the preview, so it stays truthful while
  // open (boost/group/key-point edits all funnel through here)
  syncPreview();
}

function clearDropMarks() {
  document.querySelectorAll('.hit').forEach(h =>
    h.classList.remove('ins-before', 'ins-after'));
}

/* A drag started in the pool sets effectAllowed='copy' while one started on a
   tile sets 'move'. If a drop target then asks for a different effect, the
   browser refuses the drop and the drag silently does nothing — which is
   exactly how dragging a candidate onto the map used to fail. Every dragover
   handler therefore announces the effect that matches the current source. */
function dragEffect() {
  return S.dragFromPool ? 'copy' : 'move';
}

/* Drop onto empty map area: append, ungrouped. */
$('stage').addEventListener('dragover', (e) => {
  if (!S.dragRepo) return;
  e.preventDefault();
  e.dataTransfer.dropEffect = dragEffect();
});
$('stage').addEventListener('drop', (e) => {
  const src = S.dragRepo;
  if (!src) return;
  e.preventDefault();
  const cfg = S.config;
  const from = cfg.projects.findIndex(p => p.repo === src);
  let item;
  if (from >= 0) item = cfg.projects.splice(from, 1)[0];
  else {
    const src0 = S.pool.find(r => r.repo === src) || {};
    item = {repo:src, boost:1.0, group:'', key_points:src0.desc ? [src0.desc.slice(0,60)] : []};
  }
  item.group = '';
  cfg.projects.push(item);
  S.dragRepo = null;
  $('stage').classList.remove('drop-hot');
  renderAll(); preview();
});

/* ================= ordering helpers ================= */

function moveBeforeAfter(srcRepo, dstRepo, after, group) {
  const arr = S.config.projects;
  const from = arr.findIndex(p => p.repo === srcRepo);
  let item;
  if (from >= 0) item = arr.splice(from, 1)[0];
  else {
    const src = S.pool.find(r => r.repo === srcRepo) || {};
    item = {repo:srcRepo, boost:1.0, group:'',
            key_points:src.desc ? [src.desc.slice(0,60)] : []};
  }
  item.group = group || '';
  let idx = arr.findIndex(p => p.repo === dstRepo);
  if (idx < 0) idx = arr.length;
  arr.splice(after ? idx + 1 : idx, 0, item);
  renderAll(); preview();
}

function assignGroup(repo, group, append) {
  const arr = S.config.projects;
  let item = arr.find(p => p.repo === repo);
  if (!item) {
    const src = S.pool.find(r => r.repo === repo) || {};
    item = {repo, boost:1.0, group:'',
            key_points:src.desc ? [src.desc.slice(0,60)] : []};
    arr.push(item);
  }
  item.group = group || '';
  if (append) {
    // move it to the end of its group so the group reads as a contiguous run
    const i = arr.indexOf(item);
    arr.splice(i, 1);
    let last = -1;
    arr.forEach((p, k) => { if ((p.group || '') === (group || '')) last = k; });
    arr.splice(last + 1, 0, item);
  }
  renderAll(); preview();
}

/* ================= tile editor ================= */

function openEditor(repo, keepPos) {
  const p = S.config.projects.find(x => x.repo === repo);
  if (!p) return closeEditor();
  const m = S.meta[repo] || {};
  const kps = p.key_points || [];

  const box = $('editor');
  box.innerHTML = `
    <div class="hd">
      <span class="rp"><span class="o">${esc(ownerOf(repo))}/</span>${esc(shortName(repo))}</span>
      <span class="x" id="ed-close">✕</span>
    </div>
    <div class="stats">
      <span><i>★</i> ${m.stars ?? '—'} <i>fork</i> ${m.forks ?? '—'}</span>
      <span>${esc(m.lang || '—')}</span>
      <span><i>w</i> ${m.weight != null ? m.weight.toFixed(1) : '—'}</span>
      <span><i>面积</i> ${m.share != null ? (m.share*100).toFixed(1)+'%' : '—'}</span>
      <span>${esc(m.pushed || '')}</span>
    </div>
    <label>加权 boost</label>
    <input type="number" id="ed-boost" value="${p.boost}" step="0.1" min="0.1" max="100"
      title="0 < boost ≤ 100，越大方块越大">
    <label>要点（卡片上最多 3 条）</label>
    <div class="kp">${[0,1,2].map(k =>
      `<input data-kp="${k}" value="${esc(kps[k] || '')}"
        placeholder="${k===0?'主要亮点':'要点 '+(k+1)+'（可选）'}">`).join('')}</div>
    <div class="row">
      <button class="sm danger" id="ed-remove">移出画面</button>
      <span class="hintx" style="margin:0">分组请拖到顶部标签或图里的空组框</span>
    </div>`;
  box.classList.add('show');

  if (!keepPos) {
    // Anchor beside the tile. In preview mode the tile lives in the 1:1 stage
    // (scrolled inside .pv), so the editor must follow that box instead.
    const L = S.layout && S.layout.tiles && S.layout.tiles[repo];
    const inPreview = $('pv').classList.contains('on');
    const stage = (inPreview ? $('pv-stage') : $('stage')).getBoundingClientRect();
    const BW = box.offsetWidth || 310;
    const BH = box.offsetHeight || 340;
    const M = 12;
    let x = 40, y = 80;
    if (L) {
      const sx = stage.width / S.layout.w, sy = stage.height / S.layout.h;
      const tRight = stage.left + (L.x + L.w) * sx;
      const tLeft = stage.left + L.x * sx;
      const tTop = stage.top + L.y * sy;
      x = (tRight + M + BW <= innerWidth) ? tRight + M : tLeft - BW - M;
      y = tTop;
    }
    x = Math.min(Math.max(M, x), Math.max(M, innerWidth - BW - M));
    y = Math.min(Math.max(M, y), Math.max(M, innerHeight - BH - M));
    box.style.left = Math.round(x) + 'px';
    box.style.top = Math.round(y) + 'px';
  }

  $('ed-close').onclick = closeEditor;
  $('ed-boost').onchange = (e) => {
    const v = parseFloat(e.target.value);
    if (!isFinite(v) || v <= 0 || v > 100) { toast('boost 需在 (0, 100]', 'err'); return; }
    p.boost = v; renderAll(); preview();
  };
  box.querySelectorAll('[data-kp]').forEach(inp => {
    inp.onchange = () => {
      const arr = (p.key_points ||= []);
      while (arr.length < 3) arr.push('');
      arr[+inp.dataset.kp] = inp.value.trim();
      p.key_points = arr.filter(Boolean);
      renderOverlay(); preview();
    };
  });
  $('ed-remove').onclick = () => {
    const i = S.config.projects.findIndex(x => x.repo === repo);
    if (i >= 0) S.config.projects.splice(i, 1);
    closeEditor(); renderAll(); preview();
  };
}

function closeEditor() {
  S.selected = null;
  $('editor').classList.remove('show');
  renderOverlay();
}

document.addEventListener('mousedown', (e) => {
  const box = $('editor');
  if (!box.classList.contains('show')) return;
  if (box.contains(e.target)) return;
  if (e.target.closest('.hit')) return;
  closeEditor();
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    // Escape backs out one level: editor popover first, then preview mode
    if ($('editor').classList.contains('show')) closeEditor();
    else if ($('pv').classList.contains('on')) setPreview(false);
  }
});

/* ================= candidate pool ================= */

function renderPool() {
  const cfg = S.config;
  const q = $('pool-search').value.trim().toLowerCase();
  const picked = new Set(cfg.projects.map(p => p.repo));

  const owners = [];
  if (cfg.user) owners.push({key:'user', label:'@' + cfg.user});
  for (const o of (cfg.orgs || [])) owners.push({key:o, label:o});

  // no "all" chip: the personal account is the default view
  if (!S.poolOwner || !owners.some(o => o.key === S.poolOwner)) {
    S.poolOwner = owners.length ? owners[0].key : 'user';
  }

  const countFor = (key) => {
    if (key === 'user') return S.pool.filter(r => !r.from_org).length;
    return S.pool.filter(r => r.owner === key).length;
  };
  const REFRESH_ICON = '<svg viewBox="0 0 16 16" width="11" height="11" fill="currentColor" aria-hidden="true"><path d="M8 3a5 5 0 1 0 4.9 6h-1.6A3.4 3.4 0 1 1 8 4.6v1.6L10.8 3.6 8 1v2z"/></svg>';
  const chip = (key, label) => {
    const on = S.poolOwner === key ? ' on' : '';
    // per-source refresh: pulling one org is 1-3 requests instead of
    // 1 + N orgs, which is what keeps an unauthenticated session alive
    return `<span class="fchip${on}" data-owner="${esc(key)}">${esc(label)}`
      + `<span class="c">${countFor(key)}</span>`
      + `<button class="orefresh" data-refresh="${esc(key)}"`
      + ` title="只刷新 ${esc(label)} 的仓库">${REFRESH_ICON}</button></span>`;
  };
  $('pool-filter').innerHTML = '<span class="lbl">来源</span>'
    + owners.map(o => chip(o.key, o.label)).join('');
  $('pool-filter').querySelectorAll('[data-owner]').forEach(el => {
    el.onclick = () => { S.poolOwner = el.dataset.owner; renderPool(); };
  });
  $('pool-filter').querySelectorAll('[data-refresh]').forEach(el => {
    el.onclick = (e) => { e.stopPropagation(); doRefresh([el.dataset.refresh]); };
  });

  let rows = S.pool.slice();
  if (S.poolOwner === 'user') rows = rows.filter(r => !r.from_org);
  else rows = rows.filter(r => r.owner === S.poolOwner);
  if (q) rows = rows.filter(r => r.repo.toLowerCase().includes(q));

  if (S.poolSort === 'weight') rows.sort((a,b) => b.weight - a.weight);
  else if (S.poolSort === 'name') rows.sort((a,b) => a.repo.localeCompare(b.repo));
  else if (S.poolSort === 'pushed') rows.sort((a,b) => b.pushed.localeCompare(a.pushed));
  else if (S.poolSort === 'free') rows.sort((a,b) => (picked.has(a.repo)?1:0) - (picked.has(b.repo)?1:0));

  $('pool-list').innerHTML = rows.length ? rows.map(r => {
    const on = picked.has(r.repo);
    const org = r.from_org ? '<span class="org">org</span>' : '';
    const stats = `★ ${r.stars} · F ${r.forks}`;
    return `<div class="prow" draggable="true" data-repo="${esc(r.repo)}"
        title="${esc(r.repo)}\n★${r.stars} · fork ${r.forks}`
      + `${r.lang ? ' · ' + esc(r.lang) : ''}\n拖到右边画面里添加${on ? '\n（已在画面中）' : ''}">
      <span class="nm"><span class="o">${esc(r.owner)}/</span>${esc(shortName(r.repo))}${org}</span>
      <span class="stats">${esc(stats)}</span>
      <span class="meta">${on ? '已加入' : r.weight.toFixed(1)}</span>
      <button class="add sm" data-add="${esc(r.repo)}"
        title="${on ? '已在画面中，再点会移除' : '添加到末尾'}">${on ? '−' : '+'}</button>
    </div>`;
  }).join('') : `<div class="pool-empty">没有匹配的候选仓库<br>
      点上方「↻」按白名单拉取</div>`;

  $('pool-list').querySelectorAll('.prow').forEach(row => {
    const repo = row.dataset.repo;

    row.addEventListener('dragstart', (e) => {
      S.dragRepo = repo; S.dragFromPool = true;
      row.classList.add('drag');
      e.dataTransfer.effectAllowed = 'copy';
      e.dataTransfer.setData('text/plain', repo);
      $('stage').classList.add('drop-hot');
    });
    row.addEventListener('dragend', () => {
      row.classList.remove('drag');
      S.dragRepo = null;
      clearDropMarks();
      $('stage').classList.remove('drop-hot');
    });
  });

  $('pool-list').querySelectorAll('[data-add]').forEach(btn => {
    btn.onclick = (e) => {
      e.stopPropagation();
      const repo = btn.dataset.add;
      const i = S.config.projects.findIndex(p => p.repo === repo);
      if (i >= 0) {
        S.config.projects.splice(i, 1);
      } else {
        const src = S.pool.find(r => r.repo === repo) || {};
        S.config.projects.push({
          repo, boost:1.0, group:'',
          key_points: src.desc ? [src.desc.slice(0,60)] : [],
        });
      }
      renderAll(); preview();
    };
  });
}

/* ================= actions ================= */

let previewTimer = null;
function preview() {
  clearTimeout(previewTimer);
  previewTimer = setTimeout(async () => {
    try {
      const st = await api('/api/svg', S.config);
      if (st.svg) {
        const stage = $('stage');
        const old = stage.querySelector('svg');
        if (old) old.remove();
        stage.insertAdjacentHTML('afterbegin', st.svg);
      }
      if (st.layout) S.layout = st.layout;
      if (S.layout && S.layout.date) S.renderedDate = S.layout.date;
      if (st.markdown) S.markdown = st.markdown;
      if (st.meta && st.meta.items) {
        S.meta = {};
        for (const it of st.meta.items) S.meta[it.repo] = it;
      }
      // the canvas may have grown or shrunk with the tile count, so the stage
      // size has to be recomputed here too
      scheduleFit();
      renderOverlay();
      if (S.selected) openEditor(S.selected, true);
    } catch (e) {
      toast('预览失败：' + e.message, 'err');
    }
  }, 220);
}

/* Refresh one source (or all, when no owners are given). The old global ↻
   button is gone; each source chip carries its own. */
async function doRefresh(owners) {
  const only = owners && owners.length ? owners : null;
  const oref = only
    ? document.querySelector(`[data-refresh="${CSS.escape(only[0])}"]`)
    : null;
  if (oref && oref.disabled) return;
  if (oref) { oref.disabled = true; oref.classList.add('busy'); }
  const n0 = S.pool.length;
  try {
    const st = await api('/api/refresh', only ? { owners: only } : {});
    applyState(st);
    const added = Math.max(0, (st.pool || []).length - n0);
    if (st.meta?.note) toast(st.meta.note, /限流|失败/.test(st.meta.note) ? 'err' : 'ok');
    else toast(added ? `新增 ${added} 个候选` : '候选已是最新', 'ok');
  } catch (e) {
    toast('刷新失败：' + e.message, 'err');
  } finally {
    if (oref) { oref.disabled = false; oref.classList.remove('busy'); }
  }
}

async function doSave() {
  try { applyState(await api('/api/config', S.config)); }
  catch (e) { toast('保存失败：' + e.message, 'err'); }
}

async function doExport() {
  try {
    const st = await api('/api/export', S.config);
    if (st.svg) {
      const stage = $('stage');
      const old = stage.querySelector('svg');
      if (old) old.remove();
      stage.insertAdjacentHTML('afterbegin', st.svg);
    }
    if (st.layout) S.layout = st.layout;
    if (S.layout && S.layout.date) S.renderedDate = S.layout.date;
    if (st.markdown) S.markdown = st.markdown;
    scheduleFit();
    renderOverlay();
    toast(st.meta?.note || '已导出', 'ok');
  } catch (e) { toast('导出失败：' + e.message, 'err'); }
}

/* ================= GitHub profile preview ================= */

/* Renders the same SVG inside a faithful copy of GitHub's README card, so the
   map is judged the way the profile actually shows it. GitHub's content column
   is 846px wide and README images are capped at max-width:100%, so a native
   SVG is generated at exactly 846px so GitHub renders it 1:1. Hit boxes are
   mirrored read-only: clicking still opens the editor. */
function syncPreview() {
  const pv = $('pv');
  // only refresh while fully open; during the close animation the panel is
  // display:block but on its way out, and re-rendering it would flicker
  if (!pv.classList.contains('on')) return;

  const L = S.layout || {};
  const svg = $('stage').querySelector('svg');

  // drop a copy of the rendered SVG into the preview stage
  const stage = $('pv-stage');
  stage.querySelectorAll('svg').forEach(s => s.remove());
  if (svg) {
    const clone = svg.cloneNode(true);
    clone.removeAttribute('style');
    stage.insertBefore(clone, stage.firstChild);
  }

  const natW = L.w || 846, natH = L.h || 580;
  $('pv-size').textContent = natW + '×' + natH;
  $('pv-dims').textContent = natW + '×' + natH;

  // GitHub's usable README width is fixed at 846px (896 box - 2*24 padding - 2 border).
  // Anything wider is scaled down by the browser; say so next to the size.
  const CONTENT_W = 846;
  const note = $('pv-scale-note');
  if (note) {
    if (natW > CONTENT_W) {
      note.className = 'warn';
      note.textContent = `　→ GitHub 上会缩放到 ${CONTENT_W}px（×${(CONTENT_W / natW).toFixed(3)}）`;
    } else {
      note.className = '';
      note.textContent = `　→ 1:1 原尺寸显示`;
    }
  }

  const cfg = S.config || {};
  const user = cfg.user || 'Weidows';
  $('pv-name').textContent = user;
  $('pv-login').textContent = user;
  $('pv-avatar').textContent = user.slice(0, 1).toUpperCase();
  $('pv-readme-name').textContent = user + ' / README.md';
  $('pv-link').textContent = 'github.com/' + user;

  const projects = cfg.projects || [];
  $('pv-repos').textContent = String(projects.length);
  // stars come from the rendered meta, summed across the tiles on the map
  const starTotal = projects.reduce(
    (sum, p) => sum + ((S.meta[p.repo] || {}).stars || 0), 0);
  $('pv-stars').textContent = String(starTotal);

  renderOverlayInto($('pv-overlay'), { readonly: true });
  renderProjectList();
}

/* The list under the image: GitHub-style bold group headings + a real <ul>
   with one linked entry per project. Built from the same config order as the
   map, so the two always agree. Clicking a name opens that project's editor
   instead of navigating — this is a preview of the README, not the README. */
function renderProjectList() {
  const box = $('pv-projects');
  if (!box) return;
  const cfg = S.config || {};
  const projects = cfg.projects || [];
  if (!projects.length) { box.innerHTML = ''; return; }

  const groups = (cfg.groups || []).map(g => g.name);
  const buckets = new Map(groups.map(n => [n, []]));
  const orphans = [];
  for (const p of projects) {
    const name = p.group || '';
    (buckets.has(name) ? buckets.get(name) : orphans).push(p);
  }

  const entry = (p) => {
    const m = S.meta[p.repo] || {};
    const slug = shortName(p.repo);
    const stats = [];
    if (m.stars) stats.push('★ ' + m.stars);
    if (m.forks) stats.push('fork ' + m.forks);
    if (m.lang && m.lang !== '—') stats.push(m.lang);
    if (m.share != null) stats.push((m.share * 100).toFixed(1) + '%');
    const kps = (p.key_points || []).map(k => esc(k)).join(' / ');
    return `<li><a href="https://github.com/${esc(p.repo)}" data-repo="${esc(p.repo)}"`
      + ` title="点击编辑">${esc(slug)}</a>`
      + (stats.length ? ` <span class="meta">— ${esc(stats.join(' · '))}</span>` : '')
      + (kps ? `<span class="kp">： ${kps}</span>` : '')
      + `</li>`;
  };

  let html = '';
  for (const name of groups) {
    const members = buckets.get(name) || [];
    if (!members.length) continue;
    html += `<h3>${esc(name)}</h3><ul>${members.map(entry).join('')}</ul>`;
  }
  if (orphans.length) {
    html += `<ul>${orphans.map(entry).join('')}</ul>`;
  }
  box.innerHTML = html;

  // clicking a name opens its editor (keeps the preview interactive)
  box.querySelectorAll('a[data-repo]').forEach((a) => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      S.selected = a.dataset.repo;
      renderOverlay();
      openEditor(a.dataset.repo);
    });
  });
}

function setPreview(on) {
  const pv = $('pv');
  const btn = $('btn-preview');
  btn.classList.toggle('on', on);
  document.body.classList.toggle('previewing', on);

  if (on) {
    btn.textContent = '退出预览';
    // Two frames so the browser paints the display:block state before the
    // opacity/transform transition runs; otherwise it snaps in with no animation.
    pv.classList.remove('closing');
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        pv.classList.add('on');
        syncPreview();   // must run after 'on' is set — syncPreview() guards on it
        pv.scrollTop = 0;
      });
    });
  } else {
    if (!pv.classList.contains('on')) return;
    pv.classList.add('closing');
    pv.classList.remove('on');
    btn.textContent = 'Preview';
    setTimeout(() => {
      pv.classList.remove('closing');
      scheduleFit();
    }, 260);
  }
}

function togglePreview() {
  setPreview(!$('pv').classList.contains('on'));
}

/* ================= boot ================= */

$('btn-preview').onclick = togglePreview;
$('btn-preview-close').onclick = () => setPreview(false);
$('btn-save').onclick = doSave;
$('btn-export').onclick = doExport;

/* New group lives in the top bar: Enter or + creates it, and the map picks up
   a fresh empty region to drop projects into. */
const newGroupIn = $('new-group');
const submitNewGroup = () => { if (addGroup(newGroupIn.value)) newGroupIn.value = ''; };
$('btn-add-group').onclick = submitNewGroup;
newGroupIn.onkeydown = (e) => {
  if (e.key === 'Enter') submitNewGroup();
  else if (e.key === 'Escape') newGroupIn.blur();
};
$('pool-search').oninput = renderPool;
$('btn-pool-sort').onclick = () => {
  const order = ['weight', 'name', 'pushed', 'free'];
  S.poolSort = order[(order.indexOf(S.poolSort) + 1) % order.length];
  $('btn-pool-sort').textContent =
    {weight:'权重 ↓', name:'名称 ↑', pushed:'push ↓', free:'未加入优先'}[S.poolSort];
  renderPool();
};
window.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 's') { e.preventDefault(); doSave(); }
});

api('/api/state').then(st => applyState(st)).catch(e => {
  $('stage').insertAdjacentHTML('beforeend',
    `<div class="empty-stage" style="color:#dfa08a">加载失败：${esc(e.message)}</div>`);
});
</script>
</body></html>
"""
