import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'

export async function GET(request: NextRequest) {
  try {
    const cookieStore = cookies()
    const provider = cookieStore.get('git_provider')?.value
    const token = cookieStore.get('git_token')?.value
    const userStr = cookieStore.get('git_user')?.value

    if (!provider || !token || !userStr) {
      return NextResponse.json({ connected: false })
    }

    const user = JSON.parse(userStr)

    return NextResponse.json({
      connected: true,
      provider,
      user,
      hasToken: !!token
    })
  } catch (error) {
    console.error('Error checking auth status:', error)
    return NextResponse.json({ connected: false })
  }
}