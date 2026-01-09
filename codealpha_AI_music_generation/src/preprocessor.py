import os
import glob
from music21 import converter, instrument, note, chord
from src.utils import save_pickle, ensure_directory_exists
from tqdm import tqdm

class Preprocessor:
    def __init__(self, data_dir="data", output_dir="outputs/processed"):
        self.data_dir = data_dir
        self.output_dir = output_dir
        ensure_directory_exists(self.output_dir)

    def preprocess(self):
        """Loads MIDI files and converts them into a list of notes."""
        notes = []
        midi_files = glob.glob(os.path.join(self.data_dir, "*.mid"))
        
        print(f"Found {len(midi_files)} MIDI files.")

        for file in tqdm(midi_files, desc="Processing MIDI files"):
            try:
                midi = converter.parse(file)
                
                parts = instrument.partitionByInstrument(midi)
                if parts:
                    notes_to_parse = parts.parts[0].recurse()
                else:
                    notes_to_parse = midi.flat.notes

                for element in notes_to_parse:
                    if isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        notes.append('.'.join(str(n) for n in element.normalOrder))
            except Exception as e:
                print(f"Error processing {file}: {e}")

        # Save the notes for training
        save_pickle(notes, os.path.join(self.output_dir, "notes.pkl"))
        print(f"Saved {len(notes)} notes/chords to {self.output_dir}/notes.pkl")
        return notes

if __name__ == "__main__":
    p = Preprocessor()
    p.preprocess()
