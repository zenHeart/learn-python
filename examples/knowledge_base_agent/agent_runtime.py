from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor, TimeoutError as FutureTimeout
from dataclasses import dataclass, field
from typing import Any, Callable


class AgentRuntimeError(Exception):
    """Base error for deterministic teaching runtime failures."""


class ToolContractError(AgentRuntimeError):
    pass


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]
    idempotency_key: str | None = None


@dataclass(frozen=True)
class ToolResult:
    tool_call_id: str
    name: str
    status: str
    output: Any = None
    error: str | None = None
    replayed: bool = False


@dataclass(frozen=True)
class ToolSpec:
    name: str
    handler: Callable[[dict[str, Any]], Any]
    read_only: bool = True
    requires_approval: bool = False
    timeout_seconds: float = 0.25


@dataclass
class AgentState:
    run_id: str
    status: str = "created"
    steps: int = 0
    results_by_call_id: dict[str, ToolResult] = field(default_factory=dict)
    results_by_idempotency_key: dict[str, ToolResult] = field(default_factory=dict)


class ToolRegistry:
    def __init__(self, specs: list[ToolSpec] | None = None) -> None:
        self._specs: dict[str, ToolSpec] = {}
        for spec in specs or []:
            self.register(spec)

    def register(self, spec: ToolSpec) -> None:
        if not spec.name or not callable(spec.handler):
            raise ToolContractError("tool name and callable handler are required")
        if spec.timeout_seconds <= 0:
            raise ToolContractError("tool timeout must be positive")
        if not spec.read_only and not spec.requires_approval:
            raise ToolContractError("side-effect tools must require explicit approval")
        if spec.name in self._specs:
            raise ToolContractError(f"duplicate tool: {spec.name}")
        self._specs[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        try:
            return self._specs[name]
        except KeyError as exc:
            raise ToolContractError(f"unknown tool: {name}") from exc


def _run_with_deadline(spec: ToolSpec, arguments: dict[str, Any]) -> ToolResult | Any:
    executor = ThreadPoolExecutor(max_workers=1)
    future: Future[Any] = executor.submit(spec.handler, arguments)
    try:
        return future.result(timeout=spec.timeout_seconds)
    except FutureTimeout as exc:
        future.cancel()
        raise TimeoutError("tool deadline exceeded") from exc
    finally:
        # Do not wait for a timed-out handler in the request path. A real
        # service would cancel the downstream request through its context.
        executor.shutdown(wait=False, cancel_futures=True)


def execute_tool(
    call: ToolCall,
    registry: ToolRegistry,
    state: AgentState,
    *,
    approved: bool = False,
) -> ToolResult:
    """Execute once, or replay a result for the same call/idempotency key."""
    if not call.id or not call.name or not isinstance(call.arguments, dict):
        raise ToolContractError("tool call requires id, name and object arguments")
    if call.id in state.results_by_call_id:
        previous = state.results_by_call_id[call.id]
        return ToolResult(
            call.id,
            previous.name,
            previous.status,
            previous.output,
            previous.error,
            replayed=True,
        )

    if call.idempotency_key and call.idempotency_key in state.results_by_idempotency_key:
        previous = state.results_by_idempotency_key[call.idempotency_key]
        replay = ToolResult(
            call.id,
            previous.name,
            previous.status,
            previous.output,
            previous.error,
            replayed=True,
        )
        state.results_by_call_id[call.id] = replay
        return replay

    spec = registry.get(call.name)
    state.steps += 1
    if spec.requires_approval and not approved:
        result = ToolResult(call.id, call.name, "approval_required", error="human approval required")
    else:
        state.status = "tool_running"
        try:
            output = _run_with_deadline(spec, call.arguments)
        except TimeoutError as exc:
            result = ToolResult(call.id, call.name, "timeout", error=str(exc))
        except Exception as exc:  # fixture intentionally reports structured failure
            result = ToolResult(call.id, call.name, "failed", error=f"{type(exc).__name__}: {exc}")
        else:
            result = ToolResult(call.id, call.name, "ok", output=output)
        state.status = "tool_completed" if result.status == "ok" else "tool_failed"

    state.results_by_call_id[call.id] = result
    if call.idempotency_key:
        state.results_by_idempotency_key[call.idempotency_key] = result
    return result


def run_agent(
    model: Callable[[list[dict[str, Any]]], dict[str, Any]],
    registry: ToolRegistry,
    *,
    run_id: str = "fixture-run",
    max_steps: int = 3,
    approved: bool = False,
) -> dict[str, Any]:
    """Run a fake-model Agent loop with bounded steps and tool result ID alignment."""
    if max_steps < 1:
        raise ValueError("max_steps must be positive")
    state = AgentState(run_id=run_id)
    messages: list[dict[str, Any]] = []
    while state.steps < max_steps:
        response = model(messages)
        if not isinstance(response, dict):
            raise ToolContractError("model response must be an object")
        if response.get("type") == "final":
            state.status = "completed"
            return {
                "status": "completed",
                "answer": response.get("answer", ""),
                "steps": state.steps,
                "messages": messages,
            }
        if response.get("type") != "tool_call":
            raise ToolContractError("model must return final or tool_call")
        call = ToolCall(
            id=response.get("id", ""),
            name=response.get("name", ""),
            arguments=response.get("arguments", {}),
            idempotency_key=response.get("idempotency_key"),
        )
        result = execute_tool(call, registry, state, approved=approved)
        messages.append({"role": "assistant", "tool_call_id": call.id, "name": call.name})
        messages.append({
            "role": "tool",
            "tool_call_id": result.tool_call_id,
            "name": result.name,
            "status": result.status,
            "output": result.output,
            "error": result.error,
            "replayed": result.replayed,
        })
        if result.status in {"approval_required", "timeout", "failed"}:
            state.status = "stopped"
            return {
                "status": "stopped",
                "reason": result.status,
                "steps": state.steps,
                "messages": messages,
            }
    state.status = "stopped"
    return {
        "status": "stopped",
        "reason": "max_steps",
        "steps": state.steps,
        "messages": messages,
    }
