#!/usr/bin/env python3
"""
Main entry point for the video subtitling tool.

This module provides the command-line interface for the tool,
which adds English subtitles to videos with non-English audio in various languages.
"""

import argparse
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

from subtitler import __version__
from subtitler.audio import extract_audio
from subtitler.transcribe import transcribe_audio
from subtitler.video import embed_subtitles
from subtitler.utils import (
    check_dependencies,
    cleanup_temp_dir,
    create_temp_dir,
    validate_file_exists,
)

logger = logging.getLogger("subtitler")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Add English subtitles to videos with non-English audio",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "video_file",
        type=str,
        help="Path to the input video file",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to the output video file (default: input_file_subtitled.mp4)",
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model to use for transcription",
    )

    parser.add_argument(
        "-k",
        "--keep-temp",
        action="store_true",
        help="Keep temporary files after processing",
    )

    parser.add_argument(
        "-f",
        "--font-size",
        type=int,
        default=24,
        help="Font size for subtitles",
    )

    parser.add_argument(
        "-p",
        "--position",
        type=str,
        default="lower_center",
        choices=[
            "lower_center",
            "lower_left",
            "lower_right",
            "upper_center",
            "upper_left",
            "upper_right",
        ],
        help="Position of subtitles",
    )

    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="de",
        help="Source language code (e.g., de for German, fr for French, etc.)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser.parse_args()


def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def main():
    """Main entry point for the CLI."""
    args = parse_args()
    setup_logging(args.verbose)

    logger.info(f"Starting video subtitling tool v{__version__}")

    # Check dependencies
    if not check_dependencies():
        logger.error(
            "Missing required dependencies. Please install ffmpeg and whisper."
        )
        sys.exit(1)

    try:
        # Validate input file
        video_path = validate_file_exists(args.video_file)

        # Create temporary directory
        temp_dir = create_temp_dir()
        logger.info(f"Using temporary directory: {temp_dir}")

        # Determine output file
        output_file = args.output
        if output_file is None:
            output_file = video_path.with_stem(f"{video_path.stem}_subtitled")
        output_file = Path(output_file)

        # Extract audio
        logger.info("Extracting audio from video...")
        audio_file = extract_audio(
            video_file=video_path,
            output_file=temp_dir / f"{video_path.stem}.wav",
        )

        # Transcribe and translate audio
        logger.info(
            f"Transcribing and translating audio using Whisper model '{args.model}' for language '{args.language}'..."
        )
        subtitle_file = transcribe_audio(
            audio_file=audio_file,
            output_dir=temp_dir,
            model=args.model,
            language=args.language,
            task="translate",
            output_format="srt",
        )

        # Embed subtitles
        logger.info("Embedding subtitles into video...")
        output_video = embed_subtitles(
            video_file=video_path,
            subtitle_file=subtitle_file,
            output_file=output_file,
            font_size=args.font_size,
            position=args.position,
        )

        logger.info(f"Successfully created subtitled video: {output_video}")

        # Clean up temporary files
        if not args.keep_temp:
            logger.info("Cleaning up temporary files...")
            cleanup_temp_dir(temp_dir)
        else:
            logger.info(f"Temporary files kept at: {temp_dir}")

        return 0

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
