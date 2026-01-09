from music21 import stream, note, chord, meter, tempo
import os

def create_sample_midi():
    s = stream.Stream()
    s.append(tempo.MetronomeMark(number=120))
    s.append(meter.TimeSignature('4/4'))

    # Generate enough notes for sequence_length=100
    # Let's generate 200 notes
    notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
    for i in range(200):
        n_str = notes[i % len(notes)]
        n = note.Note(n_str)
        n.quarterLength = 0.5
        s.append(n)

    if not os.path.exists("data"):
        os.makedirs("data")
        
    s.write('midi', fp='data/sample_scale_long.mid')
    print("Created data/sample_scale_long.mid")

if __name__ == "__main__":
    create_sample_midi()
