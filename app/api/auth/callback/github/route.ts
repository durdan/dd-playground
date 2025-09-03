import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const code = searchParams.get('code')
  
  if (!code) {
    // Redirect to GitHub OAuth
    const clientId = process.env.GITHUB_CLIENT_ID
    if (!clientId) {
      return NextResponse.json({ error: 'GitHub OAuth not configured' }, { status: 500 })
    }
    
    const redirectUri = `${process.env.NEXTAUTH_URL || 'http://localhost:3000'}/api/auth/callback/github`
    const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=repo,user`
    
    return NextResponse.redirect(githubAuthUrl)
  }
  
  try {
    // Exchange code for access token
    const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: process.env.GITHUB_CLIENT_ID,
        client_secret: process.env.GITHUB_CLIENT_SECRET,
        code,
      }),
    })
    
    const tokenData = await tokenResponse.json()
    
    if (tokenData.error) {
      throw new Error(tokenData.error_description || 'OAuth error')
    }
    
    // Get user info
    const userResponse = await fetch('https://api.github.com/user', {
      headers: {
        'Authorization': `Bearer ${tokenData.access_token}`,
        'Accept': 'application/json',
      },
    })
    
    const userData = await userResponse.json()
    
    // Store in session/cookies (simplified - in production use proper session management)
    const redirectResponse = NextResponse.redirect(new URL('/', request.url))
    redirectResponse.cookies.set('git_provider', 'github', { httpOnly: true, secure: true })
    redirectResponse.cookies.set('git_token', tokenData.access_token, { httpOnly: true, secure: true })
    redirectResponse.cookies.set('git_user', JSON.stringify({
      username: userData.login,
      userId: userData.id.toString(),
      name: userData.name || userData.login
    }), { httpOnly: true, secure: true })
    
    return redirectResponse
    
  } catch (error) {
    console.error('GitHub OAuth error:', error)
    return NextResponse.json({ error: 'Authentication failed' }, { status: 500 })
  }
}