'use client'

import { useState, useEffect, useRef } from 'react'
import { ChevronDownIcon, ChevronRightIcon } from '@heroicons/react/24/outline'

interface CLILogEntry {
  id: string
  stage: string
  message: string
  timestamp: Date
  type: 'info' | 'success' | 'error' | 'warning'
}

interface CLIStage {
  id: string
  name: string
  status: 'pending' | 'running' | 'completed' | 'error'
  logs: CLILogEntry[]
  startTime?: Date
  endTime?: Date
  collapsed: boolean
}

interface CLIProgressPanelProps {
  isRunning: boolean
  currentStage: string
  stageHistory: Array<{stage: string, status: 'completed' | 'current' | 'pending', output?: string}>
  onStageUpdate?: (stage: string, logs: CLILogEntry[]) => void
}

export default function CLIProgressPanel({ isRunning, currentStage, stageHistory, onStageUpdate }: CLIProgressPanelProps) {
  const [stages, setStages] = useState<CLIStage[]>([
    {
      id: 'planning',
      name: 'Planning Agent',
      status: 'pending',
      logs: [],
      collapsed: false
    },
    {
      id: 'development', 
      name: 'Development Agent',
      status: 'pending',
      logs: [],
      collapsed: false
    },
    {
      id: 'review',
      name: 'Review Agent', 
      status: 'pending',
      logs: [],
      collapsed: false
    }
  ])

  const [currentLogs, setCurrentLogs] = useState<CLILogEntry[]>([])
  const scrollRef = useRef<HTMLDivElement>(null)
  const logIdCounter = useRef(0)

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [currentLogs])

  // Handle streaming and completed stages
  useEffect(() => {
    stageHistory.forEach((historyItem) => {
      const stageId = historyItem.stage.toLowerCase()
      const existingStage = stages.find(s => s.id === stageId)
      
      if (!existingStage) return
      
      // Handle real-time streaming content (preserve the real streaming)
      if (historyItem.status === 'current' && historyItem.output) {
        // Update stage with streaming content and mark as streaming
        setStages(prev => prev.map(s => 
          s.id === stageId ? { 
            ...s, 
            status: 'running',
            logs: [{
              id: 'real-streaming-content',
              stage: stageId,
              message: historyItem.output,
              timestamp: new Date(),
              type: 'info'
            }]
          } : s
        ))
      }
      // Handle completed stages - preserve the final content
      else if (historyItem.status === 'completed' && historyItem.output) {
        // Preserve the real content and mark as completed
        setStages(prev => prev.map(s => 
          s.id === stageId ? { 
            ...s, 
            status: 'completed',
            endTime: new Date(),
            logs: [{
              id: 'final-content',
              stage: stageId,
              message: historyItem.output,
              timestamp: new Date(),
              type: 'success'
            }]
          } : s
        ))
        
        // Auto-collapse after 3 seconds
        setTimeout(() => {
          setStages(prev => prev.map(s => 
            s.id === stageId ? { ...s, collapsed: true } : s
          ))
        }, 3000)
      }
    })
  }, [stageHistory])

  const streamContentForCompletedStage = async (stageId: string, content: string) => {
    const stage = stages.find(s => s.id === stageId)
    if (!stage) return

    // Update stage to running first
    setStages(prev => prev.map(s => 
      s.id === stageId ? { 
        ...s, 
        status: 'running', 
        startTime: new Date(),
        collapsed: false,
        logs: []
      } : s
    ))

    const allLogs: CLILogEntry[] = []
    
    // Initial setup logs with realistic timing
    const initialLogs = [
      `${stage.name} initializing...`,
      `Connecting to OpenAI API...`,
      `Processing requirements...`,
      `Analyzing context and constraints...`,
      `Generating ${stage.name.toLowerCase()} content...`
    ]

    // Add initial logs with realistic delays
    for (let i = 0; i < initialLogs.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 400 + Math.random() * 300))
      
      const log: CLILogEntry = {
        id: `log-${logIdCounter.current++}`,
        stage: stageId,
        message: initialLogs[i],
        timestamp: new Date(),
        type: 'info'
      }
      
      allLogs.push(log)
      setStages(prev => prev.map(s => 
        s.id === stageId ? { ...s, logs: [...allLogs] } : s
      ))
    }

    // Add content header with longer delay to simulate processing
    await new Promise(resolve => setTimeout(resolve, 800))
    allLogs.push({
      id: `log-${logIdCounter.current++}`,
      stage: stageId,
      message: `Generated ${stage.name.toLowerCase()} content:`,
      timestamp: new Date(),
      type: 'success'
    })

    allLogs.push({
      id: `log-${logIdCounter.current++}`,
      stage: stageId,
      message: '─'.repeat(50),
      timestamp: new Date(),
      type: 'info'
    })

    setStages(prev => prev.map(s => 
      s.id === stageId ? { ...s, logs: [...allLogs] } : s
    ))

    // Stream the actual content with character-by-character typing effect
    if (content && content.trim()) {
      const contentLines = content.split('\n').filter(line => line.trim())
      const linesToShow = Math.min(contentLines.length, 12) // Show fewer lines for better UX

      for (let i = 0; i < linesToShow; i++) {
        const line = contentLines[i].trim()
        if (!line) continue

        // Always show content with typing effect for better visual appeal
        if (line.length > 30) {
          // Character-by-character typing for longer lines
          let currentText = ''
          for (let charIndex = 0; charIndex < line.length; charIndex++) {
            currentText += line[charIndex]
            
            // Update or create the typing log entry
            const typingLogId = `typing-${i}`
            const existingIndex = allLogs.findIndex(log => log.id === typingLogId)
            
            const updatedLog: CLILogEntry = {
              id: typingLogId,
              stage: stageId,
              message: currentText + (charIndex < line.length - 1 ? '█' : ''),
              timestamp: new Date(),
              type: 'info'
            }
            
            if (existingIndex >= 0) {
              allLogs[existingIndex] = updatedLog
            } else {
              allLogs.push(updatedLog)
            }

            setStages(prev => prev.map(s => 
              s.id === stageId ? { ...s, logs: [...allLogs] } : s
            ))

            // Variable speed typing - faster for spaces, slower for punctuation
            const char = line[charIndex]
            const delay = char === ' ' ? 30 : 
                         char.match(/[.!?;:]/) ? 150 : 
                         char.match(/[,]/) ? 100 : 
                         60 + Math.random() * 40
            
            await new Promise(resolve => setTimeout(resolve, delay))
          }
        } else {
          // Word-by-word for shorter lines
          const words = line.split(' ')
          let currentText = ''
          
          for (let wordIndex = 0; wordIndex < words.length; wordIndex++) {
            currentText += (wordIndex > 0 ? ' ' : '') + words[wordIndex]
            
            const typingLogId = `typing-${i}`
            const existingIndex = allLogs.findIndex(log => log.id === typingLogId)
            
            const updatedLog: CLILogEntry = {
              id: typingLogId,
              stage: stageId,
              message: currentText + (wordIndex < words.length - 1 ? '█' : ''),
              timestamp: new Date(),
              type: 'info'
            }
            
            if (existingIndex >= 0) {
              allLogs[existingIndex] = updatedLog
            } else {
              allLogs.push(updatedLog)
            }

            setStages(prev => prev.map(s => 
              s.id === stageId ? { ...s, logs: [...allLogs] } : s
            ))

            await new Promise(resolve => setTimeout(resolve, 200 + Math.random() * 200))
          }
        }
      }

      // Add truncation notice if needed
      if (contentLines.length > 12) {
        await new Promise(resolve => setTimeout(resolve, 300))
        allLogs.push({
          id: `log-${logIdCounter.current++}`,
          stage: stageId,
          message: `[... ${contentLines.length - 12} more lines truncated for display]`,
          timestamp: new Date(),
          type: 'warning'
        })
      }
    }

    // Add footer
    await new Promise(resolve => setTimeout(resolve, 400))
    allLogs.push({
      id: `log-${logIdCounter.current++}`,
      stage: stageId,
      message: '─'.repeat(50),
      timestamp: new Date(),
      type: 'info'
    })

    allLogs.push({
      id: `log-${logIdCounter.current++}`,
      stage: stageId,
      message: `${stage.name} completed successfully ✓`,
      timestamp: new Date(),
      type: 'success'
    })

    // Update to completed status
    setStages(prev => prev.map(s => 
      s.id === stageId ? { 
        ...s, 
        logs: [...allLogs],
        status: 'completed',
        endTime: new Date()
      } : s
    ))

    // Auto-collapse after 3 seconds to give time to read
    setTimeout(() => {
      setStages(prev => prev.map(s => 
        s.id === stageId ? { ...s, collapsed: true } : s
      ))
    }, 3000)
  }

  // Handle real-time logs for currently running stage
  useEffect(() => {
    if (!isRunning || !currentStage) return

    const stageName = currentStage.charAt(0).toUpperCase() + currentStage.slice(1)
    
    // Clear current logs and start new stage
    setCurrentLogs([])
    
    const initialLogs = [
      `${stageName} agent initializing...`,
      `Loading ${stageName.toLowerCase()} configurations...`,
      `Connecting to OpenAI API...`,
      `Processing requirements...`,
      `Analyzing context and constraints...`,
      `Generating ${stageName.toLowerCase()} output...`
    ]

    let logIndex = 0
    const interval = setInterval(() => {
      if (logIndex < initialLogs.length) {
        const newLog: CLILogEntry = {
          id: `log-${logIdCounter.current++}`,
          stage: currentStage,
          message: initialLogs[logIndex],
          timestamp: new Date(),
          type: 'info'
        }
        
        setCurrentLogs(prev => [...prev, newLog])
        logIndex++
      } else {
        clearInterval(interval)
      }
    }, 400 + Math.random() * 200)

    return () => clearInterval(interval)
  }, [currentStage, isRunning])

  const toggleStageCollapse = (stageId: string) => {
    setStages(prev => prev.map(stage => 
      stage.id === stageId 
        ? { ...stage, collapsed: !stage.collapsed }
        : stage
    ))
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <div className="w-2 h-2 rounded-full bg-gray-400" />
      case 'running':
        return <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
      case 'completed':
        return <div className="w-2 h-2 rounded-full bg-green-500" />
      case 'error':
        return <div className="w-2 h-2 rounded-full bg-red-500" />
      default:
        return <div className="w-2 h-2 rounded-full bg-gray-400" />
    }
  }

  const getLogLineColor = (type: string) => {
    switch (type) {
      case 'success': return 'text-green-400'
      case 'error': return 'text-red-400'
      case 'warning': return 'text-yellow-400'
      default: return 'text-gray-300'
    }
  }

  const formatTimestamp = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour12: false, 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    })
  }

  const getDuration = (start?: Date, end?: Date) => {
    if (!start) return ''
    const endTime = end || new Date()
    const duration = Math.round((endTime.getTime() - start.getTime()) / 1000)
    return `${duration}s`
  }

  if (!isRunning && stages.every(s => s.status === 'pending')) {
    return null
  }

  return (
    <div className="mt-6 bg-gray-900 border border-gray-700 rounded-lg overflow-hidden font-mono text-sm">
      {/* Header */}
      <div className="bg-gray-800 px-4 py-3 border-b border-gray-700">
        <div className="flex items-center space-x-3">
          <div className="flex space-x-1">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="text-gray-300 font-medium">LangGraph SDLC Pipeline</span>
            <div className="flex items-center space-x-1 px-2 py-1 bg-purple-900/30 border border-purple-600/30 rounded-full">
              <svg className="w-4 h-4 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
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
              <span className="text-xs font-semibold text-purple-300">LangGraph</span>
            </div>
          </div>
          {isRunning && (
            <div className="flex items-center space-x-2 text-blue-400 bg-blue-900/20 px-2 py-1 rounded-full border border-blue-500/30">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
              <span className="text-xs font-medium">Orchestrating Agents...</span>
            </div>
          )}
        </div>
      </div>

      {/* Stages */}
      <div className="max-h-96 overflow-y-auto">
        {stages.map((stage) => (
          <div key={stage.id} className="border-b border-gray-700 last:border-b-0">
            {/* Stage Header */}
            <div 
              className="flex items-center justify-between px-4 py-3 hover:bg-gray-800 cursor-pointer transition-colors"
              onClick={() => toggleStageCollapse(stage.id)}
            >
              <div className="flex items-center space-x-3">
                {stage.collapsed ? (
                  <ChevronRightIcon className="w-4 h-4 text-gray-400" />
                ) : (
                  <ChevronDownIcon className="w-4 h-4 text-gray-400" />
                )}
                {getStatusIcon(stage.status)}
                <span className="text-gray-200 font-medium">{stage.name}</span>
                {stage.status === 'running' && (
                  <div className="flex items-center space-x-1 px-2 py-0.5 bg-purple-900/40 border border-purple-500/30 rounded text-xs">
                    <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-pulse"></div>
                    <span className="text-purple-300 font-medium">LangGraph Node</span>
                  </div>
                )}
              </div>
              
              <div className="flex items-center space-x-4 text-xs text-gray-400">
                {stage.startTime && (
                  <span>{formatTimestamp(stage.startTime)}</span>
                )}
                {stage.status !== 'pending' && (
                  <span className="bg-gray-700 px-2 py-1 rounded">
                    {getDuration(stage.startTime, stage.endTime)}
                  </span>
                )}
              </div>
            </div>

            {/* Stage Logs */}
            {!stage.collapsed && (
              <div className="bg-gray-900">
                {/* Completed stage logs */}
                {stage.status === 'completed' && stage.logs.length > 0 && (
                  <div className="px-6 pb-4 space-y-1 max-h-32 overflow-y-auto">
                    {stage.logs.map((log) => (
                      <div key={log.id} className="flex items-start space-x-2">
                        <span className="text-gray-500 text-xs mt-0.5">
                          {formatTimestamp(log.timestamp)}
                        </span>
                        <span className={`${getLogLineColor(log.type)} flex-1`}>
                          {log.message}
                        </span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Current running stage logs */}
                {stage.status === 'running' && stage.id === currentStage && (
                  <div 
                    ref={scrollRef}
                    className="px-6 pb-4 space-y-1 max-h-32 overflow-y-auto"
                  >
                    {currentLogs.map((log) => (
                      <div key={log.id} className="flex items-start space-x-2">
                        <span className="text-gray-500 text-xs mt-0.5">
                          {formatTimestamp(log.timestamp)}
                        </span>
                        <span className={`${getLogLineColor(log.type)} flex-1`}>
                          {log.message}
                        </span>
                      </div>
                    ))}
                    {currentLogs.length > 0 && (
                      <div className="flex items-center space-x-2 mt-2">
                        <div className="w-1 h-4 bg-green-400 animate-pulse"></div>
                        <span className="text-gray-400 text-xs">Processing...</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}