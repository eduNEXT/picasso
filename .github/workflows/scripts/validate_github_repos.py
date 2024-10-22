"""
Validate that GitHub repository URLs exist in the YAML configuration file.

This script checks whether the specified GitHub repositories and branches
defined in a YAML file are accessible, ensuring that they exist and are reachable.
"""

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import List, Optional

import requests
import yaml
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate GitHub repository URLs in a YAML configuration file."
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to the YAML configuration file.",
    )
    return parser.parse_args()


def load_yaml(file_path: Path) -> Optional[dict]:
    """Load data from a YAML file."""
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return data
    except yaml.YAMLError as e:
        logger.exception(f"Failed to parse YAML file: {file_path}")
        return None
    except FileNotFoundError:
        logger.exception(f"YAML file not found: {file_path}")
        return None


def validate_github_url(url: str) -> bool:
    """Check if a GitHub URL is accessible."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.info(f"Successfully accessed URL: {url}")
        return True
    except RequestException as e:
        logger.error(f"Failed to access URL: {url} | Exception: {e}")
        return False


def strip_git_suffix(repo_url: str) -> str:
    """Remove '.git' suffix from a repository URL if present."""
    return repo_url[:-4] if repo_url.endswith(".git") else repo_url


def validate_edx_platform_repository(data: dict) -> bool:
    """Validate the EDX_PLATFORM_REPOSITORY and EDX_PLATFORM_VERSION."""
    repo_url = data.get("EDX_PLATFORM_REPOSITORY", "")
    repo_url = strip_git_suffix(repo_url)
    version = data.get("EDX_PLATFORM_VERSION", "main")  # Default to 'main' if not specified

    full_url = f"{repo_url}/tree/{version}"
    logger.info(f"Validating EDX_PLATFORM_REPOSITORY URL: {full_url}")
    return validate_github_url(full_url)


def validate_openedx_extra_pip_requirements(data: dict) -> bool:
    """Validate repositories specified in OPENEDX_EXTRA_PIP_REQUIREMENTS."""
    requirements: List[str] = data.get("OPENEDX_EXTRA_PIP_REQUIREMENTS", [])
    git_url_pattern = re.compile(r"git\+(https?://[^@]+)@([^#]+)")

    all_valid = True
    for requirement in requirements:
        match = git_url_pattern.search(requirement)
        if match:
            repo_url = strip_git_suffix(match.group(1))
            version = match.group(2)
            full_url = f"{repo_url}/tree/{version}"
            logger.info(f"Validating requirement URL: {full_url}")
            if not validate_github_url(full_url):
                logger.error(f"Invalid requirement URL or version: {full_url}")
                all_valid = False
        else:
            logger.warning(f"No valid Git URL found in requirement: {requirement}")
    return all_valid


def main() -> int:
    """Main function to validate GitHub repository URLs in the YAML file."""
    args = parse_arguments()
    data = load_yaml(args.file)

    if data is None:
        return 1

    valid_edx_repo = validate_edx_platform_repository(data)
    valid_requirements = validate_openedx_extra_pip_requirements(data)

    if valid_edx_repo and valid_requirements:
        logger.info("All repository URLs and branches are valid.")
        return 0
    else:
        logger.error("One or more repository URLs or branches are invalid.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
