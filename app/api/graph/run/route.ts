import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { createGraph } from '../../../lib/graph/tools';

// Define the Zod schema for the PipelineState input
const PipelineStateSchema = z.object({
  state: z.string(),
});

export default async function handler(req: NextRequest) {
  if (req.method !== 'POST') {
    return new NextResponse('Method Not Allowed', { status: 405 });
  }

  try {
    const body = await req.json();
    const validatedBody = PipelineStateSchema.parse(body);
    const graph = createGraph();
    const finalState = await graph.invoke(validatedBody.state);
    return new NextResponse(JSON.stringify({ finalState }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return new NextResponse(JSON.stringify({ error: 'Invalid input format' }), {
        status: 400,
        headers: {
          'Content-Type': 'application/json',
        },
      });
    }
    // Handle other errors
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}