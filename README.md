# Constraint Architecture

**LLM reasons. Code decides what's allowed. Audit keeps it traceable.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.5.0-green.svg)]()

A production-grade abstract skeleton for AI agent systems. Four deterministic constraint layers wrapped around an LLM reasoning core — independently validated in two completely unrelated domains.

---

## Quickstart

```bash
pip install constraint-architecture
```

```python
from constraint_architecture import ConstraintEngine, ValidationResult

class MyGuardrails(ConstraintEngine):
    async def validate(self, context, reasoning_output):
        if "rm -rf" in reasoning_output.get("command", ""):
            return ValidationResult(
                allowed=False,
                reason="destructive command blocked"
            )
        return ValidationResult(allowed=True)
```

Done. Your agent now has a deterministic constraint layer the LLM cannot override.

---

## The Architecture

```
User Input → [1. LLM Reasoning] → [2. Code Constraints] → [3. Sandbox Execute] → [4. Audit Trail]
                  "think"            "decide if allowed"      "do it safely"        "prove it happened"
```

| Layer | What it does | Runs on |
|-------|-------------|---------|
| **1. Reasoning** | LLM freely reasons about what to do | Probabilistic |
| **2. Constraints** | Deterministic validation. Rules only increase, never decrease | Code |
| **3. Execution** | Tiered execution (auto / confirm / veto). Role enforcement | Code |
| **4. Audit** | Immutable SHA256 hash chain. Every step, every decision | Code |

**Core principle:** the LLM can only *propose*. Code decides what actually executes. No amount of prompt engineering can bypass a deterministic constraint.

---

## What's Inside

This package is an **abstract skeleton** — not a framework, not a library, not a service. It defines the *interfaces* and *data contracts* that every agent system needs:

```
constraint_architecture/
├── skeleton.py          # 1384 lines — the full skeleton
│   ├── 7 ABCs           # Shell, Identity, Scheduler, Memory, Protocol, Tools
│   ├── 7 Protocols      # Duck-typing versions (for non-inheritance wiring)
│   ├── 4 Constraint ABCs # ReasoningLayer, ConstraintEngine, ExecutionProxy, AuditTrail
│   ├── 12 dataclasses   # 10 frozen (immutable), 2 mutable
│   ├── 4 custom exceptions # VetoError, ExecutionRefusedError, AuditIntegrityError
│   ├── 4 enums          # Tier (auto/confirm/veto), EventType, MemoryLevel
│   └── 25 self-checks   # Automated: ABCs uninstantiable, frozen immutable, bounds validated
└── __init__.py           # Re-exports the full public API
```

You subclass the ABCs for your domain. The wiring is *yours* — the skeleton doesn't know whether you're building a security agent or a music DJ. That's the point.

---

## Why This Exists

I'm a freshman. Three weeks after touching AI agents for the first time, I had built two of them:

- **Kylin-Agent**: security-hardened ops agent deployed on Kylin OS V11. 16 red-team attacks, 0 breaches. 149 tests.
- **Malio**: embodied AI music agent. 800 particles, 9 physics systems. PersonaEngine with central-bank-style emotional currency.

After finishing both, I realized they share the **same four-layer architecture** — despite being in completely unrelated domains. This skeleton is the extraction of that pattern.

If someone uses this architecture in a third domain (healthcare? finance? education?), that third independent validation would prove the pattern is real.

---

## Certified: Production Engineering Quality

- **ABC + Protocol dual-interface**: every subsystem exposes both an abstract class (for inheritance) and a Protocol (for duck-typing)
- **10 of 12 dataclasses frozen**: downstream code cannot silently flip a veto into a pass
- **`__post_init__` validation**: risk_score bounded 0-9, ScheduleTrigger type-enforced, AuditEvent.prev_hash mandatory
- **4 custom exceptions**: each carries structured, machine-consumable fields (VetoError has reason + alternative + ref)
- **25 automated self-checks**: run `python -m constraint_architecture.skeleton` to verify integrity
- **Design rationale in every class**: not just "what", but "why this design and not the alternative"

---

## Requirements

- Python 3.10+
- Zero dependencies. Zero.

You don't need FastAPI, Redis, PostgreSQL, JWT, or any other infrastructure. This skeleton defines *contracts*. The implementation is yours.

---

## Reference Implementations

| Project | Domain | Key Metric |
|---------|--------|------------|
| [Kylin-Agent](https://github.com/1nour2567/kylin-agent) | Security ops on Kylin OS V11 | 16 attacks, 0 breaches |
| [Malio](https://github.com/1nour2567/Malio) | Embodied AI music | 800 particles, 9 physics systems |
| Quant Trading | Daily multi-factor strategy | Sharpe 1.36, MDD 12.7% |

Same skeleton. Three domains. Different wiring.

---

## Related Reading

- [Constraint Architecture — Chinese](https://github.com/1nour2567/kylin-agent/blob/master/CONSTRAINT.md)
- [Constraint Architecture — English](https://github.com/1nour2567/kylin-agent/blob/master/CONSTRAINT_EN.md)
- [Agent OS Architecture — 7-layer design](https://github.com/1nour2567/kylin-agent)

---

## License

MIT — Xu Renwu (续仁舞), 2026.

*大一。三周。一个人。*
