// Dynamic API route to interact with a single run. Forward GET and
// approval POST requests to the FastAPI backend. The backend URL is
// configured via NEXT_PUBLIC_API_BASE_URL environment variable.

import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const runId = params.id;
    console.log(`🔍 Fetching run details for: ${runId}`);
    
    // Fetch from backend with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
    
    const response = await fetch(`${BACKEND_URL}/runs/${runId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      console.error(`❌ Backend responded with status: ${response.status}`);
      if (response.status === 404) {
        return NextResponse.json({ error: 'Run not found' }, { status: 404 });
      }
      return NextResponse.json(
        { error: `Backend error: ${response.status}` },
        { status: response.status }
      );
    }
    
    const runData = await response.json();
    console.log(`✅ Successfully fetched run data for: ${runId}`);
    
    return NextResponse.json(runData);
    
  } catch (error) {
    console.error('❌ Error fetching run details:', error);
    
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        return NextResponse.json(
          { error: 'Request timeout - backend not responding' },
          { status: 408 }
        );
      }
      
      if (error.message.includes('fetch')) {
        return NextResponse.json(
          { error: 'Cannot connect to backend server' },
          { status: 503 }
        );
      }
    }
    
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  try {
    const body = await req.json();
    console.log(`🔍 Sending approval for run ${id}:`, body);
    
    // Expect body to contain gate and decision keys
    const res = await fetch(`${BACKEND_URL}/runs/${id}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    
    if (!res.ok) {
      const text = await res.text();
      console.error(`❌ Backend approval failed for run ${id}: ${res.status} - ${text}`);
      return new NextResponse(text, { status: res.status });
    }
    
    const data = await res.json();
    console.log(`✅ Successfully approved run ${id}`);
    return NextResponse.json(data);
  } catch (error) {
    console.error(`❌ Error approving run ${id}:`, error);
    return NextResponse.json(
      { error: 'Failed to connect to backend' },
      { status: 500 }
    );
  }
}