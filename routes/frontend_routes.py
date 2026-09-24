from flask import Blueprint, render_template, send_from_directory
import os
from config.config import Config

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    return render_template('index.html')

@frontend_bp.route('/login')
def login():
    return render_template('login.html')

@frontend_bp.route('/register')
def register():
    return render_template('register.html')

@frontend_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@frontend_bp.route('/report-lost')
def report_lost():
    return render_template('report-lost.html')

@frontend_bp.route('/report-found')
def report_found():
    return render_template('report-found.html')

@frontend_bp.route('/browse')
def browse():
    return render_template('browse.html')

@frontend_bp.route('/item/<id>')
def item_details(id):
    return render_template('item-details.html', item_id=id)

@frontend_bp.route('/matches')
def matches():
    return render_template('matches.html')

@frontend_bp.route('/profile')
def profile():
    return render_template('profile.html')

@frontend_bp.route('/uploads/<type>/<filename>')
def uploaded_file(type, filename):
    if type not in ['lost', 'found']:
        return "Invalid type", 400
    folder_path = os.path.join(Config.UPLOAD_FOLDER, type)
    return send_from_directory(folder_path, filename)
