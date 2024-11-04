#!/usr/bin/env python
"""
Validate syntax in a YAML file based on specific rules.
"""

from __future__ import annotations

import argparse
import logging
import re
from collections.abc import Sequence
from io import TextIOWrapper
from typing import Any, Dict

import yaml
from schema import Schema, And, Optional, Use, SchemaError, Regex

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TUTOR_VERSION_REGEX = r"^v\d+\.\d+\.\d+$"
EMPTY_LIST_ERROR_MSG = "{} must be a non-empty list of non-empty strings"


def perform_extra_validations(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform additional validations on the strain configuration data.

    Checks for custom conditions not covered by the schema:
    
    - Ensure either PICASSO_THEMES_NAME or PICASSO_DEFAULT_SITE_THEME is defined
    if PICASSO_THEMES exists.

    Args:
        data (Dict[str, Any]): The YAML data dictionary.

    Returns:
        Dict[str, Any]: Validated data dictionary.

    Raises:
        SchemaError: If required conditions are not met.
    """
    if "PICASSO_THEMES" in data and not ("PICASSO_THEMES_NAME" in data or "PICASSO_DEFAULT_SITE_THEME" in data):
        raise SchemaError("PICASSO_THEMES_NAME or PICASSO_DEFAULT_SITE_THEME must be defined.")
    return data

STRAIN_SCHEMA = Schema(
    Use(perform_extra_validations),
    {
        "TUTOR_VERSION": And(
            str,
            Regex(TUTOR_VERSION_REGEX, error="TUTOR_VERSION must be in the format vX.Y.Z (e.g., v5.3.0)")
        ),
        Optional(Regex(r"^PICASSO_.+_DPKG$")): {
            "name": And(str, len),
            "repo": And(str, len),
            "version": And(str, len)
        },
        Optional("PICASSO_THEMES"): And(
            list,
            len,
            [
                {
                    "name": And(str, len),
                    "repo": And(str, len),
                    "version": And(str, len)
                }
            ]
        ),
        Optional("PICASSO_THEMES_NAME"): And(
            list,
            len,
            lambda x: all(isinstance(item, str) and item for item in x),
            error=EMPTY_LIST_ERROR_MSG.format("PICASSO_THEMES_NAME"),
        ),
        Optional("PICASSO_THEME_DIRS"): And(
            list,
            len,
            lambda x: all(isinstance(item, str) and item for item in x),
            error=EMPTY_LIST_ERROR_MSG.format("PICASSO_THEME_DIRS"),
        )
    },
    ignore_extra_keys=True
)

def validate_with_warnings(data: Dict[str, Any]) -> bool:
    """
    Validate the data against the strain schema and log warnings for missing optional keys.

    Args:
        data (Dict[str, Any]): The loaded YAML data to validate.

    Returns:
        bool: True if validation is successful; otherwise, False.

    Logs warnings for missing optional keys such as PICASSO_THEMES and PICASSO_THEMES_NAME.
    """
    try:
        STRAIN_SCHEMA.validate(data)
        if not data.get("PICASSO_THEMES"):
            LOG.warning("No PICASSO_THEMES key found; themes will not be enabled.")
        if not data.get("PICASSO_THEMES") and not data.get("PICASSO_THEMES_NAME"):
            LOG.warning("No PICASSO_THEMES_NAME key found; default themes will be used.")
        LOG.info("Strain syntax and structure validation completed successfully.")
        return True
    except SchemaError as e:
        LOG.error("Schema validation failed: %s", e)
        return False

def validate_yaml_file(yaml_file: TextIOWrapper) -> bool:
    """
    Load and validate YAML file structure against the defined schema.

    Args:
        yaml_file (TextIOWrapper): Opened YAML file for reading.

    Returns:
        bool: True if YAML content is valid; otherwise, False.

    Logs syntax errors in the YAML structure.
    """
    try:
        config_yml = yaml.safe_load(yaml_file)
        return validate_with_warnings(config_yml)
    except yaml.YAMLError as yaml_error:
        LOG.error("YAML syntax error: %s", yaml_error)
    return False

def main(argv: Sequence[str] | None = None) -> int:
    """
    Execute syntax checks on a configuration file for strains.

    Args:
        argv (Sequence[str] | None): Command-line arguments.

    Returns:
        int: 0 if configuration file is valid; 1 if invalid.
    """
    parser = argparse.ArgumentParser(description="Validate YAML file syntax and strain schema.")
    parser.add_argument("file", type=argparse.FileType("r"), nargs="+", help="YAML file to validate.")
    args = parser.parse_args(argv)

    strain_file: TextIOWrapper = args.file[0]
    if not validate_yaml_file(strain_file):
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
