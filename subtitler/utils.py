"""
Utility functions for the video subtitling tool.

This module provides helper functions for:
- Temporary file management
- Command execution
- Logging and error handling
"""

import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("subtitler")


def create_temp_dir() -> Path:
    """
    Create a temporary directory for processing files.

    Returns:
        Path: Path to the temporary directory
    """
    temp_dir = Path(tempfile.mkdtemp(prefix="subtitler_"))
    logger.debug(f"Created temporary directory: {temp_dir}")
    return temp_dir


def cleanup_temp_dir(temp_dir: Path) -> None:
    """
    Remove a temporary directory and all its contents.

    Args:
        temp_dir (Path): Path to the temporary directory
    """
    if temp_dir.exists():
        logger.debug(f"Cleaning up temporary directory: {temp_dir}")
        shutil.rmtree(temp_dir)


def run_command(
    cmd: List[str], check: bool = True, timeout: Optional[int] = None
) -> Tuple[int, str, str]:
    """
    Run a command and return its exit code, stdout, and stderr.

    Args:
        cmd (List[str]): Command to run as a list of strings
        check (bool): Whether to raise an exception if the command fails
        timeout (Optional[int]): Timeout in seconds

    Returns:
        Tuple[int, str, str]: Exit code, stdout, and stderr

    Raises:
        subprocess.CalledProcessError: If the command fails and check is True
        subprocess.TimeoutExpired: If the command times out
    """
    logger.debug(f"Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd, check=check, timeout=timeout, capture_output=True, text=True
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        return e.returncode, e.stdout, e.stderr
    except subprocess.TimeoutExpired as e:
        logger.error(f"Command timed out: {' '.join(cmd)}")
        return 1, "", f"Command timed out after {timeout} seconds"


def check_dependencies() -> bool:
    """
    Check if required dependencies (ffmpeg and whisper) are installed.

    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    dependencies = ["ffmpeg", "whisper"]
    missing = []

    for dep in dependencies:
        try:
            subprocess.run(["which", dep], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            missing.append(dep)

    if missing:
        logger.error(f"Missing dependencies: {', '.join(missing)}")
        return False

    return True


def validate_file_exists(file_path: Union[str, Path]) -> Path:
    """
    Validate that a file exists and return its Path object.

    Args:
        file_path (Union[str, Path]): Path to the file

    Returns:
        Path: Path object for the file

    Raises:
        FileNotFoundError: If the file does not exist
    """
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        logger.error(f"Not a file: {path}")
        raise ValueError(f"Not a file: {path}")

    return path


def get_output_filename(input_file: Path, suffix: str = "_subtitled") -> Path:
    """
    Generate an output filename based on the input filename.

    Args:
        input_file (Path): Input file path
        suffix (str): Suffix to add to the filename

    Returns:
        Path: Output file path
    """
    return input_file.with_stem(f"{input_file.stem}{suffix}")
