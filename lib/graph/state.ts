import { z } from 'zod';

const PipelineState = z.object({
  req_summary: z.string(),
  repo_url: z.string().url(),
  branch: z.string(),
  code_patch: z.string(),
  review_notes: z.array(z.string()),
  test_report: z.object({
    passed: z.number(),
    failed: z.number(),
    skipped: z.number(),
    details: z.array(z.object({
      test: z.string(),
      outcome: z.string(),
      duration: z.number().nullable().default(null),
      error_message: z.string().nullable().default(null)
    })).optional().default([])
  }),
  doc_artifacts: z.array(z.string()).optional().default([]),
  security_report: z.object({
    vulnerabilities: z.number(),
    issues: z.array(z.object({
      id: z.string(),
      level: z.string(),
      description: z.string()
    })).optional().default([])
  }),
  build_artifacts: z.array(z.string()).optional().default([]),
  deploy_result: z.object({
    success: z.boolean(),
    environment: z.string().nullable().default(null),
    url: z.string().url().nullable().default(null)
  }),
  loop_counts: z.record(z.number()).optional().default({}),
  stop_reason: z.string().nullable().default(null)
});

export { PipelineState };