# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **LangGraph-powered SDLC Pipeline** automation framework with **real-time streaming AI agents** and **stunning n8n-style workflow visualization**. The system orchestrates multiple AI agents through real LangGraph StateGraph for autonomous planning, development, and code review phases, featuring **true token-level streaming** from OpenAI GPT-4 and **professional visual workflow management**.

## Development Commands

### Core Development
- `npm run dev` - Start Next.js development server (runs on http://localhost:3000)
- `npm run build` - Build the application for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint to check code quality

### Testing
- Tests are located in `__tests__` directories alongside source files
- Test files follow the pattern `*.test.ts`
- No specific test runner command found - check with user if needed

## Architecture Overview

### Core Components

**Real LangGraph Integration (`lib/graph/langgraph-pipeline.ts`)**
- `LangGraphSDLCPipeline` - Actual LangGraph StateGraph with proper node transitions
- **START → planning → development → review → END** workflow
- **Real-time streaming** with OpenAI token-level updates
- **Channel-based state management** with proper LangGraph patterns

**Visual Workflow System (`components/WorkflowVisualizer.tsx`)**
- **n8n-style animated workflow** with professional SVG icons
- **Real-time node status updates** synchronized with LangGraph execution
- **Interactive node selection** with detailed output viewing
- **Flowing animated connections** with gradient effects

**Claude Code Style CLI Panel (`components/CLIProgressPanel.tsx`)**
- **Terminal-style progress display** with collapsible stages
- **Real streaming content** with character-by-character typing animation
- **LangGraph orchestration indicators** and visual badges
- **Auto-scroll and auto-collapse** for optimal UX

**Multi-Provider Git Integration (`lib/git/providers.ts`)**
- **GitHub/Bitbucket/GitLab OAuth** with secure token management
- **Repository and branch selection** with real-time API calls
- **Git connection panel** with provider-specific authentication

### Key Technologies
- **Next.js 14** - React framework with App Router
- **LangGraph** - Agent orchestration and workflow management
- **LangChain** - LLM integration utilities
- **Zod** - Runtime schema validation
- **TypeScript** - Type safety throughout
- **Tailwind CSS** - Styling framework

## Configuration

### Environment Variables
Create `.env` file in root directory with:

**Required:**
- `OPENAI_API_KEY` - OpenAI API key for GPT-4 streaming
- `OPENAI_MODEL` - Model to use (default: gpt-4)

**Optional (for Git integration):**
- `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`
- `BITBUCKET_CLIENT_ID` and `BITBUCKET_CLIENT_SECRET`  
- `GITLAB_CLIENT_ID` and `GITLAB_CLIENT_SECRET`
- `NEXTAUTH_URL` - Base URL for OAuth callbacks

**LangSmith Tracing (optional):**
- `LANGCHAIN_TRACING_V2=true`
- `LANGCHAIN_API_KEY` - LangSmith API key
- `LANGCHAIN_PROJECT` - Project name for traces

### TypeScript Configuration
- Path mapping configured with `@/*` pointing to project root
- Strict mode enabled
- Next.js plugin integrated

## File Structure Patterns

- `/lib/graph/` - Core pipeline logic and agent nodes
- `/lib/graph/nodes/` - Individual agent implementations
- `/lib/graph/__tests__/` - Pipeline-level tests
- `/app/` - Next.js App Router pages and components
- Node tests co-located in `__tests__/` directories

## Development Guidelines

### State Management
- All pipeline state changes must go through Zod schema validation
- Use helper functions like `createInitialPipelineState()` and `updateLoopCount()`
- State includes comprehensive tracking: test reports, security scans, build artifacts, deployment results

### Agent Development
- Each agent node should implement the `NodeInput` → `NodeOutput` interface
- Agents operate on `SDLCState` and return updated state plus output message
- Follow existing patterns in `/lib/graph/nodes/` for consistency

### Schema Design
- Use Zod schemas for all data structures
- Export both schema and TypeScript type definitions
- Include default values and validation rules

## Dependencies Note

## 🚀 Advanced Features

### ⚡ Real-Time LangGraph Streaming
- **True token-level streaming** from OpenAI GPT-4 through LangGraph nodes
- **Character-by-character typing animation** in Claude Code style terminal
- **Real-time progress updates** via Server-Sent Events
- **LangGraph orchestration visibility** with console logging and UI indicators

### 🎨 n8n-Style Workflow Visualization  
- **Professional animated workflow** with enterprise-grade SVG icons
- **Real-time node status updates** synchronized with LangGraph execution
- **Interactive node selection** to view detailed AI-generated outputs
- **Flowing data connections** with animated gradients and particles
- **Responsive design** adapting to different screen sizes

### 🔗 Multi-Provider Git Integration
- **GitHub, Bitbucket, GitLab** OAuth 2.0 authentication
- **Repository browser** with real-time API calls
- **Branch selection** with automatic detection
- **Secure token management** with HTTP-only cookies

### 🖥️ Claude Code Style Interface
- **Terminal-style CLI progress panel** with collapsible stages
- **LangGraph branding** with purple badges and network icons
- **Auto-scroll and auto-collapse** for optimal user experience
- **Real content preservation** - no mock data, actual AI outputs

### 📊 LangGraph Orchestration Visibility
- **Console logging** with `🔗 LangGraph:` prefixed messages
- **UI indicators** showing active LangGraph nodes
- **Purple branding** throughout interface for LangGraph identity
- **Network graph icons** representing the StateGraph architecture

## Dependencies Note

This project uses specific versions of LangGraph (`@langchain/langgraph ^0.4.9`) and LangChain libraries. When adding new LLM or agent functionality, ensure compatibility with the existing LangGraph/LangChain ecosystem already established in the codebase.

## Git Provider Setup

To enable Git integration, configure OAuth apps for your providers and add to `.env.local`:
- `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`
- `BITBUCKET_CLIENT_ID` and `BITBUCKET_CLIENT_SECRET`  
- `GITLAB_CLIENT_ID` and `GITLAB_CLIENT_SECRET`