# 🌍 Language Translator

A beautiful and intuitive web-based language translation tool built with Flask and Google Translate API. Translate text between multiple languages with features like auto-detection, text-to-speech, and copy functionality.

## ✨ Features

- **Multi-Language Support**: Translate between 15+ languages including English, Spanish, French, German, Hindi, Tamil, Japanese, Chinese, Korean, Arabic, Russian, Portuguese, Italian, and more
- **Auto-Detect Language**: Automatically detect the source language
- **Text-to-Speech**: Listen to translations with built-in speech synthesis
- **Copy to Clipboard**: Easily copy translated text with one click
- **Swap Languages**: Quickly swap source and target languages
- **Character Counter**: Track input text length in real-time
- **Responsive Design**: Beautiful, modern UI that works on all devices
- **Premium Aesthetics**: Glassmorphism effects, smooth animations, and gradient backgrounds

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd codealpha_language_translator
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

1. **Run the application**
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. **Start translating!**
   - Enter your text in the input area
   - Select source language (or use Auto Detect)
   - Select target language
   - Click "Translate"
   - Use Copy or Speak buttons for additional features

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Translation API**: Google Translate (googletrans library)
- **Frontend**: HTML5, CSS3, JavaScript
- **Design**: Modern UI with glassmorphism and gradient effects
- **Fonts**: Google Fonts (Poppins)

## 📁 Project Structure

```
codealpha_language_translator/
│
├── app.py                 # Flask application backend
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
│
├── templates/
│   └── index.html        # Main HTML template
│
├── static/
│   └── style.css         # Stylesheet with premium design
│
└── venv/                 # Virtual environment (not in git)
```

## 🎨 Features in Detail

### Supported Languages
- English, Spanish, French, German, Italian, Portuguese
- Hindi, Tamil, Japanese, Chinese (Simplified), Korean
- Arabic, Russian, Dutch, Turkish

### Interactive Features
- **Real-time character counting**: See how long your text is
- **Language swap**: Quickly reverse translation direction
- **Loading states**: Visual feedback during translation
- **Error handling**: Graceful error messages for failed translations
- **Responsive layout**: Works perfectly on desktop, tablet, and mobile

## 🔮 Future Enhancements

- Translation history
- Multiple translation engine support
- Offline mode with cached translations
- File upload for document translation
- API endpoint for programmatic access
- User accounts and saved preferences

## 📝 License

This project is created as part of CodeAlpha internship tasks.

## 👤 Author

Varsha Kaleeswaran

## 🙏 Acknowledgments

- Google Translate API for translation services
- Flask framework for the web application
- CodeAlpha for the internship opportunity

---

**Enjoy translating! 🌐**
