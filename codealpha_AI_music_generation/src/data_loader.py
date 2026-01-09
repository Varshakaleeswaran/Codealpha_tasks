import numpy as np
from tensorflow.keras.utils import to_categorical
from src.utils import load_pickle, save_pickle
import os

class DataLoader:
    def __init__(self, data_path="outputs/processed/notes.pkl", sequence_length=100):
        self.data_path = data_path
        self.sequence_length = sequence_length
        self.notes = load_pickle(self.data_path)
        if self.notes is None:
            raise FileNotFoundError(f"Data file not found at {self.data_path}. Run preprocessor.py first.")
        
        # Get all pitch names and map to integers
        self.pitches = sorted(set(item for item in self.notes))
        self.n_vocab = len(self.pitches)
        self.note_to_int = {note: number for number, note in enumerate(self.pitches)}
        self.int_to_note = {number: note for number, note in enumerate(self.pitches)}
        
        # Save mappings for generation later
        mapping_dir = os.path.dirname(self.data_path)
        save_pickle(self.pitches, os.path.join(mapping_dir, 'pitches.pkl'))
        save_pickle(self.note_to_int, os.path.join(mapping_dir, 'note_to_int.pkl'))
        save_pickle(self.int_to_note, os.path.join(mapping_dir, 'int_to_note.pkl'))

    def prepare_sequences(self):
        """Prepare the sequences used by the Neural Network"""
        network_input = []
        network_output = []

        # Create input sequences and the corresponding outputs
        for i in range(0, len(self.notes) - self.sequence_length, 1):
            sequence_in = self.notes[i:i + self.sequence_length]
            sequence_out = self.notes[i + self.sequence_length]
            network_input.append([self.note_to_int[char] for char in sequence_in])
            network_output.append(self.note_to_int[sequence_out])

        n_patterns = len(network_input)

        # Reshape the input into a format compatible with LSTM layers
        network_input = np.reshape(network_input, (n_patterns, self.sequence_length, 1))
        
        # Normalize input
        network_input = network_input / float(self.n_vocab)

        # One-hot encode the output
        network_output = to_categorical(network_output, num_classes=self.n_vocab)

        return network_input, network_output
