// API route for runs
// This route proxies requests from the Next.js frontend to the FastAPI
// backend. At runtime ``process.env.NEXT_PUBLIC_API_BASE_URL`` should be
// defined with the URL of the backend, e.g. ``http://localhost:8000``.

import { NextRequest, NextResponse } from 'next/server';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Mock data for development
const mockRuns = [
  {
    runId: 'run_123456789',
    issueUrl: 'https://github.com/example/repo/issues/123',
    repo: 'example/repo',
    status: 'completed'
  },
  {
    runId: 'run_987654321',
    issueUrl: 'https://github.com/example/repo/issues/456',
    repo: 'example/repo',
    status: 'running'
  }
];

export async function GET() {
  try {
    const res = await fetch(`${API_BASE}/runs`);
    if (!res.ok) {
      // Return mock data if backend is not available
      return NextResponse.json(mockRuns);
    }
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    // Return mock data if connection fails
    return NextResponse.json(mockRuns);
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const res = await fetch(`${API_BASE}/runs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const text = await res.text();
      return new NextResponse(text, { status: res.status });
    }
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    // Return success response with mock data if backend is not available
    const mockRun = {
      runId: `run_${Date.now()}`,
      issueUrl: body.issueUrl,
      repo: body.repo,
      status: 'pending'
    };
    return NextResponse.json(mockRun);
  }
}