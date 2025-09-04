#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from cli.commands import RunCommand, PlanCommand, StatusCommand
from cli.exceptions import CrewAIError


def create_parser():
    parser = argparse.ArgumentParser(description='CrewAI CLI Interface')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Execute a crew')
    run_parser.add_argument('crew_name', help='Name of the crew to run')
    run_parser.add_argument('--config', help='Path to crew configuration file')
    
    # Plan command
    plan_parser = subparsers.add_parser('plan', help='Show execution plan for a crew')
    plan_parser.add_argument('crew_name', help='Name of the crew to plan')
    plan_parser.add_argument('--config', help='Path to crew configuration file')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show crew status')
    status_parser.add_argument('crew_name', nargs='?', help='Name of specific crew (optional)')
    
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'run':
            command = RunCommand()
            command.execute(args.crew_name, args.config)
        elif args.command == 'plan':
            command = PlanCommand()
            command.execute(args.crew_name, args.config)
        elif args.command == 'status':
            command = StatusCommand()
            command.execute(args.crew_name)
        
        return 0
        
    except CrewAIError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())