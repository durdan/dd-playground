#!/usr/bin/env python3
"""
Developer-friendly CLI framework with notifications and documentation.
"""
import sys
import argparse
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

class NotificationLevel:
    SUCCESS = "success"
    ERROR = "error" 
    WARNING = "warning"
    INFO = "info"

class Notifier:
    """Handle different types of notifications with proper formatting."""
    
    COLORS = {
        NotificationLevel.SUCCESS: "\033[92m",  # Green
        NotificationLevel.ERROR: "\033[91m",    # Red
        NotificationLevel.WARNING: "\033[93m",  # Yellow
        NotificationLevel.INFO: "\033[94m",     # Blue
    }
    RESET = "\033[0m"
    
    @classmethod
    def notify(cls, message: str, level: str = NotificationLevel.INFO, prefix: bool = True):
        """Send a notification with appropriate formatting."""
        if level not in cls.COLORS:
            raise ValueError(f"Invalid notification level: {level}")
        
        color = cls.COLORS[level]
        level_prefix = f"[{level.upper()}] " if prefix else ""
        print(f"{color}{level_prefix}{message}{cls.RESET}")
    
    @classmethod
    def success(cls, message: str):
        cls.notify(message, NotificationLevel.SUCCESS)
    
    @classmethod
    def error(cls, message: str):
        cls.notify(message, NotificationLevel.ERROR)
    
    @classmethod
    def warning(cls, message: str):
        cls.notify(message, NotificationLevel.WARNING)
    
    @classmethod
    def info(cls, message: str):
        cls.notify(message, NotificationLevel.INFO)

class Command(ABC):
    """Base class for CLI commands."""
    
    def __init__(self):
        self.name = self.__class__.__name__.lower().replace('command', '')
        self.description = self.__doc__ or f"Execute {self.name} command"
    
    @abstractmethod
    def execute(self, args: argparse.Namespace) -> int:
        """Execute the command. Return 0 for success, non-zero for failure."""
        pass
    
    def add_arguments(self, parser: argparse.ArgumentParser):
        """Add command-specific arguments to the parser."""
        pass

class CommandRegistry:
    """Registry for managing CLI commands."""
    
    def __init__(self):
        self._commands: Dict[str, Command] = {}
    
    def register(self, command: Command):
        """Register a new command."""
        if not isinstance(command, Command):
            raise ValueError("Command must inherit from Command class")
        
        self._commands[command.name] = command
        Notifier.info(f"Registered command: {command.name}")
    
    def get_command(self, name: str) -> Optional[Command]:
        """Get a command by name."""
        return self._commands.get(name)
    
    def list_commands(self) -> List[str]:
        """List all registered command names."""
        return list(self._commands.keys())
    
    def get_all_commands(self) -> Dict[str, Command]:
        """Get all registered commands."""
        return self._commands.copy()

class DocumentationGenerator:
    """Generate documentation for CLI commands."""
    
    def __init__(self, registry: CommandRegistry, app_name: str = "cli"):
        self.registry = registry
        self.app_name = app_name
    
    def generate_help(self) -> str:
        """Generate help text for all commands."""
        commands = self.registry.get_all_commands()
        if not commands:
            return f"No commands registered for {self.app_name}"
        
        help_text = [f"{self.app_name} - Developer CLI Tool\n"]
        help_text.append("Available commands:")
        
        for name, command in sorted(commands.items()):
            help_text.append(f"  {name:<15} {command.description}")
        
        help_text.append(f"\nUse '{self.app_name} <command> --help' for command-specific help")
        return "\n".join(help_text)
    
    def generate_markdown_docs(self) -> str:
        """Generate markdown documentation."""
        commands = self.registry.get_all_commands()
        if not commands:
            return f"# {self.app_name}\n\nNo commands available."
        
        docs = [f"# {self.app_name} CLI Documentation\n"]
        docs.append("## Available Commands\n")
        
        for name, command in sorted(commands.items()):
            docs.append(f"### {name}")
            docs.append(f"{command.description}\n")
            docs.append(f"