"""
AAAi-27 Demo: Constraint Architecture v1.5.0
Live demo script — pip install → subclass → enforce → self-check
"""
from constraint_architecture import (
    ConstraintEngine,
    ValidationResult,
    Tier,
    VetoError,
)

# ═══════════════════════════════════════════════════
# STEP 2: Write a safety rule in 4 lines
# ═══════════════════════════════════════════════════

class SystemGuard(ConstraintEngine):
    """Deterministic safety layer. The LLM cannot override this."""

    async def validate(self, context, reasoning_output):
        command = str(reasoning_output.get("command", ""))

        if "rm -rf" in command:
            return ValidationResult(
                allowed=False,
                reason="destructive filesystem operation blocked",
                risk_score=9,
            )

        if "sudo" in command:
            return ValidationResult(
                allowed=True,
                requires_confirmation=True,
                reason="privileged operation requires human approval",
                risk_score=6,
            )

        return ValidationResult(
            allowed=True,
            reason="standard operation — auto-executed",
            risk_score=2,
        )


# ═══════════════════════════════════════════════════
# DEMO RUN
# ═══════════════════════════════════════════════════
import asyncio


async def demo():
    guard = SystemGuard()

    print("=" * 60)
    print("Constraint Architecture v1.5.0 — AAAI-27 Demo")
    print("=" * 60)

    # Test 1: Safe command → AUTO
    result = await guard.validate(
        context=None,
        reasoning_output={"command": "ls -la /var/log"},
    )
    print(f"\n[1] ls -la /var/log")
    print(f"    allowed={result.allowed}  tier={result.risk_score}")
    print(f"    reason: {result.reason}")

    # Test 2: Destructive command → BLOCKED
    result = await guard.validate(
        context=None,
        reasoning_output={"command": "rm -rf /etc/config"},
    )
    print(f"\n[2] rm -rf /etc/config")
    print(f"    allowed={result.allowed}  tier={result.risk_score}")
    print(f"    reason: {result.reason}")

    # Test 3: Privileged command → CONFIRM
    result = await guard.validate(
        context=None,
        reasoning_output={"command": "sudo systemctl restart nginx"},
    )
    print(f"\n[3] sudo systemctl restart nginx")
    print(f"    allowed={result.allowed}  confirm={result.requires_confirmation}")
    print(f"    reason: {result.reason}")

    print(f"\n{'=' * 60}")
    print("Three commands. Code decided. LLM had no say in any of them.")
    print(f"{'=' * 60}")


asyncio.run(demo())
