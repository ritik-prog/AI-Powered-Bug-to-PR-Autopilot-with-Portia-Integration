'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  ArrowRightIcon, 
  CheckCircleIcon, 
  CodeBracketIcon,
  CpuChipIcon,
  RocketLaunchIcon,
  ShieldCheckIcon,
  SparklesIcon,
  UserGroupIcon,
  WrenchScrewdriverIcon,
  ChartBarIcon,
  ClockIcon,
  DocumentCheckIcon
} from '@heroicons/react/24/outline';
import ThemeToggle from './components/ThemeToggle';

export default function LandingPage() {
  const [activeTab, setActiveTab] = useState('overview');

  const features = [
    {
      icon: <CodeBracketIcon className="w-5 h-5" />,
      title: "Automated Bug Detection",
      description: "Intelligent analysis of GitHub issues and Sentry events to identify and reproduce bugs automatically."
    },
    {
      icon: <CpuChipIcon className="w-5 h-5" />,
      title: "AI-Powered Fix Generation",
      description: "Leverage Portia AI to generate intelligent code fixes and test cases for identified issues."
    },
    {
      icon: <ShieldCheckIcon className="w-5 h-5" />,
      title: "Human-in-the-Loop Approval",
      description: "Two-stage approval process ensures quality control while maintaining automation efficiency."
    },
    {
      icon: <RocketLaunchIcon className="w-5 h-5" />,
      title: "Automated PR Creation",
      description: "Seamlessly create pull requests with comprehensive documentation and CI/CD integration."
    },
    {
      icon: <ChartBarIcon className="w-5 h-5" />,
      title: "Risk Assessment",
      description: "Advanced risk scoring based on code changes, test coverage, and impact analysis."
    },
    {
      icon: <DocumentCheckIcon className="w-5 h-5" />,
      title: "Post-Deployment Verification",
      description: "Automated health checks and monitoring after deployment to ensure system stability."
    }
  ];

  const workflowSteps = [
    {
      step: "01",
      title: "Issue Analysis",
      description: "Analyze GitHub issues or Sentry events to understand the problem scope and impact.",
      icon: <DocumentCheckIcon className="w-4 h-4" />
    },
    {
      step: "02", 
      title: "Bug Reproduction",
      description: "Automatically reproduce the failing scenario and create comprehensive test cases.",
      icon: <CodeBracketIcon className="w-4 h-4" />
    },
    {
      step: "03",
      title: "Fix Generation",
      description: "Generate intelligent code fixes using AI analysis and best practices.",
      icon: <SparklesIcon className="w-4 h-4" />
    },
    {
      step: "04",
      title: "Human Review",
      description: "Present the proposed fix for human approval with detailed risk assessment.",
      icon: <UserGroupIcon className="w-4 h-4" />
    },
    {
      step: "05",
      title: "PR Creation",
      description: "Create pull requests with comprehensive documentation and CI/CD integration.",
      icon: <RocketLaunchIcon className="w-4 h-4" />
    },
    {
      step: "06",
      title: "Deployment & Verification",
      description: "Monitor deployment and perform health checks to ensure system stability.",
      icon: <ShieldCheckIcon className="w-4 h-4" />
    }
  ];

  const benefits = [
    "Reduce bug resolution time by 80%",
    "Improve code quality with AI-powered analysis",
    "Maintain human oversight for critical decisions",
    "Automate repetitive development tasks",
    "Enhance team productivity and focus",
    "Reduce deployment risks with automated testing"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <RocketLaunchIcon className="w-4 h-4 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">Bug-to-PR Autopilot</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/dashboard" className="btn btn-ghost">
                Dashboard
              </Link>
              <ThemeToggle />
              <Link href="/dashboard" className="btn btn-primary">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="animate-fade-in">
              <h1 className="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-6">
                Automate Your
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  {" "}Bug-to-PR{" "}
                </span>
                Workflow
              </h1>
              <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
                Transform bug reports into pull requests automatically with AI-powered analysis, 
                human oversight, and seamless GitHub integration.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/dashboard" className="btn btn-primary text-lg px-8 py-4 flex items-center">
                  Start Automating
                  <ArrowRightIcon className="w-5 h-5 ml-2" />
                </Link>
                <button className="btn btn-outline text-lg px-8 py-4">
                  Watch Demo
                </button>
              </div>
            </div>
          </div>
        </div>
        
        {/* Floating elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-blue-200 dark:bg-blue-800 rounded-full opacity-20 animate-pulse-slow"></div>
        <div className="absolute top-40 right-20 w-16 h-16 bg-purple-200 dark:bg-purple-800 rounded-full opacity-20 animate-pulse-slow" style={{animationDelay: '1s'}}></div>
        <div className="absolute bottom-20 left-1/4 w-12 h-12 bg-green-200 dark:bg-green-800 rounded-full opacity-20 animate-pulse-slow" style={{animationDelay: '2s'}}></div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Powerful Features
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Everything you need to automate your development workflow with confidence
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="card card-hover animate-fade-in" style={{animationDelay: `${index * 0.1}s`}}>
                <div className="text-blue-600 dark:text-blue-400 mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">{feature.title}</h3>
                <p className="text-gray-600 dark:text-gray-300">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              A streamlined 6-step process that transforms bug reports into production-ready pull requests
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {workflowSteps.map((step, index) => (
              <div key={index} className="relative">
                <div className="card text-center animate-fade-in" style={{animationDelay: `${index * 0.1}s`}}>
                  <div className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-4">{step.step}</div>
                  <div className="text-blue-600 dark:text-blue-400 mb-4 flex justify-center">{step.icon}</div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">{step.title}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{step.description}</p>
                </div>
                {index < workflowSteps.length - 1 && (
                  <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                    <ArrowRightIcon className="w-6 h-6 text-gray-300 dark:text-gray-600" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="animate-fade-in">
              <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
                Why Choose Bug-to-PR Autopilot?
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
                Experience the future of automated development with our intelligent bug-to-PR pipeline.
              </p>
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <CheckCircleIcon className="w-4 h-4 text-green-500 flex-shrink-0" />
                    <span className="text-gray-700 dark:text-gray-300">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="animate-fade-in">
              <div className="card bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 border-0">
                <div className="text-center">
                  <WrenchScrewdriverIcon className="w-8 h-8 text-blue-600 dark:text-blue-400 mx-auto mb-6" />
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                    Ready to Transform Your Workflow?
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-6">
                    Join the future of automated development. Start your first automated bug-to-PR workflow today.
                  </p>
                  <Link href="/dashboard" className="mx-auto btn btn-primary flex justify-center items-center">
                    Get Started Now
                    <ArrowRightIcon className="w-5 h-5 ml-2" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="animate-fade-in">
            <h2 className="text-4xl font-bold text-white mb-6">
              Start Automating Today
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Transform your development workflow with intelligent automation. 
              No more manual bug fixes - let AI handle the heavy lifting.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/dashboard" className="btn bg-white text-blue-600 hover:bg-gray-100 text-lg px-8 py-4 flex items-center">
                Launch Dashboard
                <ArrowRightIcon className="w-5 h-5 ml-2" />
              </Link>
              <button className="btn border-2 border-white text-white hover:bg-white hover:text-blue-600 text-lg px-8 py-4">
                View Documentation
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <RocketLaunchIcon className="w-4 h-4 text-white" />
                </div>
                <span className="text-xl font-bold">Bug-to-PR Autopilot</span>
              </div>
              <p className="text-gray-400">
                Automating the future of software development with AI-powered bug resolution.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/dashboard" className="hover:text-white">Dashboard</Link></li>
                <li><a href="#" className="hover:text-white">Features</a></li>
                <li><a href="#" className="hover:text-white">Pricing</a></li>
                <li><a href="#" className="hover:text-white">API</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Resources</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Documentation</a></li>
                <li><a href="#" className="hover:text-white">Tutorials</a></li>
                <li><a href="#" className="hover:text-white">Blog</a></li>
                <li><a href="#" className="hover:text-white">Support</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">About</a></li>
                <li><a href="#" className="hover:text-white">Careers</a></li>
                <li><a href="#" className="hover:text-white">Privacy</a></li>
                <li><a href="#" className="hover:text-white">Terms</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>© 2024 Bug-to-PR Autopilot. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}