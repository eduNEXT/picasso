"""Script to search for errors in the build process and stop the workflow. 
Also highlight some warings.

To use this script, you need to:

1. Pass the required and optional keys as command-line arguments.
2. The script will print the error or warning line.
3. Prevent the execution of the next step if a error is detected.

You can run the script using the following command:

python ./scripts/identify_silent_errors.py {{ file_path }}

See the `parse_args` function for more details on the command-line arguments. Find a usage example in the `.github/workflows/build.yml` file.
"""

import re
import sys
import argparse


def parse_error(build_logs: str):
    """
    Search for errors that does not stop the build process but
    result in an unusable image.

    Arg:
        build_logs: Build process logs to scan
    """
    error_list = [
        "^Error",
        "ValueError",
        "Theme not found",
        "ERROR: Repository not found",
    ]

    warning_list = [
        "fatal: not a git repository (or any of the parent directories): .git",
        "Error: No such command 'init'",
    ]

    for line_number, line in enumerate(build_logs, 1):
        if any(keyword.lower() in line.lower() for keyword in warning_list):
            print("\033[33m", f"Warning at line {line_number}: {line}")
            continue

        if any(re.search(keyword, line) for keyword in error_list):
            print(
                "\033[31m",
                f"Error detected in build process at line {line_number}: {line}",
            )
            sys.exit(1)


def parse_args():
    """Parse command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Process a build log file and search for errors."
    )

    parser.add_argument(
        "file_path",
        type=str,
        help="Path to the log file",
    )
    args = parser.parse_args()

    return args


def main(args):
    """
    Open the logs file and read its content to be processed.
    """
    file_path = args.file_path

    with open(file_path, "r", encoding="utf-8") as build_logs:
        parse_error(build_logs)


if __name__ == "__main__":
    main(parse_args())
