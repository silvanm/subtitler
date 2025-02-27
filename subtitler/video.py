"""
Video processing module for the video subtitling tool.

This module provides functionality to embed subtitles into video files
using FFmpeg.
"""

import logging
from pathlib import Path
from typing import Optional

from subtitler.utils import run_command, validate_file_exists

logger = logging.getLogger("subtitler.video")


def embed_subtitles(
    video_file: Path,
    subtitle_file: Path,
    output_file: Optional[Path] = None,
    font_size: int = 24,
    position: str = "lower_center",
    font_color: str = "white",
    font_outline: str = "black",
    outline_width: float = 1.0,
) -> Path:
    """
    Embed subtitles into a video file using FFmpeg.

    Args:
        video_file (Path): Path to the video file
        subtitle_file (Path): Path to the subtitle file (SRT format)
        output_file (Optional[Path]): Path to save the output video
                                     (if None, uses video filename with _subtitled suffix)
        font_size (int): Font size for subtitles
        position (str): Position of subtitles (lower_center, lower_left, lower_right, etc.)
        font_color (str): Font color
        font_outline (str): Outline color
        outline_width (float): Outline width

    Returns:
        Path: Path to the output video file

    Raises:
        FileNotFoundError: If the video or subtitle file does not exist
        RuntimeError: If subtitle embedding fails
    """
    # Validate input files
    video_path = validate_file_exists(video_file)
    subtitle_path = validate_file_exists(subtitle_file)

    # Determine output file if not provided
    if output_file is None:
        output_file = video_path.with_stem(f"{video_path.stem}_subtitled")

    logger.info(f"Embedding subtitles from {subtitle_path} into {video_path}")

    # Map position to FFmpeg alignment value
    alignment = "2"  # Default: lower center
    if position == "lower_left":
        alignment = "1"
    elif position == "lower_right":
        alignment = "3"
    elif position == "upper_left":
        alignment = "7"
    elif position == "upper_center":
        alignment = "8"
    elif position == "upper_right":
        alignment = "9"

    # Build FFmpeg command
    # Using subtitles filter with force_style to customize appearance
    style = (
        f"Alignment={alignment},"
        f"FontSize={font_size},"
        f"PrimaryColour=&H{font_color_to_hex(font_color)},"
        f"OutlineColour=&H{font_color_to_hex(font_outline)},"
        f"BorderStyle=1,"
        f"Outline={outline_width},"
        f"MarginV=30"
    )

    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vf",
        f"subtitles={subtitle_path}:force_style='{style}'",
        "-c:a",
        "copy",  # Copy audio stream without re-encoding
        "-y",  # Overwrite output file if it exists
        str(output_file),
    ]

    # Run FFmpeg command
    returncode, stdout, stderr = run_command(cmd)

    if returncode != 0:
        logger.error(f"Subtitle embedding failed: {stderr}")
        raise RuntimeError(f"Failed to embed subtitles: {stderr}")

    logger.info(f"Subtitle embedding completed successfully: {output_file}")
    return output_file


def font_color_to_hex(color: str) -> str:
    """
    Convert a color name to FFmpeg-compatible hex format.

    Args:
        color (str): Color name (white, black, yellow, etc.)

    Returns:
        str: Hex color code in FFmpeg format
    """
    # Common colors in BGR format (FFmpeg uses BGR)
    colors = {
        "white": "FFFFFF",
        "black": "000000",
        "yellow": "00FFFF",
        "red": "0000FF",
        "green": "00FF00",
        "blue": "FF0000",
        "cyan": "FFFF00",
        "magenta": "FF00FF",
    }

    return colors.get(color.lower(), "FFFFFF")  # Default to white if color not found
