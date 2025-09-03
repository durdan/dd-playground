'use client'

import { useState, useEffect } from 'react'
import { GIT_PROVIDERS, GitProvider } from '../lib/git/providers'
import { GitHubIcon, BitbucketIcon } from './Icons'

interface GitUser {
  username: string
  userId: string
  name: string
}

interface GitConnectionPanelProps {
  onRepositorySelect: (repoUrl: string, branches: string[]) => void
}

export default function GitConnectionPanel({ onRepositorySelect }: GitConnectionPanelProps) {
  const [connectedProvider, setConnectedProvider] = useState<string | null>(null)
  const [user, setUser] = useState<GitUser | null>(null)
  const [repositories, setRepositories] = useState<any[]>([])
  const [selectedRepo, setSelectedRepo] = useState<string>('')
  const [branches, setBranches] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Check if user is already connected
    checkExistingConnection()
  }, [])

  const checkExistingConnection = async () => {
    try {
      const response = await fetch('/api/auth/status')
      if (response.ok) {
        const data = await response.json()
        if (data.connected) {
          setConnectedProvider(data.provider)
          setUser(data.user)
          await loadRepositories()
        }
      }
    } catch (error) {
      console.error('Error checking connection:', error)
    }
  }

  const handleConnect = (provider: GitProvider) => {
    window.location.href = provider.authUrl
  }

  const loadRepositories = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/git/repositories')
      if (response.ok) {
        const repos = await response.json()
        setRepositories(repos)
      }
    } catch (error) {
      console.error('Error loading repositories:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRepoSelect = async (repoFullName: string) => {
    setSelectedRepo(repoFullName)
    setLoading(true)
    
    try {
      const response = await fetch(`/api/git/branches?repo=${encodeURIComponent(repoFullName)}`)
      if (response.ok) {
        const branchList = await response.json()
        setBranches(branchList)
        
        // Find the selected repository to get its URL
        const repo = repositories.find(r => r.fullName === repoFullName)
        if (repo) {
          onRepositorySelect(repo.url, branchList)
        }
      }
    } catch (error) {
      console.error('Error loading branches:', error)
    } finally {
      setLoading(false)
    }
  }

  const getProviderIcon = (providerId: string) => {
    switch (providerId) {
      case 'github': return <GitHubIcon className="w-5 h-5" />
      case 'bitbucket': return <BitbucketIcon className="w-5 h-5" />
      default: return <GitHubIcon className="w-5 h-5" />
    }
  }

  if (!connectedProvider) {
    return (
      <div className="p-6 border border-gray-200 dark:border-gray-800 rounded-lg">
        <h3 className="text-lg font-semibold mb-4">Connect Your Git Repository</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Connect to GitHub, Bitbucket, or GitLab to access your repositories and enable automated deployments.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {GIT_PROVIDERS.map((provider) => (
            <button
              key={provider.id}
              onClick={() => handleConnect(provider)}
              className={`flex items-center justify-center space-x-3 p-4 rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 transition-colors ${provider.color} hover:bg-opacity-10`}
            >
              <div className="text-white">
                {getProviderIcon(provider.id)}
              </div>
              <span className="font-medium text-gray-700 dark:text-gray-300">
                Connect {provider.name}
              </span>
            </button>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 border border-gray-200 dark:border-gray-800 rounded-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Connected Repository</h3>
        <div className="flex items-center space-x-2 text-sm text-green-600 dark:text-green-400">
          {getProviderIcon(connectedProvider)}
          <span>Connected as {user?.username}</span>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Select Repository</label>
            <select
              value={selectedRepo}
              onChange={(e) => handleRepoSelect(e.target.value)}
              className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800"
            >
              <option value="">Choose a repository...</option>
              {repositories.map((repo) => (
                <option key={repo.id} value={repo.fullName}>
                  {repo.fullName} {repo.isPrivate ? '🔒' : '🌐'}
                </option>
              ))}
            </select>
          </div>

          {branches.length > 0 && (
            <div>
              <label className="block text-sm font-medium mb-2">Available Branches</label>
              <div className="flex flex-wrap gap-2">
                {branches.map((branch) => (
                  <span
                    key={branch}
                    className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm"
                  >
                    {branch}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}