
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import random

class CampusBot:
    def __init__(self, faq_file):
        """Initialize CampusBot with FAQ data"""
        print("Initializing CampusBot...")
        
        # Load FAQs
        self.faqs = self.load_faqs(faq_file)
        self.questions = [faq['question'] for faq in self.faqs]
        self.answers = [faq['answer'] for faq in self.faqs]
        
        # Initialize NLP tools
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Preprocess all FAQ questions
        print("Preprocessing FAQ questions...")
        self.processed_questions = [self.preprocess_text(q) for q in self.questions]
        
        # Create TF-IDF vectorizer
        print("Creating TF-IDF vectors...")
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.processed_questions)
        
        # Conversational patterns
        self.greeting_patterns = [
            'hi', 'hello', 'hey', 'hii', 'hiii', 'helloo', 'hola', 
            'good morning', 'good afternoon', 'good evening', 'greetings',
            'sup', 'whats up', "what's up", 'yo', 'hiya'
        ]
        
        self.how_are_you_patterns = [
            'how are you', 'how r you', 'how are u', 'how r u',
            'how do you do', 'how are you doing', 'hows it going',
            "how's it going", 'how you doing', 'whats up', "what's up",
            'how have you been', 'how u doing'
        ]
        
        self.help_patterns = [
            'help', 'help me', 'can you help', 'i need help',
            'what can you do', 'what do you do', 'how can you help',
            'what are you', 'who are you', 'tell me about yourself'
        ]
        
        self.thanks_patterns = [
            'thank you', 'thanks', 'thank u', 'thanku', 'thnx', 'thnks',
            'appreciate it', 'thanks a lot', 'thank you so much',
            'thx', 'ty', 'tysm'
        ]
        
        self.bye_patterns = [
            'bye', 'goodbye', 'see you', 'see ya', 'later',
            'catch you later', 'gotta go', 'talk to you later',
            'ttyl', 'take care', 'peace out'
        ]
        
        print("CampusBot is ready!\n")
    
    def load_faqs(self, filename):
        """Load FAQs from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                faqs = json.load(file)
                print(f"Loaded {len(faqs)} FAQs")
                return faqs
        except FileNotFoundError:
            print(f"Error: {filename} not found!")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {filename}")
            return []
    
    def preprocess_text(self, text):
        """
        Preprocess text using NLP techniques:
        1. Lowercase conversion
        2. Tokenization
        3. Remove punctuation
        4. Remove stop words
        5. Lemmatization
        """
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize (split into words)
        tokens = word_tokenize(text)
        
        # Remove punctuation, stop words, and lemmatize
        processed_tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in string.punctuation and token not in self.stop_words
        ]
        
        # Join tokens back into string
        return ' '.join(processed_tokens)
    
    def check_greeting(self, text):
        """Check if user message is a greeting"""
        text_lower = text.lower().strip()
        for pattern in self.greeting_patterns:
            if pattern in text_lower:
                return True
        return False
    
    def check_how_are_you(self, text):
        """Check if user is asking how are you"""
        text_lower = text.lower().strip()
        for pattern in self.how_are_you_patterns:
            if pattern in text_lower:
                return True
        return False
    
    def check_help(self, text):
        """Check if user is asking for help"""
        text_lower = text.lower().strip()
        for pattern in self.help_patterns:
            if pattern in text_lower:
                return True
        return False
    
    def check_thanks(self, text):
        """Check if user is saying thanks"""
        text_lower = text.lower().strip()
        for pattern in self.thanks_patterns:
            if pattern in text_lower:
                return True
        return False
    
    def check_bye(self, text):
        """Check if user is saying goodbye"""
        text_lower = text.lower().strip()
        for pattern in self.bye_patterns:
            if pattern in text_lower:
                return True
        return False
    
    def get_greeting_response(self):
        """Generate greeting response"""
        responses = [
            "Hello! 👋 Welcome to CampusBot! How can I help you today?",
            "Hi there! 😊 I'm here to assist you with any questions about college. What would you like to know?",
            "Hey! 🎓 Great to see you! Feel free to ask me anything about campus life, courses, or facilities.",
            "Hello! I'm CampusBot, your friendly campus assistant. What can I help you with today?",
            "Hi! 👋 Nice to meet you! I'm here to answer your questions about college. How can I assist you?"
        ]
        return random.choice(responses)
    
    def get_how_are_you_response(self):
        """Generate response to 'how are you'"""
        responses = [
            "I'm doing great, thank you for asking! 😊 I'm here and ready to help you with any college-related questions. What would you like to know?",
            "I'm wonderful, thanks! 🤖 Always excited to help students like you. How can I assist you today?",
            "I'm doing fantastic! Thanks for asking. 😊 Now, how can I help you with your queries?",
            "I'm great! 🎓 Working hard to help students like you. What information do you need today?",
            "Doing really well, thank you! 😊 More importantly, how can I help YOU today?"
        ]
        return random.choice(responses)
    
    def get_help_response(self):
        """Generate help response"""
        return """I'm CampusBot, your student information assistant! 🎓 I can help you with:

📚 **Academics**: Course registration, exam schedules, results, attendance policies
🏛️ **Facilities**: Library timings, WiFi access, campus locations
💰 **Finance**: Fee structure, scholarship applications, payment methods
🏠 **Hostel**: Room facilities, mess charges, hostel rules
📄 **Administration**: ID cards, certificates, NOC, leave applications
🎯 **Student Life**: Clubs, activities, dress code, campus events

Just ask me anything! For example:
- "How do I register for courses?"
- "What are the hostel fees?"
- "Where is the library?"
- "How to check my results?"

What would you like to know? 😊"""
    
    def get_thanks_response(self):
        """Generate thanks response"""
        responses = [
            "You're very welcome! 😊 Happy to help! If you have any other questions, feel free to ask anytime.",
            "No problem at all! 🎓 That's what I'm here for. Don't hesitate to reach out if you need anything else!",
            "Glad I could help! 😊 If you think of any other questions, I'm always here for you.",
            "You're welcome! 👋 Remember, I'm available 24/7 for any college-related queries. Have a great day!",
            "My pleasure! 😊 Feel free to come back anytime you need assistance. Good luck with your studies!"
        ]
        return random.choice(responses)
    
    def get_bye_response(self):
        """Generate goodbye response"""
        responses = [
            "Goodbye! 👋 Have a great day! Come back anytime you need help.",
            "See you later! 🎓 Best of luck with your studies. Feel free to return anytime!",
            "Take care! 😊 Don't hesitate to reach out if you need anything. Have a wonderful day!",
            "Bye! 👋 Stay awesome and ace those exams! I'll be here whenever you need me.",
            "Farewell! 🎓 Wishing you all the best. Come back anytime for help!"
        ]
        return random.choice(responses)
    
    def get_response(self, user_question, threshold=0.2):
        """
        Get the best matching answer for user's question
        Handles both conversational queries and FAQ matching
        """
        if not user_question.strip():
            return {
                'answer': "I didn't catch that. Could you please ask me something? 😊",
                'confidence': 0.0,
                'matched_question': None,
                'type': 'empty'
            }
        
        # Check for conversational patterns
        if self.check_greeting(user_question):
            return {
                'answer': self.get_greeting_response(),
                'confidence': 1.0,
                'matched_question': None,
                'type': 'greeting'
            }
        
        if self.check_how_are_you(user_question):
            return {
                'answer': self.get_how_are_you_response(),
                'confidence': 1.0,
                'matched_question': None,
                'type': 'how_are_you'
            }
        
        if self.check_help(user_question):
            return {
                'answer': self.get_help_response(),
                'confidence': 1.0,
                'matched_question': None,
                'type': 'help'
            }
        
        if self.check_thanks(user_question):
            return {
                'answer': self.get_thanks_response(),
                'confidence': 1.0,
                'matched_question': None,
                'type': 'thanks'
            }
        
        if self.check_bye(user_question):
            return {
                'answer': self.get_bye_response(),
                'confidence': 1.0,
                'matched_question': None,
                'type': 'bye'
            }
        
        # Preprocess user's question for FAQ matching
        processed_question = self.preprocess_text(user_question)
        
        # Convert to TF-IDF vector
        user_vector = self.vectorizer.transform([processed_question])
        
        # Calculate similarity with all FAQ questions
        similarities = cosine_similarity(user_vector, self.tfidf_matrix)[0]
        
        # Find best match
        best_match_idx = similarities.argmax()
        best_similarity = similarities[best_match_idx]
        
        # Return answer if similarity is above threshold
        if best_similarity > threshold:
            # Add conversational prefix to make it more natural
            prefixes = [
                "Great question! ",
                "I can help you with that! ",
                "Sure, let me explain. ",
                "Here's what you need to know: ",
                "I'm happy to help! ",
                "Let me answer that for you. "
            ]
            prefix = random.choice(prefixes)
            
            return {
                'answer': prefix + self.answers[best_match_idx],
                'confidence': float(best_similarity),
                'matched_question': self.questions[best_match_idx],
                'type': 'faq'
            }
        else:
            return {
                'answer': "Hmm, I'm not sure I have information about that specific question. 🤔 Could you try rephrasing it? Or you can contact the Administration Office for detailed assistance. You can also ask me things like 'What can you help me with?' to see what topics I cover! 😊",
                'confidence': 0.0,
                'matched_question': None,
                'type': 'no_match'
            }
    
    def chat(self):
        """Console-based chat interface"""
        print("\n" + "="*60)
        print("🎓 CAMPUSBOT - Your Student Information Assistant")
        print("="*60)
        print("Chat naturally with me! Type 'quit' to exit.")
        print("="*60 + "\n")
        
        # Initial greeting
        print("CampusBot: Hello! I'm CampusBot, your friendly campus assistant.")
        print("              Feel free to ask me anything about college!\n")
        
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"\nCampusBot: {self.get_bye_response()}\n")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Get response
            result = self.get_response(user_input)
            
            # Display response
            print(f"\nCampusBot: {result['answer']}")
            
            if result['confidence'] > 0 and result['type'] == 'faq':
                print(f"\n   Related FAQ: '{result['matched_question']}'")
                print(f"   Confidence: {result['confidence']:.2%}")
            
            print("\n" + "-"*60 + "\n")

# Main execution
if __name__ == "__main__":
    # Create chatbot instance
    bot = CampusBot('faqs.json')
    
    # Start chat
    bot.chat()
