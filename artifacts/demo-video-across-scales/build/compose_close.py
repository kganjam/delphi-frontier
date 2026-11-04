#!/usr/bin/env python3
"""Compose an unchanged PCM prefix with a recorded closing, entirely offline."""
import argparse
import copy
import importlib.util
from pathlib import Path
import wave

spec = importlib.util.spec_from_file_location("voice", Path(__file__).with_name("prepare_voice.py"))
voice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-manifest", type=Path, required=True)
    parser.add_argument("--closing-take", type=Path, required=True)
    parser.add_argument("--splice", type=float, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--pronunciation", action="append", default=[], help="e.g. yoo=you")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    base_file = args.base_manifest.resolve()
    base = voice.read_json(base_file)
    base_wav = base_file.parent / base["wav_file"]
    base_timing = base_file.parent / base["timings_file"]
    if voice.sha(base_wav) != base["wav_sha256"] or voice.sha(base_timing) != base["timings_sha256"]:
        raise ValueError("Base files do not match manifest")
    take, closing_audio, subtitles = voice.load_take(args.closing_take.resolve())
    text = base["text"]
    ending = voice.replace_pronunciations(take["text"].strip(), args.pronunciation)
    if not text.rstrip().casefold().endswith(ending.casefold()):
        raise ValueError("Closing must match the canonical script suffix")
    suffix_start = len(text.rstrip()) - len(ending)
    canonical_ending = text[suffix_start:suffix_start + len(ending)]
    close_timing = voice.timings(canonical_ending, subtitles, offset=args.splice, aliases=args.pronunciation)
    params, original = voice.pcm(base_wav)
    frame = round(args.splice * params.framerate)
    if not 0 < frame < params.nframes:
        raise ValueError("Splice must lie inside the base audio")
    if args.dry_run:
        print(voice.json.dumps(dict(splice_frame=frame, canonical_ending=canonical_ending,
                                    closing_take=args.closing_take.name)))
        return
    out = voice.output_dir(args.out_dir)
    close_wav = out / "closing.wav"
    voice.ffmpeg("-i", str(closing_audio), "-ar", "32000", "-ac", "1", "-c:a", "pcm_s16le", str(close_wav))
    _, ending_pcm = voice.pcm(close_wav)
    prefix = original[:frame * 2]
    combined = prefix + ending_pcm
    # Retain an existing track's final hold when the new closing is shorter.
    combined += bytes(max(0, len(original) - len(combined)))
    wav = out / "narration.wav"
    with wave.open(str(wav), "wb") as file:
        file.setparams(params)
        file.writeframes(combined)
    _, written = voice.pcm(wav)
    if written[:len(prefix)] != prefix or written[len(prefix):len(prefix) + len(ending_pcm)] != ending_pcm:
        raise RuntimeError("PCM preservation failed")
    timing = copy.deepcopy(voice.read_json(base_timing))
    if "raw_subtitles" in timing:
        raw_subtitles = (base_timing.parent / timing["raw_subtitles"]).resolve()
        timing.update(raw_subtitles=voice.relative(raw_subtitles, out),
                      raw_subtitles_sha256=voice.sha(raw_subtitles))
    for group in ("words", "sentences", "paragraphs"):
        preserved = [entry for entry in timing[group] if entry["source_char_end"] <= suffix_start]
        additions = copy.deepcopy(close_timing[group])
        for index, entry in enumerate(additions, len(preserved) + 1):
            entry.update(id=index, source_char_begin=entry["source_char_begin"] + suffix_start,
                         source_char_end=entry["source_char_end"] + suffix_start, timing_origin="closing")
        timing[group] = preserved + additions
    timing.pop("tempo_factor", None)
    timing.update(parent_timings=voice.relative(base_timing, out), parent_timings_sha256=voice.sha(base_timing),
        closing_subtitles=voice.relative(subtitles, out), closing_subtitles_sha256=voice.sha(subtitles),
        splice_time_s=args.splice, closing_post_tempo_factor=1.0, pronunciation_aliases=args.pronunciation)
    voice.write_json(out / "timings.json", timing)
    manifest = dict(text=text, text_sha256=voice.digest(text.encode()), wav_file="narration.wav",
        wav_sha256=voice.sha(wav), wav_duration_s=len(written) / 2 / params.framerate,
        pcm_sha256=voice.digest(written), timings_file="timings.json", timings_sha256=voice.sha(out / "timings.json"),
        base_manifest=voice.relative(base_file, out), base_manifest_sha256=voice.sha(base_file),
        closing_take=voice.relative(args.closing_take, out), closing_take_sha256=voice.sha(args.closing_take),
        splice_time_s=args.splice, splice_frame=frame, unchanged_pcm_prefix_sha256=voice.digest(prefix),
        closing_pcm_sha256=voice.digest(ending_pcm), pcm_prefix_byte_identical=True,
        closing_pcm_byte_identical=True, closing_post_tempo_factor=1.0,
        model=take["model"], voice_id=take["voice_id"], closing_provider_speed=take["speed"])
    voice.write_json(out / "manifest.json", manifest)
    print(voice.json.dumps(dict(wav_duration_s=manifest["wav_duration_s"], wav_sha256=manifest["wav_sha256"])))


if __name__ == "__main__":
    main()
