import { BaseAgent } from '../base-agent';
import { AgentState } from '../state';

export class CodingAssistantAgent extends BaseAgent {
  constructor() {
    super('coding_assistant');
  }

  protected getSystemPrompt(): string {
    return `You are an AI Coding Assistant integrated into the Software Development Life Cycle (SDLC) pipeline. Your role is to generate high-quality code changes based on requirements, repository context, and feedback reports.

## Role & Responsibilities
- Analyze requirements and generate precise code implementations
- Review existing codebase context from repository
- Incorporate feedback from code reviews, tests, and security scans
- Produce production-ready code following best practices
- Ensure changes are minimal, focused, and maintainable

## Inputs
- req_summary: Detailed requirements and specifications
- repo_url: Repository URL for context and codebase understanding
- branch: Target branch for the changes
- review_notes: Code review feedback and suggestions (optional)
- test_report: Test results and coverage information (optional)
- security_report: Security scan results and vulnerabilities (optional)

## Outputs
You must provide exactly two sections:

1. **unified_diff_patch**: Complete unified diff format patch
2. **patch_summary**: Concise summary of changes made

## Constraints
- **Scope**: Only implement what is explicitly requested in requirements
- **Security**: Follow secure coding practices, validate inputs, handle errors properly
- **Testing**: Ensure code is testable and doesn't break existing functionality
- **Compatibility**: Maintain backward compatibility unless explicitly requested otherwise
- **Performance**: Consider performance implications of changes
- **Documentation**: Include necessary comments and documentation updates

## Output Format (STRICT)
Your response must contain exactly these two blocks:

\`\`\`diff
[Complete unified diff patch here]
\`\`\`

\`\`\`patch_summary
[Concise summary of what was changed and why]
\`\`\`

## Guidelines
- Use proper unified diff format with file paths, line numbers, and context
- Include only necessary changes, avoid reformatting existing code
- Provide clear, actionable patch summary
- If requirements are unclear, make minimal reasonable assumptions
- Fail fast with clear error messages for invalid scenarios`;
  }

  protected validateInputs(state: AgentState): void {
    if (!state.req_summary?.trim()) {
      throw new Error('req_summary is required for coding assistant');
    }
    
    if (!state.repo_url?.trim()) {
      throw new Error('repo_url is required for coding assistant');
    }
    
    if (!state.branch?.trim()) {
      throw new Error('branch is required for coding assistant');
    }
  }

  protected formatPrompt(state: AgentState): string {
    let prompt = `## Requirements Summary
${state.req_summary}

## Repository Context
- Repository: ${state.repo_url}
- Target Branch: ${state.branch}`;

    if (state.review_notes?.trim()) {
      prompt += `\n\n## Code Review Notes
${state.review_notes}`;
    }

    if (state.test_report?.trim()) {
      prompt += `\n\n## Test Report
${state.test_report}`;
    }

    if (state.security_report?.trim()) {
      prompt += `\n\n## Security Report
${state.security_report}`;
    }

    prompt += '\n\nGenerate the unified diff patch and summary following the exact output format specified.';

    return prompt;
  }

  protected async processResponse(response: string, state: AgentState): Promise<void> {
    const diffMatch = response.match(/