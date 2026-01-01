"""
Input validation utilities for the Todo Console App.

This module provides utility functions for validating user inputs.
"""


def trim_whitespace(text: str) -> str:
    """
    Trim whitespace from a string.

    Args:
        text (str): The string to trim

    Returns:
        str: The trimmed string
    """
    return text.strip()


def convert_to_int(value: str) -> int:
    """
    Convert a string to an integer.

    Args:
        value (str): The string value to convert

    Returns:
        int: The converted integer

    Raises:
        ValueError: If the value cannot be converted to an integer
    """
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Cannot convert '{value}' to an integer")


def validate_non_empty(value: str, field_name: str) -> str:
    """
    Validate that a string value is not empty after trimming.

    Args:
        value (str): The string value to validate
        field_name (str): The name of the field for error messages

    Returns:
        str: The trimmed value

    Raises:
        ValueError: If the value is empty after trimming
    """
    trimmed_value = trim_whitespace(value)
    if not trimmed_value:
        raise ValueError(f"{field_name.capitalize()} cannot be empty")
    return trimmed_value


def is_valid_task_status(status: str) -> bool:
    """
    Check if a status value is valid for a task.

    Args:
        status (str): The status value to check

    Returns:
        bool: True if the status is valid, False otherwise
    """
    return status in ["incomplete", "complete"]


def format_error_message(message: str) -> str:
    """
    Format an error message with the "Error:" prefix.

    Args:
        message (str): The error message to format

    Returns:
        str: The formatted error message
    """
    return f"Error: {message}"