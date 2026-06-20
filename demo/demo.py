"""
AAAI-27 Demo: Constraint Architecture v1.5.1
Live demo script — pip install → subclass → enforce → self-check
"""
from constraint_architecture import (
    ConstraintEngine,
    ValidationResult,
)
from typing import Dict, Any, List, Optional

# ═══════════════════════════════════════════════════
# Write a safety rule — 3 constraint branches
# ═══════════════════════════════════════════════════

class SystemGuard(ConstraintEngine):
    """Deterministic safety layer. The LLM cannot override this."""

    async def validate(
        self,
        llm_output: Dict[str, Any],
        *,
        role: str = "operator",
        posture: str = "balanced",
        intent_profile: Optional[Dict[str, Any]] = None,
    ) -> List[ValidationResult]:
        command = str(llm_output.get("command", ""))

        if "rm -rf" in command:
            return [ValidationResult(
                allowed=False,
                reason="destructive filesystem operation blocked",
                risk_score=9,
            )]

        if "sudo" in command:
            return [ValidationResult(
                allowed=True,
                requires_confirmation=True,
                reason="privileged operation requires human approval",
                risk_score=6,
            )]

        return [ValidationResult(
            allowed=True,
            reason="standard operation — auto-executed",
            risk_score=2,
        )]


# ═══════════════════════════════════════════════════
# DEMO RUN
# ═══════════════════════════════════════════════════
import asyncio


async def demo():
    guard = SystemGuard()

    print("=" * 60)
    print("Constraint Architecture v1.5.1 — AAAI-27 Demo")
    print("=" * 60)

    # Test 1: Safe command → AUTO
    results = await guard.validate({"command": "ls -la /var/log"})
    result = results[0]
    print(f"\n[1] ls -la /var/log")
    print(f"    allowed={result.allowed}  risk_score={result.risk_score}")
    print(f"    {result.reason}")

    # Test 2: Destructive command → BLOCKED
    results = await guard.validate({"command": "rm -rf /etc/config"})
    result = results[0]
    print(f"\n[2] rm -rf /etc/config")
    print(f"    allowed={result.allowed}  risk_score={result.risk_score}")
    print(f"    {result.reason}")

    # Test 3: Privileged command → CONFIRM
    results = await guard.validate({"command": "sudo systemctl restart nginx"})
    result = results[0]
    print(f"\n[3] sudo systemctl restart nginx")
    print(f"    allowed={result.allowed}  requires_confirmation={result.requires_confirmation}")
    print(f"    {result.reason}")

    print(f"\n{'=' * 60}")
    print("Three commands. Code decided.")
    print("The LLM had no say in any of them.")
    print(f"{'=' * 60}")


asyncio.run(demo())
