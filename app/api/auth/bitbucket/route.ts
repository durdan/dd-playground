import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const code = searchParams.get('code')
  
  if (!code) {
    // Redirect to Bitbucket OAuth
    const clientId = process.env.BITBUCKET_CLIENT_ID
    if (!clientId) {
      return NextResponse.json({ error: 'Bitbucket OAuth not configured' }, { status: 500 })
    }
    
    const redirectUri = `${process.env.NEXTAUTH_URL || 'http://localhost:3000'}/api/auth/bitbucket`
    const bitbucketAuthUrl = `https://bitbucket.org/site/oauth2/authorize?client_id=${clientId}&response_type=code&redirect_uri=${redirectUri}&scope=repositories:read,account`
    
    return NextResponse.redirect(bitbucketAuthUrl)
  }
  
  try {
    // Exchange code for access token
    const tokenResponse = await fetch('https://bitbucket.org/site/oauth2/access_token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Basic ${Buffer.from(`${process.env.BITBUCKET_CLIENT_ID}:${process.env.BITBUCKET_CLIENT_SECRET}`).toString('base64')}`
      },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
      }),
    })
    
    const tokenData = await tokenResponse.json()
    
    if (tokenData.error) {
      throw new Error(tokenData.error_description || 'OAuth error')
    }
    
    // Get user info
    const userResponse = await fetch('https://api.bitbucket.org/2.0/user', {
      headers: {
        'Authorization': `Bearer ${tokenData.access_token}`,
        'Accept': 'application/json',
      },
    })
    
    const userData = await userResponse.json()
    
    // Store in session/cookies
    const redirectResponse = NextResponse.redirect(new URL('/', request.url))
    redirectResponse.cookies.set('git_provider', 'bitbucket', { httpOnly: true, secure: true })
    redirectResponse.cookies.set('git_token', tokenData.access_token, { httpOnly: true, secure: true })
    redirectResponse.cookies.set('git_user', JSON.stringify({
      username: userData.username,
      userId: userData.uuid,
      name: userData.display_name || userData.username
    }), { httpOnly: true, secure: true })
    
    return redirectResponse
    
  } catch (error) {
    console.error('Bitbucket OAuth error:', error)
    return NextResponse.json({ error: 'Authentication failed' }, { status: 500 })
  }
}