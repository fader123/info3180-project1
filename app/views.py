"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
from models import UserProfile
from werkzeug.security import check_password_hash
from forms import MyForm
from werkzeug.utils import secure_filename
import os, datetime
###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    

@app.route('/profile', methods=['POST','GET'])
def profile():
    form = MyForm()
    print form.validate_on_submit()
    print form.errors
    print request.form
    if request.method=='POST' and form.validate_on_submit():
        count = db.session.query(UserProfile).count()
        location=form.location.data
        bio=form.biography.data
        lname=form.lastname.data
        fname=form.firstname.data
        mail=form.email.data
        gender=form.gender.data
        photograph = form.photo.data
        date = datetime.date.today()
        uid = 10000 + count
        filename = str(uid)+".jpg"
        photograph.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user = UserProfile(id= uid,first_name=fname, last_name = lname,gender=gender,location=location,bio= bio,email=mail,created_on=date)
        db.session.add(user)
        db.session.commit()
        flash('Profile created!', 'success')
        return redirect(url_for('profiles'))
    else:
        return render_template('profile.html', form = form)
        

@app.route('/profiles', methods=['POST','GET'])
def profiles():
    users = db.session.query(UserProfile).all()
    if request.method == 'GET':
        return  render_template('profiles.html', users = users)
    elif request.method == "POST" and request.headers['Content-Type'] == "application/json":
        users_list = []
        for user in users:
            users_list += [{"username": user.first_name+user.get_id, "userid":user.get_id}]
        user_json = {"users":users_list}
        return jsonify(user_json)
    else:
        flash("Unable to get request")
        return redirect(url_for('home'))
        

@app.route('/userprofile/<userid>')
def user(userid):
    user = UserProfile.query.filter_by(id = userid ).first()
    if request.method=='GET':
        return render_template('userprofile.html', user =user )
    elif request.method == "POST" and request.headers['Content-Type'] == "application/json":
        user_json = {}
        user_json["userid"] = user.id
        user_json["username"] = user.first_name + user.last_name
        user_json["image"] = user.id + '.jpg'
        user_json["gender"] = user.gender
        user_json["age"] = user.age
        user_json["profile_created_on"] = user.date
        return jsonify(user_json)
    return render_template('userprofile.html')
    


    



# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
