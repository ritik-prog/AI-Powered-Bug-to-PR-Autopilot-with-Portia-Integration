export interface RunDetail {
  runId: string;
  issueUrl: string;
  repo: string;
  startedAt: string;
  status: string;
  plan: { name: string; status: string }[];
  approvals: Record<string, any>;
  github_data?: {
    portia_plan?: {
      portia_plan_id: string;
      status: string;
      portia_features_used: string[];
    };
    branch?: string;
    pr_url?: string;
    pr_number?: number;
    pr_title?: string;
    issue_details?: any;
    repo_analysis?: any;
    ai_fix?: {
      files?: Array<{
        path: string;
        content: string;
        message: string;
      }>;
      pr_title?: string;
      pr_body?: string;
      fix_type?: string;
    };
  };
}
