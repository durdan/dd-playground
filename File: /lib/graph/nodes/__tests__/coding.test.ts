import { CodingAssistantAgent } from '../coding';
import { AgentState } from '../../state';

describe('CodingAssistantAgent', () => {
  let agent: CodingAssistantAgent;
  let mockState: AgentState;

  beforeEach(() => {
    agent = new CodingAssistantAgent();
    mockState = {
      req_summary: 'Add user authentication feature',
      repo_url: 'https://github.com/example/repo',
      branch: 'feature/auth',
      code_patch: '',
      patch_summary: ''
    };
  });

  describe('input validation', () => {
    it('should require req_summary', async () => {
      mockState.req_summary = '';
      
      await expect(agent.execute(mockState)).rejects.toThrow('req_summary is required');
    });

    it('should require repo_url', async () => {
      mockState.repo_url = '';
      
      await expect(agent.execute(mockState)).rejects.toThrow('repo_url is required');
    });

    it('should require branch', async () => {
      mockState.branch = '';
      
      await expect(agent.execute(mockState)).rejects.toThrow('branch is required');
    });
  });

  describe('response processing', () => {
    it('should extract diff and summary from valid response', async () => {
      const mockResponse = `Here's the implementation:

\`\`\`diff
--- a/src/auth.ts
+++ b/src/auth.ts
@@ -1,3 +1,8 @@
 export class Auth {
+  login(user: string, pass: string) {
+    return user === 'admin' && pass === 'secret';
+  }
+
   logout() {
     // existing code
   }
\`\`\`

\`\`\`patch_summary
Added login method to Auth class with basic username/password validation
\`\`\``;

      // Mock the LLM call
      jest.spyOn(agent as any, 'callLLM').mockResolvedValue(mockResponse);

      await agent.execute(mockState);

      expect(mockState.code_patch).toContain('--- a/src/auth.ts');
      expect(mockState.code_patch).toContain('+++ b/src/auth.ts');
      expect(mockState.code_patch).toContain('login(user: string, pass: string)');
      expect(mockState.patch_summary).toBe('Added login method to Auth class with basic username/password validation');
    });

    it('should handle optional inputs in prompt', async () => {
      mockState.review_notes = 'Consider using bcrypt for passwords';
      mockState.test_report = 'Coverage: 85%';
      mockState.security_report = 'No vulnerabilities found';

      const mockResponse = `\`\`\`diff
--- a/test.ts
+++ b/test.ts
@@ -1 +1,2 @@
 // test
+// updated
\`\`\`

\`\`\`patch_summary
Minor test update
\`\`\``;

      jest.spyOn(agent as any, 'callLLM').mockResolvedValue(mockResponse);

      await agent.execute(mockState);

      expect(mockState.code_patch).toContain('// updated');
      expect(mockState.patch_summary).toBe('Minor test update');
    });

    it('should reject response without diff block', async () => {
      const mockResponse = `\`\`\`patch_summary
Summary without diff
\`\`\``;

      jest.spyOn(agent as any, 'callLLM').mockResolvedValue(mockResponse);

      await expect(agent.execute(mockState)).rejects.toThrow('No unified diff patch found');
    });

    it('should reject response without summary block', async () => {
      const mockResponse = `\`\`\`diff
--- a/file.ts
+++ b/file.ts
@@ -1 +1,2 @@
 line1
+line2
\`\`\``;

      jest.spyOn(agent as any, 'callLLM').mockResolvedValue(mockResponse);

      await expect(agent.execute(mockState)).rejects.toThrow('No patch summary found');
    });

    it('should reject empty diff content', async () => {
      const mockResponse = `\`\`\`diff

\`\`\`

\`\`\`patch_summary
Empty diff
\`\`\``;

      jest.spyOn(agent as any, 'callLLM').mockResolvedValue(mockResponse);

      await expect(agent.execute(mockState)).rejects.toThrow('Empty diff patch provided');
    });

    it('should validate basic diff format', async () => {
      const mockResponse = `\`\`\`diff
just some random text without diff markers
\`\`\`

\`\`\`patch_summary
Invalid diff format
\`\`\``;

      jest.spyOn(agent as any, 'callLLM').mockResolvedValue(mockResponse);

      await expect(agent.execute(mockState)).rejects.toThrow('Invalid unified diff format');
    });
  });
});