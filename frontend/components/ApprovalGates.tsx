'use client';

import { useState } from 'react';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

interface ApprovalGatesProps {
  runId: string;
  plan: { name: string; status: string }[];
  onApproval: () => void;
  runData?: any; // Add run data to access ai_fix information
}

export function ApprovalGates({ runId, plan, onApproval, runData }: ApprovalGatesProps) {
  const [loadingGate, setLoadingGate] = useState<string | null>(null);
  const [approvalNote, setApprovalNote] = useState('');



  async function sendApproval(gate: string, decision: 'approve' | 'reject') {
    setLoadingGate(gate);
    let retryCount = 0;
    const maxRetries = 3;
    
    while (retryCount < maxRetries) {
      try {
        console.log(`Attempting approval (attempt ${retryCount + 1}/${maxRetries})`);
        
        const response = await fetch(`/api/runs/${runId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ gate, decision, note: approvalNote }),
        });

        if (!response.ok) {
          throw new Error(`Approval failed: ${response.status}`);
        }

        setApprovalNote('');
        
        // Wait for the workflow to progress to the next step with better retry logic
        let statusAttempts = 0;
        const maxStatusAttempts = 45; // Wait up to 45 seconds
        
        while (statusAttempts < maxStatusAttempts) {
          await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second between checks
          
          try {
            const updatedRun = await fetch(`/api/runs/${runId}`).then(r => r.json());
            
            // Check if the approved gate is no longer waiting
            const approvedStep = updatedRun.plan?.find((step: any) => step.name === gate);
            if (approvedStep && approvedStep.status !== 'waiting') {
              // Gate has been processed, stop loading
              onApproval();
              return; // Success, exit the function
            }
            
            // Check if there's a new waiting step (workflow progressed)
            const waitingSteps = updatedRun.plan?.filter((step: any) => 
              step.status === 'waiting' && ['propose-fix', 'merge-pr'].includes(step.name)
            );
            
            if (waitingSteps.length === 0 || !waitingSteps.find((step: any) => step.name === gate)) {
              // No more waiting steps or this gate is no longer waiting
              onApproval();
              return; // Success, exit the function
            }
            
            statusAttempts++;
          } catch (statusError) {
            console.error('Error checking workflow status:', statusError);
            statusAttempts++;
          }
        }
        
        // If we've waited long enough, stop loading anyway
        onApproval();
        return; // Success, exit the function
        
      } catch (error) {
        console.error(`Approval attempt ${retryCount + 1} failed:`, error);
        retryCount++;
        
        if (retryCount < maxRetries) {
          // Wait before retrying (exponential backoff)
          const waitTime = Math.pow(2, retryCount) * 1000; // 2s, 4s, 8s
          console.log(`Waiting ${waitTime}ms before retry...`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
        } else {
          // All retries failed
          console.error('All approval attempts failed');
          alert(`Approval failed after ${maxRetries} attempts. Please try again or contact support.`);
        }
      }
    }
    
    setLoadingGate(null);
  }

  // Find waiting gates
  const waitingGates = plan.filter(step => 
    step.status === 'waiting' && ['propose-fix', 'merge-pr'].includes(step.name)
  );

  if (waitingGates.length === 0) {
    return (
      <div className="text-center py-8">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircleIcon className="w-8 h-8 text-green-600" />
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Approval Required</h3>
        <p className="text-gray-600">All steps are proceeding automatically or have been completed.</p>
        <div className="mt-4 text-sm text-gray-500">
          The workflow will continue automatically through all remaining steps.
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {waitingGates.map((gateStep) => {
        const gate = gateStep.name;
        return (
          <div key={gate} className="border border-yellow-200 bg-yellow-50 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-lg font-semibold text-gray-900">
                {gate === 'propose-fix' ? '💡 Propose Fix' : '🔀 Merge PR'}
              </h4>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                Waiting for Approval
              </span>
            </div>
            
            <div className="space-y-4">
              {/* Show proposed fix details for propose-fix gate */}
              {gate === 'propose-fix' && (
                <div>
                  {runData?.github_data?.ai_fix ? (
                    <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                      <h5 className="font-medium text-blue-900 mb-3">📋 Proposed Fix Details</h5>
                      
                      {/* PR Title */}
                      {runData.github_data.ai_fix.pr_title && (
                        <div className="mb-3">
                          <h6 className="text-sm font-medium text-blue-800 mb-1">PR Title:</h6>
                          <p className="text-sm text-blue-700 bg-white p-2 rounded border">
                            {runData.github_data.ai_fix.pr_title}
                          </p>
                        </div>
                      )}
                      
                      {/* Files to be changed */}
                      {runData.github_data.ai_fix.files && runData.github_data.ai_fix.files.length > 0 && (
                        <div className="mb-3">
                          <h6 className="text-sm font-medium text-blue-800 mb-2">Files to be modified:</h6>
                          <div className="space-y-2">
                            {runData.github_data.ai_fix.files.map((file: any, index: number) => (
                              <div key={index} className="bg-white p-3 rounded border">
                                <div className="flex items-center justify-between mb-2">
                                  <span className="text-sm font-medium text-blue-800">
                                    📄 {file.path}
                                  </span>
                                  <span className="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded">
                                    {file.message || 'New file'}
                                  </span>
                                </div>
                                {file.content && (
                                  <details className="mt-2">
                                    <summary className="text-xs text-blue-600 cursor-pointer hover:text-blue-800">
                                      View content preview
                                    </summary>
                                    <pre className="text-xs text-gray-700 bg-gray-50 p-2 rounded mt-1 overflow-x-auto max-h-32 overflow-y-auto">
                                      {file.content.length > 500 
                                        ? file.content.substring(0, 500) + '...'
                                        : file.content
                                      }
                                    </pre>
                                  </details>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {/* Fix Type */}
                      {runData.github_data.ai_fix.fix_type && (
                        <div className="mb-3">
                          <h6 className="text-sm font-medium text-blue-800 mb-1">Fix Type:</h6>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            {runData.github_data.ai_fix.fix_type}
                          </span>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                      <div className="flex items-center mb-3">
                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                          <span className="text-lg">🤖</span>
                        </div>
                        <div>
                          <h5 className="font-medium text-blue-900">AI Fix Generation Process</h5>
                          <p className="text-sm text-blue-700">Ready to analyze and generate a fix</p>
                        </div>
                      </div>
                      
                      <div className="bg-white p-3 rounded border border-blue-200 mb-3">
                        <h6 className="text-sm font-medium text-blue-800 mb-2">What happens when you approve:</h6>
                        <ul className="text-xs text-blue-700 space-y-1">
                          <li>• 🔍 AI analyzes the GitHub issue</li>
                          <li>• 📊 Repository structure analysis</li>
                          <li>• 💡 Intelligent fix generation</li>
                          <li>• 📝 Creates necessary files/changes</li>
                          <li>• 🎯 Prepares pull request</li>
                        </ul>
                      </div>
                      
                      <div className="text-xs text-blue-600">
                        <strong>Note:</strong> Fix details will be generated after approval. The AI will analyze the issue and create the appropriate solution.
                      </div>
                    </div>
                  )}
                </div>
              )}
              
              <div className="bg-white rounded-md p-4 border border-yellow-200">
                <p className="text-sm text-gray-700 mb-3">
                  {gate === 'propose-fix' 
                    ? runData?.github_data?.ai_fix 
                      ? 'Review the proposed fix above and approve or reject the changes.'
                      : 'Approve to start AI-powered fix generation, or reject to skip this step.'
                    : 'Review the pull request and approve or reject the merge.'
                  }
                </p>
                <textarea
                  placeholder="Add a note (optional)"
                  value={approvalNote}
                  onChange={(e) => setApprovalNote(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows={3}
                />
              </div>
              
              <div className="flex space-x-3">
                <button
                  className="flex-1 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                  disabled={loadingGate === gate}
                  onClick={() => sendApproval(gate, 'approve')}
                >
                  {loadingGate === gate ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Processing...
                    </>
                  ) : (
                    <>
                      <CheckCircleIcon className="w-4 h-4 mr-2" />
                      Approve
                    </>
                  )}
                </button>
                
                <button
                  className="flex-1 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                  disabled={loadingGate === gate}
                  onClick={() => sendApproval(gate, 'reject')}
                >
                  {loadingGate === gate ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Processing...
                    </>
                  ) : (
                    <>
                      <XCircleIcon className="w-4 h-4 mr-2" />
                      Reject
                    </>
                  )}
                </button>
              </div>
              
              {loadingGate === gate && (
                <div className="mt-3 p-3 bg-blue-50 border border-blue-200 rounded-md">
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                    <span className="text-sm text-blue-700">
                      Processing approval and waiting for workflow to progress...
                    </span>
                  </div>
                  <div className="mt-2 text-xs text-blue-600">
                    This may take a few moments. The system will automatically retry if needed.
                  </div>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
