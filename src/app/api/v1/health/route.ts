import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { config } from '@/lib/config';

export const dynamic = 'force-dynamic';

export async function GET() {
  const startTime = Date.now();
  let dbStatus: 'connected' | 'error' = 'error';

  try {
    await db.$queryRaw`SELECT 1`;
    dbStatus = 'connected';
  } catch {
    dbStatus = 'error';
  }

  const latency = Date.now() - startTime;
  const status = dbStatus === 'connected' ? 'healthy' : 'degraded';
  const httpStatus = status === 'healthy' ? 200 : 503;

  return NextResponse.json(
    {
      success: status === 'healthy',
      data: {
        status,
        version: config.app.version,
        name: config.app.name,
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        services: {
          database: dbStatus,
        },
        latency: `${latency}ms`,
      },
    },
    {
      status: httpStatus,
      headers: {
        'Cache-Control': 'no-cache, no-store',
        'X-Response-Time': `${latency}ms`,
      },
    }
  );
}
