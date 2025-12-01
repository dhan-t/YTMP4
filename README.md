# Cutie Converter — Lightweight YouTube/TikTok Downloader & Converter

A small, lightweight utility to download videos from YouTube or TikTok
and convert them to high-quality MP3 or MP4 files while preserving
original quality whenever possible.

Features
- Download from YouTube and TikTok using `yt-dlp`.
- Save highest-quality video/audio streams and prefer stream-copy (no re-encode) for MP4.
- Extract audio and convert to high-quality MP3 using `ffmpeg`.
- Simple CLI-first design; optional GUI can be layered later.

Prerequisites
- Python 3.8+ installed.
- `ffmpeg` available on your PATH (download from https://ffmpeg.org/).
- Recommended to install Python dependencies listed in `requirements.txt`.

Quick install
1. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

2. Install `ffmpeg` and ensure it's on your `PATH`.

Basic usage examples
- Download and merge best video+audio into MP4 (preserves quality):
```powershell
yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 <URL>
```

- Extract audio and convert to high-quality MP3 using `yt-dlp` + `ffmpeg`:
```powershell
yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 <URL>
```

Notes & Legal
- This tool is intended for downloading content you own, have permission to use, or
  that is freely licensed. Respect copyright and platform terms of service.
- I will not help bypass watermarks, DRM, or other protective measures. If you need
  non-watermarked source files, obtain them directly from the content owner or official APIs.

Next steps
- Implement a small `app.py` wrapper to provide a friendly CLI and call `yt-dlp`/`ffmpeg`.
- Add progress reporting, output templates, and optional GUI.

# YTMP4
