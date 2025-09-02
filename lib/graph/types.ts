import { z } from 'zod'

// Base state schema for the SDLC pipeline
export const SDLCStateSchema = z.object({
  requirements: z.string().optional(),
  plan: z.string().optional(),
  code: z.string().optional(),
  review: z.string().optional(),
  status: z.enum(['planning', 'developing', 'reviewing', 'completed']).default('planning'),
  errors: z.array(z.string()).default([]),
  metadata: z.record(z.any()).default({})
})

export type SDLCState = z.infer<typeof SDLCStateSchema>

// Node input/output schemas
export const NodeInputSchema = z.object({
  state: SDLCStateSchema,
  input: z.string()
})

export const NodeOutputSchema = z.object({
  state: SDLCStateSchema,
  output: z.string()
})

export type NodeInput = z.infer<typeof NodeInputSchema>
export type NodeOutput = z.infer<typeof NodeOutputSchema>