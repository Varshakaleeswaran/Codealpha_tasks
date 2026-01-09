from src.data_loader import DataLoader
from src.model_gan import MusicGAN
import numpy as np
import os
from src.utils import ensure_directory_exists

def train_gan(epochs=2000, batch_size=32, sample_interval=200):
    print("Loading data...")
    loader = DataLoader()
    # For GAN, we just need the input sequences, not the next note targets usually.
    # We will use the normalized network_input from DataLoader.
    # Note: DataLoader returns (input, output). We only use input here.
    network_input, _ = loader.prepare_sequences()
    
    # Reshape input for GAN: (samples, sequence_length, 1) - already is this shape from DataLoader
    X_train = network_input 
    
    gan_model = MusicGAN(loader.sequence_length, loader.n_vocab)
    
    valid = np.ones((batch_size, 1))
    fake = np.zeros((batch_size, 1))
    
    weights_dir = "models/gan_weights"
    ensure_directory_exists(weights_dir)

    print("Starting GAN training...")
    for epoch in range(epochs):
        # ---------------------
        #  Train Discriminator
        # ---------------------
        idx = np.random.randint(0, X_train.shape[0], batch_size)
        real_seqs = X_train[idx]
        
        noise = np.random.normal(0, 1, (batch_size, gan_model.latent_dim))
        gen_seqs = gan_model.generator.predict(noise)
        
        d_loss_real = gan_model.discriminator.train_on_batch(real_seqs, valid)
        d_loss_fake = gan_model.discriminator.train_on_batch(gen_seqs, fake)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        
        # ---------------------
        #  Train Generator
        # ---------------------
        noise = np.random.normal(0, 1, (batch_size, gan_model.latent_dim))
        g_loss = gan_model.gan.train_on_batch(noise, valid)
        
        if epoch % sample_interval == 0:
            print(f"{epoch} [D loss: {d_loss[0]}, acc.: {100*d_loss[1]}] [G loss: {g_loss}]")
            gan_model.generator.save_weights(os.path.join(weights_dir, f"gan_generator_{epoch}.weights.h5"))

    gan_model.generator.save("models/gan_generator_final.h5")
    print("GAN Training complete.")

if __name__ == "__main__":
    train_gan()
