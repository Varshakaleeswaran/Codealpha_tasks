from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Reshape, BatchNormalization, LeakyReLU, Flatten, Conv1D, Input, Dropout
from tensorflow.keras.optimizers import Adam
import numpy as np

class MusicGAN:
    def __init__(self, sequence_length, n_vocab):
        self.sequence_length = sequence_length
        self.n_vocab = n_vocab
        self.latent_dim = 100
        
        self.generator = self.build_generator()
        self.discriminator = self.build_discriminator()
        
        self.discriminator.compile(loss='binary_crossentropy', 
                                   optimizer=Adam(0.0002, 0.5), 
                                   metrics=['accuracy'])
        
        # Combined GAN model
        self.discriminator.trainable = False
        self.gan = Sequential([self.generator, self.discriminator])
        self.gan.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5))

    def build_generator(self):
        model = Sequential()
        model.add(Dense(256, input_dim=self.latent_dim))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        # Determine output shape. 
        # For simplicity in this example, we generate a flat sequence of integers 
        # representing notes, scaled/normalized. 
        # A more complex GAN might output (sequence_length, n_vocab) with softmax.
        # Here we will try to generate a sequence of continuous values we map to notes.
        model.add(Dense(self.sequence_length, activation='sigmoid'))
        model.add(Reshape((self.sequence_length, 1)))
        return model

    def build_discriminator(self):
        model = Sequential()
        model.add(Conv1D(64, kernel_size=3, strides=2, input_shape=(self.sequence_length, 1), padding="same"))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv1D(128, kernel_size=3, strides=2, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))
        return model
