"""
Transcription module for the video subtitling tool.

This module provides functionality to transcribe and translate audio
using Whisper, generating subtitle files in SRT format.
"""

import logging
import os
from pathlib import Path
from typing import Optional

from subtitler.utils import run_command, validate_file_exists

logger = logging.getLogger("subtitler.transcribe")


def transcribe_audio(
    audio_file: Path,
    output_dir: Optional[Path] = None,
    model: str = "medium",
    language: str = "de",
    task: str = "translate",
    output_format: str = "srt",
) -> Path:
    """
    Transcribe and translate audio using Whisper.

    Args:
        audio_file (Path): Path to the audio file
        output_dir (Optional[Path]): Directory to save the output files
                                    (if None, uses the same directory as the audio file)
        model (str): Whisper model to use (tiny, base, small, medium, large)
        language (str): Source language code (default: de for German)
        task (str): Task to perform (transcribe or translate)
        output_format (str): Output format (srt, vtt, txt, etc.)

    Returns:
        Path: Path to the generated subtitle file

    Raises:
        FileNotFoundError: If the audio file does not exist
        RuntimeError: If transcription fails
    """
    # Validate input file
    audio_path = validate_file_exists(audio_file)

    # Determine output directory if not provided
    if output_dir is None:
        output_dir = audio_path.parent

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Transcribing audio {audio_path} using Whisper model {model}")

    # Build Whisper command
    cmd = [
        "whisper",
        str(audio_path),
        "--model",
        model,
        "--language",
        language,
        "--task",
        task,
        "--output_dir",
        str(output_dir),
        "--output_format",
        output_format,
    ]

    # Run Whisper command
    returncode, stdout, stderr = run_command(cmd, timeout=None)

    if returncode != 0:
        logger.error(f"Transcription failed: {stderr}")
        raise RuntimeError(f"Failed to transcribe audio: {stderr}")

    # Determine the output file path
    # Whisper typically names the output file with the same stem as the input
    output_file = output_dir / f"{audio_path.stem}.{output_format}"

    if not output_file.exists():
        logger.error(f"Expected output file {output_file} not found")
        raise FileNotFoundError(f"Expected output file {output_file} not found")

    logger.info(f"Transcription completed successfully: {output_file}")
    return output_file
