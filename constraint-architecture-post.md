# 两周。两个 Agent。同一个架构。

我大一，三周前还没碰过 Agent。

莫名奇妙做了两个东西——

**Kylin-Agent**：部署在麒麟 V11 上的安全运维 Agent。四层安全防线，每层不依赖 LLM。16 次红队攻击，0 次打穿。

**Malio**：具身化 AI 音乐 Agent。800 粒子 9 大物理系统。Persona 约束 + DSL 规则引擎 + 联邦规则交换。

一个是运维安全。一个是音乐 DJ。完全没有交集的两个领域。

做完之后我发现它们共享同一个架构。不是"有点像"——是同一套四层分层，在两个领域各自独立验证了一遍：

---

**Layer 1 — Reasoning (LLM)**
自由推理。LLM 只管想，不管能不能做。

**Layer 2 — Constraints (Deterministic)**
代码层约束。不依赖 LLM——约束只增不减，无论当前模式多"宽松"，基础规则不撤。

**Layer 3 — Execution (Sandbox)**
分级执行。auto / confirm / veto。角色和权限在这一层强制生效。

**Layer 4 — Audit (Immutable Record)**
每步可追溯。理想形式 SHA256 链不可篡改，轻量版至少做到规则有效性反馈。

---

核心原则就一行：**LLM 负责想。代码负责决定能不能做。**

不是"更强的 prompt"。是不靠 prompt 做约束。

---

我把这个架构写了篇东西：[Constraint Architecture](https://github.com/1nour2567/kylin-agent/blob/master/CONSTRAINT.md)

两个参考实现的代码都在 GitHub 上。

发出来是想问——你在做的 Agent，它的约束是什么？

如果有人用这个架构在第三个领域（医疗？金融？教育？）做了一个东西——那第三个参考实现就是最有力的验证。

---

*大一。三周。一个人。*
