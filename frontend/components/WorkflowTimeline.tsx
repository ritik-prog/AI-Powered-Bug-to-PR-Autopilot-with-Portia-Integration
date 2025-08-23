'use client';

import { CheckCircleIcon, XCircleIcon, ClockIcon, ExclamationTriangleIcon, PlayIcon } from '@heroicons/react/24/outline';

interface WorkflowTimelineProps {
  plan: { name: string; status: string }[];
}

const stepNames = {
  'fetch-issue-details': '📋 Fetch Issue Details',
  'portia-analysis': '🔮 Portia Analysis',
  'analyze-repository': '📊 Analyze Repository',
  'create-branch': '🌿 Create Branch',
  'push-failing-test': '🧪 Push Failing Test',
  'propose-fix': '💡 Propose Fix',
  'open-pr': '🚀 Open Pull Request',
  'merge-pr': '🔀 Merge PR',
  'post-deploy-check': '✅ Post-Deploy Check',
  'finalize': '🎉 Finalize'
};

const stepDescriptions = {
  'fetch-issue-details': 'Fetching issue details from GitHub',
  'portia-analysis': 'Analyzing issue with Portia AI',
  'analyze-repository': 'Analyzing repository structure and context',
  'create-branch': 'Creating feature branch for the fix',
  'push-failing-test': 'Pushing test files to verify the issue',
  'propose-fix': 'Generating AI-powered fix proposal',
  'open-pr': 'Creating pull request with the fix',
  'merge-pr': 'Merging the pull request',
  'post-deploy-check': 'Verifying the fix after deployment',
  'finalize': 'Finalizing the workflow'
};

export function WorkflowTimeline({ plan }: WorkflowTimelineProps) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'failed':
      case 'rejected':
        return <XCircleIcon className="w-5 h-5 text-red-500" />;
      case 'running':
        return <PlayIcon className="w-5 h-5 text-blue-500 animate-pulse" />;
      case 'waiting':
        return <ExclamationTriangleIcon className="w-5 h-5 text-yellow-500" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'border-green-500 bg-green-50';
      case 'failed':
      case 'rejected':
        return 'border-red-500 bg-red-50';
      case 'running':
        return 'border-blue-500 bg-blue-50';
      case 'waiting':
        return 'border-yellow-500 bg-yellow-50';
      default:
        return 'border-gray-300 bg-gray-50';
    }
  };

  return (
    <div className="space-y-4">
      {plan.map((step, index) => (
        <div key={step.name} className="flex items-start space-x-4">
          <div className="flex-shrink-0">
            <div className={`w-10 h-10 rounded-full border-2 flex items-center justify-center ${getStatusColor(step.status)}`}>
              {getStatusIcon(step.status)}
            </div>
            {index < plan.length - 1 && (
              <div className="w-0.5 h-8 bg-gray-300 mx-auto mt-2"></div>
            )}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">
                {stepNames[step.name as keyof typeof stepNames] || step.name}
              </h3>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                step.status === 'success' ? 'bg-green-100 text-green-800' :
                step.status === 'failed' || step.status === 'rejected' ? 'bg-red-100 text-red-800' :
                step.status === 'running' ? 'bg-blue-100 text-blue-800' :
                step.status === 'waiting' ? 'bg-yellow-100 text-yellow-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {step.status.charAt(0).toUpperCase() + step.status.slice(1)}
              </span>
            </div>
            <p className="text-gray-600 mt-1">
              {stepDescriptions[step.name as keyof typeof stepDescriptions] || 
                (step.status === 'success' && 'Step completed successfully') ||
                (step.status === 'failed' && 'Step failed') ||
                (step.status === 'rejected' && 'Step was rejected') ||
                (step.status === 'running' && 'Step is currently running') ||
                (step.status === 'waiting' && 'Waiting for approval') ||
                (step.status === 'pending' && 'Step is pending') ||
                (step.status === 'cancelled' && 'Step was cancelled') ||
                'Step is pending'
              }
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
