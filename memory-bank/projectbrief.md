# Project Brief: Video Subtitling Tool

## Overview
A command-line tool that adds English subtitles to videos with German audio. The tool extracts audio from video files, uses Whisper to transcribe and translate the German audio to English, and then embeds the subtitles back into the video using FFmpeg.

## Core Requirements
1. Accept video files (MP4) as input
2. Extract audio from the video
3. Transcribe German audio to English text using Whisper
4. Generate properly formatted subtitles
5. Embed subtitles into the video (positioned in the lower third, centered)
6. Output a new video file with embedded subtitles
7. Implement as a Python CLI tool

## Goals
- Create a simple, user-friendly command-line interface
- Ensure high-quality transcription and translation
- Produce professional-looking subtitled videos
- Handle errors gracefully
- Maintain clean, well-documented code

## Constraints
- Whisper and FFmpeg must be pre-installed on the system
- Focus on German to English translation only for the initial version
