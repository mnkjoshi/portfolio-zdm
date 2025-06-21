import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('zidanni.html', title="Zidanni Clerigo", url=os.getenv("URL"))


@app.route('/manav')
def page2():
    return render_template('manav.html', title="Manav", url=os.getenv("URL"))


@app.route('/deeptanshu')
def page3():
    return render_template('deeptanshu.html', title="Deeptanshu Sankhwar", url=os.getenv("URL"))


@app.route('/hobbies')
def page4():
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))
