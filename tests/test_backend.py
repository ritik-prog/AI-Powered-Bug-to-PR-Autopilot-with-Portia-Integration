"""
Integration tests for the FastAPI backend and the in‑memory RunService.

These tests use FastAPI's TestClient to exercise the REST endpoints
exposed by ``autopilot_app.backend.main``. Since the RunService
executes the plan asynchronously, the tests include short sleeps
between API calls to allow the state machine to progress. The
durations are tuned to match the simulated delays in
``RunService._run_plan``.

To run these tests install pytest and run ``pytest`` from the
repository root. The tests do not require any external services.
"""

import time
import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_run_lifecycle_approval_flow() -> None:
    """End‑to‑end happy path: approve both gates and reach completion."""
    # Start a new run
    response = client.post(
        "/runs", json={"issueUrl": "https://example.com/issue/1", "repo": "your-org/demo-repo"}
    )
    assert response.status_code == 200
    run_id = response.json()["runId"]
    assert run_id

    # Allow the plan to progress to the first gate
    time.sleep(1.0)  # create-branch and push-failing-test should finish (0.1s each)
    data = client.get(f"/runs/{run_id}").json()
    # Check initial plan statuses
    statuses = {step["name"]: step["status"] for step in data["plan"]}
    assert statuses["create-branch"] == "success"
    assert statuses["push-failing-test"] == "success"
    assert statuses["propose-fix"] == "waiting"
    assert data["status"] == "paused"

    # Approve the propose-fix gate
    resp = client.post(
        f"/runs/{run_id}/approve",
        json={"gate": "propose-fix", "decision": "approve", "note": "looks good"},
    )
    assert resp.status_code == 200

    # Wait for the plan to process propose-fix and open-pr; next gate will pause
    time.sleep(1.0)
    data = client.get(f"/runs/{run_id}").json()
    statuses = {step["name"]: step["status"] for step in data["plan"]}
    assert statuses["propose-fix"] == "success"
    assert statuses["open-pr"] == "success"
    assert statuses["merge-pr"] == "waiting"
    assert data["status"] == "paused"

    # Approve the merge-pr gate
    resp = client.post(
        f"/runs/{run_id}/approve",
        json={"gate": "merge-pr", "decision": "approve", "note": "ship it"},
    )
    assert resp.status_code == 200

    # Wait for remaining steps to complete (post-deploy-check and finalize)
    time.sleep(0.5)
    data = client.get(f"/runs/{run_id}").json()
    statuses = {step["name"]: step["status"] for step in data["plan"]}
    assert data["status"] == "completed"
    # All steps should be successful
    assert all(s == "success" for s in statuses.values())


def test_run_lifecycle_rejection_flow() -> None:
    """Ensure that rejecting at the first gate aborts the run."""
    response = client.post(
        "/runs", json={"issueUrl": "https://example.com/issue/2", "repo": "your-org/demo-repo"}
    )
    run_id = response.json()["runId"]
    time.sleep(0.5)
    # Reject the propose-fix gate
    resp = client.post(
        f"/runs/{run_id}/approve",
        json={"gate": "propose-fix", "decision": "reject", "note": "needs work"},
    )
    assert resp.status_code == 200
    time.sleep(0.2)
    data = client.get(f"/runs/{run_id}").json()
    assert data["status"] == "failed"
    statuses = {step["name"]: step["status"] for step in data["plan"]}
    assert statuses["propose-fix"] == "rejected"
    # Subsequent steps should be cancelled
    assert statuses["open-pr"] == "cancelled"
    assert statuses["merge-pr"] == "cancelled"
    assert statuses["post-deploy-check"] == "cancelled"
    assert statuses["finalize"] == "cancelled"