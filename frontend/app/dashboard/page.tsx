'use client';

import { useState } from 'react';
import useSWR from 'swr';
import Link from 'next/link';
import { 
  PlusIcon, 
  ClockIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  ExclamationTriangleIcon,
  PlayIcon,
  ArrowRightIcon,
  RocketLaunchIcon,
  CodeBracketIcon,
  UserGroupIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import ThemeToggle from '../components/ThemeToggle';

interface Run {
  runId: string;
  issueUrl: string;
  repo: string;
  status: string;
}

const fetcher = (url: string) => fetch(url).then(res => res.json());

export default function Dashboard() {
  const [issueUrl, setIssueUrl] = useState('');
  const [repo, setRepo] = useState('');
  const [isSubmitting, setSubmitting] = useState(false);
  const [showCreateForm, setShowCreateForm] = useState(false);
  
  const { data: runs, mutate } = useSWR<Run[]>(
    '/api/runs',
    fetcher,
    { refreshInterval: 5000 }
  );

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!issueUrl || !repo) return;
    setSubmitting(true);
    try {
      await fetch('/api/runs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ issueUrl, repo }),
      });
      setIssueUrl('');
      setRepo('');
      setShowCreateForm(false);
      mutate();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircleIcon className="w-5 h-5 text-red-500" />;
      case 'running':
        return <PlayIcon className="w-5 h-5 text-blue-500" />;
      case 'paused':
        return <ExclamationTriangleIcon className="w-5 h-5 text-yellow-500" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusBadge = (status: string) => {
    const baseClasses = "status-badge";
    switch (status) {
      case 'completed':
        return `${baseClasses} status-success`;
      case 'failed':
        return `${baseClasses} status-error`;
      case 'running':
        return `${baseClasses} status-info`;
      case 'paused':
        return `${baseClasses} status-warning`;
      default:
        return `${baseClasses} status-pending`;
    }
  };

  const stats = {
    total: runs?.length || 0,
    completed: runs?.filter(r => r.status === 'completed').length || 0,
    running: runs?.filter(r => r.status === 'running').length || 0,
    failed: runs?.filter(r => r.status === 'failed').length || 0,
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <Link href="/" className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <RocketLaunchIcon className="w-4 h-4 text-white" />
                </div>
                <span className="text-xl font-bold text-gray-900 dark:text-white">Bug-to-PR Autopilot</span>
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/" className="btn btn-ghost">
                Home
              </Link>
              <ThemeToggle />
              <button 
                onClick={() => setShowCreateForm(true)}
                className="btn btn-primary flex items-center"
              >
                <PlusIcon className="w-5 h-5 mr-2" />
                New Run
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center">
              <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                <RocketLaunchIcon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Total Runs</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total}</p>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-lg">
                <CheckCircleIcon className="w-5 h-5 text-green-600 dark:text-green-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Completed</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.completed}</p>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                <PlayIcon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Running</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.running}</p>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <div className="p-3 bg-red-100 dark:bg-red-900/30 rounded-lg">
                <XCircleIcon className="w-5 h-5 text-red-600 dark:text-red-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Failed</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.failed}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Create Run Form */}
        {showCreateForm && (
          <div className="card mb-8 animate-fade-in">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Create New Run</h2>
              <button 
                onClick={() => setShowCreateForm(false)}
                className="btn btn-ghost"
              >
                <XCircleIcon className="w-5 h-5" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="form-label">GitHub Issue URL</label>
                  <input
                    type="text"
                    className="form-input"
                    value={issueUrl}
                    onChange={(e) => setIssueUrl(e.target.value)}
                    placeholder="https://github.com/your-org/repo/issues/123"
                    required
                  />
                </div>
                <div>
                  <label className="form-label">Repository</label>
                  <input
                    type="text"
                    className="form-input"
                    value={repo}
                    onChange={(e) => setRepo(e.target.value)}
                    placeholder="your-org/repo"
                    required
                  />
                </div>
              </div>
              
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="btn btn-ghost"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary flex items-center"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <div className="spinner mr-2"></div>
                      Creating...
                    </>
                  ) : (
                    <>
                      <PlusIcon className="w-5 h-5 mr-2" />
                      Create Run
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Runs List */}
        <div className="card">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Recent Runs</h2>
            {!showCreateForm && (
              <button 
                onClick={() => setShowCreateForm(true)}
                className="btn btn-primary flex items-center"
              >
                <PlusIcon className="w-5 h-5 mr-2" />
                New Run
              </button>
            )}
          </div>
          
          {runs && runs.length > 0 ? (
            <div className="space-y-4">
              {runs.map((run) => (
                <div key={run.runId} className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 hover:shadow-md transition-shadow dark:hover:shadow-lg dark:hover:shadow-gray-900/20">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      {getStatusIcon(run.status)}
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                          <Link href={`/runs/${run.runId}`} className="hover:text-blue-600 dark:hover:text-blue-400">
                            {run.issueUrl}
                          </Link>
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-300">{run.repo}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-4">
                      <span className={getStatusBadge(run.status)}>
                        {run.status}
                      </span>
                      <Link 
                        href={`/runs/${run.runId}`}
                        className="btn btn-ghost"
                      >
                        <ArrowRightIcon className="w-4 h-4" />
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                <RocketLaunchIcon className="w-8 h-8 text-gray-400 dark:text-gray-500" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No runs yet</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">Get started by creating your first automated bug-to-PR workflow.</p>
              <button 
                onClick={() => setShowCreateForm(true)}
                className="btn btn-primary flex items-center"
              >
                <PlusIcon className="w-5 h-5 mr-2" />
                Create Your First Run
              </button>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                        <div className="card card-hover">
                <div className="text-center">
                  <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <CodeBracketIcon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">View Documentation</h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-4">Learn how to integrate with your repositories and customize the workflow.</p>
                  <a 
                    href="https://github.com/ritik-prog/n8n-automation-templates-5000" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="btn btn-outline w-full"
                  >
                    Read Docs
                  </a>
                </div>
              </div>
              
              <div className="card card-hover">
                <div className="text-center">
                  <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <UserGroupIcon className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Team Setup</h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-4">Configure team permissions and approval workflows for your organization.</p>
                  <button 
                    onClick={() => alert('Team setup feature coming soon! Configure GitHub tokens and team permissions.')}
                    className="btn btn-outline w-full"
                  >
                    Configure
                  </button>
                </div>
              </div>
              
              <div className="card card-hover">
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <ChartBarIcon className="w-6 h-6 text-green-600 dark:text-green-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Analytics</h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-4">Track performance metrics and optimize your automation workflows.</p>
                  <button 
                    onClick={() => {
                      const stats = {
                        total: runs?.length || 0,
                        completed: runs?.filter(r => r.status === 'completed').length || 0,
                        running: runs?.filter(r => r.status === 'running').length || 0,
                        failed: runs?.filter(r => r.status === 'failed').length || 0,
                      };
                      alert(`Analytics:\nTotal Runs: ${stats.total}\nCompleted: ${stats.completed}\nRunning: ${stats.running}\nFailed: ${stats.failed}`);
                    }}
                    className="btn btn-outline w-full"
                  >
                    View Analytics
                  </button>
                </div>
              </div>
        </div>
      </div>
    </div>
  );
}
