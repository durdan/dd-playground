import { NextRequest, NextResponse } from 'next/server'
import { LangGraphSDLCPipeline } from '@/lib/graph/langgraph-pipeline'

export async function POST(request: NextRequest) {
  const body = await request.json()
  const { req_summary, repo_url, branch = 'main' } = body

  if (!req_summary || !repo_url) {
    return NextResponse.json(
      { error: 'req_summary and repo_url are required' },
      { status: 400 }
    )
  }

  // Create a readable stream for real-time updates
  const encoder = new TextEncoder()
  const stream = new ReadableStream({
    async start(controller) {
      const sendUpdate = (stage: string, status: string, output?: string) => {
        const data = JSON.stringify({ 
          stage, 
          status, 
          output, 
          timestamp: new Date().toISOString(),
          source: 'langgraph'
        })
        controller.enqueue(encoder.encode(`data: ${data}\n\n`))
        console.log(`LangGraph Stream Update: ${stage} -> ${status}`)
      }

      try {
        // Initialize real LangGraph pipeline with OpenAI streaming
        const pipeline = new LangGraphSDLCPipeline(sendUpdate)

        console.log('LangGraph Pipeline: Starting execution...')
        
        // Execute the entire LangGraph workflow
        const result = await pipeline.execute(req_summary)
        
        console.log('LangGraph Pipeline: Execution completed')
        sendUpdate('complete', 'completed', 'LangGraph pipeline execution finished')

      } catch (error) {
        console.error('LangGraph Pipeline Error:', error)
        const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
        sendUpdate('pipeline', 'error', errorMessage)
      } finally {
        controller.close()
      }
    }
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  })
}