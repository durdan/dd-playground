# 🚀 LangGraph SDLC Pipeline

> **Real-time AI Agent Orchestration with Stunning Workflow Visualization**

A **LangGraph-powered Software Development Lifecycle (SDLC) Pipeline** featuring **real-time streaming AI agents**, **n8n-style workflow visualization**, and **Claude Code-inspired terminal interface**. Watch AI agents collaborate in real-time to analyze, develop, and review your code with **true token-level streaming** from OpenAI GPT-4.

![LangGraph SDLC Pipeline](https://img.shields.io/badge/LangGraph-Powered-purple?style=for-the-badge&logo=graphql)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green?style=for-the-badge&logo=openai)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript)

## ✨ Features

### 🔗 **Real LangGraph Integration**
- **Actual LangGraph StateGraph** with proper node transitions
- **START → planning → development → review → END** workflow  
- **Channel-based state management** following LangGraph patterns
- **Visible orchestration** with real-time logging and UI indicators

### ⚡ **True Real-Time Streaming**
- **Token-level streaming** from OpenAI GPT-4 through LangGraph nodes
- **Character-by-character typing animation** in terminal-style interface
- **Live progress updates** via Server-Sent Events
- **No mock data** - actual AI-generated content streams in real-time

### 🎨 **n8n-Style Workflow Visualization**
- **Professional animated workflow** with enterprise-grade SVG icons
- **Real-time node status updates** synchronized with LangGraph execution
- **Interactive node selection** to view detailed AI outputs
- **Flowing data connections** with animated gradients and particles

### 🖥️ **Claude Code Style Interface**
- **Terminal-style CLI progress panel** with collapsible stages
- **LangGraph branding** with purple badges and network icons
- **Auto-scroll and auto-collapse** for optimal user experience
- **Professional styling** matching enterprise workflow tools

### 🔗 **Multi-Provider Git Integration**
- **GitHub, Bitbucket, GitLab** OAuth 2.0 authentication
- **Repository browser** with real-time API calls
- **Branch selection** with automatic detection
- **Secure token management** with HTTP-only cookies

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- OpenAI API key
- Git providers (optional: GitHub/Bitbucket/GitLab OAuth apps)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd dd-playground
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   # Required - OpenAI Configuration
   OPENAI_API_KEY=sk-your-openai-api-key
   OPENAI_MODEL=gpt-4
   
   # Optional - Git Provider OAuth (for repository integration)
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   NEXTAUTH_URL=http://localhost:3000
   
   # Optional - LangSmith Tracing
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your_langsmith_api_key
   LANGCHAIN_PROJECT=langgraph-sdlc-pipeline
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🎯 How to Use

### 1. **Enter Requirements**
- Describe what you want to build (e.g., "create user management REST API endpoints")
- Optionally connect a Git repository for context

### 2. **Watch LangGraph Orchestration**
- **Visual workflow** shows agent progress in real-time
- **Console logs** display LangGraph node transitions: `🔗 LangGraph: planning -> streaming`
- **CLI terminal** streams content as it's generated

### 3. **View AI-Generated Content**
- **Planning Agent** creates detailed development plans
- **Development Agent** generates production-ready code
- **Review Agent** provides comprehensive code reviews
- **Click workflow nodes** to see detailed outputs

### 4. **Monitor Real-Time Streaming**
- Content appears **character-by-character** as OpenAI generates it
- **No waiting** for completion - see progress immediately
- **Auto-collapse** completed stages for clean interface

## 🏗️ Architecture

### Core Components

**LangGraph Pipeline (`lib/graph/langgraph-pipeline.ts`)**
```typescript
const graph = new StateGraph<GraphStateType>({
  channels: { /* state channels */ }
})
graph.addNode("planning", this.planningNode.bind(this))
graph.addNode("development", this.developmentNode.bind(this))  
graph.addNode("review", this.reviewNode.bind(this))
```

**Real-Time Streaming (`app/api/pipeline/stream/route.ts`)**
```typescript
const stream = await this.llm.stream([new HumanMessage(prompt)])
for await (const chunk of stream) {
  content += chunk.content
  this.onUpdate?.("planning", "streaming", content)
}
```

**Workflow Visualization (`components/WorkflowVisualizer.tsx`)**
- Professional SVG icons and animations
- Real-time status synchronization with LangGraph
- Interactive node selection and detailed output viewing

## 🔧 Development

### Project Structure
```
├── app/                    # Next.js App Router pages
│   ├── api/pipeline/      # Pipeline API endpoints  
│   └── page.tsx           # Main application interface
├── components/            # React components
│   ├── WorkflowVisualizer.tsx    # n8n-style workflow
│   ├── CLIProgressPanel.tsx      # Terminal-style progress
│   └── GitConnectionPanel.tsx    # Git provider integration
├── lib/
│   ├── graph/             # LangGraph implementation
│   │   ├── langgraph-pipeline.ts # Real LangGraph StateGraph
│   │   └── nodes/         # Legacy node implementations
│   └── git/               # Git provider integrations
└── CLAUDE.md              # Claude Code documentation
```

### Key Technologies
- **LangGraph** `@langchain/langgraph ^0.4.9` - Agent orchestration
- **LangChain** `@langchain/openai ^0.0.14` - LLM integration  
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety throughout
- **Tailwind CSS** - Professional styling
- **Zod** - Schema validation

### Development Commands
```bash
npm run dev      # Start development server
npm run build    # Build for production  
npm run start    # Start production server
npm run lint     # Run ESLint
```

## 🎨 UI Features

### LangGraph Visual Indicators
- **Purple "LangGraph" badges** throughout the interface
- **Network graph icons** representing StateGraph architecture
- **"Powered by LangGraph"** branding on workflow visualization
- **"Orchestrating Agents..."** status when pipeline is running

### Claude Code Style Terminal
- **Terminal-style header** with red/yellow/green dots
- **Collapsible stages** with expand/collapse functionality
- **Real-time content streaming** with typing animation
- **Auto-scroll** to follow content as it appears

### Professional Animations
- **Pulsing indicators** for active nodes and streaming
- **Gradient connections** between workflow nodes
- **Smooth transitions** for status changes
- **Responsive design** for different screen sizes

## 🔐 Security & Authentication

### Git Provider OAuth
- **Secure token storage** using HTTP-only cookies
- **OAuth 2.0 flow** for GitHub, Bitbucket, GitLab
- **Repository permissions** respect provider access controls

### API Security
- **Server-side OpenAI key** storage (never exposed to client)
- **Environment variable** configuration
- **CORS headers** properly configured

## 📊 Monitoring & Debugging

### LangSmith Integration
- **Trace LangGraph execution** in LangSmith dashboard
- **View token usage** and performance metrics
- **Debug agent interactions** and state transitions

### Console Logging
- **LangGraph orchestration**: `🔗 LangGraph: planning -> streaming`
- **Stream updates**: Shows content length and node transitions
- **Error handling**: Detailed error messages and stack traces

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph** team for the powerful agent orchestration framework
- **OpenAI** for GPT-4 and streaming capabilities
- **n8n** for workflow visualization inspiration
- **Claude Code** for terminal interface styling inspiration

---

<div align="center">

**Built with ❤️ using LangGraph, Next.js, and OpenAI**

[🔗 LangGraph Documentation](https://langchain.com/langgraph) • [🎯 Next.js](https://nextjs.org) • [🤖 OpenAI](https://openai.com)

</div>