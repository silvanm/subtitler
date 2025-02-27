"""
Audio extraction module for the video subtitling tool.

This module provides functionality to extract audio from video files
using FFmpeg for further processing with Whisper.
"""

import logging
from pathlib import Path
from typing import Optional

from subtitler.utils import run_command, validate_file_exists

logger = logging.getLogger("subtitler.audio")


def extract_audio(
    video_file: Path,
    output_file: Optional[Path] = None,
    sample_rate: int = 16000,
    channels: int = 1,
) -> Path:
    """
    Extract audio from a video file using FFmpeg.

    Args:
        video_file (Path): Path to the video file
        output_file (Optional[Path]): Path to save the extracted audio
                                     (if None, uses video filename with .wav extension)
        sample_rate (int): Audio sample rate in Hz
        channels (int): Number of audio channels (1 for mono, 2 for stereo)

    Returns:
        Path: Path to the extracted audio file

    Raises:
        FileNotFoundError: If the video file does not exist
        RuntimeError: If audio extraction fails
    """
    # Validate input file
    video_path = validate_file_exists(video_file)

    # Determine output file if not provided
    if output_file is None:
        output_file = video_path.with_suffix(".wav")

    logger.info(f"Extracting audio from {video_path} to {output_file}")

    # Build FFmpeg command
    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vn",  # No video
        "-acodec",
        "pcm_s16le",  # PCM 16-bit little-endian audio
        "-ar",
        str(sample_rate),  # Sample rate
        "-ac",
        str(channels),  # Channels
        "-y",  # Overwrite output file if it exists
        str(output_file),
    ]

    # Run FFmpeg command
    returncode, stdout, stderr = run_command(cmd)

    if returncode != 0:
        logger.error(f"Audio extraction failed: {stderr}")
        raise RuntimeError(f"Failed to extract audio: {stderr}")

    logger.info("Audio extraction completed successfully")
    return output_file
