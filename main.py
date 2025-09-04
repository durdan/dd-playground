#!/usr/bin/env python3
"""
Main entry point for the developer CLI tool.
"""
from cli import CLI
from example_commands import GreetCommand, StatusCommand, ConfigCommand

def main():
    # Create CLI application
    app = CLI(app_name="devcli", version="1.0.0")
    
    # Register custom commands
    app.register_command(GreetCommand())
    app.register_command(StatusCommand())
    app.register_command(ConfigCommand())
    
    # Run the CLI
    return app.run()

if __name__ == "__main__":
    exit(main())