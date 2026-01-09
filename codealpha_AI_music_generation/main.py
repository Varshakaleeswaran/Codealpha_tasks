import argparse
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.preprocessor import Preprocessor
from src.train_lstm import train_network
from src.train_gan import train_gan
from src.generator import MusicGenerator

def main():
    parser = argparse.ArgumentParser(description="AI Music Generation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Preprocess
    parser_preprocess = subparsers.add_parser("preprocess", help="Preprocess MIDI files")
    parser_preprocess.add_argument("--data_dir", default="data", help="Directory containing .mid files")
    
    # Train LSTM
    parser_train_lstm = subparsers.add_parser("train-lstm", help="Train the LSTM model")
    parser_train_lstm.add_argument("--epochs", type=int, default=50, help="Number of epochs to train")
    
    # Train GAN
    parser_train_gan = subparsers.add_parser("train-gan", help="Train the GAN model")
    parser_train_gan.add_argument("--epochs", type=int, default=2000, help="Number of epochs to train")
    
    # Generate
    parser_generate = subparsers.add_parser("generate", help="Generate music using trained model")
    parser_generate.add_argument("--model", choices=["lstm", "gan"], default="lstm", help="Model type to use")
    
    # Web App
    parser_web = subparsers.add_parser("web", help="Start the Web Interface")

    args = parser.parse_args()

    if args.command == "preprocess":
        p = Preprocessor(data_dir=args.data_dir)
        p.preprocess()
        
    elif args.command == "train-lstm":
        train_network(epochs=args.epochs)
        
    elif args.command == "train-gan":
        train_gan(epochs=args.epochs)
        
    elif args.command == "generate":
        gen = MusicGenerator(model_type=args.model)
        gen.run()
        
    elif args.command == "web":
        print("Starting Web App...")
        from web.app import app
        app.run(debug=True, port=5000)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
