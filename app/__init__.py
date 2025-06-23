import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

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
    return render_template('zidanni.html', title="Zidanni Clerigo", url=os.getenv("URL"), nav_items=nav_data)


@app.route('/manav')
def manav():
    nav_data = get_nav_data('manav')
    return render_template('manav.html', title="Manav", url=os.getenv("URL"), nav_items=nav_data)


@app.route('/deeptanshu')
def deeptanshu():
    nav_data = get_nav_data('deeptanshu')
    return render_template('deeptanshu.html', title="Deeptanshu Sankhwar", url=os.getenv("URL"), nav_items=nav_data)


@app.route('/hobbies')
def hobbies():
    nav_data = get_nav_data('hobbies')
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"), nav_items=nav_data)
