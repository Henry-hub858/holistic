from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash
from datetime import datetime
import re


app = Flask(__name__)

application = app
# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hii_website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'a9f8c9a9d7eeb0bc1341a76c95ba9c1e3d97e0a69a3566b85d02ecad874bd7fa'

db = SQLAlchemy(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'henryokumu2018@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'SharonCherono@123#'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'henryokumu2018@gmail.com'  # Replace with your email

mail = Mail(app)

# Chat history for maintaining conversation context
chat_history = {}

# Function to handle hardcoded responses
def get_hardcoded_response(user_input):
    patterns = {
        r"(hello|hi|hey)": "Hello! How can I assist you today?",
        r"(bye|goodbye)": "Goodbye! Have a great day!",
        r"(volunteer|help)": "You can volunteer by filling out the form on our Volunteer page.",
        r"(donate|donation)": "Thank you for your generosity! Visit our Donate page for more details.",
        r"(services|offerings)": "We offer essay writing, proofreading, and research paper services.",
    }

    for pattern, response in patterns.items():
        if re.search(pattern, user_input, re.IGNORECASE):
            return response
    return None

# Function to generate a response using Hugging Face DialoGPT
def get_nlp_response(user_input, user_id):
    global chat_history

    # Encode user input
    
def send_feedback_email(name, email, message):
    subject = f"New Feedback from {name}"
    body = f"""
    You have received new feedback:
    
    Name: {name}
    Email: {email}
    Message: {message}
    """
    msg = Message(subject, recipients=['henryokumu2018@gmail.com'])  # Replace with your email
    msg.body = body
    mail.send(msg)
   
    
# Route for AI-based Chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    user_id = request.json.get("user_id", "default")  # Default ID if no user ID provided

    if not user_message:
        return jsonify({"error": "Message is required!"}), 400

    # Try hardcoded responses first
    hardcoded_response = get_hardcoded_response(user_message)
    if hardcoded_response:
        return jsonify({"response": hardcoded_response})

    # Fallback to Hugging Face model for dynamic NLP-based responses
    try:
        nlp_response = get_nlp_response(user_message, user_id)
        return jsonify({"response": nlp_response})
    except Exception as e:
        print(f"Error with NLP response: {e}")
        return jsonify({"response": "Sorry, I couldn't process your request. Please try again later."})

# Existing Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/program')
def program():
    return render_template('program.html')

@app.route('/events')
def events():
    return render_template('events.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')
@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if not name or not email or not message:
            return render_template('contact.html', error="All fields are required!")

        # Save to database
        contact_message = ContactMessage(name=name, email=email, message=message)
        db.session.add(contact_message)
        db.session.commit()

        return render_template('thank_you.html', message="Thank you for contacting us!")
    return render_template('contact.html')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        donor_name = request.form.get('name')
        donation_amount = request.form.get('donation-amount')
        donation_method = request.form.get('donation-method')

        print(f"Donor Name: {donor_name}")
        print(f"Donation Amount: {donation_amount}")
        print(f"Donation Method: {donation_method}")

        return redirect(url_for('thank_you', donor_name=donor_name, donation_amount=donation_amount))

    return render_template('donate.html')
#

@app.route('/thank-you')
def thank_you():
    donor_name = request.args.get('donor_name')
    donation_amount = request.args.get('donation_amount')

    return render_template('thank_you.html', donor_name=donor_name, donation_amount=donation_amount)

# Database Models
class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    interest = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class NewsletterSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

if __name__ == '__main__':
    app.run(debug=True)
