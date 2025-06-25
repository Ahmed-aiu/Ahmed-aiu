# global imports
from flask import Blueprint, render_template, session, redirect, url_for, current_app
from static.py import get_flask_folders
from static.py.decorators import inject_config, check_login_and_rights, track_time

template_folder, static_folder, static_url_path = get_flask_folders.get(file=__file__)

# Initalize Blueprint
engineering_bp = Blueprint(
                                'engineering_bp',
                                __name__,
                                template_folder=template_folder,
                                static_folder=static_folder,
                                static_url_path=static_url_path
                                )

@engineering_bp.route("/engineering")
@check_login_and_rights()
@track_time()
@inject_config(['auth'])
def engineering(auth):
        return render_template('engineering.html', login=session['loggedin'])
