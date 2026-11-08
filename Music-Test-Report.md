# Strata Music Generation Test Report

- Date: 2026-11-09 (local)
- Status: **PASS** - a 2-minute MP3 was produced.
- Model: `qwen3.8-flash-next-coder-iq1_m`
- Model source: Qwen3.8-Flash-Next Coder IQ1_M (ISTA-DASLab GSQ-RCO)
- Strata: 0.2.12 / engine 0.1.58 CUDA 13
- API: `http://127.0.0.1:8081/v1`
- Repository: <https://github.com/wahaha232/strata-music-test>

## 1. Objective and model limitation

The requested test was to generate a 2-minute piece of music. This Strata model
is a text/code-only model and has no audio output; it cannot emit an MP3 or WAV
directly. The test therefore asked the model to write a self-contained Python
synthesizer, executed that program, and converted the result to MP3.

## 2. Environment

- GPU: NVIDIA RTX 3060 12 GB, driver 610.88, CUDA UMD 13.3
- GPU use during generation: about 11.8 GB; Folding@home was PAUSED by Strata
- RAM: 31.94 GB total, about 0.74 GB free during/after generation
- Storage: G: ADATA NH13 USB HDD (about 287 GB free)
- Runtime: 32,768 context, KV int8, parallel 1, thinking off (`reasoning_effort=none`)

## 3. Prompt sent to the model

```text
Write a complete, self-contained Python 3 script that uses ONLY the Python
standard library (wave, math, struct, random) to synthesize exactly 120 seconds
of pleasant ambient music and write it to G:\Strata\Tests\music_2min.wav.
Use 22050 Hz, 16-bit, mono. Include a chord progression and a simple melody.
Keep the script under 60 lines. Output only raw Python code, with no markdown
fences and no explanation.
```

## 4. Generation result

- Parameters: `max_tokens=600`, `temperature=0.2`, `stream=false`
- Usage: prompt 115 tokens, completion 600 tokens, total 715 tokens
- Finish reason: **length** (the 600-token cap was reached)
- Server-measured speed: about 0.8 tokens/s; total about 17 minutes
- Output: a 46-line Python synthesizer (1,725 bytes)
- Truncation: the response ended inside the `wave.open` block, after the comment
  `# Pack all samples into bytes using struct`. The missing final line was added
  manually:
  `wf.writeframes(b"".join(pack("<h", s) for s in audio_data))`
  All other synthesizer code is the model's output.

The script uses:
- a four-chord progression (C, Dm, F, G voicings), 8 seconds per chord
- an 8-note melody changing every 2 seconds
- a sine pad/chord layer, sine melody with vibrato, and sparse noise
- 22,050 Hz, 16-bit, mono, 120 seconds

## 5. Execution and audio files

- Executed with the Strata bundled Python 3.12 (standard library only)
- Script runtime: 13.2 seconds
- WAV: `music_2min.wav`, 5,292,044 bytes, 2:00.00, 22,050 Hz, 16-bit mono
- MP3: `music_2min.mp3`, 2,881,454 bytes, 2:00.00, 192 kbps, 44.1 kHz mono
- MP3 encoder: ffmpeg 8.1.2 with libmp3lame
- Volume analysis: mean -12.8 dB, max -5.5 dB (audible, not silent, not clipped)

## 6. SHA-256

| File | Bytes | SHA-256 |
|---|---:|---|
| music_2min.mp3 | 2,881,454 | `776697B556492C8AD248CB822FCB448B835D317E6E8453C03A134353524285E9` |
| music_2min.wav | 5,292,044 | `E2676D10B6881AB63410CCF9440F8721365CEE88F0CDBABFA447E8D1024CDBC7` |
| music_code.py | 1,725 | `6A412DD82DE6A5FFD32302E66DF06EDFF7BB4985123F6A4A8CC04E3CE0F8389E` |

## 7. Download links

- Repository: <https://github.com/wahaha232/strata-music-test>
- MP3 direct:
  <https://raw.githubusercontent.com/wahaha232/strata-music-test/main/music_2min.mp3>
- WAV direct:
  <https://raw.githubusercontent.com/wahaha232/strata-music-test/main/music_2min.wav>
- Python source:
  <https://raw.githubusercontent.com/wahaha232/strata-music-test/main/music_code.py>
- This report:
  <https://raw.githubusercontent.com/wahaha232/strata-music-test/main/Music-Test-Report.md>

## 8. Verdict

PASS for the music output and for the model's coding ability: the model produced
a working ambient synthesizer, and the resulting audio is a valid, audible
2-minute MP3.

Caveats:
1. The model is text/code-only; audio was produced by executing its code.
2. The completion hit the 600-token budget and needed one final `writeframes`
   line to be completed manually.
3. Generation took about 17 minutes at roughly 0.8 tokens/s.

## 9. Reproduction

1. Start Strata with `G:\Strata\Scripts\Start-Strata.bat` (pauses Folding@home).
2. Send the prompt in section 3 to
   `POST http://127.0.0.1:8081/v1/chat/completions` with `max_tokens=600`.
3. Save the returned code as `music_code.py` and run it with the bundled Python.
4. Convert the WAV to MP3:
   `ffmpeg -y -i music_2min.wav -codec:a libmp3lame -b:a 192k -ar 44100 music_2min.mp3`

All generated Strata/test files are under `G:\Strata`; no Strata files were
written to C:, D: or another drive. The pre-existing FDM Portable ffmpeg was used
only as a converter, with output written to G:.
