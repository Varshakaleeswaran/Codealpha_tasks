# CampusBot - FAQ Chatbot Project

## Overview
CampusBot is an intelligent, conversational FAQ chatbot designed to help students with common queries about university life, academics, and administration. It uses Natural Language Processing (NLTK) and Machine Learning (TF-IDF + Cosine Similarity) to understand questions and provide accurate answers.

## Features
- 🤖 **Conversational AI**: Understands greetings, pleasantries ("thank you"), and requests for help.
- 📚 **University Knowledge Base**: Answers questions about courses, exams, fees, hostels, and more.
- 🔍 **Smart Matching**: Uses TF-IDF vectorization to match queries even if phrased differently.
- 💻 **Web Interface**: Modern, responsive chat UI with typing indicators and confidence scores.
- ⚡ **Quick Questions**: One-click suggestions to get started easily.

## Technologies Used
- **Language**: Python 3.x
- **Web Framework**: Flask
- **NLP**: NLTK (Natural Language Toolkit)
- **ML**: scikit-learn (TF-IDF, Cosine Similarity)
- **Frontend**: HTML5, CSS3, JavaScript

## Installation

1.  **Clone or Open the Project**
    Ensure you are in the project directory:
    ```bash
    cd campus-faq-chatbot
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

3.  **Download NLTK Data**
    Run the following python commands:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    ```

## Usage

### Web Interface (Recommended)
1.  Run the Flask application:
    ```bash
    python app.py
    ```
2.  Open your browser and navigate to:
    `http://127.0.0.1:5000`

### Console Version
To test the chatbot logic directly in the terminal:
```bash
python chatbot.py
```

## Project Structure
- `app.py`: The Flask web server.
- `chatbot.py`: Core logic class `CampusBot`.
- `faqs.json`: The database of Questions and Answers.
- `templates/index.html`: The frontend user interface.
- `requirements.txt`: List of python dependencies.

## Key Files Explained
- **`chatbot.py`**: Handles text preprocessing (tokenization, lemmatization), vectorization, and managing state (greetings vs. FAQ lookup).
- **`faqs.json`**: Make sure strictly valid JSON format is used here.

## Author
[Your Name]
