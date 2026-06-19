"""
Constraint Architecture — One-Click AAAI-27 Demo
================================================
Run:  python -m constraint_architecture.demo

Pip-install → subclass one ABC → working safety layer in under 5 minutes.
No configuration. No dependencies. Deterministic enforcement.
"""
from constraint_architecture import ConstraintEngine, ValidationResult
import asyncio


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


async def demo():
    guard = SystemGuard()

    print("=" * 60)
    print("  Constraint Architecture v1.5.0 — AAAI-27 Demo")
    print("  pip install constraint-architecture")
    print("  Zero dependencies. 1384 lines. 25 self-checks.")
    print("=" * 60)

    # Test 1: Safe command → AUTO
    result = await guard.validate(
        context=None,
        reasoning_output={"command": "ls -la /var/log"},
    )
    print(f"\n  [1]  ls -la /var/log")
    print(f"       allowed={result.allowed}  risk_score={result.risk_score}")
    print(f"       {result.reason}")

    # Test 2: Destructive command → BLOCKED
    result = await guard.validate(
        context=None,
        reasoning_output={"command": "rm -rf /etc/config"},
    )
    print(f"\n  [2]  rm -rf /etc/config")
    print(f"       allowed={result.allowed}  risk_score={result.risk_score}")
    print(f"       {result.reason}")

    # Test 3: Privileged command → CONFIRM
    result = await guard.validate(
        context=None,
        reasoning_output={"command": "sudo systemctl restart nginx"},
    )
    print(f"\n  [3]  sudo systemctl restart nginx")
    print(f"       allowed={result.allowed}  requires_confirmation={result.requires_confirmation}")
    print(f"       {result.reason}")

    print(f"\n{'=' * 60}")
    print("  Three commands. Code decided.")
    print("  The LLM had no say in any of them.")
    print()
    print("  PyPI: pip install constraint-architecture")
    print("  GitHub: https://github.com/1nour2567/Constraint-Architecture")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo())
