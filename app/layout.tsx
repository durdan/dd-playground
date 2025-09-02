import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'LangGraph SDLC Pipeline',
  description: 'Agent-to-agent software development lifecycle pipeline using LangGraph',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-background text-foreground">
        <header className="border-b border-gray-200 dark:border-gray-800">
          <div className="container mx-auto px-4 py-4">
            <h1 className="text-2xl font-bold">LangGraph SDLC Pipeline</h1>
          </div>
        </header>
        <main className="container mx-auto px-4 py-8">
          {children}
        </main>
      </body>
    </html>
  )
}