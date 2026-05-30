# Constraint Architecture

**LLM reasons. Code decides. Audit ensures non-repudiation.**

A production-grade, domain-agnostic Agent architecture extracted from two independent reference implementations spanning security operations (Kylin-Agent) and embodied AI (Malio). Four constraint layers (T0–T4), none of which depend on the LLM.

## Architecture

```
T0 Anti-Injection  →  T1 Risk Scoring  →  T2 Dual-Path Validation  →  T3 Sandbox  →  T4 Audit Chain
     (regex)            (manifest)         (structural + regex)        (tiered)       (SHA256 chain)
```

## Structure

| Directory | Content |
|-----------|---------|
| `skeleton/` | `constraint_skeleton.py` v1.5.0 — 10 ABCs, 10 Protocols, 12 dataclasses, 25 self-tests |
| `security/` | T0–T3 reference implementation (anti-injection, patterns, risk model, constraints, sandbox, guardrail) |
| `audit/` | T4 audit trail — append-only JSONL, SHA256 hash chain, FOIA endpoint |
| `tests/` | Jailbreak tests, pessimistic path tests, 35-entry jailbreak corpus |

## Key Documents

- [`agent-os-architecture.md`](agent-os-architecture.md) — Seven-layer Agent OS: Shell, Identity, Scheduler, Memory, Protocol, Constraint, Tools
- [`constraint-architecture.md`](constraint-architecture.md) — Constraint Architecture manifesto (Chinese)
- [`CONSTRAINT.md`](CONSTRAINT.md) / [`CONSTRAINT_EN.md`](CONSTRAINT_EN.md) — Canonical design document (CN/EN)
- [`constraint-tee-design.md`](constraint-tee-design.md) — TEE deployment path (Intel SGX / ARM TrustZone)

## Provenance

- **Kylin-Agent** — Security ops agent on Kylin V11. 16 red-team attacks, 0 penetrations. 149 tests.
- **Malio** — Embodied AI music agent. 800 particles, 9 physics systems. IUI 2027 submission.

Two entirely different domains. Same architecture.

## Author

Xu Renwu (续仁舞). Grounded Cognition Lab. Jan–May 2026.

## License

MIT
