#!/usr/bin/env python3
"""
Regex-ing
filtered_logger
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specified fields in a log message.

    Args:
        fields (list): List of fields to obfuscate.
        redaction (str): String to replace field values with.
        message (str): Log message containing fields.
        separator (str): Separator between fields in the message.

    Returns:
        str: Obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(
        pattern,
        lambda m: f"{m.group().split('=')[0]}={redaction}",
        message
    )
