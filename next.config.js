/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['langgraph', 'langchain']
  }
}

module.exports = nextConfig