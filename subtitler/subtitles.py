"""
Subtitle processing module for the video subtitling tool.

This module provides functionality to process and format subtitle files.
"""

import logging
import re
from pathlib import Path
from typing import List, Optional, Tuple

from subtitler.utils import validate_file_exists

logger = logging.getLogger("subtitler.subtitles")


class SubtitleEntry:
    """Class representing a single subtitle entry."""

    def __init__(self, index: int, start_time: str, end_time: str, text: str):
        """
        Initialize a subtitle entry.

        Args:
            index (int): Subtitle index number
            start_time (str): Start timestamp (HH:MM:SS,mmm)
            end_time (str): End timestamp (HH:MM:SS,mmm)
            text (str): Subtitle text
        """
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def __str__(self) -> str:
        """Return the subtitle entry as a string in SRT format."""
        return f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.text}\n"


def parse_srt(srt_file: Path) -> List[SubtitleEntry]:
    """
    Parse an SRT file into a list of SubtitleEntry objects.

    Args:
        srt_file (Path): Path to the SRT file

    Returns:
        List[SubtitleEntry]: List of subtitle entries

    Raises:
        FileNotFoundError: If the SRT file does not exist
        ValueError: If the SRT file is invalid
    """
    # Validate input file
    srt_path = validate_file_exists(srt_file)

    logger.info(f"Parsing SRT file: {srt_path}")

    entries = []
    current_index = None
    current_time = None
    current_text = []

    with open(srt_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Parse index
        if current_index is None:
            try:
                current_index = int(line)
                i += 1
                continue
            except ValueError:
                logger.error(f"Invalid subtitle index: {line}")
                raise ValueError(f"Invalid subtitle index: {line}")

        # Parse timestamp
        if current_time is None:
            time_match = re.match(
                r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line
            )
            if time_match:
                current_time = (time_match.group(1), time_match.group(2))
                i += 1
                continue
            else:
                logger.error(f"Invalid timestamp format: {line}")
                raise ValueError(f"Invalid timestamp format: {line}")

        # Parse text
        if line and current_index is not None and current_time is not None:
            current_text.append(line)
            i += 1
            continue

        # End of entry
        if not line and current_index is not None and current_time is not None:
            text = "\n".join(current_text)
            entries.append(
                SubtitleEntry(current_index, current_time[0], current_time[1], text)
            )
            current_index = None
            current_time = None
            current_text = []
            i += 1
            continue

        # Unexpected line
        logger.warning(f"Unexpected line in SRT file: {line}")
        i += 1

    # Add the last entry if there is one
    if current_index is not None and current_time is not None and current_text:
        text = "\n".join(current_text)
        entries.append(
            SubtitleEntry(current_index, current_time[0], current_time[1], text)
        )

    logger.info(f"Parsed {len(entries)} subtitle entries")
    return entries


def write_srt(entries: List[SubtitleEntry], output_file: Path) -> Path:
    """
    Write subtitle entries to an SRT file.

    Args:
        entries (List[SubtitleEntry]): List of subtitle entries
        output_file (Path): Path to the output SRT file

    Returns:
        Path: Path to the written SRT file
    """
    logger.info(f"Writing {len(entries)} subtitle entries to {output_file}")

    with open(output_file, "w", encoding="utf-8") as f:
        for i, entry in enumerate(entries):
            # Update index to ensure sequential numbering
            entry.index = i + 1
            f.write(str(entry))
            if i < len(entries) - 1:
                f.write("\n")

    logger.info(f"Successfully wrote subtitle file: {output_file}")
    return output_file


def adjust_subtitle_timing(
    entries: List[SubtitleEntry], offset_ms: int = 0, scale_factor: float = 1.0
) -> List[SubtitleEntry]:
    """
    Adjust the timing of subtitle entries.

    Args:
        entries (List[SubtitleEntry]): List of subtitle entries
        offset_ms (int): Time offset in milliseconds (positive or negative)
        scale_factor (float): Time scale factor (e.g., 1.1 to slow down by 10%)

    Returns:
        List[SubtitleEntry]: List of adjusted subtitle entries
    """
    logger.info(
        f"Adjusting subtitle timing: offset={offset_ms}ms, scale={scale_factor}"
    )

    adjusted_entries = []

    for entry in entries:
        # Parse timestamps
        start_h, start_m, start_s = map(int, entry.start_time.split(",")[0].split(":"))
        start_ms = int(entry.start_time.split(",")[1])

        end_h, end_m, end_s = map(int, entry.end_time.split(",")[0].split(":"))
        end_ms = int(entry.end_time.split(",")[1])

        # Convert to milliseconds
        start_total_ms = ((start_h * 3600 + start_m * 60 + start_s) * 1000) + start_ms
        end_total_ms = ((end_h * 3600 + end_m * 60 + end_s) * 1000) + end_ms

        # Apply adjustments
        start_total_ms = int((start_total_ms * scale_factor) + offset_ms)
        end_total_ms = int((end_total_ms * scale_factor) + offset_ms)

        # Ensure times are not negative
        start_total_ms = max(0, start_total_ms)
        end_total_ms = max(0, end_total_ms)

        # Convert back to timestamp format
        start_h = start_total_ms // 3600000
        start_m = (start_total_ms % 3600000) // 60000
        start_s = (start_total_ms % 60000) // 1000
        start_ms = start_total_ms % 1000

        end_h = end_total_ms // 3600000
        end_m = (end_total_ms % 3600000) // 60000
        end_s = (end_total_ms % 60000) // 1000
        end_ms = end_total_ms % 1000

        # Format timestamps
        start_time = f"{start_h:02d}:{start_m:02d}:{start_s:02d},{start_ms:03d}"
        end_time = f"{end_h:02d}:{end_m:02d}:{end_s:02d},{end_ms:03d}"

        # Create adjusted entry
        adjusted_entry = SubtitleEntry(entry.index, start_time, end_time, entry.text)
        adjusted_entries.append(adjusted_entry)

    logger.info(f"Adjusted timing for {len(adjusted_entries)} subtitle entries")
    return adjusted_entries
