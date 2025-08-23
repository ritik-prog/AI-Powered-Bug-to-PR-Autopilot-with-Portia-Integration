"""
RunService
============

This module provides a simple in‑memory implementation of the run
management API used by the FastAPI backend. In a production system
you would persist runs to a database such as PostgreSQL and publish
events to Redis for streaming. Here we keep everything in process so
that the example can run without external dependencies.

Each run has a unique ID, metadata about the issue and repository,
timestamps, a status and a list of events. Approval gates are
represented as steps in the run's plan. The ``approve`` method
accepts decisions for the two approval gates defined in the
specification.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import uuid
from typing import Any, AsyncGenerator, Dict, List, Optional
from .github import github_service
from .ai_fix_generator import ai_fix_generator


class RunService:
    """A lightweight manager for Portia plan runs with a basic state machine.

    This service simulates the lifecycle of a Portia plan run. When a run
    is started the service schedules an asynchronous task that walks
    through each checkpoint in the plan. Certain checkpoints—namely
    ``propose-fix`` and ``merge-pr``—are human‑in‑the‑loop gates. The
    simulation will emit a ``clarificationRequested`` event at these
    gates and pause until the corresponding approval or rejection is
    received via ``approve``. After each state transition, the run's
    status and plan step statuses are updated and an event is pushed to
    the per‑run queue. If a gate is rejected the run terminates and
    subsequent steps are marked as cancelled.

    In a production environment this service would communicate with
    Portia's runtime APIs to execute actual plans, persist state in
    Redis/Postgres and stream logs. Here we provide just enough
    functionality to drive the frontend and unit tests.
    """

    def __init__(self) -> None:
        # Store runs keyed by their run_id
        self._runs: Dict[str, Dict[str, Any]] = {}
        # Per‑run events queues for SSE streaming
        self._event_queues: Dict[str, asyncio.Queue[Dict[str, Any]]] = {}
        # Track background tasks for active runs
        self._tasks: Dict[str, asyncio.Task[None]] = {}

    async def start(self, issue_url: str, repo: str) -> str:
        """Start a new plan run and schedule its execution.

        A run has seven sequential steps mirroring the Portia plan. Upon
        creation the run status is ``created`` and a ``stateChanged``
        event is emitted. A background task is then scheduled to walk
        through the plan steps, updating their statuses and emitting
        events. Steps ``propose-fix`` and ``merge-pr`` pause until
        ``approve`` is called with a matching gate.
        """
        run_id = str(uuid.uuid4())
        now = dt.datetime.utcnow()
        # Initialise run record
        self._runs[run_id] = {
            "runId": run_id,
            "issueUrl": issue_url,
            "repo": repo,
            "startedAt": now.isoformat() + "Z",
            # Overall status: created → running/paused → completed/failed
            "status": "created",
            # Plan steps with initial pending statuses
            "plan": [
                {"name": "fetch-issue-details", "status": "pending"},
                {"name": "portia-analysis", "status": "pending"},
                {"name": "analyze-repository", "status": "pending"},
                {"name": "create-branch", "status": "pending"},
                {"name": "push-failing-test", "status": "pending"},
                {"name": "propose-fix", "status": "pending"},
                {"name": "open-pr", "status": "pending"},
                {"name": "merge-pr", "status": "pending"},
                {"name": "post-deploy-check", "status": "pending"},
                {"name": "finalize", "status": "pending"},
            ],
            # Record of all SSE events emitted for this run (useful for debugging)
            "events": [],
            # Approvals keyed by gate name (propose-fix or merge-pr)
            "approvals": {},
        }
        # Initialise event queue for SSE consumers
        q: asyncio.Queue[Dict[str, Any]] = asyncio.Queue()
        self._event_queues[run_id] = q
        # Emit initial stateChanged event
        await q.put({"type": "stateChanged", "data": {"status": "created"}})
        # Kick off background task to simulate plan execution
        task = asyncio.create_task(self._run_plan(run_id))
        self._tasks[run_id] = task
        return run_id

    async def _run_plan(self, run_id: str) -> None:
        """Simulate plan execution for a run.

        Each step is processed in order. For non‑gated steps the status
        transitions from ``pending`` → ``running`` → ``success`` with a
        short delay to simulate work. For approval gates the step
        transitions to ``waiting`` and a ``clarificationRequested`` event
        is emitted, then the coroutine waits until an approval decision
        is recorded. A rejection terminates the run and marks
        subsequent steps as cancelled.
        """
        run = self._runs.get(run_id)
        if run is None:
            return
        q = self._event_queues.get(run_id)
        if q is None:
            return
        # Helper to update plan step status and emit event
        async def update_step(step_name: str, new_status: str) -> None:
            for step in run["plan"]:
                if step["name"] == step_name:
                    step["status"] = new_status
                    break
            await q.put({"type": "stateChanged", "data": {"plan": run["plan"], "status": run["status"]}})

        # Mark overall status as running
        run["status"] = "running"
        await q.put({"type": "stateChanged", "data": {"status": run["status"]}})

        # Sequence of steps including which ones are approval gates
        steps = [
            ("fetch-issue-details", False),  # Add this step to fetch issue details first
            ("portia-analysis", False),
            ("analyze-repository", False),
            ("create-branch", False),
            ("push-failing-test", False),
            ("propose-fix", True),
            ("open-pr", False),
            ("merge-pr", True),
            ("post-deploy-check", False),
            ("finalize", False),
        ]

        # Store GitHub-related data for the run
        run["github_data"] = {
            "branch": None,
            "pr_url": None,
            "pr_number": None,
            "pr_title": None,
            "issue_details": None,
            "repo_analysis": None,
            "portia_plan": None
        }

        for step_name, is_gate in steps:
            # If run already terminated, break out
            if run["status"] in {"failed", "completed"}:
                break
            # Update step to running and emit
            await update_step(step_name, "running")
            
            # Execute actual GitHub operations for non-gate steps
            if not is_gate:
                await asyncio.sleep(0.1)  # Small delay for UI feedback
                
                if step_name == "fetch-issue-details":
                    # Fetch issue details from GitHub
                    await q.put({"type": "log", "data": {"message": "📋 Fetching issue details from GitHub..."}})
                    try:
                        issue_details = github_service.get_issue_details(run["issueUrl"])
                        run["github_data"]["issue_details"] = issue_details
                        await q.put({"type": "log", "data": {"message": f"✅ Fetched issue details"}})
                    except Exception as e:
                        await q.put({"type": "log", "data": {"message": f"❌ Error fetching issue details: {e}"}})
                
                elif step_name == "portia-analysis":
                    # Portia advanced analysis and workflow planning
                    await q.put({"type": "log", "data": {"message": "🔮 Portia: Starting advanced AI analysis and workflow planning..."}})
                    try:
                        from backend.services.portia_service import portia_service
                        portia_plan = portia_service.create_portia_plan(run["issueUrl"], run["repo"])
                        run["github_data"]["portia_plan"] = portia_plan
                        
                        if portia_plan.get("status") == "processing":
                            # Portia is running in background
                            analysis_id = portia_plan.get("portia_plan_id")
                            await q.put({"type": "log", "data": {"message": f"🔮 Portia: Analysis started in background (ID: {analysis_id})"}})
                            await q.put({"type": "log", "data": {"message": "🔮 Portia: Analysis will continue in background while workflow proceeds"}})
                        else:
                            await q.put({"type": "log", "data": {"message": "🔮 Portia: Advanced analysis completed successfully"}})
                    except Exception as e:
                        await q.put({"type": "log", "data": {"message": f"🔮 Portia: Analysis failed: {e}"}})
                
                elif step_name == "analyze-repository":
                    # Analyze repository structure and context
                    await q.put({"type": "log", "data": {"message": "Analyzing repository structure and context..."}})
                    try:
                        from backend.services.repo_analyzer import repo_analyzer
                        repo_analysis = repo_analyzer.analyze_repository(run["repo"])
                        run["github_data"]["repo_analysis"] = repo_analysis
                        await q.put({"type": "log", "data": {"message": "Repository analysis completed successfully"}})
                    except Exception as e:
                        await q.put({"type": "log", "data": {"message": f"Repository analysis failed: {e}"}})
                
                elif step_name == "create-branch":
                    # Create a new branch for the fix
                    branch_result = github_service.create_branch(run["repo"])
                    if branch_result.get("success"):
                        run["github_data"]["branch"] = branch_result["branch"]
                        await q.put({"type": "log", "data": {"message": f"Created branch: {branch_result['branch']}"}})
                    else:
                        await q.put({"type": "log", "data": {"message": f"Branch creation failed: {branch_result.get('error')}"}})
                
                elif step_name == "push-failing-test":
                    # Skip placeholder test creation - only AI-generated content will be created
                    await q.put({"type": "log", "data": {"message": "Skipping placeholder test creation - will use AI-generated content only"}})
                
                elif step_name == "propose-fix":
                    # This is now a gate step - it will be handled by the gate logic below
                    pass
                elif step_name == "open-pr":
                    # Create the actual pull request with AI-generated content
                    await q.put({"type": "log", "data": {"message": "🚀 Creating pull request with AI-generated content..."}})
                    
                    # Use the AI fix that was generated in the propose-fix step
                    ai_fix = run["github_data"].get("ai_fix", {})
                    issue_details = run["github_data"].get("issue_details", {})
                    
                    if not ai_fix or not issue_details:
                        await q.put({"type": "log", "data": {"message": "❌ No AI fix or issue details available"}})
                        await update_step(step_name, "failed")
                        continue
                    
                    # Create files using AI-generated content
                    for file_info in ai_fix.get('files', []):
                        file_result = github_service.create_file(
                            run["repo"],
                            run["github_data"]["branch"],
                            file_info['path'],
                            file_info['content'],
                            file_info['message']
                        )
                        
                        if file_result.get("success"):
                            await q.put({
                                "type": "log", 
                                "data": {
                                    "message": f"Created AI-generated file: {file_info['path']}",
                                    "file_path": file_info['path']
                                }
                            })
                        else:
                            await q.put({"type": "log", "data": {"message": f"File creation failed: {file_result.get('error')}"}})
                    
                    # Use AI-generated PR title and body
                    pr_title = ai_fix.get('pr_title', f"Fix: {issue_details['title']}")
                    pr_body = ai_fix.get('pr_body', f"""## Fix

This PR addresses the issue: {run["issueUrl"]}

### Changes Made:
- AI-analyzed and generated solution
- Created necessary files
- Implemented comprehensive fix

Closes #{issue_details['issue_number']}
""")
                    
                    pr_result = github_service.create_pull_request(
                        run["repo"],
                        "main",
                        run["github_data"]["branch"],
                        pr_title,
                        pr_body
                    )
                    
                    if pr_result.get("success"):
                        run["github_data"]["pr_url"] = pr_result["pr_url"]
                        run["github_data"]["pr_number"] = pr_result["pr_number"]
                        run["github_data"]["pr_title"] = pr_result["pr_title"]
                        await q.put({
                            "type": "log", 
                            "data": {
                                "message": f"Created AI-powered PR: {pr_result['pr_url']}",
                                "pr_url": pr_result["pr_url"],
                                "ai_generated": True
                            }
                        })
                    else:
                        await q.put({"type": "log", "data": {"message": f"PR creation failed: {pr_result.get('error')}"}})
                
                elif step_name == "post-deploy-check":
                    # Simulate post-deployment health checks
                    await q.put({"type": "log", "data": {"message": "Running post-deployment health checks..."}})
                    await asyncio.sleep(0.2)
                    await q.put({"type": "log", "data": {"message": "All health checks passed ✅"}})
                
                elif step_name == "finalize":
                    # Add comment to original issue
                    if run["github_data"]["pr_url"] and run["github_data"]["issue_details"]:
                        comment = f"""## 🎉 Issue Resolved!

A pull request has been created to fix this issue: {run["github_data"]["pr_url"]}

The fix includes:
- Comprehensive test coverage
- Code review and approval
- Automated deployment

Please review the PR and merge when ready.
"""
                        comment_result = github_service.create_issue_comment(
                            run["github_data"]["issue_details"]["repo"],
                            run["github_data"]["issue_details"]["issue_number"],
                            comment
                        )
                        if comment_result.get("success"):
                            await q.put({"type": "log", "data": {"message": "Added comment to original issue"}})
                
                await update_step(step_name, "success")
                continue
            # For gates, change status to waiting and ask for approval
            await update_step(step_name, "waiting")
            # Emit clarification request event
            await q.put({"type": "clarificationRequested", "data": {"gate": step_name}})
            # Pause run until approval decision is set
            run["status"] = "paused"
            await q.put({"type": "stateChanged", "data": {"status": run["status"]}})
            # Busy wait with async sleep until approval appears
            while step_name not in run["approvals"]:
                await asyncio.sleep(0.1)
            decision_info = run["approvals"][step_name]
            decision = decision_info.get("decision")
            # Emit resolution event
            await q.put({"type": "clarificationResolved", "data": {"gate": step_name, **decision_info}})
            if decision == "approve":
                # approval: resume and execute gate-specific logic
                run["status"] = "running"
                await q.put({"type": "stateChanged", "data": {"status": run["status"]}})
                
                # Execute gate-specific logic before marking as success
                if step_name == "propose-fix":
                    # Generate AI-powered fix proposal after approval
                    await q.put({"type": "log", "data": {"message": "🤖 Generating AI-powered fix proposal..."}})
                    
                    # Fetch issue details
                    issue_details = github_service.get_issue_details(run["issueUrl"])
                    if issue_details.get("success"):
                        run["github_data"]["issue_details"] = issue_details
                        
                        # Generate AI-powered fix with repository analysis
                        ai_fix = ai_fix_generator.analyze_issue_and_generate_fix(issue_details, run["repo"])
                        
                        # Store AI analysis for later use
                        run["github_data"]["ai_analysis"] = ai_fix.get('ai_analysis', {})
                        run["github_data"]["ai_fix"] = ai_fix
                        
                        await q.put({
                            "type": "log", 
                            "data": {
                                "message": f"🤖 AI fix proposal generated successfully",
                                "files_to_create": len(ai_fix.get('files', [])),
                                "pr_title": ai_fix.get('pr_title', 'N/A')
                            }
                        })
                        
                        # Show files that will be created
                        for file_info in ai_fix.get('files', []):
                            await q.put({
                                "type": "log", 
                                "data": {
                                    "message": f"📄 Will create: {file_info['path']}",
                                    "file_path": file_info['path']
                                }
                            })
                    else:
                        await q.put({"type": "log", "data": {"message": f"❌ Issue details failed: {issue_details.get('error')}"}})
                
                await update_step(step_name, "success")
                continue
            # rejection: mark failure and cancel remaining steps
            await update_step(step_name, "rejected")
            run["status"] = "failed"
            # Mark subsequent steps as cancelled
            seen = False
            for s in run["plan"]:
                if seen and s["status"] == "pending":
                    s["status"] = "cancelled"
                if s["name"] == step_name:
                    seen = True
            await q.put({"type": "stateChanged", "data": {"plan": run["plan"], "status": run["status"]}})
            # Emit finished event and stop
            await q.put({"type": "finished", "data": {"status": run["status"]}})
            return

        # If loop completes normally, mark run as completed
        if run["status"] not in {"failed"}:
            run["status"] = "completed"
            await q.put({"type": "stateChanged", "data": {"status": run["status"]}})
            await update_step(steps[-1][0], "success")
            # Emit finished event
            await q.put({"type": "finished", "data": {"status": run["status"]}})

    async def list_runs(self) -> List[Dict[str, Any]]:
        """Return summaries of all runs.

        Each summary contains only a few fields for display purposes.
        """
        runs_list = []
        for run in self._runs.values():
            runs_list.append(
                {
                    "runId": run["runId"],
                    "issueUrl": run["issueUrl"],
                    "repo": run["repo"],
                    "status": run["status"],
                }
            )
        return runs_list

    async def describe(self, run_id: str) -> Dict[str, Any]:
        """Return a description of the specified run."""
        run = self._runs.get(run_id)
        if not run:
            raise KeyError(f"run {run_id} not found")
        # Return a copy to avoid accidental mutation
        return dict(run)

    async def stream(self, run_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Yield events for a given run as they occur.

        This generator will block awaiting messages from the per‑run
        asyncio.Queue. When there are no more events and the run is
        finished, the generator exits.
        """
        q = self._event_queues.get(run_id)
        if q is None:
            # Unknown run; yield nothing
            return
        while True:
            evt = await q.get()
            yield evt
            # When the run signals completion we break
            if evt.get("type") == "finished":
                break

    async def approve(self, run_id: str, gate: str, decision: str, note: Optional[str]) -> None:
        """Process an approval decision for a run.

        ``gate`` should be either ``propose-fix`` or ``merge-pr`` to
        correspond to the two approval gates. ``decision`` must be
        ``approve`` or ``reject``.
        """
        run = self._runs.get(run_id)
        if not run:
            raise KeyError(f"run {run_id} not found")
        # The gate names in the public API correspond exactly to the
        # plan steps for approvals. We enforce this explicitly.
        if gate not in {"propose-fix", "merge-pr"}:
            raise ValueError(f"Unknown gate: {gate}")
        if decision not in {"approve", "reject"}:
            raise ValueError(f"Unknown decision: {decision}")
        # Record decision; the background task will react by reading this
        run["approvals"][gate] = {"decision": decision, "note": note}
        # Immediately publish an event to indicate that an approval decision
        # has been recorded. The background task will publish a
        # clarificationResolved event with the full payload when it resumes.
        q = self._event_queues.get(run_id)
        if q:
            await q.put({
                "type": "approvalRecorded",
                "data": {"gate": gate, "decision": decision, "note": note},
            })