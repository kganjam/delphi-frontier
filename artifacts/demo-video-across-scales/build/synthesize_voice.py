#!/usr/bin/env python3
"""Opt-in MiniMax narration using the caller's MINIMAX_API_KEY environment variable."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import signal
import urllib.parse
import urllib.request

spec = importlib.util.spec_from_file_location("voice", Path(__file__).with_name("prepare_voice.py"))
voice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)

ENDPOINT = "https://api.minimax.io/v1/t2a_v2"
MAX_AUDIO_BYTES = 8_000_000


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--speed", type=float, default=1.2)
    parser.add_argument("--model", default="speech-2.8-hd")
    parser.add_argument("--voice", default="English_expressive_narrator")
    parser.add_argument("--dry-run", action="store_true", help="No credential lookup or network request")
    args = parser.parse_args()
    text = args.text.read_text(encoding="utf-8")
    if not 0 < len(text) < 10000 or not 0.5 <= args.speed <= 2:
        raise ValueError("Text must be under 10000 characters; speed must be 0.5–2")
    recipe = dict(provider="MiniMax", endpoint=ENDPOINT, model=args.model, voice_id=args.voice,
                  speed=args.speed, text=text, text_sha256=voice.digest(text.encode()))
    if args.dry_run:
        print(json.dumps({**recipe, "network_requests": 0}, ensure_ascii=False))
        return
    key = os.environ.get("MINIMAX_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Set MINIMAX_API_KEY in your environment; no credential files are read")
    out = voice.output_dir(args.out_dir)
    body = json.dumps(dict(model=args.model, text=text, stream=False, output_format="hex",
        subtitle_enable=True, subtitle_type="word",
        voice_setting=dict(voice_id=args.voice, speed=args.speed, vol=1.0, pitch=0),
        audio_setting=dict(sample_rate=32000, bitrate=128000, format="mp3", channel=1))).encode()
    request = urllib.request.Request(ENDPOINT, data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})

    def deadline(signum, frame):
        raise TimeoutError("Speech request deadline exceeded")

    previous = signal.signal(signal.SIGALRM, deadline)
    signal.setitimer(signal.ITIMER_REAL, 120)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload_bytes = response.read(MAX_AUDIO_BYTES * 2 + 65537)
        if len(payload_bytes) > MAX_AUDIO_BYTES * 2 + 65536:
            raise RuntimeError("Speech response exceeded size bound")
        payload = json.loads(payload_bytes)
    except Exception as error:
        raise RuntimeError("Speech request failed (" + type(error).__name__ + ")") from None
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
    if (payload.get("base_resp") or {}).get("status_code") != 0:
        raise RuntimeError("Speech service returned a failed status")
    data = payload.get("data") or {}
    audio = bytes.fromhex(data.get("audio") or "")
    if not 2000 < len(audio) <= MAX_AUDIO_BYTES:
        raise RuntimeError("Empty or oversized audio response")
    audio_path = out / "audio.mp3"
    with audio_path.open("xb") as file:
        file.write(audio)
    receipt = {**recipe, "audio_file": audio_path.name, "audio_sha256": voice.sha(audio_path),
               "audio_bytes": len(audio), "duration_s": float(voice.probe(audio_path)["format"]["duration"])}
    voice.write_json(out / "receipt.json", receipt)
    subtitle_url = data.get("subtitle_file") or payload.get("subtitle_file")
    if not isinstance(subtitle_url, str) or urllib.parse.urlparse(subtitle_url).scheme != "https":
        raise RuntimeError("Audio saved, but no HTTPS subtitle file returned; do not repeat synthesis blindly")
    try:
        with urllib.request.urlopen(subtitle_url, timeout=30) as response:
            subtitles = response.read(2_000_001)
        if len(subtitles) > 2_000_000:
            raise ValueError("Subtitle response exceeded limit")
        json.loads(subtitles)
    except Exception as error:
        raise RuntimeError("Audio saved; subtitle download failed (" + type(error).__name__ + ")") from None
    with (out / "subtitles.json").open("xb") as file:
        file.write(subtitles)
    take = {**receipt, "subtitle_file": "subtitles.json", "subtitle_sha256": voice.sha(out / "subtitles.json"),
            "receipt_file": "receipt.json", "receipt_sha256": voice.sha(out / "receipt.json")}
    voice.write_json(out / "take.json", take)
    print(json.dumps(dict(duration_s=take["duration_s"], audio_sha256=take["audio_sha256"])))


if __name__ == "__main__":
    main()
