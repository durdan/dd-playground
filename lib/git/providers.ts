export interface GitProvider {
  name: string
  id: 'github' | 'bitbucket' | 'gitlab'
  icon: string
  color: string
  authUrl: string
  apiBaseUrl: string
}

export const GIT_PROVIDERS: GitProvider[] = [
  {
    name: 'GitHub',
    id: 'github',
    icon: 'M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z',
    color: 'bg-gray-900',
    authUrl: '/api/auth/callback/github',
    apiBaseUrl: 'https://api.github.com'
  },
  {
    name: 'Bitbucket',
    id: 'bitbucket', 
    icon: 'M0 7.6c0-0.4 0.3-0.7 0.7-0.7h14.6c0.4 0 0.7 0.3 0.7 0.7 0 0.1 0 0.1 0 0.2l-2.1 12.4c-0.1 0.4-0.4 0.7-0.8 0.7h-9.8c-0.3 0-0.6-0.2-0.7-0.5l-2.6-12.6c0-0.1 0-0.1 0-0.2zM9.9 13.9h-3.8l-0.8-4.1h5.4l-0.8 4.1z',
    color: 'bg-blue-600',
    authUrl: '/api/auth/callback/bitbucket',
    apiBaseUrl: 'https://api.bitbucket.org/2.0'
  },
  {
    name: 'GitLab',
    id: 'gitlab',
    icon: 'M8.081 13.414L16 8.414V4.586c0-.89-1.077-1.337-1.707-.707L8.081 10.086v3.328zM7.081 10.086L.707 3.879C.077 3.249-.367 4.696.293 4.586v3.828l7.374 5zM0 8.414v7.172c0 .89 1.077 1.337 1.707.707l6.374-6.207V8.414L0 8.414zM16 15.586v-7.172l-7.374 5v1.672l6.374 6.207c.63.63 1.707.183 1.707-.707z',
    color: 'bg-orange-600', 
    authUrl: '/api/auth/callback/gitlab',
    apiBaseUrl: 'https://gitlab.com/api/v4'
  }
]

export interface GitConnection {
  provider: GitProvider
  accessToken: string
  refreshToken?: string
  username: string
  userId: string
  connectedAt: Date
}

export interface GitRepository {
  id: string
  name: string
  fullName: string
  url: string
  defaultBranch: string
  isPrivate: boolean
  description?: string
  provider: 'github' | 'bitbucket' | 'gitlab'
}

export class GitService {
  static async getRepositories(connection: GitConnection): Promise<GitRepository[]> {
    try {
      const response = await fetch(`${connection.provider.apiBaseUrl}/user/repos`, {
        headers: {
          'Authorization': `Bearer ${connection.accessToken}`,
          'Accept': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch repositories: ${response.statusText}`)
      }

      const repos = await response.json()
      
      return repos.map((repo: any) => ({
        id: repo.id.toString(),
        name: repo.name,
        fullName: repo.full_name,
        url: repo.html_url,
        defaultBranch: repo.default_branch || 'main',
        isPrivate: repo.private,
        description: repo.description,
        provider: connection.provider.id
      }))
    } catch (error) {
      console.error('Error fetching repositories:', error)
      throw error
    }
  }

  static async getBranches(connection: GitConnection, repoFullName: string): Promise<string[]> {
    try {
      const response = await fetch(`${connection.provider.apiBaseUrl}/repos/${repoFullName}/branches`, {
        headers: {
          'Authorization': `Bearer ${connection.accessToken}`,
          'Accept': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch branches: ${response.statusText}`)
      }

      const branches = await response.json()
      return branches.map((branch: any) => branch.name)
    } catch (error) {
      console.error('Error fetching branches:', error)
      throw error
    }
  }

  static async createPullRequest(
    connection: GitConnection, 
    repoFullName: string, 
    title: string, 
    body: string, 
    headBranch: string, 
    baseBranch: string = 'main'
  ): Promise<any> {
    try {
      const response = await fetch(`${connection.provider.apiBaseUrl}/repos/${repoFullName}/pulls`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${connection.accessToken}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title,
          body,
          head: headBranch,
          base: baseBranch
        })
      })

      if (!response.ok) {
        throw new Error(`Failed to create pull request: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error creating pull request:', error)
      throw error
    }
  }
}