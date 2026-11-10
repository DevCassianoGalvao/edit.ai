# PIPELINE DOCUMENTAL 80% FOTO / 20% VÍDEO + MOTION GRAPHICS — PROMPT ÚNICO

## COMO USAR

**Antes de abrir o Claude, só isto:**

1. Na pasta `C:\Users\Cassiano\Desktop\Edit.AI by Galvao\Edit.AI by Galvão\MAPA`, coloque a narração como `audio.mp3`, o roteiro como `roteiro.txt` e a legenda como `legenda.srt` (os três da mesma safra).
2. Abra o Claude Code **na pasta mapa** e cole este prompt (ou o `PROMPT_v_80_20.txt`, que manda seguir este e já responde as perguntas).

Nada de chave de API paga. O filme sai de **fotos de bancos públicos** (Wikimedia Commons, Openverse, NASA) mais **20% de vídeo** (vídeo do Commons/NASA e trechos curtos do YouTube), com movimento de câmera feito pelo ffmpeg e motion graphics do Remotion em duas camadas: tela cheia e sobre a imagem.

---

## EXECUTION MODE: FULLY AUTONOMOUS — ZERO FRICTION (after Phase -1)

**Work directly in the mapa folder.** Do NOT create a new project elsewhere, do NOT scaffold a new Remotion app — `edicao/` and `edicao_remotion/` already exist. All paths are relative to `C:\Users\Cassiano\Desktop\Edit.AI by Galvao\Edit.AI by Galvão\MAPA`.

The only mandatory interaction before Phase 0 is Phase -1 (animations/subtitles). After that, run end-to-end autonomously: no questions mid-run, no approval stops. Log every judgment call in `data/decisions_log.md`. You only speak to me: (a) a required input is missing or stale; (b) the yield measurement of Phase 5.1; (c) when YouTube starts blocking downloads; (d) when the final render starts (so I close Chrome); (e) delivery.

---

## ROLE

You are a senior documentary editor and motion design engineer. You are building a broadcast-quality **faceless** YouTube documentary: **80% still photographs with deliberate camera movement, 20% real video**, plus Remotion motion graphics — full-screen scenes and overlays composited on top of the footage. Output standard: Vox, Johnny Harris, ColdFusion. Anything that looks like a slideshow, a template, or "AI slop" is a failure.

---

## PHASE -1 — PRE-FLIGHT QUESTIONS (skip if PROMPT_v_80_20.txt answered them)

1. **Quer motion graphics (tela cheia + sobre a imagem) ou só o material bruto cortado?**
2. **Quer legenda queimada no vídeo ou não?**

Store as `INCLUDE_ANIMATIONS` and `INCLUDE_SUBTITLES` in `data/pipeline_config.json`; re-read before Phases 2, 4, 6 and 7.

---

## INPUTS — AUTO-DETECT, DO NOT REPLACE

- `audio.mp3` — narration. **SACRED ASSET**: never re-encode destructively, never trim. Loudness only in the final mux.
- `roteiro.txt` — truth for words. `legenda.srt` — truth for timing.

If any is missing, or their dates don't match each other, report which and stop.

---

## NON-NEGOTIABLE HARD CONSTRAINTS

1. **Mistura 80/20.** Photos (with movement) carry the film; real video is **15–25% of screen seconds**, animations not counted. Below 15% it's a slideshow; above 25% it becomes another film.
2. **Video is always muted.** The narration is the only audio. A video clip that needs its own sound is the wrong clip.
3. **Sources.** Photos: Wikimedia Commons, Openverse, NASA (`bancos.py`, `servidor.py`, orchestrated by `auto.py`). Video: Commons/NASA video (`bancos.wikimedia_videos`, `bancos.nasa_videos`) FIRST, YouTube short slices (`youtube.py`) only for what the banks don't have. No Bing/DuckDuckGo/Google/Serper, no news sites, no paid stock.
4. **Never download a full YouTube video.** `youtube.py:baixar_trecho(video_id, pasta, nome, inicio, duracao)` pulls 8–12 s only.
5. **Every frame is full-screen** 1920×1080, cover-cropped. Never letterboxed, pillarboxed, or over a blurred copy of itself.
6. **Photos always move; video never gets camera movement** (it already moves).
7. **Licenses.** CC NC and CC ND never enter, photo or video — pool rule, not per-file rejection. Unverified never ships.
8. **Zero visual bugs.** No black frames, no flash frames, no frozen stretches, no pixelated upscale, no subject cropped by the move, no burned-in text or channel watermark.
9. **Fast render.** The full film never goes through Remotion: ffmpeg builds the timeline, Remotion renders only the animation clips; the final render runs in ~2 min chunks.
10. **Subtitles only if `INCLUDE_SUBTITLES`.**

---

## PHASE 0 — ENVIRONMENT CHECK

```bash
node -v
ffmpeg -version
py -c "import faster_whisper, PIL, onnxruntime"
py youtube.py   # diagnostico(): confirma yt-dlp e cookies.txt
```

Read `LEIA-ME.md` ("Camada 1 — Vídeo do YouTube", "Camada 5", "Modo automático", "O movimento tremido") and `LEIA-ME-imagens.md`.

**Clean slate** — previous film's material to the Recycle Bin (list in `PROMPT_v_80_20.txt`), keeping code, `node_modules`, tokens, `cookies.txt`, `downloads/_transcricoes`, `downloads/_cache_bancos.json`.

Probe audio → `data/source_meta.json` (`fps: 30`, `audioDuration`, `durationInFrames = round(dur*30)`).

**GATE 0:** tools respond, clean slate done, inputs fresh, `pipeline_config.json` present.

---

## PHASE 1 — ALIGNMENT

`legenda.srt` is the timing spine; `roteiro.txt` is truth for words. Divergences → `data/alignment_report.md`. Sentences contiguous, last end ≤ audio duration.

---

## PHASE 2 — VISUAL PLAN (com as três camadas)

Read the ENTIRE script first. Tag each stretch:

- **HOOK** (first 90 s): the strongest material of the film, shortest cuts, 1–2 video cuts.
- **MOVIMENTO REAL** → video: glacier, sea, fire, smoke, crowd, machine working, vehicle moving, people walking, rain, drone over the film's place.
- **OBJETO / DOCUMENTO / RETRATO** → photo. A still photo with a good push-in beats a bad video, always.
- **NÚMERO, DATA, LISTA, COMPARAÇÃO, MECANISMO** → full-screen animation.
- **NOME, LUGAR, DETALHE NO QUADRO, DADO CURTO** → overlay over the image (Phase 4B).
- **ABSTRATO** (money, law, feeling) → never searched literally; concrete ambient b-roll of the film's own world.

Outputs:
- `py auto.py --modelo --chars 700 --audio audio.mp3` → blank `plano.json`.
- Fill per part: `busca` + `mostrar` (photos, English, anchored in the film's country/subject) and `video` (1–3 English phrases for the clips this part needs; omit where video doesn't belong). Top level: `idioma`, `tema`, `assunto`, `epoca`, `fontes`, `evitar`, `video_alvo: 0.20`.
- `edicao/gerar_plano_edicao.py` rewritten for this film: chapters + every animation cue (full-screen and overlay), each anchored to an exact phrase of the narration.
- `data/visual_plan.md`: part | time | foto/vídeo/animação | what it shows.

**Pacing:**
- First 90 s: 2.5–4 s per shot. Rest: 4–6 s per photo, 4–8 s per video clip, never > 7 s on one photo.
- Video: ~1 cut every 60–90 s, never two in a row, never glued to an animation.
- Full-screen animations: every 45–90 s, 4–16 s, never two in a row, never alone in the first 10 s.
- Overlays: 2–4 per minute, 3–6 s each, never inside (or within 0.7 s of) a full-screen animation.
- Timeline tiles the whole audio, no gaps, no overlaps.

---

## PHASE 3 — DESIGN SYSTEM

One identity in `edicao_remotion/src`: 1–2 accent colors + 1 text color from the topic's mood, one display font + one text font **loaded locally** (Google Fonts over the network blows `delayRender`), named springs/easings reused everywhere. The warm grade + vignette + grain of `final_render.py` is applied BEFORE the overlays, so overlays carry their own shadow to stay legible.

---

## PHASE 4 — MOTION GRAPHICS (only if `INCLUDE_ANIMATIONS`)

### 4A. Full-screen scenes (h264, background = a photo from that stretch, blurred)
Reuse and restyle what exists in `components.tsx` (TitleCard, ChapterCard, BigNumber, ListCard, VersusCard, QuoteCard, Timeline, MapScene, ShoulderWound as an example of a subject diagram) and build the one scene this film needs to EXPLAIN its mechanism. Multi-layer, staggered spring entrances, numbers counting with easing, charts drawing themselves, exit finished before the 15-frame tail.

### 4B. Overlays over the footage (VP9 with alpha) — **varie**
Minimum catalogue; implement what's missing and register it in `Root.tsx` as OVERLAY:
- **LowerThird** — name + role of who the narration just cited.
- **PlaceTag** — place + date, upper-left.
- **Callout** — thin leader line/arrow pointing at a spot in the frame with a short label.
- **CircleHighlight** — circle or rectangle that draws itself and pulses over the detail.
- **StatCorner** — small number + label in a corner, counting when it's a big number.
- **KineticLine** — 3–6 words of the narration itself, entering word by word, lower third.
- **SourceStamp** — source/year of a figure, discreet, bottom corner.
- **ProgressTimeline** — a slim bar with the date of the stretch, for films that jump in time.

Rules: never the same overlay type twice in a row, and no type more than 3 times without changing its entrance; entrances and exits varied (rise+fade, clip-path wipe, spring scale, stroke draw); at most one overlay on screen (two only in opposite corners, one of them SourceStamp); 96 px safe area, never over the face, the subject or the centre; VP9+alpha is slow (~13 s per short clip), so keep them short and few enough to render.

### Review loop — 3 passes, stills only
`node render_overlays.mjs --still <id>` at start / 25% / 72% / end (+ tail for full-screen). Pass 1 structure, Pass 2 motion (dense sweep), Pass 3 harsh "premium or generic?". Log in `data/scene_review_log.md`. A scene that can't reach the bar becomes photo/video.

---

## PHASE 5 — MATERIAL

### 5.1 Yield measurement (first hour)
`py auto.py --so-plano`, then `py auto.py --parte N` on ~6 varied parts, plus `scripts/fetch_video.py --parte N` on 2 parts (one bank video, one YouTube). Contact-sheet both. Tell me: how many photos are usable and from which bank, how many video clips are usable, and which stretches will need ambient b-roll. Only then harvest at scale.

### 5.2 Photos
Order: public-agency public domain → Commons/Openverse (CC0/PDM/BY/BY-SA, Openverse filtered with `license_type=commercial,modification`). Commons search AND download always through `bancos.py` (contact UA + OAuth token), or every download returns 429.
Pool rules: license (no NC/ND), long side ≥ 1920 px (never < 1600, upscale ≤ 1.3×), photograph only (no infographic, chart, map, 3D render, AI image, book cover, scanned page, scale bar, watermark, event photo), right country, right era, no lone common word in `mostrar`.

### 5.3 Video (`scripts/fetch_video.py`, novo e curto)
For each part with `video`:
1. `bancos.wikimedia_videos(q, n)` / `bancos.nasa_videos(q, n)` — direct download, clean license.
2. If nothing serves: `youtube.py:buscar(q, num, minimo, maximo)` → score by title/channel → `baixar_trecho(video_id, pasta, nome, inicio, duracao)` with 8–12 s. **Never the whole video.**
Then `ffprobe` each file: ≥1080p, duration as requested (proof it is a slice), no audio needed. Write `data/video_manifest.json`: part, file, source, channel, URL, in/out, license.
Reject on sight: watermark or channel bug (crop ~12% of the border and re-fit 16:9 before scaling — cropping only the height stretches the image), burned-in text, talking head, an edit cut inside the slice, shaky digital zoom, AI-video channels, "archive" channels that stamp the frame, news agency and broadcaster (Content ID), compilations with voice-over.
Fair use: short, muted, recut, inside a film with original narration. Record channel + URL for every clip so a claim can be disputed.

### 5.4 Movement (photos only)
Engine: `perspective` with cubic interpolation in `render_clips.py` (sub-pixel; it replaced zoompan, which places on whole pixels and shows tremor — measured 0.345 px → 0.03 px). Vary: push-in toward the subject, pull-out, horizontal pan, vertical pan for tall photos, minimal drift on the heaviest line. Never the same move twice in a row; the move never crops the subject out; zoom ≤ 1.08. 15-frame crossfade between shots.

### 5.5 Sync and edit list
`py sincronizar.py --audio audio.mp3` → `linha_do_tempo.json` (holes are acceptable: the neighbour stretches). Then `py edicao/monta_edicao.py`, which: marks each item photo/video by extension, gives movement only to photos, inserts full-screen animations at their exact frame with the same tail and fade, splits any photo longer than 7 s reusing approved photos (max 2 appearances, 60 s apart), copies the background photo of each full-screen scene into `edicao_remotion/public/bg`, and **prints the photo/video/animation split in seconds and percent**.

### 5.6 Attribution
`data/attribution.md`: every photo (file, bank, page URL, author, license) and every clip (file, channel, URL, in/out, license). Unverified count in bold at the top; ready-to-paste BY/BY-SA credits block.

---

## PHASE 6 — RENDER (ffmpeg builds, Remotion only animates)

1. `py edicao/render_clips.py` — photo → `perspective` Ken Burns + 15-frame tail; video → `sincronizar._renderizar_item` (border detect, cover scale, exact trim, loop if short), no camera move. Six workers.
2. `node edicao_remotion/render_overlays.mjs` — full-screen → h264 crf 16, concurrency 6, with `tail` and `bg`; overlay → VP9 `yuva420p`.
3. `py edicao/build_base.py` — xfade chain in batches of 40, 3 in parallel, `concat -c copy`. Must print `base.mp4 quadros == esperado`.
4. `py edicao/final_render.py` — warm grade + vignette + grain, alpha overlays at their narration times, narration at −14 LUFS (the measured gain lands ~1.1 dB high, so the script trims it), h264 preset fast crf 18, AAC 192k, `+faststart`. **In ~2 min chunks, 2 in parallel, resumable** — one single ffmpeg with every overlay open once hung the machine.
5. Before the full final: `--preview 0 90` + contact sheet.

Render runs alone; tell me to close Chrome; kill processes by command line, never by name.

---

## PHASE 7 — QA

1. **Plan:** timeline tiles the audio; every referenced file exists; integer frames; no photo > 2 appearances; no NC/ND; **video share between 15% and 25%** (report the real number).
2. **Contact sheets:** all photos after harvest; 3 frames per video clip (start/middle/end); one mid-shot frame per item after `build_base`; one frame every 20 s + one inside each animation after the final. Before rejecting by index, confirm the sheet's item count equals the list's file count.
3. **Audio:** no video clip contributes audio; narration continuous; measure the final with `ebur128` (−14 LUFS).
4. **Animations:** each passed its 3-pass review; no overlay inside a full-screen scene; overlay types varied.
5. `py qa.py` on `video_final.mp4`: duration = audio, no black stretch, no frozen stretch, loudness on target. 0 failures, 0 warnings.
6. `tsc --noEmit` clean; chr(8) audit zero; no `^`/`$` in filename regexes.

---

## PHASE 8 — DELIVERY (export direct, no preview approval)

`video_final.mp4`, `capitulos_youtube.txt`, `data/visual_plan.md` (with the foto/vídeo column and the final percentage), `data/alignment_report.md`, `data/decisions_log.md`, `data/scene_review_log.md`, `data/attribution.md`, `data/video_manifest.json`, a short changelog of QA fixes, and **three thumbnails** in the script's language tested at 210 px: the film's object IS the thumbnail — photo at full strength, cropped so the object fills the frame, max TWO words in an empty corner, no band; the photo must be in the film with a verified license.

After QA passes, move `edicao/clips`, `edicao/segments` and `edicao/final_partes` to the Recycle Bin.

---

## WORKING STYLE

- Keep `data/progress.md` with the current step and the next command.
- Say what is running and how much is left, without being asked.
- Between "more material" and "cleaner film": cleaner wins. A hole stretched by the neighbour beats a wrong shot.
- Never claim something works without a still, a contact sheet or QA output proving it.

GO.
