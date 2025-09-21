import os
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, session, url_for
import sqlite3


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def setup_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    # Insert dummy users
    users = [('student1', 'password123'), ('student2', 'password456')]
    for username, password in users:
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        except sqlite3.IntegrityError:
            continue  # Skip if user already exists
    conn.commit()
    conn.close()

setup_db()

import sqlite3

# Connect to SQLite database (this creates the file if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    subscribed_courses TEXT
);
''')

# Insert dummy users
dummy_users = [
    ('john_doe', 'password123', 'Anatomy & Physiology, Nutrition & Healing'),
    ('jane_smith', 'mypassword', 'Islamic Medicine, Pulse Diagnosis'),
    ('alice_williams', 'alicepass', 'Fundamentals of Homeopathy, Nutrition & Healing'),
    ('bob_jones', 'bobpass', 'Anatomy & Physiology, Islamic Medicine'),
]

# Insert users into the database
cursor.executemany('''
INSERT INTO users (username, password, subscribed_courses)
VALUES (?, ?, ?)
''', dummy_users)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Dummy users have been added to the database.")


# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('user_data.db')
    conn.row_factory = sqlite3.Row
    return conn



# Dictionary to store service details
services_data = {
    "chronic-disease": {"title": "Chronic Disease Management", "description": "Homeopathy helps manage chronic diseases like arthritis, asthma, and hypertension by addressing the root cause."},
    "migraine-headache": {"title": "Migraine & Headache Relief", "description": "Get relief from migraines and chronic headaches with our holistic homeopathic approach."},
    "allergy-asthma": {"title": "Allergy & Asthma Treatment", "description": "Effective remedies to treat asthma and allergies without side effects."},
    "arthritis-joint": {"title": "Arthritis & Joint Pain Treatment", "description": "Natural pain relief and long-term joint health support using homeopathy."},
    # Add all 40 services in the same format
}

# Path where articles are stored
ARTICLE_FOLDER = "articles"

@app.route('/')
def home():
    articles = [
        {"title": "Homeopathy and Immunity", "description": "How homeopathy boosts the immune system."},
        {"title": "Natural Remedies for Stress", "description": "Learn how homeopathy helps with stress relief."},
        {"title": "Homeopathy for Chronic Diseases", "description": "An effective approach for long-term health issues."}
    ]
    return render_template('index.html', articles=articles)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/marifa')
def marifa_home():
    return render_template('marifa_home.html')  # The Marifa University homepage

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect to home if not logged in

    # Get user data
    user_id = session['user_id']
    username = session['username']
    subscribed_courses = session['subscribed_courses'].split(',')

    # Fetch course details based on subscribed courses
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses WHERE id IN ({})'.format(','.join('?' for _ in subscribed_courses)), subscribed_courses).fetchall()
    conn.close()

    return render_template('dashboard.html', username=username, courses=courses)

@app.route('/marifa/anatomy')
def anatomy_course():
    return render_template('courses/anatomy.html')

@app.route('/marifa/homeopathy')
def homeopathy_course():
    return render_template('courses/homeopathy.html')

@app.route('/marifa/nutrition')
def nutrition_course():
    return render_template('courses/nutrition.html')

@app.route('/marifa/islamic-medicine')
def islamic_medicine_course():
    return render_template('courses/islamic_medicine.html')

@app.route('/marifa/pulse')
def pulse_diagnosis_course():
    return render_template('courses/pulse.html')

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

@app.route('/offline')
def offline():
    return render_template('offline.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    services_list = [
        {"name": "Chronic Disease Management", "short_desc": "Natural remedies for long-term health issues.", "long_desc": "Homeopathy helps manage chronic conditions like diabetes, arthritis, and asthma with minimal side effects.", "icon": "chronic.png"},
        {"name": "Skin & Hair Treatments", "short_desc": "Solutions for acne, hair loss, and skin disorders.", "long_desc": "Gentle yet effective treatments for eczema, dandruff, psoriasis, and hair fall.", "icon": "skin.png"},
        {"name": "Allergy & Asthma Relief", "short_desc": "Holistic approach to respiratory health.", "long_desc": "Homeopathy can significantly reduce symptoms of allergies and asthma by boosting immunity.", "icon": "asthma.png"},
        # Add more services here...
    ]
    return render_template('services.html', services=services_list)

@app.route('/service/<service_id>')
def service_detail(service_id):
    service = services_data.get(service_id)
    if service:
        return render_template('service_detail.html', service=service)
    else:
        return "Service Not Found", 404



@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/internship')
def internship():
    return render_template('internship.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

# Dummy data for articles (replace with database later)
articles = [
    {"title": "The Benefits of Homeopathy", "filename": "benefits-homeopathy", "image": "homeopathy.jpg", "preview": "Homeopathy is a holistic approach..."},
    {"title": "How Homeopathy Works", "filename": "how-homeopathy-works", "image": "how-homeopathy.jpg", "preview": "Homeopathy uses natural remedies..."},
    {"title": "Common Homeopathic Remedies", "filename": "common-remedies", "image": "remedies.jpg", "preview": "Here are some effective homeopathic remedies..."}
]

@app.route('/knowledge')
def knowledge():
    return render_template('knowledge.html', articles=articles)

@app.route("/articles/<article_name>")
def article_page(article_name):
    try:
        return render_template(f"articles/{article_name}.html")
    except:
        return "Article Not Found", 404


@app.route('/consultation')
def consultation():
    return render_template('consultation.html')
    

if __name__ == '__main__':
    app.run(debug=True)

# Project Structure:
# QaisarClinic/
# │── templates/                # HTML files (Flask templates)
# │   ├── base.html             # Common layout for all pages
# │   ├── index.html            # Home Page
# │   ├── about.html            # About Us
# │   ├── services.html         # Services
# │   ├── staff.html            # Staff
# │   ├── internship.html       # Internship
# │   ├── blogs.html            # Blog Page
# │   ├── knowledge.html        # Knowledge Page
# │   ├── consultation.html     # "Coming Soon" page
# │
# │── static/                   # Static files
# │   ├── css/
# │   │   ├── style.css         # Main stylesheet
# │   ├── js/
# │   │   ├── script.js         # JavaScript for animations
# │   ├── images/               # All website images
# │   │   ├── logo.png          # Clinic Logo
# │
# │── app.py                    # Flask backend
# │── README.md                 # Project documentation
