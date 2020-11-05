from flask import render_template, current_app as app
from google_auth import CheckLogin

@app.route('/')
@CheckLogin(redirect=True)
def index():

    return render_template('student_list.html')

