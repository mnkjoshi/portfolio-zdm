import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
from jinja2 import Environment, PackageLoader, select_autoescape
import datetime
import re
from playhouse.shortcuts import model_to_dict
from app.timeline import timeline_bp

# Initialize Jinja2 environment

env = Environment(
    loader=PackageLoader("app", "templates"),
    autoescape=select_autoescape()
)

load_dotenv()
app = Flask(__name__)

# print("ENV VARS:", dict(os.environ))  # Add this line temporarily


if os.getenv("TESTING") == "true":
    print("Running in Test Mode.")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared')
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        port=3306
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb
        
mydb.connect()
mydb.create_tables([TimelinePost])


NAV_ITEMS = [
    {'name': 'Zidanni', 'url': '/', 'route': 'index'},
    {'name': 'Manav', 'url': '/manav', 'route': 'manav'},
    {'name': 'Deeptanshu', 'url': '/deeptanshu', 'route': 'deeptanshu'},
    {'name': 'Hobbies', 'url': '/hobbies', 'route': 'hobbies'},
    {'name': 'Timeline', 'url': '/timeline', 'route': 'timeline'}
]

def get_nav_data(current_route):
    nav_data = []
    for item in NAV_ITEMS:
        nav_item = item.copy()
        nav_item['is_current'] = (item['route'] == current_route)
        nav_data.append(nav_item)
    return nav_data


@app.route('/')
def index():
    nav_data = get_nav_data('index')
    
    EXPERIENCE = [
        {'company': 'Independent', 'title': 'Software Developer', 'date': 'September 2024 – Present'},
        {'company': 'Elmhurst Care Center Nursing Home', 'title': 'Software Developer', 'date': 'July 2022 – August 2023'},
        {'company': 'NYU Tandon School of Engineering', 'title': 'Researcher and Game Developer', 'date': 'April 2022 – June 2024'},
    ]

    EDUCATION = [
        {'school': 'Stevens Institute of Technology', 'title': 'Bachelor of Science in Computer Science'},
    ]
    
    return render_template('profile.html', title="Zidanni Clerigo", url=os.getenv("URL"), map="./static/img/zidanni-map.jpg",  nav_items=nav_data, profile_picture="./static/img/zidanni.jpg", education=EDUCATION, experience=EXPERIENCE, about_me_text="Hello! I'm Zidanni Clerigo, an incoming second year Computer Science student at Stevens Institute of Technology. I'm super passionate about building projects and pitching them to other people! Deployment and maintenance has always been a roadblock for me so I'm very excited to be in the Production Engineering track.")


@app.route('/manav')
def manav():
    nav_data = get_nav_data('manav')
    template = env.get_template("profile.html")

    EXPERIENCE = [
        {'company': 'CN', 'title': 'Operational Technology Intern', 'date': 'May 2024 - Aug 2024'},
        {'company': 'Jam', 'title': 'Full Stack Developer Intern', 'date': 'Dec 2023 - Feb 2024'},
        {'company': 'University of Alberta', 'title': 'Research Assistant', 'date': 'May 2023 - Aug 2023'},
    ]

    EDUCATION = [
        {'school': 'University of Alberta', 'title': 'Electrical Engineering'},
        {'school': 'Old Scona Academic', 'title': 'International Baccalaureate Diploma'},
    ]
    # Render the template with the provided data
    return template.render(title="Manav", url=os.getenv("URL"), nav_items=nav_data, profile_picture="./static/img/manav.jpg", education=EDUCATION, experience=EXPERIENCE, map="./static/img/manav-map.png", about_me_text="Hi there! I'm Manav, a third-year Electrical Engineering student at the University of Alberta. Planning, building, and deploying projects has been a pursuit of mine for a long time, and I'm excited to be part of the Production Engineering track. I love working on projects that involve hardware and software integration, and I'm always looking for new challenges to tackle.")

    # return render_template('manav.html', title="Manav", url=os.getenv("URL"), nav_items=nav_data)


@app.route('/deeptanshu')
def deeptanshu():
    nav_data = get_nav_data('deeptanshu')
    return render_template('deeptanshu.html', title="Deeptanshu Sankhwar", url=os.getenv("URL"), nav_items=nav_data)


@app.route('/hobbies')
def hobbies():
    nav_data = get_nav_data('hobbies')
    
    # Manav's hobbies
    MANAV_HOBBIES = [
        {'title': 'Sports', 'about': 'I enjoy playing sports in my free time, from Soccer to Badminton!', 'icon': 'https://cdn-icons-png.flaticon.com/512/11438/11438126.png'},
        {'title': 'Gaming', 'about': 'Video games can be fun! You can sometimes catch me playing games from Paradox Studios or Rocket League!', 'icon': 'https://cdn-icons-png.flaticon.com/512/5260/5260498.png'},
        {'title': 'Movies & TV', 'about': 'I love a good movie or show! One of my favourite shows is Succession!', 'icon': 'https://thumbs.dreamstime.com/b/big-open-clapper-board-movie-reel-cinema-icon-set-movie-film-elements-flat-design-cinema-movie-time-flat-icons-f-95500226.jpg'},
    ]
    
    # Zidanni's hobbies
    ZIDANNI_HOBBIES = [
    ]
    
    # Deeptanshu's hobbies
    DEEPTANSHU_HOBBIES = [
    ]

    about_text = "We all have various hobbies and interests that help us recharge and grow outside of our professional lives. Here's a glimpse into what we enjoy doing in our free time."
    
    return render_template('hobbies.html', 
                          title="Our Hobbies", 
                          url=os.getenv("URL"), 
                          nav_items=nav_data, 
                          manav_hobbies=MANAV_HOBBIES,
                          zidanni_hobbies=ZIDANNI_HOBBIES,
                          deeptanshu_hobbies=DEEPTANSHU_HOBBIES,
                          about_me_text=about_text)


@app.route('/timeline')
def timeline():
    nav_data = get_nav_data('timeline')
    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"), nav_items=nav_data)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            name = data.get('name', '')
            email = data.get('email', '')
            content = data.get('content', '')
        else:
            name = request.form.get('name', '')
            email = request.form.get('email', '')
            content = request.form.get('content', '')
        
        # Validate Name
        if not name:
            return "Invalid name", 400
        
        # Validate Content
        if not content:
            return "Invalid content", 400

        # Validate Email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not re.match(email_pattern, email):
            return "Invalid email", 400
            
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return jsonify(model_to_dict(timeline_post))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    try:
        post = TimelinePost.get_by_id(post_id)
        post.delete_instance()
        return {'message': f'Post {post_id} deleted successfully.'}
    except TimelinePost.DoesNotExist:
        return {'error': 'Post not found'}, 404
    

def create_app():
    app.register_blueprint(timeline_bp)