# FFmpeg Video Merger

FFmpeg Video Merger is a Python application that allows you to merge multiple video files into a single output file using FFmpeg in GUI.

## Features

- Select multiple video files to merge.
- Specify the input and output file locations.
- Progress bar to show the merging process.

## Requirements
- Python 3.7+
- FFmpeg and FFprobe installed and accessible in the system's PATH.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/mykolamyronenko/FFmpegVideoMerger.git
    cd FFmpegVideoMerger
    ```

2. Create a virtual environment and activate it:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

4. Ensure FFmpeg and FFprobe are installed and accessible in your system's PATH.

## Usage

1. Run the application:
    ```
    python main.py
    ```

2. Use the GUI to select video files, specify the output location, and start the merging process.



