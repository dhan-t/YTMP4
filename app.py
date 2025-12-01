#!/usr/bin/env python3
"""
Minimal interactive CLI wrapper for downloading from YouTube/TikTok
Uses `questionary` for arrow-key menus and `yt-dlp` as the downloader.

Notes:
- Requires `ffmpeg` on PATH for post-processing (merging/conversion).
"""
import sys
import os
import yt_dlp
import questionary


def progress_hook(d):
    status = d.get('status')
    if status == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        speed = d.get('speed')
        eta = d.get('eta')
        if total:
            pct = downloaded / total * 100
            print(f"\rDownloading: {pct:5.1f}% ({downloaded}/{total})", end="")
        else:
            print(f"\rDownloading: {downloaded} bytes", end="")
    elif status == 'finished':
        print("\nDownload finished, now processing...")
    elif status == 'error':
        print("\nError during download:", d)


def download_url(url: str, output_format: str):
    # output_format: 'mp4' or 'mp3'
    if output_format == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
        }
    else:  # mp3
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0',
            }],
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Starting download for: {url}")
            ydl.download([url])
            print("Done.")
    except Exception as e:
        print("Failed:", e)


def main():
    print("YTMP4 — Minimal downloader (interactive CLI)")

    while True:
        action = questionary.select(
            "Choose an action",
            choices=[
                'Download a URL',
                'Quit',
            ],
        ).ask()

        if action == 'Quit' or action is None:
            print("Goodbye")
            sys.exit(0)

        # Download flow
        url = questionary.text("Enter video URL:").ask()
        if not url:
            print("No URL provided — returning to menu.")
            continue

        fmt = questionary.select(
            "Select output format",
            choices=[
                'MP4 (video)',
                'MP3 (audio)',
            ],
        ).ask()

        output_format = 'mp4' if fmt.startswith('MP4') else 'mp3'

        confirm = questionary.confirm(f"Download {output_format.upper()} for this URL?").ask()
        if not confirm:
            print("Cancelled — returning to menu.")
            continue

        # Run the download
        download_url(url, output_format)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(1)
# Main file
