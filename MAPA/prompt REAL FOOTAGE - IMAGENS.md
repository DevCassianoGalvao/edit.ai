# PIPELINE DOCUMENTAL DE FOTOS (BANCOS PÚBLICOS) + FFMPEG + REMOTION — PROMPT ÚNICO

## COMO USAR

**Antes de abrir o Claude, só isto:**

1. Na pasta `C:\Users\Cassiano\Desktop\Edit.AI by Galvao\Edit.AI by Galvão\MAPA`, coloque a narração como `audio.mp3`, o roteiro como `roteiro.txt` e a legenda como `legenda.srt` (os três da mesma safra).
2. Abra o Claude Code **na pasta mapa** e cole este prompt (ou o `PROMPT_v_IMAGENS.txt`, que manda seguir este e já responde as perguntas).

Nada de chave de API paga, nada de YouTube. O filme sai inteiro de **fotos de bancos públicos já integrados na pasta mapa** (Wikimedia Commons, NASA, Internet Archive, Openverse), com movimento de câmera feito pelo ffmpeg e animações do Remotion.

---

## EXECUTION MODE: FULLY AUTONOMOUS — ZERO FRICTION (after Phase -1)

**Work directly in the mapa folder.** Do NOT create a new project elsewhere, do NOT scaffold a new Remotion app — `edicao/` and `edicao_remotion/` already exist. All paths below are relative to `C:\Users\Cassiano\Desktop\Edit.AI by Galvao\Edit.AI by Galvão\MAPA`.

The ONLY mandatory interaction before Phase 0 is Phase -1 (animations/subtitles). After that, run the full pipeline end-to-end autonomously. No questions mid-run, no approval stops. Make every decision yourself using the rules below, log it in `data/decisions_log.md`, and keep going. You only speak to me: (a) a required input is missing or stale at startup; (b) the yield measurement of Phase 5.1; (c) when the final render starts (so I close Chrome); (d) delivery.

---

## ROLE

You are a senior documentary editor and motion design engineer. You are building a broadcast-quality **faceless** YouTube documentary made **only of still photographs** from public image banks, brought to life with deliberate camera movement, plus full-screen Remotion animations. Output standard: a professional studio — think Vox, Johnny Harris, ColdFusion, Ken Burns' own films. Anything that looks like a slideshow, a template, or "AI slop" is a failure.

---

## PHASE -1 — PRE-FLIGHT QUESTIONS (skip if PROMPT_v_IMAGENS.txt already answered them)

Ask me in chat and WAIT:

1. **Quer cenas de animação no Remotion (motion graphics em tela cheia) ou só fotos com movimento, uma após a outra?**
2. **Quer legenda queimada no vídeo ou não?**

Store as `INCLUDE_ANIMATIONS` and `INCLUDE_SUBTITLES` in `data/pipeline_config.json`. Re-read that file before Phases 2, 4, 6 and 7.

---

## INPUTS — AUTO-DETECT, DO NOT REPLACE

- `audio.mp3` (or `.wav/.m4a/.aac`) — narration. **SACRED ASSET**: never re-encode destructively, never trim, never alter. Loudness normalization happens only in the final mux.
- `roteiro.txt` — the narrated script (truth for words).
- `legenda.srt` — the timing (truth for when each part starts/ends).

If any is missing, or their modification dates don't match each other (leftover from the previous film), report exactly which and stop.

**No avatar, no background, no video footage in this workflow.** Every frame is a full-screen moving photo or (if enabled) a full-screen Remotion animation.

---

## NON-NEGOTIABLE HARD CONSTRAINTS

1. **Visual states.** Every frame is (a) a FULL-SCREEN photo with camera movement, or (b) a FULL-SCREEN Remotion animation (if `INCLUDE_ANIMATIONS`). Small alpha elements over a photo (lower third, place tag) are the only exception, and only when they carry a name/place the narration just said.
2. **Images only — zero video.** No YouTube, no yt-dlp, no `youtube.py`, no `cookies.txt`, no Commons/NASA video, no Pexels/Pixabay. If an old route or script offers video, don't use it.
3. **Sources only from the banks already wired in mapa:** `bancos.py` (Wikimedia Commons, NASA Image Library, Internet Archive) and Openverse via `servidor.py`, orchestrated by `auto.py`. No Bing/DuckDuckGo/Google/Serper, no news sites, no paid stock.
4. **Photos are always full-screen** 1920×1080, cover-cropped, **never** letterboxed, pillarboxed, or placed over a blurred copy of themselves.
5. **Always moving.** No static photo on screen for a single frame. No linear "PowerPoint" zoom on every shot — vary the move (see Phase 5.4).
6. **Audio is continuous and untouched.** Visual cuts never cut, duck or re-time narration.
7. **Subtitles (only if `INCLUDE_SUBTITLES`)**: over photos only, absent during full-screen animations. If false, no subtitle filter anywhere in the render.
8. **Zero visual bugs.** No black frames, no flash frames, no frozen stretches, no off-by-one gaps, no pixelated upscales, no subject pushed out of frame by the move.
9. **Licenses.** CC NC and CC ND never enter — enforced as a pool rule, not per-file rejection. Every photo's license and author recorded.
10. **Fast render.** The full film never goes through Remotion. ffmpeg builds the photo timeline; Remotion renders only the animation clips. (Phase 6.)

Violating any of these = redo the affected part.

---

## PHASE 0 — ENVIRONMENT CHECK (fast path — everything is already installed)

```bash
node -v
ffmpeg -version
py -c "import faster_whisper, PIL, onnxruntime"
```

- `edicao_remotion/node_modules` exists → don't reinstall. If missing: `npm i` inside `edicao_remotion`.
- `clipcheck.py` model downloads itself on first use (~600 MB) — check it's cached before counting on it.
- Read `LEIA-ME.md` (sections "Camada 5", "Modo automático", "O movimento tremido", "Arquivos") and `LEIA-ME-imagens.md`. Read the Remotion skill (`.claude/skills/remotion-best-practices/`) if present before touching `edicao_remotion/src`.

**Clean slate** — move the previous film's material to the Recycle Bin (don't hard-delete; low disk): `downloads/paragrafo*`, `downloads/partes.json`, `downloads/motion`, `capcut/`, `plano.json`, `concat.txt`, `comando.txt`, `linha_do_tempo.json`, `auto_relatorio.json`, `mapa.json/csv`, `*.log`, `qa_fotos/`, `edicao/clips`, `edicao/segments`, `edicao/base.mp4`, `edicao/*.json`, `edicao/preview_*.mp4`, `edicao_remotion/out`, `video_final.mp4`, `capitulos_youtube.txt`, `data/`.
**Keep:** all `.py/.mjs/.tsx` code, `node_modules`, tokens, `wikimedia_contact.txt`, `downloads/_transcricoes`, `downloads/_cache_bancos.json`.

Probe audio and write `data/source_meta.json`:
```json
{ "fps": 30, "audioDuration": 0.0, "durationInFrames": 0 }
```
`durationInFrames = Math.round(audioDuration * 30)`. Never reuse the previous film's metadata.

**GATE 0:** tools respond, clean slate done, inputs fresh, `source_meta.json` and `pipeline_config.json` present.

---

## PHASE 1 — TRANSCRIPTION & ALIGNMENT

1. Use `legenda.srt` as the timing spine. If word-level timing is needed for animations, run `audio.py` (faster-whisper; it caches in `downloads/_transcricoes`).
2. `roteiro.txt` is truth for words, Whisper/SRT for timing. Divergences → `data/alignment_report.md`.
3. Sentences contiguous, no overlaps, last end ≤ audio duration. If divergence > 15%, note it, keep the spoken version, continue.

---

## PHASE 2 — DEEP ANALYSIS & VISUAL PLAN

Read the ENTIRE script before planning. Tag:

- **HOOK** (first 90 s) — strongest photos of the film, shortest cuts.
- **KEY_EXPLANATION / TECHNICAL** — numbers, dates, mechanisms, comparisons, lists, family trees, timelines → animation candidates.
- **RETENTION_PEAK** — reveals, emotional spikes → hardest cut or a hero photo held with a slow push-in.
- **PHOTO_SUPPORT** — concrete nouns (people, places, objects, machines, buildings, landscapes) → photo parts. Default state.
- **ABSTRACT** — money, debt, law, feelings, behavior → never searched literally; give them concrete **ambient** b-roll of the film's own world (the place, the factory, the street, the object), with no colliding word.

Outputs:
- `py auto.py --modelo --chars 700 --audio audio.mp3` → blank `plano.json` already split into parts with real durations.
- Fill each part: `busca` (2–4 specific English phrases taken from THAT part's text — names, places, years) and `mostrar` (English words the photo is judged against; never a lone common word). Set `idioma`, `tema`, `assunto`, `epoca` (±5 years when dated), `fontes: ["wikimedia","openverse","nasa","archive"]`, `evitar`.
- `edicao/gerar_plano_edicao.py` rewritten for this film: chapters + animation cues (start second from the SRT, duration, props).
- Human-readable `data/visual_plan.md`: part | time | treatment | what it shows | animation (if any).

**Pacing rules:**
- First 90 s: 2.5–4 s per photo, zero weak photos, no two photos from the same series back to back.
- Rest: 4–6 s per photo (`py auto.py --seg 5`), never > 7 s on one photo. Long stretches = sequence of shots of the same subject from different angles (wide → detail → person → place).
- Animations (if enabled): where the script earns them, roughly every 45–90 s, 4–14 s each, never two in a row, never in the first 10 s alone.
- Timeline tiles the whole audio with no gaps/overlaps.

**GATE 2 (harsh self-review):** hook gets the strongest treatment; every animation has a concrete concept; no part relies on a lone abstract word; country and era anchored in every `busca`. Fix and continue.

---

## PHASE 3 — DESIGN SYSTEM

In `edicao_remotion/src` keep one visual identity (tokens in one place): 1–2 accent colors + 1 text color derived from the TOPIC and MOOD (reason in `decisions_log.md`), one display font + one text font **loaded locally from files** (Google Fonts over network blows `delayRender`), fixed type scale, named springs/easings reused everywhere. Nothing appears or disappears without animation; nothing moves linearly in animations. Grade of the photo timeline (warm grade + vignette + light grain in `final_render.py`) must match the animation backgrounds so the cut between them doesn't jump.

---

## PHASE 4 — REMOTION ANIMATIONS (only if `INCLUDE_ANIMATIONS`)

Reuse and restyle the existing compositions in `edicao_remotion/src/components.tsx` (TitleCard, ChapterCard, LowerThird, PlaceTag, QuoteCard, BigNumber, FamilyTree, CausesList, MythVsScience, Timeline) and create new ones only where the script needs them (map with route drawing, comparison bars, before/after, stacked counters). Register every new one in `Root.tsx` (ids without underscore).

Per scene:
1. 3-line storyboard comment on top (what appears, how it moves, how it exits).
2. Multi-layer composition (background treatment + content + accents), staggered spring entrances, subtle continuous drift, numbers counting up with easing, charts drawing themselves, kinetic type synced to word timestamps. Exit finishes in the last 10–15 frames.
3. Robustness: every `interpolate` clamped, no division by zero, `random(seed)` never `Math.random()`, text never overflows (measure/fit), content from props — no hardcoded text of the previous film.
4. **Review loop — minimum 3 passes, stills only, no video:** `node render_overlays.mjs --still <id>` at start / 25% / 72% / end. Pass 1 structure, Pass 2 motion (dense still sweep every 5–10 frames), Pass 3 harsh "premium or generic?" critique. Log in `data/scene_review_log.md`. A scene that can't reach the bar becomes photos.

---

## PHASE 5 — PUBLIC IMAGE BANK PIPELINE

### 5.1 Yield measurement (first hour)
`py auto.py --so-plano`, then `py auto.py --parte N` on ~6 varied parts (one proper-noun, one abstract, one period). Contact sheet of what came back. Tell me: how many are usable, from which bank, which kinds of parts will need ambient b-roll. Then run the whole `py auto.py` — ideally once.

### 5.2 Source order
1. Public-agency public domain: NASA; national archives, Library of Congress, US military, the film's country's public photo agency — mostly reached through Commons.
2. Wikimedia Commons and Openverse in CC0 / PDM / CC-BY / CC-BY-SA (Openverse filtered at query time with `license_type=commercial,modification`, short 2–3 word queries).
3. Internet Archive — period photos only; license usually "unverified", use sparingly.

Commons requests (search AND download) always go through `bancos.py` with the contact User-Agent and OAuth token; without it every download returns 429.

### 5.3 Curation — what enters the pool
Pool rules (in `curadoria.py`/`bancos.py`, not per-file lists):
- **License:** read Commons `extmetadata` (LicenseShortName, Artist) and Openverse `license`; drop NC and ND; unknown → keep flagged `unverified`.
- **Resolution:** long side ≥ 1920 px; < 1600 px never. Upscale ≤ 1.3×. Portrait only if a clean 16:9 crop keeps the whole subject.
- **Format:** photograph only. Reject infographic, chart, map, flowchart, screenshot, 3D render, AI image, illustration/engraving/painting (unless the film is about that artwork or a period with no photography), book/magazine cover, scanned page, stamp/coat of arms/medal/banknote on white, product shot, event photo (ceremony, speech, parade, museum display), watermark/logo/caption/URL burned in, heavy foreign text.
- **Wrong country / wrong era:** confine to the film's country unless the part's own words (text, busca, mostrar — never `evitar`) ask for elsewhere; the "elsewhere" list needs place names, not just countries. Dated parts explicitly deny what came later.
- **Name collisions:** see the collision table in `LEIA-ME-imagens.md` and the project memory. A common word is never alone in `mostrar`.
- Then `clipcheck.py` (local CLIP, free) drops wrong-subject photos. Then the eye, by contact sheet.

Rejected → `data/image_rejects.json` AND out of the pool. Approved → `data/image_locks.json` from the first round, so a re-run only refills rejected slots (auto.py forgets between runs otherwise). Max 2 appearances per photo, never in neighboring parts, ≥ 60 s apart from all other appearances.

### 5.4 Camera movement — what makes it a documentary and not a slideshow
Motion engine: `sincronizar._renderizar_item` (zoompan at 5760 px working width = 3×1920, curve 25% ease + 75% linear — measured jitter-free; don't replace it). Choose per photo:
- **push-in** toward the subject (default for faces, objects, reveals), 1.00 → 1.06–1.08;
- **pull-out** from a detail to the whole (openings, scale reveals);
- **horizontal pan** for landscapes, ships, trains, wide groups, ≤ 8% of width;
- **vertical pan** for tall subjects / portrait photos (towers, rockets, people full-body);
- **hold with minimal drift** (1.00 → 1.02) on the heaviest emotional line.
Rules: never the same move twice in a row; the move goes toward the subject and never crops it out; the direction is decided by where the subject is in the frame (log it). 15-frame crossfade between photos; hard cut allowed on a retention peak.

### 5.5 Sync
`py sincronizar.py --audio audio.mp3` to produce `linha_do_tempo.json` (real start of each photo, stretching a neighbor where a part came out short — holes are acceptable). Don't produce the CapCut project; this pipeline renders.

### 5.6 Attribution
`data/attribution.md`: one row per photo — file, bank, source page URL, author, license, `unverified` flag. Top of file: count of unverified IN BOLD, and the ready-to-paste credits block for all BY/BY-SA photos.

---

## PHASE 6 — FAST RENDER (ffmpeg builds, Remotion only animates)

1. **Photo clips** — `py edicao/render_clips.py`: each photo → Ken Burns clip + 15-frame tail, 6 parallel workers (more = disk bottleneck). Writes `edicao/clips_frames.json`.
2. **Animation clips** — `node edicao_remotion/render_overlays.mjs`: one bundle, renders only compositions in `plano_edicao.json`.
   - Full-screen animation → **h264, crf 16, concurrency 6** (fast, no alpha) — inserted into the timeline chain as one more clip at its exact frame, with the same fade.
   - Element over a photo (lower third / place tag) → VP9 `yuva420p` with alpha (slower — keep few), composited in step 4.
3. **Base** — `py edicao/build_base.py`: xfade chain in batches of 40 clips, 3 batches in parallel, libx264 veryfast crf 16, joined with `concat -c copy`. It must print `base.mp4 quadros == esperado`.
4. **Final** — `py edicao/final_render.py`: warm grade + vignette + light grain, alpha overlays at narration times, narration normalized to −14 LUFS (`sincronizar.filtro_loudness`), h264 **preset fast, crf 18**, AAC 192k, `+faststart`. Subtitle filter only if `INCLUDE_SUBTITLES` (add a `--legenda` flag, off by default). Chapters written to `capitulos_youtube.txt` in the script's language.
5. Before the full final: `py edicao/final_render.py --preview 0 90` and contact-sheet the first 90 s.

Speed rules: the render runs alone (no auto.py, CLIP or searches at the same time); tell me when it starts so I close Chrome; long jobs on Windows only as a scheduled task with `IdleSettings.StopOnIdleEnd` off; kill processes by command line, never python/node by name. If the motion engine or the xfade math changes, validate a 60 s sample frame by frame (SSIM ≥ 0.97 per frame, compared by position with `setpts=N/30/TB`) against the previous known-good output before trusting it.

---

## PHASE 7 — QA (no extra renders)

1. **Plan:** timeline tiles the audio, every referenced photo exists with expected size, all frame values integers, no photo > 2 appearances, no NC/ND in the pool.
2. **Contact sheets** (PIL, 30 thumbs per PNG, labeled part + file):
   - after curation: every photo on disk;
   - after `build_base.py`: one frame from the MIDDLE of each shot (±20 frames away from fades — a crossfade looks like a bad composite);
   - after final: one frame every 20 s + one in the middle of each animation.
   Look for: wrong subject/country/era, text/watermark, pixelation, subject cropped by the move, black bars, same move twice in a row. Expect 3–6 rounds; diff between rounds and sheet only what changed. Four rejects from the same host/series/query = a missing rule, fix the rule.
3. **Subtitles:** if off, confirm no subtitle filter ran; if on, absent inside full-screen animations.
4. **Animations:** each passed its 3-pass review.
5. **`py qa.py`** on `video_final.mp4`: duration = audio, no black stretch, no frozen stretch, loudness on target. 0 failures, 0 warnings.
6. `tsc --noEmit` clean in `edicao_remotion`. chr(8) audit zero in script-written files. No `^`/`$` in filename regexes (files have a numeric prefix).

---

## PHASE 8 — DELIVERY (export direct, no preview approval)

Deliver: `video_final.mp4`, `capitulos_youtube.txt`, `data/visual_plan.md`, `data/alignment_report.md`, `data/decisions_log.md`, `data/scene_review_log.md` (if animations), `data/attribution.md`, a short changelog of QA fixes, and **three thumbnails** in the script's language tested at 210 px width: the film's object IS the thumbnail — photo at full strength, cropped so the object fills the frame, max TWO words on one line in an empty corner, no band, no overline; the photo must be in the film and have a verified license.

After QA passes, move `edicao/clips` and `edicao/segments` to the Recycle Bin (low disk).

---

## WORKING STYLE

- Keep `data/progress.md` with the current step and the next command — resuming after a usage cut starts there.
- On every long step, say what's running and how much is left without being asked.
- Every judgment call → one line in `data/decisions_log.md`; decide and move on.
- Between "more images" and "cleaner film": cleaner wins. A hole stretched by the neighbor beats a wrong photo.
- Never claim something works without a still, a contact sheet, or the QA output proving it.

GO.
