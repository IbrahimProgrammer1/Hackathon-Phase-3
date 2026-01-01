"""
Main entry point for the Todo Console App.

This module runs the command-line interface for the todo application.
"""

import sys
import os

# Ensure the root directory is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.cli.commands import TodoCLI


def main():
    """
    Main function to run the Todo Console App.
    """
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()