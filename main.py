#!/usr/bin/env python3
import argparse
import sys
from ci_workflow import CIWorkflow
from workflow_config import WorkflowConfig

def main():
    parser = argparse.ArgumentParser(description="CI Workflow with Docker and GitHub PR")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--branch", required=True, help="Branch name for PR")
    parser.add_argument("--title", required=True, help="PR title")
    parser.add_argument("--build-only", action="store_true", help="Only run build")
    parser.add_argument("--test-only", action="store_true", help="Only run tests")
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        if args.config:
            config = WorkflowConfig.from_file(args.config)
        else:
            config = WorkflowConfig.from_env()
        
        workflow = CIWorkflow(config)
        
        if args.build_only:
            result = workflow.run_build()
            sys.exit(0 if result.success else 1)
        elif args.test_only:
            result = workflow.run_tests()
            sys.exit(0 if result.success else 1)
        else:
            success = workflow.run_full_workflow(args.branch, args.title)
            sys.exit(0 if success else 1)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()