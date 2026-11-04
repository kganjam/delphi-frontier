# Editable video sources

One renderer builds both preserved edits. `edits/90s.json` is the final 35-shot
revision, including the longer overview and adversarial-design holds and the
approved closing voice. `edits/60s.json` is the earlier 26-shot visual revision;
it has its own dialogue and narration, not a shortened copy of the final 90s.

The profiles reference the package's canonical `.txt` dialogue, `audio/` inputs,
and one shared `sources/assets.json`. Every image, movie, preview poster, and
candidate-sequence file is explicitly pinned by bytes and SHA256. No source is
read from a developer's Documents directory, a previous render cache, or a site.
Recorded source bytes are retained. Concept art and animated explanations keep
their original scope labels; rendering does not run scientific models or TTS.

## Requirements

Tested on macOS with Python 3.13.12, Pillow 12.2.0, and FFmpeg/ffprobe 8.1.1.
Python 3.11 or later is required. Install the pinned Pillow dependency with
`python -m pip install -r build/requirements.txt` in a suitable environment.
FFmpeg must provide libx264, AAC, `setts`, and `-filter_buffered_frames`.

Font binaries are **not redistributed**. The original layout uses macOS
Helvetica Neue and Georgia, including Georgia Bold Italic for the closing word
“you”. `font-config.example.json` records the original system paths and TTC
indices. On macOS these are the default. On another installation, copy that
JSON to ignored `font-config.local.json`, point it at legally available fonts,
and pass `--font-config font-config.local.json` to both tools. The environment
variable `DELPHI_VIDEO_FONT_CONFIG` is an alternative. Substituting fonts can
change wrapping and appearance; the caption-width checks still apply. Font
file hashes are recorded by preflight.

Every FFmpeg child is capped directly at 768 MiB, with bounded threads and
queues; ffprobe is capped at 256 MiB. macOS uses `taskpolicy`. Linux uses
`systemd-run --user --scope` with a memory limit, zero swap, and TasksMax=32;
that path requires a working user manager and has not been executed here.
Run the Python process under a cap too. For Linux, a suitable outer scope is
`systemd-run --user --scope -p MemoryMax=2G -p MemorySwapMax=0 -p TasksMax=64`.
Check shared-machine headroom first. Run full renders sequentially.

## Rebuild

Run these commands from `artifacts/demo-video-across-scales/`. Replace `python`
with the interpreter containing Pillow. On macOS:

```sh
taskpolicy -m 512 python -B build/render_video.py preflight --profile edits/90s.json
taskpolicy -m 512 python -B build/render_video.py preview --profile edits/90s.json
taskpolicy -m 512 python -B build/render_video.py render --profile edits/90s.json
taskpolicy -m 512 python -B build/verify_video.py --profile edits/90s.json --all-shots
```

Use `edits/60s.json` for the shorter film. Output is restricted to the ignored
`.build/90s/` or `.build/60s/` directories. Approved movies at the package root
are never overwritten. Each build produces its MP4, SRT, cutlist, captions,
source receipt, preview frames, and QA output. The metadata-only
`preflight --assets-only` can check the shared assets before the audio is
available; its report explicitly says audio was not checked.

Resume is deliberately unavailable: a matching frame count does not prove a
cached shot matches changed artwork, text, timing, fonts, or code. Rebuild from
the archived inputs after editing. Encoded MP4 bytes may differ across library
versions and encoding histories; the approved output remains pinned separately.

## Modify an edit

- Edit the relevant profile for crops, scale labels, scene order, motion layout,
  and fixed cut points. Cut points are integer frames at 30 fps. Preserve the
  ending frame at 2700 or 1800 for the existing durations.
- Change shared sources deliberately and update their size/SHA256 pins in
  `sources/assets.json`. Never use a conceptual image as a measured result.
- For narration changes, edit the canonical dialogue and create matching audio,
  word timings, and manifest using the voice workflow documented in `VOICE.md`.
  The renderer refuses mismatched dialogue or audio/timing hashes. It does not
  silently synthesize speech or spend API credits.
- `motion_layouts.py` contains the editable animated explanations. Paths are
  conceptual unless a scene explicitly cites a recorded relationship. The
  original plots and saved simulation frames are not numerically interpolated.

`validation.json` records the asset and preview parity checks performed while
porting. Full render/decode validation with the merged audio archive is separate.
This package addition does not register or deploy a new website video family.
