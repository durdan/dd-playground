import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const repo = searchParams.get('repo')
    
    if (!repo) {
      return NextResponse.json({ error: 'Repository parameter required' }, { status: 400 })
    }

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
        apiUrl = `https://api.github.com/repos/${repo}/branches`
        break
      case 'bitbucket':
        apiUrl = `https://api.bitbucket.org/2.0/repositories/${repo}/refs/branches`
        break
      case 'gitlab':
        const projectId = encodeURIComponent(repo)
        apiUrl = `https://gitlab.com/api/v4/projects/${projectId}/repository/branches`
        break
      default:
        return NextResponse.json({ error: 'Unsupported provider' }, { status: 400 })
    }

    const response = await fetch(apiUrl, { headers })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch branches: ${response.statusText}`)
    }

    const data = await response.json()
    let branches = []

    switch (provider) {
      case 'github':
        branches = data.map((branch: any) => branch.name)
        break
      case 'bitbucket':
        branches = (data.values || []).map((branch: any) => branch.name)
        break
      case 'gitlab':
        branches = data.map((branch: any) => branch.name)
        break
    }

    return NextResponse.json(branches)
  } catch (error) {
    console.error('Error fetching branches:', error)
    return NextResponse.json({ error: 'Failed to fetch branches' }, { status: 500 })
  }
}