# Subtitler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A command-line tool that adds English subtitles to videos with non-English audio in various languages.

## Features

- Extract audio from video files
- Transcribe audio from various languages to English text using Whisper
- Support for multiple source languages (German, French, Spanish, etc.)
- Generate properly formatted subtitles
- Embed subtitles into the video with customizable position and styling
- Output a new video file with embedded subtitles

## Requirements

- Python 3.6 or higher
- FFmpeg (must be installed and accessible in your PATH)
- Whisper (must be installed and accessible in your PATH)

## Installation

### From Source

1. Clone this repository:
   ```
   git clone https://github.com/silvanm/subtitler.git
   cd subtitler
   ```

2. Install the package:
   ```
   pip install -e .
   ```

### Prerequisites

Before installing, make sure you have the following dependencies installed:

1. **FFmpeg**: 
   - [Download FFmpeg](https://ffmpeg.org/download.html)
   - Make sure it's in your PATH

2. **Whisper**:
   - Install OpenAI's Whisper: `pip install -U openai-whisper`
   - Or follow the [official installation instructions](https://github.com/openai/whisper#setup)

## Usage

### Basic Usage

```bash
subtitler video.mp4
```

This will:
1. Extract audio from `video.mp4`
2. Transcribe and translate the audio to English using Whisper (default language: German)
3. Embed the English subtitles into the video
4. Create a new file named `video_subtitled.mp4`

To specify a different source language:
```bash
subtitler video.mp4 -l fr  # For French audio
```

### Command-line Options

```
usage: subtitler [-h] [-o OUTPUT] [-m {tiny,base,small,medium,large}] [-k] [-f FONT_SIZE]
                 [-p {lower_center,lower_left,lower_right,upper_center,upper_left,upper_right}] [-l LANGUAGE]
                 [-v] [--version]
                 video_file

Add English subtitles to videos with non-English audio

positional arguments:
  video_file            Path to the input video file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to the output video file (default: input_file_subtitled.mp4)
  -m {tiny,base,small,medium,large}, --model {tiny,base,small,medium,large}
                        Whisper model to use for transcription (default: medium)
  -k, --keep-temp       Keep temporary files after processing (default: False)
  -f FONT_SIZE, --font-size FONT_SIZE
                        Font size for subtitles (default: 24)
  -p {lower_center,lower_left,lower_right,upper_center,upper_left,upper_right}, --position {lower_center,lower_left,lower_right,upper_center,upper_left,upper_right}
                        Position of subtitles (default: lower_center)
  -l LANGUAGE, --language LANGUAGE
                        Source language code (e.g., de for German, fr for French, etc.) (default: de)
  -v, --verbose         Enable verbose logging (default: False)
  --version             show program's version number and exit
```

### Examples

Specify an output file:
```bash
subtitler video.mp4 -o output.mp4
```

Use a different Whisper model:
```bash
subtitler video.mp4 -m large
```

Specify a different source language:
```bash
subtitler video.mp4 -l fr  # French
subtitler video.mp4 -l es  # Spanish
subtitler video.mp4 -l it  # Italian
```

Change subtitle position and font size:
```bash
subtitler video.mp4 -p lower_right -f 28
```

Enable verbose logging:
```bash
subtitler video.mp4 -v
```

Keep temporary files for debugging:
```bash
subtitler video.mp4 -k
```

## How It Works

1. **Audio Extraction**: Uses FFmpeg to extract audio from the video file
2. **Transcription & Translation**: Uses Whisper to transcribe audio from the specified language and translate it to English
3. **Subtitle Generation**: Creates an SRT subtitle file with proper timing
4. **Subtitle Embedding**: Uses FFmpeg to burn the subtitles into the video
5. **Output Generation**: Creates a new video file with embedded subtitles

## Examples

The `examples` directory is intended for sample videos you can use to test the tool. Due to their size, example videos are not included in the repository, but you can add your own video files for testing.

```bash
# Process an example video
subtitler examples/your_video.mp4
```

## Demo

Below is a demonstration of the subtitler tool in action:

<!-- You can embed a video in your README.md using one of these methods: -->

<!-- Method 1: Link to a video file in your repository (if small enough) -->
<!-- 
[Watch the demo video](./demo/demo.mp4)
-->

<!-- Method 2: Embed a GIF -->
<!-- 
![Demo GIF](./demo/demo.gif)
-->

<!-- Method 3: Embed a video using HTML (GitHub supports this) -->
<!-- 
<video src="./demo/demo.mp4" controls title="Subtitler Demo" width="640"></video>
-->

<!-- Method 4: Link to YouTube or other video platforms -->
<!-- 
[![Subtitler Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
-->

<!-- Uncomment one of the above methods and replace with your actual video content -->

## License

MIT License

Copyright (c) 2025 silvanm

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
