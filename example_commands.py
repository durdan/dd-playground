"""
Example commands demonstrating the CLI framework.
"""
import argparse
import time
from cli import Command, Notifier

class GreetCommand(Command):
    """Greet a user with a friendly message."""
    
    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument("name", help="Name to greet")
        parser.add_argument(
            "--enthusiastic", "-e",
            action="store_true",
            help="Use enthusiastic greeting"
        )
    
    def execute(self, args: argparse.Namespace) -> int:
        if not args.name.strip():
            Notifier.error("Name cannot be empty")
            return 1
        
        greeting = f"Hello, {args.name}!"
        if args.enthusiastic:
            greeting = f"Hello, {args.name}! 🎉"
        
        Notifier.success(greeting)
        return 0

class StatusCommand(Command):
    """Check system status with different notification types."""
    
    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "--simulate-error",
            action="store_true",
            help="Simulate an error condition"
        )
    
    def execute(self, args: argparse.Namespace) -> int:
        Notifier.info("Checking system status...")
        time.sleep(1)  # Simulate work
        
        if args.simulate_error:
            Notifier.error("System check failed!")
            return 1
        
        Notifier.info("CPU: OK")
        Notifier.info("Memory: OK")
        Notifier.warning("Disk space: 85% full")
        Notifier.success("System status: Healthy")
        return 0

class ConfigCommand(Command):
    """Manage configuration settings."""
    
    def add_arguments(self, parser: argparse.ArgumentParser):
        subparsers = parser.add_subparsers(dest="action", help="Configuration actions")
        
        # Set command
        set_parser = subparsers.add_parser("set", help="Set a configuration value")
        set_parser.add_argument("key", help="Configuration key")
        set_parser.add_argument("value", help="Configuration value")
        
        # Get command
        get_parser = subparsers.add_parser("get", help="Get a configuration value")
        get_parser.add_argument("key", help="Configuration key")
        
        # List command
        subparsers.add_parser("list", help="List all configuration")
    
    def execute(self, args: argparse.Namespace) -> int:
        if not args.action:
            Notifier.error("No action specified. Use --help for options.")
            return 1
        
        # Simple in-memory config for demo
        config = {"theme": "dark", "notifications": "enabled"}
        
        if args.action == "set":
            config[args.key] = args.value
            Notifier.success(f"Set {args.key} = {args.value}")
        
        elif args.action == "get":
            value = config.get(args.key)
            if value is None:
                Notifier.error(f"Configuration key '{args.key}' not found")
                return 1
            Notifier.info(f"{args.key} = {value}")
        
        elif args.action == "list":
            Notifier.info("Current configuration:")
            for key, value in config.items():
                print(f"  {key} = {value}")
        
        return 0