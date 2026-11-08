import wave, math, random
from struct import pack
random.seed(42)
sr = 22050
duration = 120
total_frames = sr * duration
chords = [[60, 64, 67], [62, 65, 69], [65, 69, 72], [67, 71, 74]]
melody_notes = [60, 62, 64, 65, 67, 69, 71, 72]
def note_freq(n): return 2 ** ((n - 69) / 12.0) * 440.0
def generate_audio():
    samples = []
    for t in range(total_frames):
        time_sec = t / sr
        chord_idx = int(time_sec // 8) % len(chords)
        current_chord = chords[chord_idx]
        sample_val = 0.0
        # Pad/Chord layer
        for note in current_chord:
            freq = note_freq(note)
            phase = (time_sec * freq * 2 * math.pi) % (2 * math.pi)
            amplitude = 0.15 / len(current_chord)
            sample_val += amplitude * math.sin(phase)
        # Melody layer
        melody_idx = int(time_sec // 2) % len(melody_notes)
        m_note = melody_notes[melody_idx]
        m_freq = note_freq(m_note)
        m_phase = (time_sec * m_freq * 2 * math.pi) % (2 * math.pi)
        # Add a slight vibrato/variation to melody
        m_amp = 0.3 * (1 + 0.2 * math.sin(time_sec * 5))
        sample_val += m_amp * math.sin(m_phase)
        # Simple ambient noise/arpeggiator effect
        if t % 100 == 0:
            sample_val += random.uniform(-0.05, 0.05)
        # Clamp and convert to int16
        val = max(-32767, min(32767, int(sample_val * 32767)))
        samples.append(val)
    return samples

if __name__ == "__main__":
    audio_data = generate_audio()
    with wave.open(r"G:\Strata\Tests\music_2min.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(22050)
        wf.writeframes(b"".join(pack("<h", s) for s in audio_data))

