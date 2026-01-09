import pickle
import numpy as np
from music21 import instrument, note, stream, chord, tempo
from tensorflow.keras.models import load_model
from src.utils import load_pickle, ensure_directory_exists
import os

class MusicGenerator:
    def __init__(self, model_type="lstm", mappings_path="outputs/processed"):
        self.model_type = model_type
        
        # Determine project root based on this file's location
        # src/generator.py -> parent is src -> parent is root
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.output_dir = os.path.join(self.project_root, "outputs", "generated")
        ensure_directory_exists(self.output_dir)
        
        # Fix mappings path if it's relative
        if not os.path.isabs(mappings_path):
             mappings_path = os.path.join(self.project_root, mappings_path)
        
        # Load mappings
        self.pitches = load_pickle(os.path.join(mappings_path, 'pitches.pkl'))
        self.note_to_int = load_pickle(os.path.join(mappings_path, 'note_to_int.pkl'))
        self.int_to_note = load_pickle(os.path.join(mappings_path, 'int_to_note.pkl'))
        
        if not self.pitches:
             # Just a warning or placeholder if we are running without data
             print("Warning: Could not load pitch mappings.")
             self.n_vocab = 0
        else:
            self.n_vocab = len(self.pitches)
        
        # Load model
        self.model = None
        if self.model_type == "lstm":
            self.model_path = os.path.join(self.project_root, "models", "lstm_model.h5")
            # Fallback for new keras format if h5 doesn't exist
            possible_keras = os.path.join(self.project_root, "models", "lstm_model.keras")
            if not os.path.exists(self.model_path) and os.path.exists(possible_keras):
                self.model_path = possible_keras
        elif self.model_type == "gan":
             # We should probably load the keras model then load weights, or just save full model
             # In train_gan.py we save full model as .h5 at end. 
             # The error was in intermediate saving.
            self.model_path = os.path.join(self.project_root, "models", "gan_generator_final.h5")
        else:
            raise ValueError("Unknown model type. Choose 'lstm' or 'gan'.")

        try:
             self.model = load_model(self.model_path)
             print(f"{model_type.upper()} model loaded successfully.")
        except Exception as e:
            print(f"Could not load {model_type} model at {self.model_path}: {e}")

        # Load notes data for seeding (only needed for LSTM generally)
        self.notes_data = load_pickle(os.path.join(mappings_path, 'notes.pkl'))

    def prepare_sequences(self):
        """Prepare sequences for prediction (need data for seeding)"""
        if self.notes_data is None:
            return None, None
            
        sequence_length = 100
        network_input = []
        for i in range(0, len(self.notes_data) - sequence_length, 1):
            sequence_in = self.notes_data[i:i + sequence_length]
            network_input.append([self.note_to_int[char] for char in sequence_in])
        
        n_patterns = len(network_input)
        # Reshape and normalize
        normalized_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
        normalized_input = normalized_input / float(self.n_vocab)
        
        return network_input, normalized_input

    def generate_notes_lstm(self, network_input, length=100, temperature=1.0):
        """
        Generate notes using LSTM model
        length: number of notes to generate
        temperature: controls diversity of output (0.0 to 2.0). Higher = more random.
        """
        start = np.random.randint(0, len(network_input)-1)
        pattern = network_input[start]
        prediction_output = []
        
        print(f"Generating music with LSTM (Length={length}, Temp={temperature})...")
        
        for note_index in range(length):
            prediction_input = np.reshape(pattern, (1, len(pattern), 1))
            prediction_input = prediction_input / float(self.n_vocab)
            
            prediction = self.model.predict(prediction_input, verbose=0)[0]
            
            # Apply temperature sampling
            if temperature > 0:
                prediction = np.log(prediction + 1e-7) / temperature
                exp_preds = np.exp(prediction)
                prediction = exp_preds / np.sum(exp_preds)
                
                # Sample from probability distribution
                try:
                    index = np.random.choice(len(prediction), p=prediction)
                except ValueError:
                     # Fallback if probs don't sum to 1 due to float error
                    index = np.argmax(prediction)
            else:
                # Deterministic (Temperature = 0)
                index = np.argmax(prediction)

            result = self.int_to_note[index]
            prediction_output.append(result)
            
            pattern.append(index)
            pattern = pattern[1:len(pattern)]
            
        return prediction_output

    def generate_notes_gan(self, length=100):
        """Generate notes using GAN model"""
        print(f"Generating music with GAN (Length={length})...")
        # GAN generates fixed block size usually, but we can tile or crop. 
        # Our simple GAN model was trained for fixed sequence length (e.g. 100).
        # We will generate one block for now. 
        
        latent_dim = 100
        noise = np.random.normal(0, 1, (1, latent_dim))
        generated_seq = self.model.predict(noise)
        
        prediction_output = []
        scaled_seq = generated_seq[0] * self.n_vocab
        
        # Crop or pad? For this simple GAN we just take what it gives (fixed 100)
        # Extending GAN generation is complex (requires sliding window or progressive GANs).
        # We'll just return the fixed block.
        
        for val in scaled_seq:
            index = int(val[0])
            index = max(0, min(index, self.n_vocab - 1))
            result = self.int_to_note[index]
            prediction_output.append(result)
            
        return prediction_output

    def create_midi(self, prediction_output, filename='test_output.mid', instrument_name='Piano'):
        """Convert the output from the prediction to notes and create a midi file with selected instrument"""
        offset = 0
        output_notes = []
        
        # Select Instrument
        if instrument_name == 'Violin':
            inst = instrument.Violin()
        elif instrument_name == 'Guitar':
            inst = instrument.Guitar()
        elif instrument_name == 'Flute':
            inst = instrument.Flute()
        elif instrument_name == 'Saxophone':
            inst = instrument.Saxophone()
        else:
            inst = instrument.Piano()
            
        output_notes.append(inst)
        
        for pattern in prediction_output:
            # pattern is a chord
            if ('.' in pattern) or pattern.isdigit():
                notes_in_chord = pattern.split('.')
                notes = []
                for current_note in notes_in_chord:
                    new_note = note.Note(int(current_note))
                    new_note.storedInstrument = inst
                    notes.append(new_note)
                new_chord = chord.Chord(notes)
                new_chord.offset = offset
                output_notes.append(new_chord)
            # pattern is a note
            else:
                new_note = note.Note(pattern)
                new_note.offset = offset
                new_note.storedInstrument = inst
                output_notes.append(new_note)
            
            offset += 0.5
            
        midi_stream = stream.Stream(output_notes)
        full_path = os.path.join(self.output_dir, filename)
        midi_stream.write('midi', fp=full_path)
        print(f"Music generated and saved to {full_path}")
        return full_path

    def generate_track(self, length=100, temperature=1.0, octave_shift=0):
        """Helper to generate a sequence of notes with octave shift"""
        network_input, _ = self.prepare_sequences()
        if not network_input: return []
        
        # Use existing generation logic but we assume LSTM for multi-track for now as it's more musical
        # For band mode we force LSTM or support GAN if selected
        if self.model_type == 'gan':
             base_notes = self.generate_notes_gan(length)
        else:
             base_notes = self.generate_notes_lstm(network_input, length, temperature)
             
        # Apply octave shift
        shifted_notes = []
        for n in base_notes:
            if n.isdigit() or ('.' in n):
                # It's a note index string or chord string from our mapping
                # We need to parse it to Note object to shift, but we usually return strings here
                # Let's return strings and shift in create_midi? 
                # Better to return Note objects from a new internal helper? 
                # Let's keep returning strings and handle shift later?
                # Actually, our strings are just pitch names implies 'C4', 'E4'.
                # Wait, our preprocessor saved "str(element.pitch)".
                # Music21 pitch strings can be transposed.
                shifted_notes.append(n) 
            else:
                 shifted_notes.append(n)
        return shifted_notes

    def create_multitrack_midi(self, tracks_info, filename='band_output.mid', bpm=120):
        """
        tracks_info: list of dicts { 'notes': [], 'instrument': InstrumentObj, 'octave_shift': int }
        """
        s = stream.Score()
        s.append(tempo.MetronomeMark(number=bpm))
        
        for track_data in tracks_info:
            p = stream.Part()
            p.insert(0, track_data['instrument'])
            
            notes_str = track_data['notes']
            shift = track_data['octave_shift']
            offset = 0
            
            for pattern in notes_str:
                # pattern is a chord
                if ('.' in pattern) or (pattern[0].isdigit() and '.' in pattern):
                    notes_in_chord = pattern.split('.')
                    notes = []
                    for current_note in notes_in_chord:
                        # Depending on how we saved chords, might be ints or pitch names
                        if current_note.isdigit():
                             new_note = note.Note(int(current_note))
                        else:
                             new_note = note.Note(current_note)
                        
                        # Transpose
                        new_note.pitch.transpose(shift * 12, inPlace=True)
                        new_note.storedInstrument = track_data['instrument']
                        notes.append(new_note)
                    new_chord = chord.Chord(notes)
                    new_chord.offset = offset
                    p.append(new_chord)
                    
                # pattern is a note
                else:
                    if pattern.isdigit():
                        new_note = note.Note(int(pattern))
                    else:
                        new_note = note.Note(pattern)
                    
                    new_note.pitch.transpose(shift * 12, inPlace=True)
                    new_note.offset = offset
                    new_note.storedInstrument = track_data['instrument']
                    p.append(new_note)
                
                offset += 0.5
            s.append(p)

        full_path = os.path.join(self.output_dir, filename)
        s.write('midi', fp=full_path)
        print(f"Band generated and saved to {full_path}")
        return full_path

    def run(self, length=100, temperature=1.0, instrument_name='Piano', ensemble='Solo', bpm=120):
        if not self.model:
            print("Model not loaded. Cannot generate.")
            return None

        # Build tracks based on Ensemble mode
        tracks = []
        
        # 1. Main Melody
        main_notes = self.generate_track(length, temperature)
        tracks.append({
            'notes': main_notes,
            'instrument': self.get_instrument(instrument_name),
            'octave_shift': 0
        })
        
        if ensemble in ['Duet', 'Trio', 'Band']:
            # 2. Bass Line (Lower temperature, shifted down 2 octaves)
            bass_notes = self.generate_track(length, temperature=0.5)
            # Bass usually simpler? We just reuse model.
            tracks.append({
                'notes': bass_notes,
                'instrument': instrument.ElectricBass(),
                'octave_shift': -2
            })
            
        if ensemble in ['Trio', 'Band']:
            # 3. Harmony/Pad (Violin/Strings, shifted 0 or -1)
            harmony_notes = self.generate_track(length, temperature=0.8)
            tracks.append({
                'notes': harmony_notes,
                'instrument': instrument.StringInstrument(),
                'octave_shift': -1
            })

        if ensemble == 'Band':
             # 4. Arpeggio/Counter-melody (Flute, High octave)
             extra_notes = self.generate_track(length, temperature=1.2)
             tracks.append({
                'notes': extra_notes,
                'instrument': instrument.Flute(),
                'octave_shift': 1
             })

        return self.create_multitrack_midi(tracks, filename=f"orchestra_{ensemble.lower()}.mid", bpm=bpm)

    def get_instrument(self, name):
        if name == 'Violin': return instrument.Violin()
        if name == 'Guitar': return instrument.Guitar()
        if name == 'Flute': return instrument.Flute()
        if name == 'Saxophone': return instrument.Saxophone()
        return instrument.Piano()

if __name__ == "__main__":
    # Default to LSTM for CLI test
    gen = MusicGenerator(model_type="lstm")
    gen.run()
