# AI Music Generation

A deep learning project to generate piano music using LSTM (Long Short-Term Memory) and GAN (Generative Adversarial Network) models, complete with a Flask web interface.

## Project Structure

- `src/`: Core implementation files.
  - `preprocessor.py`: Converts MIDI files to training data.
  - `data_loader.py`: Prepares data for models.
  - `model_lstm.py`: LSTM model architecture.
  - `model_gan.py`: GAN model architecture.
  - `train_lstm.py`: Training script for LSTM.
  - `train_gan.py`: Training script for GAN.
  - `generator.py`: Music generation logic.
- `web/`: Flask web application.
- `data/`: Place your training `.mid` files here.
- `outputs/`: Generated music and processed data.
- `models/`: Saved model weights.

## 🚀 Quick Start (Windows)
**Just double-click `start_app.bat`!** 
This menu lets you train models, start the web app, or generate music without typing commands.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can use the `main.py` CLI to manage the project.

### 1. Prepare Data
Place your MIDI files in the `data/` directory. Then run:
```bash
python main.py preprocess
```

### 2. Train Models
To train the LSTM model:
```bash
python main.py train-lstm
```

To train the GAN model:
```bash
python main.py train-gan
```

### 3. Generate Music (CLI)
```bash
# Basic Generation
python main.py generate

# Advanced Generation (Orchestra Mode)
# Create an Epic Band piece with guitar
python main.py generate --model lstm --ensemble Band --instrument Guitar --bpm 140
```
The output file will be saved in `outputs/generated/`.

### 4. Web Interface
Start the web app:
```bash
python main.py web
```
Open `http://localhost:5000`. 
✨ **New Features**: 
- **AI Orchestra**: Select "Band" to generate full accompaniments.
- **Moods**: Click "Happy" or "Epic" to auto-configure settings.

## Notes
- Ensure you have MIDI files in `data/` before preprocessing.
- Training can take a long time depending on your hardware.
