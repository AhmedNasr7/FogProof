import os
from flask import (
    Flask,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('new 1.html')
@app.route('/home')
def redirect_home():
    return render_template('new 1.html')
@app.route('/stream')
def stream():
    return render_template('new 2.html')
@app.route('/about')
def about():
    return render_template('aboutus.html')
@app.route('/contact')
def contact():
    return render_template('contactus.html')