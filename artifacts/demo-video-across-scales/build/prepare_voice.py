#!/usr/bin/env python3
"""Prepare a recorded TTS take offline; also provides shared voice-build utilities."""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import wave


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    with path.open("x", encoding="utf-8") as file:
        file.write(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def relative(path: Path, directory: Path) -> str:
    return Path(os.path.relpath(path.resolve(), directory.resolve())).as_posix()


def output_dir(path: Path) -> Path:
    path = path.resolve()
    if path.exists() and any(path.iterdir()):
        raise ValueError("Output directory must be new or empty; recorded assets are never overwritten")
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_media(command: list[str], memory_mib: int = 256) -> subprocess.CompletedProcess:
    """Bound one direct media process; never run a shell or another Python runner."""
    if command[0] not in {"ffmpeg", "ffprobe"}:
        raise ValueError("Only ffmpeg and ffprobe are permitted")
    executable = shutil.which(command[0])
    if executable is None:
        raise RuntimeError(f"Required command unavailable: {command[0]}")
    argv = [executable, *command[1:]]
    options = {}
    if sys.platform == "darwin":
        limiter = shutil.which("taskpolicy")
        if limiter is None:
            raise RuntimeError("macOS taskpolicy is required for the process memory cap")
        argv = [limiter, "-m", str(memory_mib), *argv]
    elif sys.platform.startswith("linux"):
        import resource

        def limit_address_space():
            # ELF/shared-library mappings also count toward RLIMIT_AS.
            cap = max(1024, memory_mib) * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
        options["preexec_fn"] = limit_address_space
    else:
        raise RuntimeError("This adapter supports macOS and Linux")
    result = subprocess.run(argv, check=True, capture_output=True, text=True, timeout=90, **options)
    if result.stderr.strip():
        raise RuntimeError(f"{command[0]} reported an error: {result.stderr[:500]}")
    return result


def ffmpeg(*args: str) -> None:
    run_media(["ffmpeg", "-nostdin", "-v", "error", "-threads", "2",
               "-filter_threads", "1", "-filter_complex_threads", "1", *args])


def probe(path: Path) -> dict:
    return json.loads(run_media(["ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_name,sample_rate,channels", "-of", "json", str(path)], 128).stdout)


def pcm(path: Path) -> tuple:
    with wave.open(str(path), "rb") as file:
        params = file.getparams()
        if (params.nchannels, params.sampwidth, params.framerate) != (1, 2, 32000):
            raise ValueError("Expected mono 32 kHz 16-bit PCM WAV")
        return params, file.readframes(file.getnframes())


def load_take(path: Path) -> tuple[dict, Path, Path]:
    take = read_json(path)
    audio = (path.parent / take["audio_file"]).resolve()
    subtitles = (path.parent / take["subtitle_file"]).resolve()
    if sha(audio) != take["audio_sha256"] or sha(subtitles) != take["subtitle_sha256"]:
        raise ValueError("Take files do not match their recorded hashes")
    if digest(take["text"].encode()) != take["text_sha256"]:
        raise ValueError("Take text does not match its recorded hash")
    return take, audio, subtitles


def replace_pronunciations(text: str, aliases: list[str]) -> str:
    for alias in aliases:
        source, separator, target = alias.partition("=")
        if not separator or len(source) != len(target) or not source.isalpha() or not target.isalpha():
            raise ValueError("Pronunciation aliases must be equal-length alphabetic pairs, e.g. yoo=you")
        text = re.sub(r"\b" + re.escape(source) + r"\b", target, text, flags=re.IGNORECASE)
    return text


def timings(text: str, subtitle_path: Path, tempo: float = 1.0,
            offset: float = 0.0, aliases: list[str] | None = None) -> dict:
    """Align real provider fragments; provider character offsets are inconsistent."""
    aliases = aliases or []
    provider = json.loads(subtitle_path.read_text())
    fragments = [word for segment in provider for word in segment["timestamped_words"]]
    positions = [i for i, char in enumerate(text) if char.isalnum()]
    normalize = lambda value: "".join(char.lower() for char in value if char.isalnum())
    spoken = "".join(word["word"] for word in fragments)
    if normalize(text) != normalize(replace_pronunciations(spoken, aliases)):
        raise ValueError("Subtitle fragments do not match the canonical spoken text")
    character_times = []
    for word in fragments:
        character_times.extend([(word["time_begin"] / 1000, word["time_end"] / 1000)]
                               * sum(char.isalnum() for char in word["word"]))
    if len(character_times) != len(positions):
        raise ValueError("Pronunciation substitution changed alignment length")

    def entry(match, number):
        left = bisect.bisect_left(positions, match.start())
        right = bisect.bisect_left(positions, match.end())
        values = character_times[left:right]
        begin, end = min(value[0] for value in values), max(value[1] for value in values)
        return dict(id=number, text=match.group().strip(), source_char_begin=match.start(),
                    source_char_end=match.end(), raw_start_s=round(begin, 6), raw_end_s=round(end, 6),
                    start_s=round(offset + begin / tempo, 6), end_s=round(offset + end / tempo, 6))

    result = {}
    patterns = {"words": r"\S+", "sentences": r'[^.!?]+[.!?][”"’\x27]*', "paragraphs": r"[^\n]+"}
    for kind, pattern in patterns.items():
        result[kind] = [entry(match, i + 1) for i, match in enumerate(re.finditer(pattern, text))]
    result.update(method="Provider fragment timestamps aligned to canonical text; timestamps are approximate.",
                  raw_character_offsets_reused=False, alphanumeric_text_matches_exactly=True,
                  tempo_factor=tempo, offset_s=offset, pronunciation_aliases=aliases)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--take", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, help="Optional canonical dialogue; whitespace may differ")
    parser.add_argument("--target", type=float, required=True, help="Target duration in seconds")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--max-tempo-change", type=float, default=0.08)
    parser.add_argument("--dry-run", action="store_true", help="Inspect inputs and plan; no media processing")
    args = parser.parse_args()
    take, source, subtitles = load_take(args.take.resolve())
    text = args.canonical.read_text() if args.canonical else take["text"]
    duration = float(take["duration_s"])
    if not math.isfinite(args.target) or args.target <= 0:
        raise ValueError("Target duration must be finite and positive")
    tempo = duration / args.target
    if not math.isfinite(tempo) or abs(tempo - 1) > args.max_tempo_change:
        raise ValueError("Tempo change exceeds limit; revise the script or record a new take")
    timing = timings(text, subtitles, tempo)
    if args.dry_run:
        print(json.dumps(dict(duration_s=duration, tempo_factor=tempo, output=str(args.out_dir))))
        return
    out = output_dir(args.out_dir)
    wav = out / "narration.wav"
    ffmpeg("-i", str(source), "-af", f"atempo={tempo:.12f}", "-c:a", "pcm_s16le", str(wav))
    meta = probe(wav)
    _, samples = pcm(wav)
    timing.update(raw_subtitles=relative(subtitles, out), raw_subtitles_sha256=sha(subtitles))
    write_json(out / "timings.json", timing)
    manifest = dict(text=text, text_sha256=digest(text.encode()),
        wav_file=wav.name, wav_sha256=sha(wav), wav_duration_s=float(meta["format"]["duration"]),
        pcm_sha256=digest(samples), timings_file="timings.json", timings_sha256=sha(out / "timings.json"),
        source_take=relative(args.take, out), source_take_sha256=sha(args.take),
        post_tempo_factor=tempo, model=take["model"], voice_id=take["voice_id"],
        provider_speed=take["speed"], postprocessing="One pitch-preserving atempo operation; no added gaps.")
    write_json(out / "manifest.json", manifest)
    print(json.dumps(dict(wav_duration_s=manifest["wav_duration_s"], wav_sha256=manifest["wav_sha256"])))


if __name__ == "__main__":
    main()
