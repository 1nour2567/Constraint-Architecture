# Constraint Architecture

[![PyPI](https://img.shields.io/badge/PyPI-constraint--architecture-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/constraint-architecture/)

**LLM reasons. Code decides. Audit ensures non-repudiation.**

A production-grade, domain-agnostic Agent architecture extracted from two independent reference implementations spanning security operations (Kylin-Agent) and embodied AI (Malio). Four constraint layers (T0–T4), none of which depend on the LLM.

```bash
pip install constraint-architecture              # from PyPI
python -m constraint_architecture.demo           # one-click demo
python -m constraint_architecture.skeleton       # 25 self-checks
```

## Architecture

```
T0 Anti-Injection  →  T1 Risk Scoring  →  T2 Dual-Path Validation  →  T3 Sandbox  →  T4 Audit Chain
     (regex)            (manifest)         (structural + regex)        (tiered)       (SHA256 chain)
```

## Structure

| Directory | Content |
|-----------|---------|
| `constraint_architecture/` | Installable package: skeleton, demo, self-checks (`pyproject.toml` builds it) |
| `skeleton/` | `constraint_skeleton.py` — 10 ABCs, 10 Protocols, 12 dataclasses, 25 self-checks |
| `security/` | T0–T3 reference implementation (anti-injection, patterns, risk model, constraints, sandbox, guardrail) |
| `audit/` | T4 audit trail — append-only JSONL, SHA256 hash chain, FOIA endpoint |
| `agent/` | Minimal tool manifest + risk posture + mock provider, vendored from Kylin-Agent so `security/` runs standalone |
| `tests/` | Jailbreak tests, pessimistic path tests, 35-entry jailbreak corpus |

## Testing

```bash
pip install pytest
pytest tests -q          # 33 tests, no LLM, no network
```

| File | Tests | Covers |
|------|------:|--------|
| `test_pessimistic.py` | 24 | Edge cases, concurrency, privilege boundaries |
| `test_jailbreak_corpus.py` | 5 | 35-entry jailbreak corpus regression (T0/T2) |
| `test_jailbreak.py` | 4 | Known attack vectors |

All structural — no LLM calls, no network, no API key. Under a second.

## Key Documents

- [`agent-os-architecture.md`](agent-os-architecture.md) — Seven-layer Agent OS: Shell, Identity, Scheduler, Memory, Protocol, Constraint, Tools
- [`constraint-architecture.md`](constraint-architecture.md) — Constraint Architecture manifesto (Chinese)
- [`CONSTRAINT.md`](CONSTRAINT.md) / [`CONSTRAINT_EN.md`](CONSTRAINT_EN.md) — Canonical design document (CN/EN)
- [`constraint-tee-design.md`](constraint-tee-design.md) — TEE deployment path (Intel SGX / ARM TrustZone)

## Provenance

- **Kylin-Agent** — Security ops agent on Kylin V11 (中国软件杯 competition entry). 89 structural tests covering injection, privilege, and audit-chain cases.
- **Malio** — Embodied AI music agent. 800 particles, 9 physics systems. 75 assertions (63 deterministic).

Two entirely different domains. Same architecture.

## Author

Xu Renwu (续仁舞). Independent work. Jan–May 2026.

## License

MIT
