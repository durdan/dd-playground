export default function Home() {
  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold mb-4">Welcome to LangGraph SDLC Pipeline</h2>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          An agent-to-agent software development lifecycle pipeline powered by LangGraph.
          This system orchestrates multiple AI agents to handle different phases of software development.
        </p>
      </div>
      
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