'use client'

import { useEffect, useState } from 'react'

import { StartIcon, PlanningIcon, CodeIcon, ReviewIcon, CompleteIcon, BotIcon } from './Icons'

export interface WorkflowNode {
  id: string
  title: string
  subtitle: string
  icon: 'start' | 'planning' | 'development' | 'review' | 'complete' | 'bot'
  status: 'pending' | 'running' | 'completed' | 'error'
  position: { x: number; y: number }
  color: string
  output?: string
}

export interface WorkflowConnection {
  from: string
  to: string
  status: 'inactive' | 'active' | 'completed'
}

interface WorkflowVisualizerProps {
  nodes: WorkflowNode[]
  connections: WorkflowConnection[]
  onNodeClick?: (nodeId: string) => void
}

export default function WorkflowVisualizer({ nodes, connections, onNodeClick }: WorkflowVisualizerProps) {
  const [dataFlows, setDataFlows] = useState<{[key: string]: boolean}>({})

  useEffect(() => {
    // Animate data flows when connections are active
    connections.forEach(conn => {
      if (conn.status === 'active') {
        setDataFlows(prev => ({ ...prev, [`${conn.from}-${conn.to}`]: true }))
        setTimeout(() => {
          setDataFlows(prev => ({ ...prev, [`${conn.from}-${conn.to}`]: false }))
        }, 2000)
      }
    })
  }, [connections])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-gray-300 border-gray-400'
      case 'running': return 'bg-blue-500 border-blue-600 animate-pulse'
      case 'completed': return 'bg-green-500 border-green-600'
      case 'error': return 'bg-red-500 border-red-600'
      default: return 'bg-gray-300 border-gray-400'
    }
  }

  const getConnectionPath = (from: WorkflowNode, to: WorkflowNode) => {
    const fromX = from.position.x + 75 // Half of node width
    const fromY = from.position.y + 40 // Half of node height
    const toX = to.position.x + 75
    const toY = to.position.y + 40

    // Create a curved path
    const midX = (fromX + toX) / 2
    const curveOffset = Math.abs(toY - fromY) * 0.3

    return `M ${fromX} ${fromY} Q ${midX} ${fromY - curveOffset} ${toX} ${toY}`
  }

  const getConnectionStatus = (connId: string) => {
    const conn = connections.find(c => `${c.from}-${c.to}` === connId)
    return conn?.status || 'inactive'
  }

  const getNodeIcon = (iconType: string, className = "w-5 h-5") => {
    switch (iconType) {
      case 'start': return <StartIcon className={className} />
      case 'planning': return <PlanningIcon className={className} />
      case 'development': return <CodeIcon className={className} />
      case 'review': return <ReviewIcon className={className} />
      case 'complete': return <CompleteIcon className={className} />
      case 'bot': return <BotIcon className={className} />
      default: return <BotIcon className={className} />
    }
  }

  return (
    <div className="relative w-full h-[500px] bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden">
      {/* Grid Pattern Background */}
      <div className="absolute inset-0 opacity-30">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="currentColor" strokeWidth="0.5" className="text-slate-300 dark:text-slate-600"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      {/* SVG for connections */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        <defs>
          {/* Gradient for active connections */}
          <linearGradient id="activeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{stopColor: '#3b82f6', stopOpacity: 1}} />
            <stop offset="100%" style={{stopColor: '#10b981', stopOpacity: 1}} />
          </linearGradient>
          
          {/* Animated gradient for data flow */}
          <linearGradient id="flowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{stopColor: '#3b82f6', stopOpacity: 0}} />
            <stop offset="50%" style={{stopColor: '#3b82f6', stopOpacity: 1}} />
            <stop offset="100%" style={{stopColor: '#3b82f6', stopOpacity: 0}} />
            <animateTransform
              attributeName="gradientTransform"
              type="translate"
              values="-100 0;100 0;-100 0"
              dur="2s"
              repeatCount="indefinite"
            />
          </linearGradient>

          {/* Arrow markers */}
          <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                  refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#3b82f6" />
          </marker>
        </defs>

        {/* Draw connections */}
        {connections.map((conn, index) => {
          const fromNode = nodes.find(n => n.id === conn.from)
          const toNode = nodes.find(n => n.id === conn.to)
          
          if (!fromNode || !toNode) return null

          const path = getConnectionPath(fromNode, toNode)
          const connId = `${conn.from}-${conn.to}`
          const isDataFlowing = dataFlows[connId]

          return (
            <g key={index}>
              {/* Base connection line */}
              <path
                d={path}
                fill="none"
                stroke={conn.status === 'completed' ? '#10b981' : 
                       conn.status === 'active' ? '#3b82f6' : '#cbd5e1'}
                strokeWidth="3"
                markerEnd="url(#arrowhead)"
                className={conn.status === 'active' ? 'animate-pulse' : ''}
              />
              
              {/* Animated data flow */}
              {isDataFlowing && (
                <path
                  d={path}
                  fill="none"
                  stroke="url(#flowGradient)"
                  strokeWidth="6"
                  opacity="0.7"
                />
              )}
            </g>
          )
        })}
      </svg>

      {/* Workflow Nodes */}
      {nodes.map((node) => (
        <div
          key={node.id}
          className={`absolute cursor-pointer transform transition-all duration-300 hover:scale-105 hover:z-10`}
          style={{
            left: node.position.x,
            top: node.position.y,
          }}
          onClick={() => onNodeClick?.(node.id)}
        >
          {/* Node Container */}
          <div className={`relative w-40 h-24 rounded-xl border-2 shadow-lg backdrop-blur-sm transition-all duration-300 ${getStatusColor(node.status)} ${node.status === 'running' ? 'shadow-blue-400/50 shadow-xl' : 'hover:shadow-xl'}`}>
            
            {/* Status indicator ring */}
            {node.status === 'running' && (
              <div className="absolute -inset-1 rounded-lg bg-gradient-to-r from-blue-400 to-blue-600 opacity-30 animate-pulse"></div>
            )}

            {/* Node Content */}
            <div className="relative h-full p-4 flex items-center space-x-3">
              {/* Icon */}
              <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-white shadow-sm ${node.color}`}>
                {getNodeIcon(node.icon, "w-5 h-5")}
              </div>
              
              {/* Text Content */}
              <div className="flex-1 min-w-0">
                <div className="text-sm font-semibold text-gray-900 dark:text-white truncate">
                  {node.title}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-300 truncate">
                  {node.subtitle}
                </div>
              </div>
            </div>

            {/* Status Badge */}
            <div className={`absolute -top-2 -right-2 w-4 h-4 rounded-full border-2 border-white ${
              node.status === 'pending' ? 'bg-gray-400' :
              node.status === 'running' ? 'bg-blue-500 animate-ping' :
              node.status === 'completed' ? 'bg-green-500' :
              'bg-red-500'
            }`}>
              {node.status === 'completed' && (
                <svg className="w-3 h-3 text-white absolute top-0.5 left-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
              {node.status === 'error' && (
                <svg className="w-3 h-3 text-white absolute top-0.5 left-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              )}
            </div>

            {/* Processing Animation */}
            {node.status === 'running' && (
              <div className="absolute inset-0 rounded-lg overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 animate-shimmer"></div>
              </div>
            )}
          </div>

          {/* Tooltip */}
          {node.output && (
            <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 opacity-0 group-hover:opacity-100 transition-opacity z-20">
              <div className="bg-black text-white text-xs rounded py-1 px-2 max-w-xs">
                {node.output.length > 100 ? node.output.substring(0, 100) + '...' : node.output}
              </div>
            </div>
          )}
        </div>
      ))}

      {/* Floating particles for ambiance */}
      <div className="absolute inset-0 pointer-events-none">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-blue-400 rounded-full opacity-30 animate-float-slow"
            style={{
              left: `${20 + i * 15}%`,
              top: `${10 + i * 10}%`,
              animationDelay: `${i * 0.5}s`,
            }}
          />
        ))}
      </div>
    </div>
  )
}