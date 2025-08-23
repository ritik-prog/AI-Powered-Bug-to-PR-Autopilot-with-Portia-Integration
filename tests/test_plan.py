"""
Unit tests for the heuristics in the BugToPRPlan.

These tests exercise the private helper ``_risk_score`` to ensure
that the heuristic returns values in the expected range and responds
to context variables. Since the plan depends on external tools for
most of its behaviour, these tests only instantiate the plan and
manipulate its internal ``ctx`` dictionary directly.
"""

import types
from agent.plan import BugToPRPlan


class DummyTools:
    """Stand‑in object for the tools dependency.

    The plan only accesses ``tools`` via ``self.t`` for side effects
    outside of the risk scoring helper. We don't need to implement
    any methods for these tests.
    """
    pass


def test_risk_score_baseline() -> None:
    plan = BugToPRPlan(tools=DummyTools(), config={"allowlist": []})
    # No context set → baseline risk should be 1
    assert plan._risk_score() == 1


def test_risk_score_failing_trace() -> None:
    plan = BugToPRPlan(tools=DummyTools(), config={"allowlist": []})
    plan.ctx["failing_trace"] = "Error: something broke"
    # With failing trace risk increases to 2
    assert plan._risk_score() == 2


def test_risk_score_with_pr() -> None:
    plan = BugToPRPlan(tools=DummyTools(), config={"allowlist": []})
    plan.ctx["failing_trace"] = "oops"
    plan.ctx["pr_number"] = 42
    # With failing trace and PR number risk increases further to 3
    assert plan._risk_score() == 3