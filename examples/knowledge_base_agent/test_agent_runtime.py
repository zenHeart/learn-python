from __future__ import annotations

import time
import unittest

from agent_runtime import (
    AgentRuntimeError,
    ToolCall,
    ToolContractError,
    ToolRegistry,
    ToolSpec,
    AgentState,
    execute_tool,
    run_agent,
)


class AgentRuntimeTests(unittest.TestCase):
    def test_tool_call_id_is_preserved(self):
        registry = ToolRegistry([ToolSpec("lookup", lambda args: {"value": args["q"]})])

        def model(messages):
            return {"type": "tool_call", "id": "call-1", "name": "lookup", "arguments": {"q": "acl"}}

        result = execute_tool(ToolCall("call-1", "lookup", {"q": "acl"}), registry, AgentState("run"))
        self.assertEqual(result.tool_call_id, "call-1")
        self.assertEqual(result.status, "ok")

    def test_missing_tool_call_id_is_rejected(self):
        registry = ToolRegistry([ToolSpec("lookup", lambda args: "ok")])
        with self.assertRaises(ToolContractError):
            execute_tool(ToolCall("", "lookup", {}), registry, AgentState("run"))

    def test_idempotency_replays_without_second_side_effect(self):
        calls = []
        registry = ToolRegistry([ToolSpec("write", lambda args: calls.append(args["value"]) or "written", read_only=False)])
        state = AgentState("run")
        first = execute_tool(ToolCall("call-1", "write", {"value": "x"}, "key-1"), registry, state, approved=True)
        second = execute_tool(ToolCall("call-2", "write", {"value": "x"}, "key-1"), registry, state, approved=True)
        self.assertEqual(first.status, "ok")
        self.assertTrue(second.replayed)
        self.assertEqual(calls, ["x"])

    def test_write_tool_requires_approval(self):
        calls = []
        registry = ToolRegistry([ToolSpec("write", lambda args: calls.append(1), read_only=False, requires_approval=True)])
        result = execute_tool(ToolCall("call-1", "write", {}), registry, AgentState("run"))
        self.assertEqual(result.status, "approval_required")
        self.assertEqual(calls, [])

    def test_side_effect_tool_cannot_skip_approval_declaration(self):
        with self.assertRaises(ToolContractError):
            ToolRegistry([ToolSpec("unsafe-write", lambda args: None, read_only=False)])

    def test_timeout_stops_before_unbounded_retry(self):
        registry = ToolRegistry([ToolSpec("slow", lambda args: time.sleep(0.2), timeout_seconds=0.01)])
        result = execute_tool(ToolCall("call-1", "slow", {}), registry, AgentState("run"))
        self.assertEqual(result.status, "timeout")

    def test_max_steps_stops_loop(self):
        registry = ToolRegistry([ToolSpec("lookup", lambda args: "ok")])

        def model(messages):
            return {"type": "tool_call", "id": f"call-{len(messages)}", "name": "lookup", "arguments": {}}

        result = run_agent(model, registry, max_steps=2)
        self.assertEqual(result["status"], "stopped")
        self.assertEqual(result["reason"], "max_steps")
        self.assertEqual(result["steps"], 2)

    def test_tool_error_stops_safely(self):
        registry = ToolRegistry([ToolSpec("lookup", lambda args: 1 / 0)])

        def model(messages):
            return {"type": "tool_call", "id": "call-1", "name": "lookup", "arguments": {}}

        result = run_agent(model, registry)
        self.assertEqual(result["status"], "stopped")
        self.assertEqual(result["reason"], "failed")
        self.assertIn("ZeroDivisionError", result["messages"][-1]["error"])

    def test_final_response_after_tool(self):
        registry = ToolRegistry([ToolSpec("lookup", lambda args: {"answer": "evidence"})])
        responses = iter([
            {"type": "tool_call", "id": "call-1", "name": "lookup", "arguments": {}},
            {"type": "final", "answer": "grounded"},
        ])
        result = run_agent(lambda messages: next(responses), registry)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["answer"], "grounded")
        self.assertEqual(result["messages"][1]["tool_call_id"], "call-1")


if __name__ == "__main__":
    unittest.main()
