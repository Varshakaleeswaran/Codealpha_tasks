from flask import Flask, render_template, request, send_file
import os
import sys

# Add project root to path so we can import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generator import MusicGenerator
from src.utils import get_timestamp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        model_type = request.form.get('model_type', 'lstm')
        length = int(request.form.get('length', 100))
        temperature = float(request.form.get('temperature', 1.0))
        instrument_name = request.form.get('instrument', 'Piano')
        ensemble = request.form.get('ensemble', 'Solo')
        bpm = int(request.form.get('bpm', 120))

        print(f"Request: Model={model_type}, Ensemble={ensemble}, Inst={instrument_name}, BPM={bpm}")
        
        gen = MusicGenerator(model_type=model_type)
        if not gen.model:
             return f"Model ({model_type}) not found. Please train it first.", 500
        
        output_filename = f"gen_{ensemble}_{instrument_name}_{get_timestamp()}.mid"
        
        file_path = gen.run(length=length, temperature=temperature, instrument_name=instrument_name, ensemble=ensemble, bpm=bpm) 
        
        if file_path and os.path.exists(file_path):
             return send_file(file_path, as_attachment=True, download_name=output_filename)
        else:
             return "Error generating music.", 500

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
