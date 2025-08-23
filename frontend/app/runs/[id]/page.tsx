'use client';

import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import useSWR from 'swr';
import Link from 'next/link';
import { RunDetail } from '../../../types/run';
import { WorkflowTimeline } from '../../../components/WorkflowTimeline';
import { ApprovalGates } from '../../../components/ApprovalGates';

const fetcher = async (url: string) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout for long-running operations
  
  try {
    const response = await fetch(url, {
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timeout - backend is processing, please wait...');
    }
    throw error;
  }
};

export default function RunDetailPage() {
  const params = useParams();
  const runId = params.id as string;
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  // Fetch run details with live updates
  const { data: run, error, mutate } = useSWR<RunDetail>(
    `/api/runs/${runId}`,
    fetcher,
    {
      refreshInterval: (data) => {
        // Reduce refresh frequency during AI-intensive steps
        if (data?.status === 'running') {
          const currentStep = data.plan?.find(step => step.status === 'running');
          if (currentStep?.name === 'propose-fix' || currentStep?.name === 'portia-analysis') {
            return 3000; // Refresh every 3 seconds during AI steps
          }
        }
        return 1000; // Default refresh every second
      },
      errorRetryCount: 5,
      errorRetryInterval: 5000,
      onError: (error) => {
        console.error('Error fetching run details:', error);
      },
      onSuccess: () => {
        setLastUpdate(new Date());
      },
    }
  );

  // Auto-refresh when run is active
  useEffect(() => {
    if (run && ['created', 'running'].includes(run.status)) {
      const currentStep = run.plan?.find(step => step.status === 'running');
      const isAIStep = currentStep?.name === 'propose-fix' || currentStep?.name === 'portia-analysis';
      
      const interval = setInterval(() => {
        mutate();
      }, isAIStep ? 3000 : 1000); // Slower refresh during AI steps
      
      return () => clearInterval(interval);
    }
  }, [run, mutate]);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h1 className="text-2xl font-bold text-red-800 mb-4">Error Loading Run</h1>
            <p className="text-red-600 mb-4">
              {error.message.includes('Request timeout - backend is processing')
                ? 'The backend is currently processing your request. This may take a few minutes for AI-intensive operations. Please wait...'
                : error.message.includes('Request timeout')
                ? 'The request is taking longer than expected. The backend might be processing a complex operation.'
                : `Failed to load run details: ${error.message}`}
            </p>
            <button
              onClick={() => mutate()}
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!run) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow p-8">
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <span className="ml-3 text-lg">Loading run details...</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Check if we're in an AI-intensive step
  const currentStep = run.plan?.find(step => step.status === 'running');
  const isAIStep = currentStep?.name === 'propose-fix' || currentStep?.name === 'portia-analysis';
  


  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto space-y-6">
              {/* Header */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
            <Link 
                  href="/dashboard" 
                  className="mb-4 inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  Back to Dashboard
                </Link>
              <div className="flex items-center space-x-3">
                
                <h1 className="text-2xl font-bold text-gray-900">Run {run.runId.slice(0, 8)}...</h1>
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                  run.status === 'completed' ? 'bg-green-100 text-green-800' :
                  run.status === 'failed' ? 'bg-red-100 text-red-800' :
                  run.status === 'paused' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-blue-100 text-blue-800'
                }`}>
                  {run.status.charAt(0).toUpperCase() + run.status.slice(1)}
                </span>
              </div>
              <p className="text-gray-600 mt-2">
                Repository: <span className="font-medium">{run.repo}</span>
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Started: {new Date(run.startedAt).toLocaleString()}
                {lastUpdate && (
                  <span className="ml-4">
                    Last update: {lastUpdate.toLocaleTimeString()}
                  </span>
                )}
              </p>
              {isAIStep && (
                <div className="mt-2 p-2 bg-blue-50 border border-blue-200 rounded-md">
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                    <span className="text-sm text-blue-700">
                      AI processing in progress - this may take a few minutes...
                    </span>
                  </div>
                </div>
              )}
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">
                Progress
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {run.plan.filter(step => step.status === 'success').length}/{run.plan.length}
              </div>
              <div className="text-xs text-gray-500">
                steps completed
              </div>
            </div>
          </div>
        </div>

        {/* Workflow Timeline */}
        {/* Workflow Progress and Approval Gates */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
         

          {/* Workflow Progress - Left Side */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold text-gray-900">Workflow Progress</h2>
                  <div className="text-sm text-gray-500">
                    {run.plan.filter(step => step.status === 'success').length} of {run.plan.length} steps completed
                  </div>
                </div>
              </div>
              <div className="p-6">
                <WorkflowTimeline plan={run.plan} />
              </div>
            </div>
          </div>

           {/* Approval Gates - Right Side */}
           <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Approval Gates</h2>
                <p className="text-sm text-gray-600 mt-1">
                  {run.status === 'paused' 
                    ? 'Manual approval required to continue the workflow'
                    : 'All approvals have been completed or are not required'
                  }
                </p>
              </div>
              <div className="p-6">
                <ApprovalGates runId={run.runId} plan={run.plan} onApproval={mutate} runData={run} />
              </div>
            </div>
          </div>
        </div>

        {/* Run Details */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Run Details</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Issue Information */}
              <div className="space-y-4">
                <h3 className="text-md font-semibold text-gray-900">Issue Information</h3>
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="space-y-2">
                    <div>
                      <span className="text-sm font-medium text-gray-600">Repository:</span>
                      <p className="text-sm text-gray-900">{run.repo}</p>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-600">Issue URL:</span>
                      <a 
                        href={run.issueUrl} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-sm text-blue-600 hover:text-blue-800 break-all"
                      >
                        {run.issueUrl}
                      </a>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-600">Started:</span>
                      <p className="text-sm text-gray-900">{new Date(run.startedAt).toLocaleString()}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* GitHub Integration */}
              <div className="space-y-4">
                <h3 className="text-md font-semibold text-gray-900">GitHub Integration</h3>
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="space-y-2">
                    {run.github_data?.branch && (
                      <div>
                        <span className="text-sm font-medium text-gray-600">Branch:</span>
                        <p className="text-sm text-gray-900 font-mono">{run.github_data.branch}</p>
                      </div>
                    )}
                    {run.github_data?.pr_url && (
                      <div>
                        <span className="text-sm font-medium text-gray-600">Pull Request:</span>
                        <a 
                          href={run.github_data.pr_url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-sm text-blue-600 hover:text-blue-800 break-all"
                        >
                          #{run.github_data.pr_number} - {run.github_data.pr_title}
                        </a>
                      </div>
                    )}
                    {run.github_data?.portia_plan?.portia_plan_id && (
                      <div>
                        <span className="text-sm font-medium text-gray-600">Portia Plan:</span>
                        <p className="text-sm text-gray-900 font-mono">{run.github_data.portia_plan.portia_plan_id}</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}