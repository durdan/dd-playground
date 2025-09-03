'use client'

import { useState, useEffect } from 'react'
import WorkflowVisualizer, { WorkflowNode, WorkflowConnection } from '../components/WorkflowVisualizer'
import GitConnectionPanel from '../components/GitConnectionPanel'
import CLIProgressPanel from '../components/CLIProgressPanel'

export default function Home() {
  const [requirements, setRequirements] = useState('')
  const [repoUrl, setRepoUrl] = useState('')
  const [branch, setBranch] = useState('main')
  const [isRunning, setIsRunning] = useState(false)
  const [pipelineState, setPipelineState] = useState<any>(null)
  const [output, setOutput] = useState('')
  const [currentStage, setCurrentStage] = useState('')
  const [stageHistory, setStageHistory] = useState<Array<{stage: string, status: 'completed' | 'current' | 'pending', output?: string}>>([])
  const [error, setError] = useState('')
  const [workflowNodes, setWorkflowNodes] = useState<WorkflowNode[]>([])
  const [workflowConnections, setWorkflowConnections] = useState<WorkflowConnection[]>([])
  const [selectedNode, setSelectedNode] = useState<string | null>(null)
  const [availableBranches, setAvailableBranches] = useState<string[]>([])
  const [eventSource, setEventSource] = useState<EventSource | null>(null)

  // Initialize workflow visualization
  useEffect(() => {
    const initialNodes: WorkflowNode[] = [
      {
        id: 'start',
        title: 'Start',
        subtitle: 'Input Requirements',
        icon: 'start',
        status: 'pending',
        position: { x: 40, y: 200 },
        color: 'bg-blue-600'
      },
      {
        id: 'planning',
        title: 'Planning Agent',
        subtitle: 'Analyze & Plan',
        icon: 'planning',
        status: 'pending',
        position: { x: 220, y: 120 },
        color: 'bg-purple-600'
      },
      {
        id: 'development',
        title: 'Development Agent',
        subtitle: 'Generate Code',
        icon: 'development',
        status: 'pending',
        position: { x: 400, y: 200 },
        color: 'bg-green-600'
      },
      {
        id: 'review',
        title: 'Review Agent',
        subtitle: 'Code Review',
        icon: 'review',
        status: 'pending',
        position: { x: 580, y: 280 },
        color: 'bg-orange-600'
      },
      {
        id: 'complete',
        title: 'Complete',
        subtitle: 'Pipeline Done',
        icon: 'complete',
        status: 'pending',
        position: { x: 760, y: 200 },
        color: 'bg-emerald-600'
      }
    ]

    const initialConnections: WorkflowConnection[] = [
      { from: 'start', to: 'planning', status: 'inactive' },
      { from: 'planning', to: 'development', status: 'inactive' },
      { from: 'development', to: 'review', status: 'inactive' },
      { from: 'review', to: 'complete', status: 'inactive' }
    ]

    setWorkflowNodes(initialNodes)
    setWorkflowConnections(initialConnections)
  }, [])

  // Update workflow visualization based on pipeline state
  useEffect(() => {
    if (!isRunning && !currentStage) return

    const updateNodeStatus = (nodeId: string, status: 'pending' | 'running' | 'completed' | 'error', output?: string) => {
      setWorkflowNodes(prev => prev.map(node => 
        node.id === nodeId ? { ...node, status, output } : node
      ))
    }

    const updateConnection = (from: string, to: string, status: 'inactive' | 'active' | 'completed') => {
      setWorkflowConnections(prev => prev.map(conn => 
        conn.from === from && conn.to === to ? { ...conn, status } : conn
      ))
    }

    if (currentStage === 'planning' && isRunning) {
      updateNodeStatus('start', 'completed')
      updateNodeStatus('planning', 'running')
      updateConnection('start', 'planning', 'active')
    } else if (currentStage === 'completed') {
      updateNodeStatus('planning', 'completed', stageHistory.find(s => s.stage === 'Planning')?.output)
      updateNodeStatus('development', 'completed', stageHistory.find(s => s.stage === 'Development')?.output)
      updateNodeStatus('review', 'completed', stageHistory.find(s => s.stage === 'Review')?.output)
      updateNodeStatus('complete', 'completed')
      updateConnection('start', 'planning', 'completed')
      updateConnection('planning', 'development', 'completed')
      updateConnection('development', 'review', 'completed')
      updateConnection('review', 'complete', 'completed')
    } else if (currentStage === 'failed') {
      const failedStage = error.includes('Planning') ? 'planning' : 
                         error.includes('Development') ? 'development' : 'review'
      updateNodeStatus(failedStage, 'error')
    }
  }, [currentStage, isRunning, stageHistory, error])

  const handleNodeClick = (nodeId: string) => {
    setSelectedNode(selectedNode === nodeId ? null : nodeId)
  }

  const handleRepositorySelect = (repoUrl: string, branches: string[]) => {
    setRepoUrl(repoUrl)
    setAvailableBranches(branches)
  }

  // Cleanup event source on unmount
  useEffect(() => {
    return () => {
      if (eventSource) {
        eventSource.close()
      }
    }
  }, [eventSource])

  const runPipelineWithRealTimeUpdates = async () => {
    if (!requirements.trim() || !repoUrl.trim()) {
      alert('Please provide both requirements and repository URL')
      return
    }

    setIsRunning(true)
    setOutput('')
    setError('')
    setCurrentStage('')
    setStageHistory([])

    // Close existing event source
    if (eventSource) {
      eventSource.close()
    }

    try {
      // Start streaming API call
      const response = await fetch('/api/pipeline/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          req_summary: requirements,
          repo_url: repoUrl,
          branch: branch
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) {
        throw new Error('No reader available')
      }

      while (true) {
        const { done, value } = await reader.read()
        
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              handleStreamUpdate(data)
            } catch (e) {
              console.error('Error parsing stream data:', e)
            }
          }
        }
      }
    } catch (error) {
      console.error('Pipeline error:', error)
      setError(error instanceof Error ? error.message : 'Unknown error occurred')
      setCurrentStage('failed')
    } finally {
      setIsRunning(false)
    }
  }

  const handleStreamUpdate = (data: any) => {
    const { stage, status, output, source } = data
    
    // Log LangGraph activity
    if (source === 'langgraph') {
      console.log(`🔗 LangGraph: ${stage} -> ${status}`, output ? `(${output.length} chars)` : '')
    }

    // Handle streaming content updates
    if (status === 'streaming') {
      // Update stage history with streaming content
      setStageHistory(prev => {
        const existing = prev.find(s => s.stage === stage)
        if (existing) {
          return prev.map(s => s.stage === stage ? { ...s, status: 'current', output } : s)
        }
        return [...prev, { stage, status: 'current', output }]
      })
      return // Don't update workflow nodes during streaming
    }

    // Update workflow nodes in real-time
    setWorkflowNodes(prev => prev.map(node => {
      if (node.id === stage) {
        return { ...node, status, output }
      }
      return node
    }))

    // Update connections
    if (status === 'running') {
      setWorkflowConnections(prev => prev.map(conn => {
        const fromCompleted = prev.find(n => n.id === conn.from)?.status === 'completed'
        return {
          ...conn,
          status: conn.to === stage && fromCompleted ? 'active' : conn.status
        }
      }))
    } else if (status === 'completed') {
      setWorkflowConnections(prev => prev.map(conn => {
        return {
          ...conn,
          status: conn.from === stage ? 'completed' : conn.status
        }
      }))
    }

    // Update stage history and current stage
    if (stage !== 'pipeline' && stage !== 'complete') {
      setCurrentStage(stage)
      setStageHistory(prev => {
        const existing = prev.find(s => s.stage === stage)
        if (existing) {
          return prev.map(s => s.stage === stage ? { ...s, status, output } : s)
        }
        return [...prev, { stage, status, output }]
      })
    }

    // Handle final completion or errors
    if (stage === 'pipeline' || stage === 'complete') {
      if (status === 'completed') {
        setCurrentStage('completed')
        setOutput(output || 'LangGraph pipeline completed successfully!')
      } else if (status === 'error') {
        setCurrentStage('failed')
        setError(output)
      }
    }
  }

  const runPipeline = async () => {
    if (!requirements.trim() || !repoUrl.trim()) {
      alert('Please provide both requirements and repository URL')
      return
    }

    setIsRunning(true)
    setOutput('')
    setError('')
    setCurrentStage('planning')
    setStageHistory([
      { stage: 'Planning', status: 'current' },
      { stage: 'Development', status: 'pending' },
      { stage: 'Review', status: 'pending' }
    ])

    // Simulate real-time pipeline progression with visual updates
    const simulateProgress = async () => {
      // Stage 1: Planning
      setCurrentStage('planning')
      setWorkflowNodes(prev => prev.map(node => ({
        ...node,
        status: node.id === 'start' ? 'completed' : 
                node.id === 'planning' ? 'running' : 'pending'
      })))
      setWorkflowConnections(prev => prev.map(conn => ({
        ...conn,
        status: conn.from === 'start' && conn.to === 'planning' ? 'active' : 'inactive'
      })))

      await new Promise(resolve => setTimeout(resolve, 2000)) // Visual delay

      // Stage 2: Development
      setCurrentStage('development')  
      setWorkflowNodes(prev => prev.map(node => ({
        ...node,
        status: node.id === 'start' || node.id === 'planning' ? 'completed' :
                node.id === 'development' ? 'running' : 'pending'
      })))
      setWorkflowConnections(prev => prev.map(conn => ({
        ...conn,
        status: conn.from === 'start' && conn.to === 'planning' ? 'completed' :
                conn.from === 'planning' && conn.to === 'development' ? 'active' : 'inactive'
      })))

      await new Promise(resolve => setTimeout(resolve, 2000))

      // Stage 3: Review  
      setCurrentStage('review')
      setWorkflowNodes(prev => prev.map(node => ({
        ...node,
        status: ['start', 'planning', 'development'].includes(node.id) ? 'completed' :
                node.id === 'review' ? 'running' : 'pending'
      })))
      setWorkflowConnections(prev => prev.map(conn => ({
        ...conn,
        status: (conn.from === 'start' && conn.to === 'planning') ||
                (conn.from === 'planning' && conn.to === 'development') ? 'completed' :
                conn.from === 'development' && conn.to === 'review' ? 'active' : 'inactive' 
      })))

      await new Promise(resolve => setTimeout(resolve, 1000))
    }

    try {
      // Start visual simulation
      await simulateProgress()
      
      const response = await fetch('/api/pipeline/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          req_summary: requirements,
          repo_url: repoUrl,
          branch: branch
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.details || `HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      setPipelineState(result.finalState)
      setOutput(result.summary)
      setCurrentStage('completed')
      
      // Update stage history with results
      setStageHistory([
        { stage: 'Planning', status: 'completed', output: result.planOutput },
        { stage: 'Development', status: 'completed', output: result.devOutput },
        { stage: 'Review', status: 'completed', output: result.reviewOutput }
      ])
      
      // Final workflow state - all completed
      setWorkflowNodes(prev => prev.map(node => ({
        ...node,
        status: 'completed',
        output: node.id === 'planning' ? result.planOutput :
                node.id === 'development' ? result.devOutput :
                node.id === 'review' ? result.reviewOutput : undefined
      })))
      setWorkflowConnections(prev => prev.map(conn => ({
        ...conn,
        status: 'completed'
      })))
      
    } catch (error) {
      console.error('Pipeline error:', error)
      setError(error instanceof Error ? error.message : 'Unknown error occurred')
      setCurrentStage('failed')
      
      // Update workflow to show error state
      const failedStage = error instanceof Error && error.message.includes('Planning') ? 'planning' : 
                         error instanceof Error && error.message.includes('Development') ? 'development' : 'review'
      setWorkflowNodes(prev => prev.map(node => ({
        ...node,
        status: node.id === failedStage ? 'error' : 
                ['start', 'planning', 'development', 'review'].indexOf(node.id) < 
                ['start', 'planning', 'development', 'review'].indexOf(failedStage) ? 'completed' : 'pending'
      })))
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold mb-4">LangGraph SDLC Pipeline</h2>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Watch AI agents collaborate in real-time to analyze, develop, and review your code
        </p>
      </div>

      {/* Stunning Workflow Visualization */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <h3 className="text-xl font-semibold">Live Agent Workflow</h3>
            <div className="flex items-center space-x-2 px-3 py-1 bg-purple-100 dark:bg-purple-900/30 border border-purple-300 dark:border-purple-600/30 rounded-full">
              <svg className="w-4 h-4 text-purple-600 dark:text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="3"/>
                <circle cx="12" cy="5" r="2"/>
                <circle cx="12" cy="19" r="2"/>
                <circle cx="5" cy="12" r="2"/>
                <circle cx="19" cy="12" r="2"/>
                <path d="M12 9V7"/>
                <path d="M12 17v2"/>
                <path d="M9 12H7"/>
                <path d="M17 12h2"/>
              </svg>
              <span className="text-sm font-semibold text-purple-700 dark:text-purple-300">Powered by LangGraph</span>
              {isRunning && (
                <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
              )}
            </div>
          </div>
          {selectedNode && (
            <button
              onClick={() => setSelectedNode(null)}
              className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              Clear Selection
            </button>
          )}
        </div>
        
        <WorkflowVisualizer
          nodes={workflowNodes}
          connections={workflowConnections}
          onNodeClick={handleNodeClick}
        />

        {/* Selected Node Details */}
        {selectedNode && (
          <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border">
            {(() => {
              const node = workflowNodes.find(n => n.id === selectedNode)
              if (!node) return null
              
              return (
                <div>
                  <div className="flex items-center space-x-3 mb-3">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${node.color}`}>
                      {node.icon}
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg">{node.title}</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">{node.subtitle}</p>
                    </div>
                    <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                      node.status === 'completed' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                      node.status === 'running' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' :
                      node.status === 'error' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                      'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                    }`}>
                      {node.status}
                    </div>
                  </div>
                  
                  {node.output && (
                    <div>
                      <h5 className="font-medium mb-2">Output:</h5>
                      <div className="bg-white dark:bg-gray-900 p-3 rounded border text-sm max-h-40 overflow-y-auto whitespace-pre-wrap">
                        {node.output}
                      </div>
                    </div>
                  )}
                </div>
              )
            })()}
          </div>
        )}
      </div>

      {/* CLI Progress Panel - Claude Code Style */}
      <CLIProgressPanel 
        isRunning={isRunning}
        currentStage={currentStage}
        stageHistory={stageHistory}
      />
      
      {/* Git Integration */}
      <GitConnectionPanel onRepositorySelect={handleRepositorySelect} />

      {/* Pipeline Input Form */}
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="p-6 border border-gray-200 dark:border-gray-800 rounded-lg">
          <h3 className="text-xl font-semibold mb-4">Start Pipeline</h3>
          
          <div className="space-y-4">
            <div>
              <label htmlFor="requirements" className="block text-sm font-medium mb-2">
                Requirements / Task Description
              </label>
              <textarea
                id="requirements"
                rows={4}
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800"
                placeholder="Describe what you want to build or implement..."
                value={requirements}
                onChange={(e) => setRequirements(e.target.value)}
                disabled={isRunning}
              />
            </div>

            <div>
              <label htmlFor="repoUrl" className="block text-sm font-medium mb-2">
                Repository URL
              </label>
              <input
                id="repoUrl"
                type="url"
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800"
                placeholder="https://github.com/username/repository"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                disabled={isRunning}
              />
            </div>

            <div>
              <label htmlFor="branch" className="block text-sm font-medium mb-2">
                Branch
              </label>
              <input
                id="branch"
                type="text"
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800"
                placeholder="main"
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                disabled={isRunning}
              />
            </div>

            <button
              onClick={runPipelineWithRealTimeUpdates}
              disabled={isRunning || !requirements.trim() || !repoUrl.trim()}
              className="w-full p-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-md font-medium transition-colors"
            >
              {isRunning ? 'Running Pipeline...' : 'Start Pipeline'}
            </button>
          </div>
        </div>

      </div>

      {/* Agent Information */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 border border-gray-200 dark:border-gray-800 rounded-lg">
          <h3 className="text-xl font-semibold mb-2">Planning Agent</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Analyzes requirements and creates development plans
          </p>
        </div>
        
        <div className="p-6 border border-gray-200 dark:border-gray-800 rounded-lg">
          <h3 className="text-xl font-semibold mb-2">Development Agent</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Implements code based on specifications and plans
          </p>
        </div>
        
        <div className="p-6 border border-gray-200 dark:border-gray-800 rounded-lg">
          <h3 className="text-xl font-semibold mb-2">Review Agent</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Reviews code quality and suggests improvements
          </p>
        </div>
      </div>
    </div>
  )
}