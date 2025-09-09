import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { LangGraphPipeline, PipelineState } from '../../../lib/graph/langgraph-pipeline';

// Define the Zod schema for PipelineState validation
const pipelineStateSchema = z.object({
  currentState: z.string(),
  data: z.record(z.any())
});

export const config = {
  runtime: 'nodejs'
};

export default async function handler(req: NextRequest) {
  if (req.method !== 'POST') {
    return new NextResponse('Method Not Allowed', { status: 405 });
  }

  try {
    const requestBody = await req.json();
    const validatedState = pipelineStateSchema.parse(requestBody);

    const graph = new LangGraphPipeline();
    const finalState = await graph.invoke(validatedState);

    return new NextResponse(JSON.stringify(finalState), {
      status: 200,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    return new NextResponse(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
}
