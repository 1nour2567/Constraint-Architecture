"""
Constraint Architecture — LLM reasons, code decides, audit keeps it traceable.

A production-grade abstract skeleton for AI agent systems with four
deterministic constraint layers wrapped around an LLM reasoning core.
Independently validated in two reference implementations spanning
security operations (Kylin-Agent) and embodied AI (Malio).

Quickstart
----------
    pip install constraint-architecture

    from constraint_architecture import ConstraintEngine, ValidationResult

    class MyGuardrails(ConstraintEngine):
        async def validate(self, context, reasoning_output):
            if "rm -rf" in reasoning_output.get("command", ""):
                return ValidationResult(
                    allowed=False,
                    reason="destructive command blocked",
                )
            return ValidationResult(allowed=True)

Layers
------
1. Reasoning (LLM)     — free reasoning, no execution authority
2. Constraints (Code)   — deterministic validation, unbypassable rules
3. Execution (Sandbox)  — tiered execution: auto / confirm / veto
4. Audit (Immutable)    — SHA256 chain, every step traceable

Reference Implementations
-------------------------
- Kylin-Agent: security-hardened ops agent on Kylin OS.
  16 red-team attacks, 0 breaches. 149 tests.
- Malio: embodied AI music agent. 800 particles, 9 physics systems.
- Quant Trading: daily frequency multi-factor strategy.
  L3 circuit-breaker (Ombudsman) enforcing Constraint Architecture in finance.

Copyright (c) 2026 Xu Renwu (续仁舞). MIT License.
"""

from constraint_architecture.skeleton import (
    # Version
    __version__,
    # Data
    ValidationResult,
    ExecutionResult,
    AuditEvent,
    PipelineContext,
    StateEvent,
    UserIntent,
    ScheduleTrigger,
    LoopTurn,
    AuthorizationResult,
    Identity,
    ToolDefinition,
    # Enums
    Tier,
    EventType,
    MemoryLevel,
    # Shell
    AgentShell,
    Shell,
    ToolResult,
    # Identity
    AgentIdentity,
    IdentityProvider,
    # Scheduler
    AgentScheduler,
    SchedulerProvider,
    # Memory
    AgentMemory,
    MemoryProvider,
    # Protocol
    AgentProtocol,
    AgentWire,
    # Tools
    AgentTools,
    ToolProvider,
    # Constraint layer ABCs
    ReasoningLayer,
    ConstraintEngine,
    ExecutionProxy,
    AuditTrail,
    # Constraint layer Protocols
    Reasoner,
    ConstraintValidator,
    Executor,
    Auditor,
    # Exceptions
    ConstraintError,
    VetoError,
    ExecutionRefusedError,
    AuditIntegrityError,
)

__all__ = [
    "__version__",
    "ValidationResult",
    "ExecutionResult",
    "AuditEvent",
    "PipelineContext",
    "StateEvent",
    "UserIntent",
    "ScheduleTrigger",
    "LoopTurn",
    "AuthorizationResult",
    "Identity",
    "ToolDefinition",
    "Tier",
    "EventType",
    "MemoryLevel",
    "AgentShell",
    "Shell",
    "ToolResult",
    "AgentIdentity",
    "IdentityProvider",
    "AgentScheduler",
    "SchedulerProvider",
    "AgentMemory",
    "MemoryProvider",
    "AgentProtocol",
    "AgentWire",
    "AgentTools",
    "ToolProvider",
    "ReasoningLayer",
    "ConstraintEngine",
    "ExecutionProxy",
    "AuditTrail",
    "Reasoner",
    "ConstraintValidator",
    "Executor",
    "Auditor",
    "ConstraintError",
    "VetoError",
    "ExecutionRefusedError",
    "AuditIntegrityError",
]
