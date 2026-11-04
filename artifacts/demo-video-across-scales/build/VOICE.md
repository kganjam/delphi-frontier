# Narration sources and rebuilds

The recorded audio is included. Video rebuilding requires no API key and makes
no TTS request. Run the commands below from this package directory.

`audio/90s/narration.wav` is the final approved 90-second film narration.
`audio/60s/narration.wav` is the latest 60-second film narration. Each directory
contains canonical `dialogue.txt`, a renderer-facing `manifest.json` and
`timings.json`, the prepared `base.wav` and its metadata, and the original
continuous and closing MP3 takes, service subtitles, and sanitized receipts in
`sources/`. Audio bytes were copied unchanged. All five closing auditions and
their exact inputs are in `audio/auditions/`; the approved 90-second closing is
`03-yoo-caps`.

| Variant | Continuous voice | Preparation | Closing splice | Closing voice |
| --- | --- | --- | --- | --- |
| 90s | `speech-2.8-hd`, `English_expressive_narrator`, speed 1.20 | 89.748s source, tempo factor 1.0141016949152544 | 85.700s | Approved `YOO` take, native speed 1.15 |
| 60s | Same model and voice, speed 1.20 | 63s source, tempo factor 1.0677966101694916 | 55.500s | Paired `YOU` closing, native speed 1.20 |

Canonical captions say “you.” The 90-second TTS input says “YOO” as a
pronunciation cue. Neither closing receives a tempo adjustment. The composition
copies the original PCM prefix and decoded closing PCM exactly, retaining the
base track's final silence if the new closing is shorter.

## Offline reproduction

Requirements: Python 3.11+, `ffmpeg`, and `ffprobe` on PATH. The three scripts use
only the Python standard library. Media processes run sequentially, with two
threads and a 90-second timeout. On macOS they use `taskpolicy` memory caps;
the Linux adapter applies a 1GiB address-space limit, including library mappings.
No Whisper model, browser, node package, or Miniconda environment is required.

```sh
python3 build/prepare_voice.py --take audio/90s/sources/continuous.json --canonical audio/90s/dialogue.txt --target 88.5 --out-dir .build/voice90-base
python3 build/compose_close.py --base-manifest .build/voice90-base/manifest.json --closing-take audio/90s/sources/closing.json --splice 85.7 --pronunciation yoo=you --out-dir .build/voice90-final

python3 build/prepare_voice.py --take audio/60s/sources/continuous.json --canonical audio/60s/dialogue.txt --target 59 --out-dir .build/voice60-base
python3 build/compose_close.py --base-manifest .build/voice60-base/manifest.json --closing-take audio/60s/sources/closing.json --splice 55.5 --out-dir .build/voice60-final
```

To change only the closing, pass `audio/90s/base-manifest.json` or
`audio/60s/base-manifest.json` directly to `compose_close.py`. Outputs must go into
a new or empty directory; the tools refuse to overwrite recorded artifacts.
Every command supports `--help` and `--dry-run`. Dry runs inspect recorded inputs
and hashes, but perform no encoding or network requests.

## Edit dialogue and record a new voice

Edit a copy of `dialogue.txt`. Supply your own `MINIMAX_API_KEY` environment
variable, then explicitly invoke synthesis:

```sh
python3 build/synthesize_voice.py --text edited-dialogue.txt --speed 1.20 --out-dir .build/new-take --dry-run
python3 build/synthesize_voice.py --text edited-dialogue.txt --speed 1.20 --out-dir .build/new-take
python3 build/prepare_voice.py --take .build/new-take/take.json --canonical edited-dialogue.txt --target 88.5 --out-dir .build/new-base
```

Synthesis sends only the requested text and voice settings to MiniMax. It reads
the key from the environment, never a home-directory file, and never prints or
writes it. The request is bounded and is not automatically retried. If audio is
saved but subtitle retrieval fails, keep the audio and resolve that failure
before generating another paid take. Provider output is nondeterministic:
re-synthesis is not a way to reproduce the archived audio hash.

A changed recording needs a newly reviewed splice boundary. The archived
85.700s and 55.500s boundaries apply only to the included bases. The supported
`--pronunciation yoo=you` alias maps the phonetic input to canonical captions;
equal-length aliases keep the fragment-to-character alignment explicit.
Provider timestamps are approximate, not manually verified word alignments.

## Provenance and archive corrections

The original session used `narrate.py`, `prepare_delivery.py`, `splice_close.py`,
and `compose_yoo.py`. These portable adapters consolidate those implementations;
they are not presented as the exact scripts originally used to generate the
masters. The HTTP request settings, PCM splice, tempo preparation, and subtitle
alignment algorithms are retained. Original helper copies with machine-specific
paths, diagnostic audio, session transcripts, model caches, and credentials are
not needed to reproduce the delivered audio.

The original final timing JSON changed its `source` path from raw subtitles to
parent timings without changing `source_sha256`. The archived JSON separates
`parent_timings`, `raw_subtitles`, and `closing_subtitles`, and hashes each actual
referenced file. The original mismatched hashes and the correction are recorded
in each final manifest. Word, sentence, and paragraph arrays are unchanged.

The 60-second canonical script now has one trailing newline instead of two,
matching the published dialogue file. Its original TTS input and hash remain
in `sources/continuous.json`; spoken words and audio were not changed. Receipts
omit provider trace identifiers and use relative filenames. No private paths,
API keys, environment files, or browser/session profiles are included.
