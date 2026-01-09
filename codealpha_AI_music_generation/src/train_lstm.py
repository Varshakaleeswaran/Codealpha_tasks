from src.data_loader import DataLoader
from src.model_lstm import create_lstm_model
from tensorflow.keras.callbacks import ModelCheckpoint
from src.utils import ensure_directory_exists
import os

def train_network(epochs=50, batch_size=64):
    print("Loading data...")
    loader = DataLoader()
    network_input, network_output = loader.prepare_sequences()
    
    n_vocab = loader.n_vocab
    input_shape = (network_input.shape[1], network_input.shape[2])
    
    print(f"Creating model with input shape {input_shape} and vocab size {n_vocab}...")
    model = create_lstm_model(input_shape, n_vocab)
    
    weights_dir = "models/lstm_weights"
    ensure_directory_exists(weights_dir)
    
    filepath = os.path.join(weights_dir, "weights-improvement-{epoch:02d}.keras")
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]
    
    print(f"Starting training for {epochs} epochs...")
    model.fit(network_input, network_output, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list)
    
    # Save final model
    model.save("models/lstm_model.h5")
    print("Training complete. Model saved to models/lstm_model.h5")

if __name__ == "__main__":
    train_network()
