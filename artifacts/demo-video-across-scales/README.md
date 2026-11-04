# Delphi Bio: designing across scales

The final approved 90-second Delphi Bio / MorphoSwarm Studio vision film, the retained 60-second cut, and the editable materials needed to rebuild both.

| Cut | Movie | Spoken dialogue | Captions | Full-size thumbnail |
| --- | --- | --- | --- | --- |
| Final 90 seconds | [MP4](delphi-bio-across-scales-90s.mp4) | [TXT](delphi-bio-across-scales-90s.txt) | [SRT](delphi-bio-across-scales-90s.srt) | [PNG](delphi-bio-across-scales-90s-poster.png) |
| Earlier 60 seconds | [MP4](delphi-bio-across-scales-60s.mp4) | [TXT](delphi-bio-across-scales-60s.txt) | [SRT](delphi-bio-across-scales-60s.srt) | [PNG](delphi-bio-across-scales-60s-poster.png) |

Both movies are 1920 × 1080 at 30 fps, narrated, with burned-in captions. The 90-second cut uses the approved third closing audition, emphasizing “you” visually and vocally, and the longer scale-overview and adversarial-design holds. Its thumbnail is the frame at 2.0 seconds: “Design a fish that can fly.” The 60-second film retains its earlier visuals and closing narration; it is a separate short edit, not a shortened copy of the final 90-second film.

## Edit and rebuild

- [Build instructions](build/README.md), [90-second edit](edits/90s.json), and [60-second edit](edits/60s.json): shared renderer, scene timing, crops, scale labels, animation layouts, captions, fonts, and media QA.
- [Voice instructions](build/VOICE.md): editable dialogue, original voice takes/settings, prepared narration, timing data, closing splice, and all five auditions. The TTS input spells the approved emphasis “YOO”; dialogue and captions retain “you”.
- [Pinned source assets](sources/assets.json): deck slides 1, 5 and 6, animated equation sphere, original art, recorded simulation and geometry clips, site captures, concept art, and sequence-viewer data.
- [Source notes](sources/source-notes.txt), [attribution](sources/attribution-and-reuse.txt), and [capture scripts](scripts/README.txt): source identity, conceptual scope, prompts, and optional future public-site captures.

Rebuilding uses archived media and audio; it does not require live sites or a speech API key. New outputs go into ignored `.build/` directories. Approved movies remain unchanged. System fonts and dependencies must be supplied separately. Fresh voice synthesis is an explicit, optional action; credentials are not included.

## Publishing and source review

- [LinkedIn post](copy/linkedin-post.txt), [optional first comment](copy/optional-first-comment.txt), and [email copy](copy/email-share.txt).
- [49-record simulation/media inventory](inventory/simulation-inventory.html), also available as [text](inventory/simulation-inventory.txt), [CSV](inventory/simulation-inventory.csv), and [JSON](inventory/simulation-inventory.json). Each entry distinguishes recorded output from a proposed design question or future experiment.
- [Public-site capture catalog](sources/site-captures/index.html).
- [Master-file manifest](manifest.json) and recorded media QA for [90 seconds](qa/90s.json) and [60 seconds](qa/60s.json).
- [Audio reproduction checks](audio/validation.json), [source/preview parity checks](build/validation.json), and [public archive audit](public-archive-audit.json), and [full rebuild checks](qa/rebuild-validation.json).
- [Archive omissions](archive-omissions.txt): private transcripts, credentials, sharing-session state, unused binaries, and redundant caches are excluded.

The film presents a biological-compiler vision using concept illustrations and recorded simulations with their limits. It does not establish a validated living organism or functional whole-organism DNA. Media checks establish file identity, render behavior, and audio/video integrity; scientific simulations and proofs were not rerun for the archive.
