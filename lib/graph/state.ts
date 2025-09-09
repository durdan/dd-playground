import { z } from 'zod';

export const PipelineStateSchema = z.object({
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
      result: z.string(),
      notes: z.string().nullable()
    })).optional()
  }),
  doc_artifacts: z.array(z.string()).nullable(),
  security_report: z.object({
    vulnerabilities: z.number(),
    issues: z.array(z.object({
      level: z.enum(['low', 'medium', 'high']),
      description: z.string()
    })).optional()
  }).nullable(),
  build_artifacts: z.array(z.string()).nullable(),
  deploy_result: z.object({
    status: z.enum(['success', 'failure']),
    details: z.string().nullable()
  }).nullable(),
  loop_counts: z.record(z.number()).optional(),
  stop_reason: z.string().nullable()
});
