import { z } from 'zod';

// Enum for stop reasons
export const StopReasonSchema = z.enum([
  'completed',
  'failed',
  'timeout',
  'max_loops_reached',
  'user_cancelled',
  'validation_failed'
]);

// Schema for individual review note
export const ReviewNoteSchema = z.object({
  id: z.string(),
  type: z.enum(['suggestion', 'issue', 'question', 'approval']),
  severity: z.enum(['low', 'medium', 'high', 'critical']).default('medium'),
  message: z.string(),
  file_path: z.string().nullable(),
  line_number: z.number().int().positive().nullable(),
  created_at: z.date().default(() => new Date()),
  resolved: z.boolean().default(false)
});

// Schema for test report
export const TestReportSchema = z.object({
  total_tests: z.number().int().min(0).default(0),
  passed_tests: z.number().int().min(0).default(0),
  failed_tests: z.number().int().min(0).default(0),
  skipped_tests: z.number().int().min(0).default(0),
  coverage_percentage: z.number().min(0).max(100).nullable(),
  test_files: z.array(z.string()).default([]),
  failures: z.array(z.object({
    test_name: z.string(),
    error_message: z.string(),
    file_path: z.string(),
    line_number: z.number().int().positive().nullable()
  })).default([]),
  execution_time_ms: z.number().int().min(0).nullable()
});

// Schema for security report
export const SecurityReportSchema = z.object({
  vulnerabilities_found: z.number().int().min(0).default(0),
  critical_count: z.number().int().min(0).default(0),
  high_count: z.number().int().min(0).default(0),
  medium_count: z.number().int().min(0).default(0),
  low_count: z.number().int().min(0).default(0),
  scan_tools: z.array(z.string()).default([]),
  vulnerabilities: z.array(z.object({
    id: z.string(),
    severity: z.enum(['critical', 'high', 'medium', 'low']),
    title: z.string(),
    description: z.string(),
    file_path: z.string().nullable(),
    line_number: z.number().int().positive().nullable(),
    cwe_id: z.string().nullable(),
    cvss_score: z.number().min(0).max(10).nullable()
  })).default([]),
  scan_timestamp: z.date().nullable()
});

// Schema for build artifacts
export const BuildArtifactSchema = z.object({
  name: z.string(),
  path: z.string(),
  size_bytes: z.number().int().min(0),
  checksum: z.string().nullable(),
  created_at: z.date().default(() => new Date())
});

export const BuildArtifactsSchema = z.object({
  build_id: z.string().nullable(),
  status: z.enum(['pending', 'building', 'success', 'failed']).default('pending'),
  artifacts: z.array(BuildArtifactSchema).default([]),
  build_logs: z.string().nullable(),
  build_duration_ms: z.number().int().min(0).nullable(),
  build_timestamp: z.date().nullable()
});

// Schema for documentation artifacts
export const DocArtifactSchema = z.object({
  type: z.enum(['readme', 'api_docs', 'changelog', 'user_guide', 'technical_spec']),
  file_path: z.string(),
  content: z.string().nullable(),
  generated: z.boolean().default(false),
  last_updated: z.date().default(() => new Date())
});

export const DocArtifactsSchema = z.array(DocArtifactSchema).default([]);

// Schema for deploy result
export const DeployResultSchema = z.object({
  deployment_id: z.string().nullable(),
  environment: z.string().nullable(),
  status: z.enum(['pending', 'deploying', 'success', 'failed', 'rolled_back']).default('pending'),
  url: z.string().url().nullable(),
  deploy_logs: z.string().nullable(),
  deploy_duration_ms: z.number().int().min(0).nullable(),
  deploy_timestamp: z.date().nullable(),
  rollback_available: z.boolean().default(false)
});

// Main PipelineState schema
export const PipelineStateSchema = z.object({
  // Core pipeline data
  req_summary: z.string().min(1, "Request summary is required"),
  repo_url: z.string().url("Must be a valid repository URL"),
  branch: z.string().min(1, "Branch name is required").default('main'),
  
  // Code changes
  code_patch: z.string().nullable(), // unified diff format
  
  // Review and feedback
  review_notes: z.array(ReviewNoteSchema).default([]),
  
  // Testing
  test_report: TestReportSchema.nullable(),
  
  // Documentation
  doc_artifacts: DocArtifactsSchema,
  
  // Security
  security_report: SecurityReportSchema.nullable(),
  
  // Build and deployment
  build_artifacts: BuildArtifactsSchema.nullable(),
  deploy_result: DeployResultSchema.nullable(),
  
  // Loop control and termination
  loop_counts: z.record(z.string(), z.number().int().min(0)).default({}),
  stop_reason: StopReasonSchema.nullable(),
  
  // Metadata
  created_at: z.date().default(() => new Date()),
  updated_at: z.date().default(() => new Date())
});

// Type exports
export type StopReason = z.infer<typeof StopReasonSchema>;
export type ReviewNote = z.infer<typeof ReviewNoteSchema>;
export type TestReport = z.infer<typeof TestReportSchema>;
export type SecurityReport = z.infer<typeof SecurityReportSchema>;
export type BuildArtifacts = z.infer<typeof BuildArtifactsSchema>;
export type DocArtifacts = z.infer<typeof DocArtifactsSchema>;
export type DocArtifact = z.infer<typeof DocArtifactSchema>;
export type DeployResult = z.infer<typeof DeployResultSchema>;
export type PipelineState = z.infer<typeof PipelineStateSchema>;

// Helper functions for state manipulation
export const createInitialPipelineState = (
  req_summary: string,
  repo_url: string,
  branch?: string
): PipelineState => {
  return PipelineStateSchema.parse({
    req_summary,
    repo_url,
    branch: branch || 'main',
    code_patch: null,
    test_report: null,
    security_report: null,
    build_artifacts: null,
    deploy_result: null,
    stop_reason: null
  });
};

export const updateLoopCount = (state: PipelineState, loopName: string): PipelineState => {
  const currentCount = state.loop_counts[loopName] || 0;
  return {
    ...state,
    loop_counts: {
      ...state.loop_counts,
      [loopName]: currentCount + 1
    },
    updated_at: new Date()
  };
};

export const validatePipelineState = (data: unknown): PipelineState => {
  return PipelineStateSchema.parse(data);
};