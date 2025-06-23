import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from jinja2 import Environment, PackageLoader, select_autoescape

# Initialize Jinja2 environment

env = Environment(
    loader=PackageLoader("app", "templates"),
    autoescape=select_autoescape()
)

load_dotenv()
app = Flask(__name__)

NAV_ITEMS = [
    {'name': 'Zidanni', 'url': '/', 'route': 'index'},
    {'name': 'Manav', 'url': '/manav', 'route': 'manav'},
    {'name': 'Deeptanshu', 'url': '/deeptanshu', 'route': 'deeptanshu'},
    {'name': 'Hobbies', 'url': '/hobbies', 'route': 'hobbies'}
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
        {'title': 'Coding', 'about': 'I love to build applications and websites in my free time!', 'icon': 'https://cdn-icons-png.flaticon.com/512/1005/1005141.png'},
        {'title': 'Reading', 'about': 'I enjoy reading books on technology and science fiction.', 'icon': 'https://cdn-icons-png.flaticon.com/512/2436/2436882.png'},
        {'title': 'Photography', 'about': 'Capturing moments and scenery through photography is one of my passions.', 'icon': 'https://cdn-icons-png.flaticon.com/512/1042/1042390.png'},
    ]
    
    # Deeptanshu's hobbies
    DEEPTANSHU_HOBBIES = [
        {'title': 'Open Source', 'about': 'I actively contribute to open source projects in my free time.', 'icon': 'https://cdn-icons-png.flaticon.com/512/2111/2111432.png'},
        {'title': 'Hiking', 'about': 'I enjoy exploring nature and going on hikes in Colorado.', 'icon': 'https://cdn-icons-png.flaticon.com/512/71/71423.png'},
        {'title': 'Coding', 'about': 'I enjoy working with Go, TypeScript, and Python to build scalable systems.', 'icon': 'https://cdn-icons-png.flaticon.com/512/6132/6132221.png'},
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
