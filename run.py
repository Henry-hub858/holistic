from flask import Flask, render_template

app = Flask(__name__)

# Route for Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Route for About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for Program Page (Latest Causes)
@app.route('/program')
def program():
    return render_template('program.html')

# Route for Events Page (Social Events)
@app.route('/events')
def events():
    return render_template('events.html')

# Route for Blog Page
@app.route('/blog')
def blog():
    return render_template('blog.html')

# Submenu: Blog Details Page
@app.route('/blog_details')
def blog_details():
    return render_template('blog_details.html')

# Submenu: Elements Page
@app.route('/elements')
def elements():
    return render_template('elements.html')

# Route for Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
