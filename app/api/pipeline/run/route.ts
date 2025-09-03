import { NextRequest, NextResponse } from 'next/server'
import { SDLCPipeline } from '@/lib/graph/pipeline'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { req_summary, repo_url, branch = 'main' } = body

    console.log('Pipeline Run: Starting with requirements:', req_summary.substring(0, 100) + '...')

    // Validate required fields
    if (!req_summary || !repo_url) {
      return NextResponse.json(
        { error: 'req_summary and repo_url are required' },
        { status: 400 }
      )
    }

    // Initialize the pipeline
    const pipeline = new SDLCPipeline({
      requirements: req_summary,
      status: 'planning'
    })

    console.log('Pipeline Run: Starting planning phase...')
    // Execute planning phase
    const planResult = await pipeline.executeStep(req_summary)
    
    console.log('Pipeline Run: Planning completed, starting development...')
    // Execute development phase
    const devResult = await pipeline.executeStep('')
    
    console.log('Pipeline Run: Development completed, starting review...')
    // Execute review phase  
    const reviewResult = await pipeline.executeStep('')

    console.log('Pipeline Run: All phases completed')

    // Create summary
    const summary = `Pipeline completed successfully! 

✅ Planning Phase: Completed
✅ Development Phase: Completed  
✅ Review Phase: Completed

Final Status: ${reviewResult.state.status}
Repository: ${repo_url}
Branch: ${branch}

The pipeline has successfully analyzed your requirements, generated implementation code, and completed a thorough code review.`

    return NextResponse.json({
      success: true,
      finalState: reviewResult.state,
      summary,
      planOutput: planResult.output,
      devOutput: devResult.output,
      reviewOutput: reviewResult.output,
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