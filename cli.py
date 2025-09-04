import click
import json
from pathlib import Path
from typing import Optional

from .plan_executor import PlanExecutor

@click.group()
def cli():
    """Extended CLI with CrewAI orchestration capabilities."""
    pass

@cli.command()
@click.option('--plan', type=str, help='Plan as JSON string')
@click.option('--plan-file', type=click.Path(exists=True, path_type=Path), help='Path to plan file')
@click.option('--crew', is_flag=True, help='Use CrewAI orchestration')
@click.option('--crew-config', type=click.Path(exists=True, path_type=Path), help='Path to crew configuration file')
@click.option('--output', type=click.Path(path_type=Path), help='Output file for results')
def execute(plan: Optional[str], plan_file: Optional[Path], crew: bool, 
           crew_config: Optional[Path], output: Optional[Path]):
    """Execute a plan with optional CrewAI orchestration."""
    
    if not plan and not plan_file:
        raise click.UsageError("Either --plan or --plan-file must be provided")
    
    if plan and plan_file:
        raise click.UsageError("Cannot specify both --plan and --plan-file")
    
    # Load crew config if provided
    crew_config_data = None
    if crew_config:
        crew_config_data = json.loads(crew_config.read_text())
    
    # Create executor
    executor = PlanExecutor(use_crew=crew, crew_config=crew_config_data)
    
    try:
        # Execute plan
        if plan_file:
            result = executor.execute_plan_file(plan_file)
        else:
            plan_data = json.loads(plan)
            result = executor.execute_plan(plan_data)
        
        # Output results
        if output:
            output.write_text(json.dumps(result, indent=2))
            click.echo(f"Results written to {output}")
        else:
            click.echo(json.dumps(result, indent=2))
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()