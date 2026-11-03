# github-profile-dashboard

GitHub profile 用的**项目热力 Treemap**：精选项目，方块面积随
`★ / fork × 新鲜度` 动态加权 — 越重要的项目越大，越冷的越小。
宽度固定 846px（贴合 GitHub README 内容区，不触发缩放），项目多了画布自动变高。

风格：暗底线框热力图（细描边热度色，muted 暗色系），字体为得意黑。
卡片上的 star / fork 用 **GitHub octicon 矢量图标**（金色 `#f8d866`）配灰色数字，
语言用**彩色圆点**（GitHub linguist 配色），与 profile 里的仓库卡片一致。

## 尺寸（宽度贴合 GitHub，高度自适应）

- GitHub README 的**可用内容宽度是 846px**（896 的卡片 − 两侧各 24px padding − 2px 边框，
  实测自真实 profile）。SVG 宽度就取 **846**，填满这个区域、不触发 `max-width:100%`
  缩放——1 个 CSS 像素对应 1 个 SVG 像素，文字边缘不会被重采样糊掉；
- **高度随项目数自动增长**，不平铺固定 600。10 个项目以内保持 846×580；
  超过后按 `n^0.6` 增长，避免每加一个项目就把所有方块压小：

  | 项目数 | 画布 |
  |---|---|
  | 1–10 | 846×580 |
  | 15 | 846×724 |
  | 20 | 846×849 |
  | 30 | 846×1067 |
  | 60 | 846×1588 |

  30 个项目的平均方块面积仍是 10 个项目时的 65%，不会碎到读不出字。
- 纯静态 SVG（无 JS），profile README 可直接渲染，hover 有 `<title>` 详情；
- 没有页脚横条：`updated` 日期挪到标题区右侧，`area ≈ weight^0.6` 只出现在编辑器顶栏；
- 编辑器里地图会等比缩放到可视区域，左侧不滚动；顶栏显示**导出尺寸**，
  高度超过 600 时会带 `↑` 标记；
- `preview.html` 只是本地查验用，不推上去。

## 用法

```bash
python generate.py            # 拉 GitHub API 实时数据 -> dashboard.svg + preview.html
python generate.py --offline  # 用 cache.json 离线重排（调样式/文案时用，不耗 API 配额）
python generate.py --serve    # 启动本地编辑器（刷新候选 / 分组 / 拖拽排序）
```

## 本地编辑器

```bash
python generate.py --serve            # 默认 http://127.0.0.1:8765/，自动开浏览器
python generate.py --serve --port 9000 --no-open
```

只监听 `127.0.0.1`，不会暴露到局域网。

界面分成两块：**左边是候选池，右边是可交互的 treemap**。没有单独的「已选列表」——
画面里的方块就是已选内容，直接点、直接拖。分组标签、`updated` 日期和面积公式都在顶栏，
地图按自身比例等比缩放填满剩余高度，不产生滚动条。

| 操作 | 说明 |
|---|---|
| **↻（每个来源 chip 上）** | **只刷新那一个来源**——个人或某个组织。拉一个组织只要 1–3 次请求；限流时用这个逐个补。没有「刷新全部」按钮，避免一发打满配额 |
| 点方块 | 弹出编辑器：改 boost、key-points，或移出画面（**分组只能拖拽**，编辑器里没有下拉） |
| 拖方块 → 另一个方块 | 换位置，并归到目标方块所在分组（左右半边决定插在它前面还是后面） |
| 拖方块 → 图上的**分组标题** | 把该方块加入那个分组；标题栏就是落点 |
| 点分组标题 | 就地变成输入框，改名后**组内所有项目跟着走**（`Enter` 提交，`Esc` 取消） |
| 分组标题右侧 `✎` / `×` | 重命名 / 删除分组（删除后组内项目回落「未分组」） |
| 画面右上角「新分组…」 | 新建分组，图上立即出现虚线占位框，可直接往里拖 |
| 拖候选池 → 画面 | 新增到末尾（未分组）；也可以直接拖到某个分组标题上 |
| 拖候选池 → 某个方块 | 新增并插到该方块旁边，同时继承它的分组 |
| 候选池 `+` / `−` | 快速添加 / 移除 |
| 候选池顶部 chips | 按来源过滤：个人 / 各个组织，带数量；默认选中个人，无「全部」项 |
| **保存配置** | 写回 `projects.json`（`Ctrl+S`） |
| **导出 SVG** | 写 `dashboard.svg` + `preview.html` + `dashboard.md` |
| **复制 README** | 把「图片 + 项目链接列表」整段复制到剪贴板 |
| **Preview** | 切换到 1:1 的 GitHub profile 仿真视图（详见下）；`Esc` 或「返回编辑器」退出 |

顶栏按钮顺序固定为 **复制 README · 导出 SVG · 保存配置 · Preview**。

### Preview 模式

点 **Preview** 会淡入一个仿 github.com 的 profile 页面。尺寸和配色是从真实
`github.com/Weidows` 上行量出来的，不是估的：

| 项目 | 真实值 | Preview |
|---|---|---|
| 画布背景 | `rgb(33,40,48)` | 同 |
| 边框 | `rgb(61,68,77)` | 同 |
| 正文 / muted 文字 | `rgb(209,215,224)` / `rgb(145,152,161)` | 同 |
| profile 布局总宽 | 1216px（296 + 24 + 896） | 同 |
| 侧栏 | 296px | 同 |
| 头像 | 296×296 圆形 | 同 |
| README 卡片 | 896px，`padding:24px` | 同 |
| **README 可用内容宽** | **846px** | 同 |

**最重要的一条**：GitHub 对 README 里的图片施加 `max-width:100%`，而内容区只有
846px。所以原生 880px 的 `dashboard.svg` 在真实 profile 上**会被缩放到 846px
（×0.961）**，并不是 1:1。Preview 忠实复现了这个压缩——底部的提示行会写出
「GitHub 上会缩放到 846px（×0.961）」，这样你看到的方块大小就是访客看到的大小。

（如果希望真正 1:1 不被缩放，把 `W` 从 880 改成 ≤846 即可，比如 800 或 840。）

侧栏复刻了 GitHub 的组成部分：头像、名字（600 字重）与登录名、bio、仓库数 / star 数、
`Edit profile` 按钮、地区与主页链接、Pinned 置顶卡片；README 区带 `Profile` 标签。

- 切换带淡入淡出 + 轻微位移动画，顶栏高度与编辑器一致（52px），切换时页面不跳动
- 预览中仍可**点击方块编辑**（boost / 分组 / 要点），改动实时反映在预览上
- 按钮文案会变成「退出预览」，`Esc` 也可以退出
- 布局宽度不足 1012px 时自动隐藏侧栏，只保留 README 内容

编辑器改动**实时预览但不落盘**，只有「保存配置」或「导出 SVG」才写文件。

### 组织白名单

`projects.json` 里的 `orgs` 是参与统计的组织列表：

```json
{
  "user": "Weidows",
  "orgs": ["u2sb", "Weidows-projects", "AierLab"],
  "projects": [ ... ]
}
```

刷新时会对每个组织调 `GET /orgs/<name>/repos`（最多 3 页）。组织里的仓库会进候选池，
在列表里带 `org` 标记，并按来源可过滤。这些通常是高 star 的项目，加进来后会自动排到前面。

接口：

```
GET  /               编辑器页面
GET  /api/state      config + 候选池 + 渲染好的 SVG + tile 坐标
POST /api/refresh    按白名单拉候选（body: {"offline": true} 跳过网络；
                     {"owners": ["user", "u2sb"]} 只刷新指定来源，省配额）
POST /api/config     校验并保存配置
POST /api/svg        只渲染，返回 SVG + tile 坐标
POST /api/export     保存并写 dashboard.svg / preview.html
```

写配置前会校验：repo 必须含 `/`、不能重复、boost 必须在 `(0, 100]`、
组织名不能含 `/` 或空格。失败返回 400 且不落盘。

未设置 `GITHUB_TOKEN` 时 GitHub 只给 60 次/小时，组织多时容易限流；
限流不会让刷新失败，会在提示里说明并继续用已有缓存。

## 分组与排序

`projects.json` 里 `projects` 的**数组顺序就是排列顺序**（不按权重排序）。
`groups` 决定区域划分：先把地图按组切成大块（块的面积 = 组内项目面积之和），
每组顶部留一条标题带，组内再用同样的 squarified 算法铺格子。

分组之间保留 14px 的空隙（`GROUP_GAP`），每个区域有淡底色和描边、左上角标组名，
所以分组边界在视觉上是明确的，而不是靠格子的间距去猜。

**空分组**也会在图上占一小块：虚线描边 + 「拖入项目」提示，总预算 14%（多个空组平分）。
这样新建分组后立刻就有拖拽落点，不必先手动塞一个项目再调整。

分组的增删改全部在**图上**完成，没有独立的标签栏：区域左上角的组名就是入口——
点名字就地改名，悬停出现 `✎` 和 `×`，整个标题栏同时是拖入落点。新建用画面右上角的
「新分组…」输入框。

`group` 为空、或指向一个已被删除的组名，都会归入一个不带标题的「未分组」区域 ——
不会因为分组配置不一致而从图上消失。

## 权重与面积

权重公式：`weight = (★×8 + fork×4 + watch + 3) × 鲜度 × boost`，
鲜度 `= 0.35 + 0.65·e^(−days/180)`，push 越近分越高。

面积不是权重的线性映射。直接按权重分配会让 38 分和 3 分相差 12 倍，
小项目被压成读不出字的碎片，所以先压缩再钳制：

```
area ≈ weight^0.60, 再缩放到 [4%, 17%] 区间（按项目数自动放宽）
```

`^0.60` 保留排名顺序但压平差距；上下限保证每格都还能放下标题和要点。
缩放用的是单因子二分求解，所以总和恒为 1、排序不会被钳制打乱。

## 排版

- 字号随格子尺寸缩放，正文行数按可用高度自动裁剪（先砍末尾要点，再砍元信息）；
- 换行按词切分 ASCII、按字切分中文，避免把 `ScriptCat` 这种词劈开；
- 字体按**实际渲染出的字符**做子集，不维护手写字符表（旧版漏字导致回退系统字体）；
- 得意黑没有的字形（emoji 等）会被剔除，否则会静默回退到系统 emoji 字体。

```bash
# 私有仓库/提高配额（也影响 --serve 的刷新）
set GITHUB_TOKEN=ghp_xxx && python generate.py
```

## 依赖

纯 stdlib 生成，只有字体子集化需要 `fonttools` + `brotli`：

```bash
python -m pip install fonttools brotli
```

缺 `brotli` 时 woff2 编码会失败，脚本会打印真实错误并回退到系统字体
（不会静默产出没有字体的 SVG）。

## 放到 profile 上

1. 把 `dashboard.svg` 拷进 `Weidows/Weidows` 仓库（或本仓库开 GitHub Pages）；
2. profile README 里引用（**不要**写 `width` 属性，让它按原生 846px 显示）：

```markdown
<img src="dashboard.svg" alt="Featured projects" />
```

3. 想刷新排名：重跑 `python generate.py`，commit 新的 `dashboard.svg` 即可。
   可加 cron / GitHub Action 定时跑（Action 里记得给 `GITHUB_TOKEN`）。

### 让卡片能点击

GitHub profile **支持 SVG**，而且点击跳转是可行的——但方式有限制。以下是在真实
`github.com/Weidows` 上实测的结论：

| 方案 | 可用性 | 说明 |
|---|---|---|
| **一整张 SVG 外包 `<a>`** | ✅ **可用** | 你现在的 profile 就在用：`<a href=".../Keeper"><img src="keeper.svg"></a>`，实测点击整图会跳转 |
| SVG **内部**的 `<a>` | ❌ 无效 | `<img>` 加载的 SVG 处于 *secure static mode*：脚本、外部资源、内部链接全部失效（实测 `contentDocument === null`） |
| `<map>` + `<area>` | ❌ 无效 | GitHub 的 markdown sanitizer 会剥掉 `<map>`/`<area>`/`usemap` |
| 透明 `<a>` 覆盖层 | ❌ 无效 | sanitizer 移除 `<style>`/定位用的 `style` 属性与 `<div>` 包裹结构 |
| `<object>` / `<iframe>` | ❌ 无效 | 同样被 sanitizer 移除；在真实 README 的 DOM 里查不到这些标签 |

**结论**：一张图只能有一个链接。要让每个项目都有自己的入口，有两条路：把地图拆成
每张卡片一个 SVG（你现有 profile 的做法），或者**保留大图、把链接放到图下面的列表里**
（本项目采用后者，见下一节）。

如果确实需要「一张图内多个可点区域」，唯一可行的路子是不走 README，而是把页面
放到 **GitHub Pages** 上（那里没有 sanitizer，可以用真 HTML/CSS/JS）。

### 图片 + 列表：让每个项目都有自己的链接

既然一张图只能挂一个链接，那就把链接放到图**下面**——GitHub 的 markdown 列表是
完全可靠的。`python generate.py` 现在会同时输出 `dashboard.md`：

```markdown
<img src="dashboard.svg" alt="Featured projects" width="846">

**AI / 工具**

- [**wutils**](https://github.com/Weidows/wutils) — ★ 5 · fork 1 · Go · 17.0%： Go 学习与开发期 utils/demos 合集 / ★5 · 持续更新的工具箱
- [**video2script**](https://github.com/Weidows/video2script) — Python · 9.7%： 视频→文稿：…
```

这个方案的取舍：

| | 说明 |
|---|---|
| ✅ 保留面积比例 | 上方仍是完整的 treemap，方块大小照旧表达权重 |
| ✅ 每项独立链接 | 列表里每个项目都是真的 markdown 链接，点击进对应仓库 |
| ✅ 顺序与分组一致 | 列表按 `groups` 和 `projects` 的数组顺序排，和图上从左到右、从上到下一致 |
| ✅ 可搜索 / 可选中 | 文字是真实文本，不是图里的像素 |
| ⚠️ 有重复 | 项目名在图和列表里各出现一次 |

列表的每一行是：`项目名 — ★/fork/语言/面积占比：key-points`。空的字段会自动省略
（比如 0 star 的项目不显示 `★ 0`）。

编辑器里「复制 README」按钮可以把这段（图片 + 列表）直接复制到剪贴板；
`导出 SVG` 会写三个文件：`dashboard.svg` / `preview.html` / `dashboard.md`。

Preview 模式里，列表按 GitHub 的真实排版渲染（粗体分组标题 + 16px 正文 + 蓝色链接），
点击项目名会打开对应的编辑器而不是跳转——那里是预览，不是真 README。

## 文件

| 文件 | 说明 |
|---|---|
| `generate.py` | 渲染与 CLI，stdlib only（含 squarified treemap、分组布局、权重钳制） |
| `server.py` | 本地编辑器服务（`--serve` 时启动），stdlib `http.server` |
| `ui.py` | 编辑器单页 UI（无构建步骤，内联 CSS/JS） |
| `projects.json` | 用户 / 组织白名单 / 分组 / 项目列表（数组顺序 = 排列顺序）+ key-points + boost |
| `dashboard.svg` | 生成产物，846×580 起，推 profile 的就是它 |
| `dashboard.md` | 配套的 README 片段：图片 + 每个项目的链接列表 |
| `preview.html` | 本地预览（含权重明细表），不推 |
| `cache.json` | API 缓存，离线重排 / 候选池数据源 |
| `assets/font/` | 得意黑 Smiley Sans（[atelier-anchor/smiley-sans](https://github.com/atelier-anchor/smiley-sans)，OFL-1.1；`subset.woff2` 由 `generate.py` 按实际用字自动裁剪内嵌进 SVG，`preview.html` 和编辑器直接引用目录下完整字重） |
