from flask import Flask, render_template, request, jsonify
from googletrans import Translator, LANGUAGES

app = Flask(__name__)
translator = Translator()

# Define supported languages with their names
SUPPORTED_LANGUAGES = {
    'auto': 'Auto Detect',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'ja': 'Japanese',
    'zh-cn': 'Chinese (Simplified)',
    'ko': 'Korean',
    'ar': 'Arabic',
    'ru': 'Russian',
    'nl': 'Dutch',
    'tr': 'Turkish'
}

@app.route("/", methods=["GET", "POST"])
def index():
    translated_text = ""
    error_message = ""
    source_lang = "en"
    target_lang = "ta"
    input_text = ""
    
    if request.method == "POST":
        try:
            input_text = request.form.get("text", "").strip()
            source_lang = request.form.get("source", "en")
            target_lang = request.form.get("target", "ta")
            
            # Validate input
            if not input_text:
                error_message = "Please enter some text to translate."
            elif source_lang == target_lang and source_lang != 'auto':
                error_message = "Source and target languages cannot be the same."
            else:
                # Perform translation
                if source_lang == 'auto':
                    result = translator.translate(input_text, dest=target_lang)
                else:
                    result = translator.translate(input_text, src=source_lang, dest=target_lang)
                
                translated_text = result.text
                
        except Exception as e:
            error_message = f"Translation failed. Please try again. Error: {str(e)}"
    
    return render_template(
        "index.html", 
        translated_text=translated_text,
        error_message=error_message,
        languages=SUPPORTED_LANGUAGES,
        source_lang=source_lang,
        target_lang=target_lang,
        input_text=input_text
    )

if __name__ == "__main__":
    app.run(debug=True)
