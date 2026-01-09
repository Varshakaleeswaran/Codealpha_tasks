
from flask import Flask, render_template, request, jsonify
from chatbot import CampusBot
import os

app = Flask(__name__)

# Initialize CampusBot
print("Starting CampusBot Web Server...")
bot = CampusBot('faqs.json')

@app.route('/')
def home():
    """Render the chat interface"""
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    """API endpoint to get chatbot response"""
    try:
        # Get user message from request
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'response': 'Please enter a question.',
                'confidence': 0.0,
                'matched_question': None
            })
        
        # Get chatbot response
        result = bot.get_response(user_message)
        
        return jsonify({
            'response': result['answer'],
            'confidence': result['confidence'],
            'matched_question': result['matched_question']
        })
    
    except Exception as e:
        return jsonify({
            'response': f'Sorry, something went wrong: {str(e)}',
            'confidence': 0.0,
            'matched_question': None
        }), 500

@app.route('/faqs')
def get_all_faqs():
    """API endpoint to get all FAQs"""
    return jsonify(bot.faqs)

@app.route('/stats')
def get_stats():
    """Get chatbot statistics"""
    return jsonify({
        'total_faqs': len(bot.faqs),
        'categories': ['Academics', 'Administration', 'Facilities', 'Student Life']
    })

if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000")
    print("Open this URL in your browser")
    app.run(debug=True, port=5000)
