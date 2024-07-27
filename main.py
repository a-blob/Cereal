import random
import mido
from mido import Message, MidiFile, MidiTrack

# Create a new MIDI file
mid = MidiFile()

# Create a new MIDI track
track = MidiTrack()
mid.tracks.append(track)

# Define the range of MIDI notes for a cello
note_range = list(range(36, 69))  # C2 to C6

# Define the range of note durations (in ticks; there are 480 ticks per beat)
short_durations = [120]*50 + [240]*40 + [480]*30  # 16th note to quarter note
long_durations = [960]*20 + [1440]*10 + [2880]*5  # half note to two whole notes

# Define the range of pause durations (in ticks)
pause_durations = [0]*80 + [480]*1 + [960]*7 + [1440]*10 + [2880]*2
# no pause, quarter note, half note, whole note, two whole notes

# Generate 100 random notes
i = 0
current_note = random.choice(note_range)
while i < 100:
    # Decide whether to generate a chunk of short or long durations
    if random.random() < 0.5:
        durations = short_durations
        chunk_size = random.randint(5, 15)
    else:
        durations = long_durations
        chunk_size = random.randint(2, 5)

    # Generate a chunk of notes with the chosen durations
    for _ in range(chunk_size):
        if i >= 100:
            break
        # Choose the next note based on the current note
        if random.random() < 0.8:
            # 80% chance to choose a note close to the current note
            next_note = current_note + random.choice([-2, -1, 1, 2])
        else:
            # 20% chance to choose any note
            next_note = random.choice(note_range)
        # Make sure the next note is within the valid range
        next_note = max(min(next_note, note_range[-1]), note_range[0])
        current_note = next_note

        duration = random.choice(durations)
        track.append(Message('note_on', note=current_note, velocity=64, time=0))
        track.append(Message('note_off', note=current_note, velocity=64, time=duration))

        # Add a random pause
        pause = random.choice(pause_durations)
        if pause > 0:
            track.append(Message('note_off', note=current_note, velocity=0, time=pause))

        i += 1

# Save the MIDI file
mid.save('random_notes.mid')
