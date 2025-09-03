import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'

export async function GET(request: NextRequest) {
  try {
    const cookieStore = cookies()
    const provider = cookieStore.get('git_provider')?.value
    const token = cookieStore.get('git_token')?.value

    if (!provider || !token) {
      return NextResponse.json({ error: 'Not authenticated' }, { status: 401 })
    }

    let apiUrl = ''
    let headers = {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/json'
    }

    switch (provider) {
      case 'github':
        apiUrl = 'https://api.github.com/user/repos?sort=updated&per_page=50'
        break
      case 'bitbucket':
        apiUrl = 'https://api.bitbucket.org/2.0/repositories?role=member&sort=-updated_on&pagelen=50'
        break
      case 'gitlab':
        apiUrl = 'https://gitlab.com/api/v4/projects?membership=true&sort=last_activity_at&per_page=50'
        break
      default:
        return NextResponse.json({ error: 'Unsupported provider' }, { status: 400 })
    }

    const response = await fetch(apiUrl, { headers })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch repositories: ${response.statusText}`)
    }

    const data = await response.json()
    let repositories = []

    switch (provider) {
      case 'github':
        repositories = data.map((repo: any) => ({
          id: repo.id.toString(),
          name: repo.name,
          fullName: repo.full_name,
          url: repo.html_url,
          defaultBranch: repo.default_branch || 'main',
          isPrivate: repo.private,
          description: repo.description,
          provider: 'github'
        }))
        break
      case 'bitbucket':
        repositories = (data.values || []).map((repo: any) => ({
          id: repo.uuid,
          name: repo.name,
          fullName: repo.full_name,
          url: repo.links.html.href,
          defaultBranch: repo.mainbranch?.name || 'main',
          isPrivate: repo.is_private,
          description: repo.description,
          provider: 'bitbucket'
        }))
        break
      case 'gitlab':
        repositories = data.map((repo: any) => ({
          id: repo.id.toString(),
          name: repo.name,
          fullName: repo.path_with_namespace,
          url: repo.web_url,
          defaultBranch: repo.default_branch || 'main',
          isPrivate: repo.visibility === 'private',
          description: repo.description,
          provider: 'gitlab'
        }))
        break
    }

    return NextResponse.json(repositories)
  } catch (error) {
    console.error('Error fetching repositories:', error)
    return NextResponse.json({ error: 'Failed to fetch repositories' }, { status: 500 })
  }
}