"""
Bug-to-PR Autopilot Portia Plan

This module defines a Plan subclass for Portia that coordinates the
workflow from a bug report (GitHub issue or Sentry event) to a pull
request with a proposed fix. The plan is intentionally skeletal but
illustrates the key checkpoints and clarifications outlined in the
project specification. You should adapt this file when integrating
with real tools (GitHub, Slack, CI, etc.) by supplying concrete
implementations for the workspace, diff and other utilities. The
`final_output_summarizer` is imported from Portia's utilities to
compose human‑readable summaries for pull request bodies and Slack
messages.

To use this plan you will need to register it with the Portia SDK
alongside your configured tool suite. See the project README for
details.
"""

from __future__ import annotations

from typing import Any, Dict, List

try:
    from portia import Plan as PortiaPlan, step, clarification
except ImportError:
    # Mock decorators for the demo - in production, these would be from the actual Portia SDK
    class Plan:
        def __init__(self, name: str) -> None:
            self.name = name
            self.ctx: Dict[str, Any] = {}
    
    def step(name: str, after: str = None):
        def decorator(func):
            return func
        return decorator
    
    def clarification(name: str):
        def decorator(func):
            return func
        return decorator
    
    PortiaPlan = Plan

# For this demo, we'll use a base Plan class that simulates the Portia plan structure
Plan = PortiaPlan

# Mock final_output_summarizer for the demo
def final_output_summarizer(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a summary for the final output of the plan."""
    issue = data.get('issue', {})
    return {
        "pr_markdown": f"# Fix for {issue.get('title', 'Unknown issue')}\n\nThis PR addresses the issue with automated bug reproduction and fix generation.\n\n**Risk Score:** {data.get('risk', 1)}\n\n**Changes:**\n- Automated fix applied\n- Tests updated",
        "slack_blocks": [
            {
                "type": "section", 
                "text": {
                    "type": "mrkdwn",
                    "text": f"🤖 *Autopilot PR Ready*\n\nIssue: {issue.get('title', 'Unknown')}\nRisk: {data.get('risk', 1)}/5"
                }
            }
        ]
    }


class BugToPRPlan(Plan):
    """A Portia Plan that drives a failing test to a merged PR.

    Each method decorated with ``@step`` represents a discrete stage of
    execution. Clarifications provide human‑in‑the‑loop approval gates
    where the plan will pause and wait for a decision before
    proceeding. Internal state is stored in ``self.ctx`` so that
    information collected in one step is available to later steps.
    """

    def __init__(self, tools: Any, config: Dict[str, Any]) -> None:
        super().__init__(name="bug_to_pr")
        self.t = tools
        self.cfg = config
        # ``ctx`` acts as a scratch pad for the plan run. Avoid large
        # objects or sensitive data here, prefer storing references or
        # summaries.
        self.ctx: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Checkpoint: create-branch
    #
    # Gather context from the issue, ensure the target repository is
    # allowed and create a working branch for the fix.
    @step(name="create-branch")
    def create_branch(self, inputs: Dict[str, Any]) -> None:
        repo: str = inputs["repo"]
        base: str = inputs.get("base", "main")
        if repo not in self.cfg.get("allowlist", []):
            raise ValueError(f"Repository {repo} is not in the allowlist")
        issue = self.t.github.get_context(repo=repo, issue_url=inputs["issueUrl"])
        # Persist issue in context for later steps
        self.ctx["issue"] = issue
        base_sha = self.t.github.get_branch_sha(repo=repo, branch=base)
        # Derive branch name from issue number and slug
        branch_name = f"bugfix/{issue['number']}-{issue['slug']}"
        self.ctx["branch"] = branch_name
        self.t.github.create_branch(repo=repo, base_sha=base_sha, new_branch=branch_name)

    # ------------------------------------------------------------------
    # Checkpoint: push-failing-test
    #
    # Reproduce the error by running the project's test command. If
    # reproduction is not possible, generate a minimal failing test
    # instead. Always commit the failing test to the working branch.
    @step(name="push-failing-test")
    def push_failing_test(self, _inputs: Any) -> None:
        issue = self.ctx["issue"]
        # Create an isolated workspace at HEAD of branch
        ws = self.t.workspace.create_ephemeral(repo=issue["repo"], ref="HEAD")
        repro = self.t.workspace.run(ws, cmd=self.cfg["commands"]["repro"], timeout=240)
        if repro["status"] == "pass":
            # Reproduction did not trigger a failure; synthesize a
            # failing test from stack traces and blame information.
            ft = self.t.tests.generate_failing_test(issue=issue, workspace=ws)
            # Keep the trace for risk scoring and PR summary
            self.ctx["failing_trace"] = ft.get("trace")
            files = ft.get("files", [])
        else:
            # Use the existing failing test artifacts from reproduction
            self.ctx["failing_trace"] = repro.get("trace")
            files = repro.get("added_test_files", [])
        # Commit and push the failing test to the branch
        self.t.github.commit_and_push(
            repo=issue["repo"], branch=self.ctx["branch"], files=files
        )

    # ------------------------------------------------------------------
    # Clarification: approve-propose-fix
    #
    # Present a preview of the fix proposal and a risk score to the
    # approver. This method must return a serialisable payload that
    # will be consumed by the frontend and Slack integration.
    @clarification(name="approve-propose-fix")
    def approve_fix(self) -> Dict[str, Any]:
        return {
            "preview": self.t.diff.preview(self.ctx),
            "risk": self._risk_score(),
        }

    # ------------------------------------------------------------------
    # Checkpoint: propose-fix
    #
    # After the first approval gate, generate a minimal patch confined
    # to the target files, apply it locally, ensure the tests pass and
    # push the changes.
    @step(name="propose-fix", after="approve-propose-fix")
    def propose_fix(self, decision: Dict[str, Any]) -> None:
        if not decision.get("approved", False):
            raise ValueError("Fix proposal was not approved")
        patch = self.t.diff.generate(
            target_files=self._target_files(), failing_trace=self.ctx.get("failing_trace")
        )
        ws = self.t.workspace.create_ephemeral(repo=self.ctx["issue"]["repo"], ref=self.ctx["branch"])
        self.t.workspace.apply_patch(ws, patch)
        test = self.t.workspace.run(ws, cmd=self.cfg["commands"]["test"], timeout=300)
        if test["status"] != "pass":
            raise AssertionError("Local tests must pass after applying the patch")
        # Commit the proposed fix
        self.t.github.commit_and_push(
            repo=self.ctx["issue"]["repo"], branch=self.ctx["branch"], files=patch.get("files", [])
        )

    # ------------------------------------------------------------------
    # Checkpoint: open-pr
    #
    # Collect CI results and artifacts, compose a PR body via the
    # summariser and open a GitHub pull request. Also notify Slack.
    @step(name="open-pr")
    def open_pr(self, _inputs: Any) -> None:
        ci = self.t.ci.fetch_latest(repo=self.ctx["issue"]["repo"], branch=self.ctx["branch"])
        self.ctx["artifacts"] = ci.get("artifacts")
        pr_body = final_output_summarizer(
            {
                "issue": self.ctx["issue"],
                "risk": self._risk_score(),
                "ci": ci,
                "trace": self.ctx.get("failing_trace"),
                "diff": self.t.diff.summarize(self.ctx),
            }
        )
        pr = self.t.github.open_pr(
            repo=self.ctx["issue"]["repo"],
            title=f"Fix: {self.ctx['issue']['title']}",
            body=pr_body["pr_markdown"],
            head=self.ctx["branch"],
            base="main",
            labels=["autopilot", "needs-approval"],
        )
        # Persist PR number for later steps
        self.ctx["pr_number"] = pr["number"]
        # Notify Slack via configured channel
        self.t.slack.notify(
            channel=self.cfg["slack"]["channel"], blocks=pr_body.get("slack_blocks", [])
        )

    # ------------------------------------------------------------------
    # Clarification: approve-merge
    #
    # Show the latest CI summary and await approval for merging the PR.
    @clarification(name="approve-merge")
    def approve_merge(self) -> Dict[str, Any]:
        return {
            "ci": self.t.ci.summary(self.ctx["issue"]["repo"], self.ctx["branch"]),
        }

    # ------------------------------------------------------------------
    # Checkpoint: merge-pr
    #
    # If the approver gave the green light and CI passed, merge the
    # pull request. Otherwise revert to a test‑only PR.
    @step(name="merge-pr", after="approve-merge")
    def merge_pr(self, decision: Dict[str, Any]) -> None:
        if not decision.get("approved", False):
            # Label PR as needing human intervention
            self.t.github.label_pr(self.ctx["issue"]["repo"], self.ctx["pr_number"], ["needs-human"])
            return
        ci = self.t.ci.fetch_latest(repo=self.ctx["issue"]["repo"], branch=self.ctx["branch"])
        if ci.get("status") != "success":
            self._revert_to_test_only()
            return
        # Merge the PR via squash merge
        self.t.github.merge_pr(
            repo=self.ctx["issue"]["repo"], pr_number=self.ctx["pr_number"], method="squash"
        )

    # ------------------------------------------------------------------
    # Checkpoint: post-deploy-check
    #
    # Run a healthcheck (e.g. Lighthouse or custom endpoint) after
    # deployment and comment the result on the PR.
    @step(name="post-deploy-check")
    def post_deploy(self, _inputs: Any) -> None:
        result = self.t.healthcheck.run(self.cfg.get("health"))
        self.t.github.comment_pr(
            self.ctx["issue"]["repo"], self.ctx["pr_number"], f"Post-deploy: {result}"
        )

    # ------------------------------------------------------------------
    # Finalization
    #
    # Summarise the run for the UI and Slack. Always executed at the
    # end of the plan.
    @step(name="finalize")
    def finalize(self, _inputs: Any) -> Dict[str, Any]:
        digest = final_output_summarizer(
            {
                "issue": self.ctx.get("issue"),
                "risk": self._risk_score(),
                "artifacts": self.ctx.get("artifacts"),
                "pr": self.ctx.get("pr_number"),
            }
        )
        self.t.slack.notify(
            channel=self.cfg["slack"]["channel"], blocks=digest.get("slack_blocks", [])
        )
        return digest

    # ------------------------------------------------------------------
    # Helper methods
    #
    # In a real implementation these helpers would compute a risk score
    # based on diff size, criticality of files, test coverage changes,
    # etc.; derive a list of target files to modify; and revert the
    # branch to a failing test–only state if CI fails.
    def _risk_score(self) -> int:
        """Compute a risk score between 1 and 5 based on simple heuristics.

        The project specification describes a multifactor risk score that
        accounts for the number of files touched, the blast radius of
        changes, test coverage delta, recent churn and whether the change
        touches critical paths. In this demonstration we don't have
        access to those metrics so we approximate risk from the context
        collected during the plan run.

        Heuristic:

        * Start with a base risk of 1 (lowest).
        * If a failing trace was captured during reproduction or
          synthesis, bump the risk to 2 – a real failure suggests the
          change might be non‑trivial.
        * If more than one approval gate has already been passed (i.e.
          propose‑fix approved), bump the risk again to 3. This implies
          the fix touches at least one file and has passed local tests.

        The score is clamped between 1 and 5.
        """
        risk = 1
        # Presence of failing trace implies real bug reproduction
        if self.ctx.get("failing_trace"):
            risk += 1
        # If a PR has been opened the propose‑fix gate must have been
        # approved; treat this as increased blast radius
        if self.ctx.get("pr_number"):
            risk += 1
        # Clamp between 1 and 5
        return max(1, min(risk, 5))

    def _target_files(self) -> List[str]:
        """Determine which files are candidates for modification.

        In practice this would inspect the failing trace, blame
        information and recent commits to scope the patch. For now it
        returns an empty list, meaning the diff generator is free to
        propose changes anywhere. This method must return a list of
        relative file paths.
        """
        return []

    def _revert_to_test_only(self) -> None:
        """Revert the branch to contain only the failing test.

        This is invoked if CI fails after the fix proposal is pushed.
        A simple implementation could reset the branch to the commit
        immediately after pushing the failing test. Here we merely
        label the PR accordingly to highlight manual intervention.
        """
        self.t.github.label_pr(
            self.ctx["issue"]["repo"], self.ctx["pr_number"], ["needs-human", "test-only"]
        )