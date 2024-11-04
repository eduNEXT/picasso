"""
Validate repository URLs and configurations in the strain config file.
"""
from __future__ import annotations

import argparse
import logging
import re
from collections.abc import Sequence
from typing import Callable, Dict, List, Any
from io import TextIOWrapper

import requests
import yaml

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def validate_repo_url(url: str) -> bool:
    """Validate a repository URL by making a GET request."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        LOG.exception("Exception while checking repo URL: %s", url)
        return False


def check_edx_platform_repo(data: Dict[str, Any]) -> bool:
    """Check the edx_platform_repository URL in the YAML data."""
    edx_platform_repository = data.get('EDX_PLATFORM_REPOSITORY', "").rstrip('.git')
    edx_platform_version = data.get('EDX_PLATFORM_VERSION', "")
    url = f"{edx_platform_repository}/tree/{edx_platform_version}"
    if not validate_repo_url(url):
        LOG.error("Failed to validate edx_platform_repository URL: %s", url)
        return False
    return True


def check_openedx_extra_pip_req_repos(data: Dict[str, Any]) -> bool:
    """Check additional pip requirement repos in the YAML data."""
    pattern = r"git\+(https?://\S+?)(?:#|$)"
    for repo in data.get('OPENEDX_EXTRA_PIP_REQUIREMENTS', []):
        match = re.search(pattern, repo)
        if match:
            url = match.group(1).replace('@', '/tree/').replace('.git', '')
            if not validate_repo_url(url):
                LOG.error("Failed to validate OPENEDX_EXTRA_PIP_REQUIREMENTS URL: %s", url)
                return False
    return True


def validate_data(data: Dict[str, Any], checks: List[Callable[[Dict[str, Any]], bool]]) -> bool:
    """Run all provided validation checks on the YAML data."""
    return all(check(data) for check in checks)


def main(argv: Sequence[str] | None = None) -> int:
    """
    Entry point for validating repository URLs in a strain configuration file.

    This function parses command-line arguments to load a YAML file, performs
    validation checks on specific repository URLs, and logs results. If any
    validation fails, an error code is returned.

    Args:
        argv (Sequence[str] | None): Optional sequence of command-line arguments.
            If None, arguments will be taken from sys.argv.

    Returns:
        int: 0 if all URLs are validated successfully, 1 if any validation fails.
    """
    parser = argparse.ArgumentParser(description="Validate repository URLs in strain config file.")
    parser.add_argument("file", type=argparse.FileType("r"), nargs="+")
    args = parser.parse_args(argv)

    strain_file: TextIOWrapper = args.file[0]
    try:
        data = yaml.safe_load(strain_file)
    except yaml.YAMLError:
        LOG.exception("Error loading YAML data.")
        return 1

    checks = [
        check_edx_platform_repo,
        check_openedx_extra_pip_req_repos
    ]

    if not validate_data(data, checks):
        return 1

    LOG.info("All repository URLs validated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
