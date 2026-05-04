"""Transcribe a video with OpenAI Whisper via docker.

Calls the local whisper-docker to transcribe the video with word-level timestamps.
Writes the full response to <edit_dir>/transcripts/<video_stem>.json.

Cached: if the output file already exists, the transcription is skipped.

Usage:
    python helpers/transcribe.py <video_path>
    python helpers/transcribe.py <video_path> --edit-dir /custom/edit
    python helpers/transcribe.py <video_path> --language Portuguese
    python helpers/transcribe.py <video_path> --backend local
"""

from __future__ import annotations

import argparse
import sys
import subprocess
import time
from pathlib import Path


def call_whisper_docker(
    video_path: Path,
    out_dir: Path,
    language: str | None = None,
    verbose: bool = True,
) -> Path:
    # Resolve whisper-docker directory relative to the current project
    search_dirs = [
        Path(__file__).resolve().parent.parent.parent.parent.parent / "whisper-docker",
        Path("/mnt/wsl/PHYSICALDRIVE1/video-use/whisper-docker"),
    ]
    
    whisper_dir = None
    for d in search_dirs:
        if d.exists() and (d / "docker-compose.yml").exists():
            whisper_dir = d
            break
            
    if not whisper_dir:
        raise RuntimeError("whisper-docker directory not found.")
        
    cmd = [
        "docker", "compose", "run", "--rm",
        "-v", f"{video_path.parent.resolve()}:/vid_data",
        "-v", f"{out_dir.resolve()}:/out_data",
        "whisper",
        f"/vid_data/{video_path.name}",
        "--model", "turbo",
        "--output_format", "json",
        "--word_timestamps", "True",
        "--output_dir", "/out_data"
    ]
    
    if language:
        cmd.extend(["--language", language])

    if verbose:
        print(f"  Running Whisper via Docker: {' '.join(cmd)}", flush=True)

    subprocess.run(cmd, cwd=whisper_dir, check=True)
    return out_dir / f"{video_path.stem}.json"


def call_whisper_local(
    video_path: Path,
    out_dir: Path,
    language: str | None = None,
    verbose: bool = True,
) -> Path:
    cmd = [
        "whisper",
        str(video_path.resolve()),
        "--model", "turbo",
        "--output_format", "json",
        "--word_timestamps", "True",
        "--output_dir", str(out_dir.resolve())
    ]
    
    if language:
        cmd.extend(["--language", language])

    if verbose:
        print(f"  Running Whisper Locally: {' '.join(cmd)}", flush=True)

    subprocess.run(cmd, check=True)
    return out_dir / f"{video_path.stem}.json"


def transcribe_one(
    video: Path,
    edit_dir: Path,
    language: str | None = None,
    backend: str = "docker",
    verbose: bool = True,
    **kwargs
) -> Path:
    """Transcribe a single video. Returns path to transcript JSON.

    Cached: returns existing path immediately if the transcript already exists.
    """
    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    out_path = transcripts_dir / f"{video.stem}.json"

    if out_path.exists():
        if verbose:
            print(f"cached: {out_path.name}")
        return out_path

    if verbose:
        print(f"  transcribing {video.name} with Whisper ({backend})", flush=True)

    t0 = time.time()
    if backend == "local":
        call_whisper_local(video, transcripts_dir, language, verbose)
    else:
        call_whisper_docker(video, transcripts_dir, language, verbose)
    dt = time.time() - t0

    if verbose:
        kb = out_path.stat().st_size / 1024
        print(f"  saved: {out_path.name} ({kb:.1f} KB) in {dt:.1f}s")

    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Transcribe a video using local Whisper-Docker")
    ap.add_argument("video", type=Path, help="Path to video file")
    ap.add_argument(
        "--edit-dir",
        type=Path,
        default=None,
        help="Edit output directory (default: <video_parent>/edit)",
    )
    ap.add_argument(
        "--language",
        type=str,
        default=None,
        help="Optional ISO language code (e.g., 'Portuguese'). Omit to auto-detect.",
    )
    ap.add_argument(
        "--backend",
        type=str,
        choices=["docker", "local"],
        default="docker",
        help="Backend to use: 'docker' (default) or 'local' (requires openai-whisper installed in current environment).",
    )
    # Keeping num-speakers just to not break existing scripts silently, though ignored
    ap.add_argument(
        "--num-speakers",
        type=int,
        default=None,
        help="Ignored for Whisper (kept for CLI compatibility).",
    )
    args = ap.parse_args()

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"video not found: {video}")

    edit_dir = (args.edit_dir or (video.parent / "edit")).resolve()

    transcribe_one(
        video=video,
        edit_dir=edit_dir,
        language=args.language,
        backend=args.backend,
    )


if __name__ == "__main__":
    main()
