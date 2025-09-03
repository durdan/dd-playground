import { NextRequest, NextResponse } from 'next/server'
import { SDLCPipeline } from '@/lib/graph/pipeline'
import { createInitialPipelineState } from '@/lib/graph/state'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { req_summary, repo_url, branch = 'main' } = body

    // Validate required fields
    if (!req_summary || !repo_url) {
      return NextResponse.json(
        { error: 'req_summary and repo_url are required' },
        { status: 400 }
      )
    }

    // Create initial pipeline state
    const initialState = createInitialPipelineState(req_summary, repo_url, branch)
    
    // Initialize the pipeline
    const pipeline = new SDLCPipeline({
      requirements: req_summary,
      status: 'planning'
    })

    // Execute the first step
    const result = await pipeline.executeStep(req_summary)

    return NextResponse.json({
      success: true,
      state: result.state,
      output: result.output,
      pipelineCompleted: pipeline.isCompleted(),
      hasErrors: pipeline.hasErrors()
    })

  } catch (error) {
    console.error('Pipeline execution error:', error)
    return NextResponse.json(
      { 
        error: 'Failed to execute pipeline',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}