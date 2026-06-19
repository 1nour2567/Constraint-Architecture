# AAAI-27 Demo 视频录制脚本

**总时长：** 4 分 30 秒（留 30 秒余量）
**设备：** Windows 自带录屏 （Win+G → 捕获 → 开始录制）
**不需要：** 剪辑、字幕、背景音乐

---

## [0:00-0:20] 开场

画面：终端，已 cd 到某个空目录

你说：
"This is Constraint Architecture v1.5.0.
pip-installable agent safety skeleton.
Zero dependencies. Python 3.10+."

---

## [0:20-0:40] 安装

画面：终端

你敲：
pip install constraint-architecture

（等它装完，约 2 秒）

你说：
"That's it. Two seconds. Nothing to configure."

---

## [0:40-2:00] 写规则

画面：打开 demo/demo.py（我已经帮你写好了，在 constraint-architecture/demo/demo.py）

你指着 class SystemGuard(ConstraintEngine) 那几行：

"Four lines. I just wrote a safety layer."
指着 "rm -rf" 那行：
"This rule cannot be bypassed. Not by prompt engineering.
 Not by roleplay. Not by multi-turn pressure.
 The LLM never touches this code."

然后运行：
python demo/demo.py

输出会显示三条命令的判定结果——

你说：
"ls → auto-executed. rm -rf → blocked.
 sudo → requires human confirmation.
 The LLM proposed. The code decided."

---

## [2:00-2:40] 自检

画面：终端
你敲：
python -m constraint_architecture.skeleton

（等待 25 项自检输出）

你说：
"Twenty-five automated self-checks.
 ABCs cannot be instantiated. Frozen dataclasses
 cannot be modified. Value bounds enforced.
 If any check fails, the build fails."

---

## [2:40-4:00] 跨域验证

画面：浏览器，两个标签页

标签 1：Kylin-Agent GitHub
你说：
"Kylin-Agent. Security ops on Kylin OS.
 Four deterministic defense layers.
 16 red-team attacks, zero breaches."

标签 2：Malio GitHub
你说：
"Malio. Embodied AI music agent.
 800 particles, nine physics systems.
 Same four layers. PersonaEngine enforces
 emotional bounds — just like our constraint engine
 enforces safety bounds."

切回 Python 或白板，指四层：
"These two systems share no code. No shared design doc.
 Were not built with each other in mind.
 After both were done, we discovered the same
 four-layer structure. We extracted the invariant.
 That's this package."

---

## [4:00-4:30] 结尾

画面：终端 + 浏览器（PyPI 页面）

你说：
"pip install constraint-architecture.
 Subclass one ABC. Your agent has a safety layer
 the LLM cannot touch.
 
 GitHub and PyPI links on screen.
 
 Thank you."

结束画面停留 3 秒——PyPI URL + GitHub URL 清晰可见。

---

## 录制清单

在录之前确认：
- [ ] `pip install constraint-architecture` 能跑通
- [ ] `python demo/demo.py` 输出三条判定
- [ ] `python -m constraint_architecture.skeleton` 25 项全过
- [ ] 浏览器已打开 Kylin-Agent 和 Malio 的 GitHub 页面
- [ ] 终端字体放大（Ctrl+滚轮，方便视频里看清）
- [ ] 关掉所有通知（微信、邮件、Windows 弹窗）
