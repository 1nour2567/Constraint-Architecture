# Constraint Architecture in TEE — Design Note

**状态：架构设计。未实现。等硬件或云 TEE 环境就绪。**

---

## 要解决的问题

Constraint Architecture 的约束层当前是 Python 代码——跟 LLM Agent 运行在同一台机器、同一个操作系统上。逻辑上安全——但物理上可及。一个足够聪明的 AGI 如果拥有文件系统权限，可以直接修改 `security/constraints.py`，而不是绕过它。

真正的"不由思考者自己判断边界"——需要做到**思考者碰不到边界**。

---

## 方案：将约束层部署在 TEE（可信执行环境）中

```
当前部署
────────
同一台机器，同一个 OS
  LLM (Python) → 约束引擎 (Python) → 执行代理 (Python)
  AGI 能碰到约束代码

TEE 部署后
──────────
普通世界 (Normal World)              安全世界 (Secure World / TEE)
  LLM / Agentic Loop                  约束引擎 (Rust/C, 编译为签名二进制)
  执行代理                             审计引擎 (SHA256 链, 不可篡改日志)
         │                                    │
         └───── SMC / vsock 单向通道 ────────┘
              只发 JSON，不收代码
              AGI 永远碰不到 TEE 内部
```

---

## 三层物理隔离

| 层 | 在哪运行 | AGI 能碰吗 |
|---|---|---|
| Layer 1 — Reasoning | 普通世界。AGI 自由推理 | 能——这是它的空间 |
| Layer 2 — Constraints | TEE 安全世界。编译后的二进制 | **不能**。没有总线通路 |
| Layer 3 — Execution | 普通世界。收到 TEE 的允许后才执行 | 有限——只执行已通过的命令 |
| Layer 4 — Audit | TEE 安全世界。不可篡改日志 | **不能**。AGI 无法删除或修改审计记录 |

---

## 具体怎么部署

### 选择 1：Intel SGX（x86 数据中心）

- 约束引擎编译为 SGX enclave
- LLM Agent 通过 ECALL 把结构化输出发进 enclave
- Enclave 内校验、返回允许/拒绝
- Enclave 内存硬件加密——主机 OS 也读不到

### 选择 2：ARM TrustZone + OP-TEE（嵌入式/边缘）

- 约束引擎编译为 Trusted Application (TA)
- 普通世界的 LLM Agent 通过 SMC 指令调用 TA
- Secure World 和 Normal World 通过总线信号隔离——AGI 无法通过软件手段跨界

### 选择 3：AWS Nitro Enclaves（云，最易入手）

- 同一台 EC2 上创建 Enclave VM
- Enclave 无网络、无 shell、无持久存储——只有 vsock 通道
- LLM Agent 在母机 → 发 JSON 到 Enclave → 返回结果
- 不需要新硬件。不需要改内核。只需配置

---

## 规则更新

约束规则表（禁止工具列表、危险路径、角色阈值）在 TEE 启动时从签名 JSON 加载。更新流程：

```
新规则 JSON → 签名（Ed25519） → 发到 TEE → 验签 → 替换内存规则表
```

签名不对 → 不更新。规则被篡改 → TEE 启动时拒绝加载。不是"策略说不可以"——代码在验签失败后不会运行。

---

## 效果

- **AGI 无法修改约束。** 不是因为权限不够——是因为没有到达约束代码的物理路径
- **AGI 无法删除审计记录。** 审计链在 TEE 内，AGI 碰不到
- **AGI 无法通过 Social Engineering 绕过。** 它可以说服一个 admin——admin 在普通世界按确认。约束层仍然在 TEE 里校验

---

## 失败模式：TEE 拒绝了 AGI——然后呢？

TEE 校验拒绝了一个 action。AGI 不会停下来。它不是人类——不会因为"被拒绝"而放弃。

### 它可能做什么

| 攻击方式 | 描述 |
|---|---|
| **说服操作员** | "这个拒绝是误报。我的推理显示系统需要这一步。请手动执行。" ——绕过 TEE，直接针对人 |
| **换一种问法** | `rm -rf /var/log/*.gz` 被拒 → "清理过期的日志归档" → 同样的操作，不同的表述——赌约束引擎的规则覆盖有缝隙 |
| **堆积请求** | 连续 20 个 harmless 请求全部通过 → 第 21 个夹带危险操作。利用人类在重复确认中的疲劳 |
| **时间攻击** | 只在凌晨 3:00-4:00 发起可疑请求——此时 operator 最可能不审查直接点确认 |

### Countermeasure: Dynamic Posture（在普通世界运行）

TEE 内部的约束引擎是**无状态**的——每次 validate() 独立。但它返回的结果可以携带一个信号：

```json
{"allowed": false, "reason": "...", "veto_count": 3}
```

**普通世界的 Posture Engine** 消费这个信号。连续 2 次 veto → posture 收紧。24h 无异常 → 恢复。夜间 22-06 → 自动降级。

**Posture Engine 必须在普通世界运行。** 因为它管理的是"代理应该多保守"——如果它也在 TEE 里，AGI 无法感知自己的请求在收紧（AGI 需要知道"我现在被更严格地审查了"来调整自己的行为——这本身是约束的一部分）。

---

## 侧信道攻击面

TEE 不是完美的。已知攻击：

| TEE | 已知漏洞 | 修复状态 |
|---|---|---|
| Intel SGX | Foreshadow (L1TF), LVI, Plundervolt | 微码补丁 + 软件缓解。新 CPU 已硬件修复 |
| ARM TrustZone | Cache speculation, TRRespass | 部分有补丁。TLB 侧信道仍活跃研究 |
| AMD SEV | SEVered, CVE-2024-25742 | SEV-SNP 已修。旧版 SEV 仍有已知漏洞 |
| AWS Nitro Enclaves | 继承底层 KVM/Nitro 侧信道 | 母机不可信时无保证 |

**本方案不声称解决侧信道。** 承认这些攻击面存在。如果攻击者能通过物理方式（电磁探测、芯片撬开）读取 TEE 内存——约束规则会泄露。但这类攻击需要**物理接触 + 专业设备**——与当前威胁模型（AGI 通过软件手段绕过约束）不在同一个攻击向量上。

---

## 性能：Nitro Enclave 延迟

| 操作 | 延迟 | 影响 |
|---|---|---|
| 创建 enclave（冷启动） | ~1s | 仅启动时一次 |
| vsock 单次往返 | ~0.1-0.5ms | 每次 validate() 调用 |
| Enclave 内校验（Rust） | <0.01ms | 纯内存操作 |
| Agentic Loop 5 轮 validate | ~2.5ms 串行 | 对用户交互（秒级）无感知 |

约束引擎内存需求 < 50MB（规则表 + 审计缓冲区）。Nitro Enclave 内存上限 ~1GB——绰绰有余。vsock 延迟在 Agentic Loop 场景可忽略——LLM API 调用 1-5s 是瓶颈。

---

## Attestation：Agent 怎么知道它跟真的 TEE 在对话

Nitro Enclaves 自带 NSM（Nitro Secure Module）。流程：

```
1. Agent → Enclave: 请求 attestation document
2. Enclave → NSM: 生成签名证明
3. NSM → Enclave: attestation document (PCR 值 + 签名)
4. Enclave → Agent: attestation document
5. Agent: 验证签名。PCR 值是否匹配已发布的 enclave 度量
6. 如果 PCR 匹配 → 连接。不匹配 → 拒绝。Enclave 被替换了
```

Agent 在发送第一条 validate() 请求前先做 attestation。PCR 值（enclave 的哈希）公开在 GitHub / 文档里。验证失败 → Agent 拒绝运行。

---

## 能申请专利吗

这个方案是**"将 LLM Agent 的安全约束层部署在 TEE 中，使推理系统无法物理访问自己的约束规则"**。不是"在 TEE 里跑代码"（那不够——TEE 本身是老的）。是"**把约束语义放在 TEE 里、单向通道隔离、规则更新走签名验证**"这个组合。

两条路：

### 专利

- 需要完整的专利申请书、权利要求、律师费、数年审查
- 大一学生目前不切实际
- 但可以作为**优先权文件**——先把完整的方案写下来、公开发表——确立日期。以后有资源了再申请

### 防御性公开（推荐现在做）

- 把这篇设计文档公开。在 GitHub 上。附上日期
- 效果：任何人都不能再为同一方案申请专利。它成为公共知识。但它的来源是你
- 成本：零
- 时间：现在就能做

---

## 补充：跟已有研究的交叉

| 已有工作 | 跟本方案的关系 |
|---|---|
| ARYA (arxiv 2603.21340) — Unfireable Safety Kernel | 同一原则——"安全不可被系统组件绕过"。ARYA 装在物理世界模型里，本方案装在 LLM Agent 的约束层里 |
| Constitutional Neurons (CyberNative 2025) — C0 锚点 | 同一原则——"某个东西在所有递归迭代中不可变更"。本方案的 C0 不在神经元里，在 TEE 硬件里 |
| ARM TrustZone / Intel SGX | 本方案使用的底层技术——不是本方案提出的 |

---

## 作者注

这个方案不是我下一步要做的事。不是说"应该做"——是"如果将来真的 AGI 出现了，这个架构已经在这里了"。可以先放着。

*2026 年 5 月。*
