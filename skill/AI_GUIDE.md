# Ren'Py MCP — AI Agent 操作规范

本文档不是参考手册，是**操作流程**。你必须按顺序执行每一步。跳过任一步骤就是 bug。

---

## 第零步：启动前置检查（不可跳过）

### 0.1 读取项目配置

在写任何代码之前，**必须**先执行这两个调用获取项目信息：

```
1. grep gui.init gui.rpy          → 获取分辨率（如 2560x1440）
2. get_image_size(立绘路径)       → 获取每张立绘真实尺寸
```

**为什么：** xysize 和 transform 的所有参数都依赖这两个数据。脑补 = 乱码/错位。

### 0.2 提取项目变量

从 0.1 的结果中提取，记录到对话里：

```
项目分辨率：W=____, H=____
立绘尺寸：角色名 = WxH
```

下面的所有操作**必须**使用这些变量，**禁止**使用你自己的示例数据。

### 0.3 从 docx 提取需求清单

读完剧本后，**必须**输出需求清单才能开始写代码：

```
[ ] 场景图：____（路径 + xysize 缩放）
[ ] 立绘：____（角色 + 表情列表 + get_image_size 尺寸）
[ ] CG：____（文件名 + xysize 缩放 + 显示/隐藏时机）
[ ] BGM：____（文件名 + 对应场景）
[ ] SFX：____（文件名 + 触发条件）
[ ] 语音：____（文件数 + 编号范围）
[ ] 选项：____（每个选项 + 好感度变化值）
[ ] 主菜单：fit "contain"
```

**禁止**"先跑通核心再补"。清单不完整 = 不准写代码。

---

## 第一步：铺素材

对 0.3 清单中的每一项素材：

```
copy_asset(project_path, source=绝对源路径, dest=相对路径)
```

结束后 compile_project(force=True) 确认无报错。

---

## 第二步：写代码

### 2.1 场景图

```renpy
scene bg_xxx:
    xysize (W, H)   # W,H 来自 0.2，不是 1280,720
```

### 2.2 立绘

根据 0.2 的立绘尺寸计算 zoom + yoffset：

```
if image_height > H:
    zoom = H / image_height        # 缩放到刚好填满屏幕高度
else:
    zoom = 1.0                     # 立绘比屏幕矮，不缩放

zoomed_height = image_height * zoom
yoffset = -(zoomed_height - H) / 2
```

transform 模板：

```renpy
transform char_pos:
    xalign 0.5
    zoom {计算值}
    yoffset {计算值}    # 不允许多余属性（如 yalign）
```

**为什么需要 zoom：** 2048px 高的立绘在 1440px 屏幕上即使居中也会上下裁掉 304px，
看起来像"放大到充满屏幕"。zoom = 1440/2048 = 0.7 才能让立绘完整显示。

### 2.3 CG 展示

CG 和场景图一样需要尺寸适配：

```renpy
show image cg_xxx:
    xysize (W, H)     # 或 fit "contain"
with dissolve
pause 3.0             # 给玩家足够时间看
hide image cg_xxx with dissolve
```

**CG 禁止不加 xysize。** 和场景图一样，素材尺寸 ≠ 屏幕分辨率。

### 2.4 语音

每条角色对话前，对照 0.3 清单加上 voice：

```renpy
voice "audio/voice/0001.wav"
h "对话内容"
```

**禁止**"先不加语音，以后补"。

### 2.5 主菜单

```renpy
add gui.main_menu_background:
    fit "contain"
```

用 replace 改 screens.rpy 中的单行——**不要多行匹配。**

### 2.6 选项

```renpy
menu:
    "选项文本":
        $ variable += N
        jump xxx
```

### 2.7 main_menu_background 的 replace

```python
# ✅ replace 目标：最短唯一单行
position="replace:    add gui.main_menu_background"
code='    add gui.main_menu_background:\n        fit "contain"'

# ❌ 不要多行 replace
```

---

## 第三步：验收

### 3.1 编译

```
compile_project(project_path, force=True)
```

### 3.2 对照清单检查

回到 0.3 的需求清单逐项确认：

```
[x] BGM 3 段 ✅
[x] 语音 19 条 ✅
[x] 场景图 2 张 + xysize ✅
[x] 立绘 6 表情 + transform ✅
[x] 主菜单 fit "contain" ✅
[x] 选项 2 组 + 好感度 ✅
```

任何 `[ ]` 没打钩 = 不合格，回到对应的步骤补上。

---

## 禁止事项（按致命程度分级）

### 🔴 致命（违反必出 bug）

| # | 规则 | 为何 |
|---|------|------|
| 1 | **读完 docx 不列清单就写代码** | 你不是在数需求，你在猜 |
| 2 | **不用 0.1 查出的 W/H 值，用了自己脑补的分辨率** | xysize 全错 |
| 3 | **立绘 transform 里加 yalign 属性** | 底部对齐 → 只看到脚 |
| 4 | **立绘比屏幕高时不加 zoom** | 溢出 → 放大到充满屏幕 |
| 5 | **CG 不加 xysize** | CG 素材尺寸 ≠ 屏幕，不缩放就变形 |
| 6 | **"先跑通核心再补细节"** | 细节永远不会补 |
| 7 | **replace 用多行匹配** | 回退之前的所有改动 |
| 8 | **分批补丁式改同一个 label** | 覆盖 + 遗漏 |

### 🟠 严重

| # | 规则 |
|---|------|
| 7 | 跳过 compile_project |
| 8 | 手动写缩进 |
| 9 | 猜立绘位置（不调 get_image_size） |

### 🟡 一般

| # | 规则 |
|---|------|
| 10 | copy_asset dest 加 game/ 前缀 |
| 11 | exec_rpy file 不加 game/ 前缀 |
| 12 | label 内用 default |
| 13 | 场景图不加 xysize |
| 14 | 不清 .rpyc 缓存 |

---

## 排错速查

| 症状 | 可能的违规 | 解决 |
|------|-----------|------|
| xysize 数值不对 | 违规 #2：脑补分辨率 | 回退到 0.1，读 gui.init(H, W) |
| 立绘只显示脚 | 违规 #3：用了 yalign | 改成 xalign 0.5 + yoffset 公式 |
| 立绘太大/溢出屏幕 | 违规 #4：缺 zoom | zoom = H / image_height |
| CG 未适配屏幕 | 违规 #5：CG 没 xysize | 加 xysize (W, H) |
| 语音缺失 | 违规 #6：先跑通再补 | 根据清单补上所有 voice 行 |
| 主菜单显示异常 | 违规 #5：多行 replace 回退 | 用单行 replace 重新写入 |
| 修改不生效 | 违规 #14 | compile_project(force=True) |
| 需求漏项 | 违规 #1：没列清单 | 停止，重新读 docx，列清单 |

---

## 核心原则

**你不是在设计，你是在搬砖。**

剧本写了什么，你就按清单实现什么。不要"我觉得可以先不加"，不要"默认值应该是对的"。

**第零步做完之前，不准碰 exec_rpy。**

*第 1 版发布于 2026-06-01，v2 重构于同一天凌晨 1:00。所有规则来自同一天的实战故障。*
