from flask import Flask, render_template, request, g, redirect, url_for, jsonify, abort, session
from urllib.parse import urlencode
import os
import db
from auth0 import auth0_setup, require_auth, auth0
from datetime import datetime
from queryResults import *
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'animalwatch2021@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ["MAIL_PASSWORD"] # must be added to .env file
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# have the DB submodule set itself up before we get started. groovy.
@app.before_first_request
def initialize():
    db.setup()
    auth0_setup()

@app.route('/')
def page_landing():
    return render_template("main.html")

@app.route('/signup')
def page_signup():
    return render_template("signup.html")

### AUTH0:
@app.route('/login')
def page_login():
    if 'profile' in session:
        return redirect(url_for('logout'))
    else:
        return auth0().authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/logout')
def logout():
    session.clear()
    params = { 'returnTo': url_for('page_landing', _external=True), 'client_id': os.environ['AUTH0_CLIENT_ID'] }
    return redirect(auth0().api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/callback')
def callback():
    auth0().authorize_access_token()
    resp = auth0().get('userinfo')
    userinfo = resp.json()
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    with db.get_db_cursor(commit=True) as cur:
        users_id = session['profile']['user_id']
        users_name = session['profile']['name']
        cur.execute("Select COUNT(*) FROM Users WHERE id = '%s';" % users_id)
        try:
            for record in cur:
                if record[0] == 0:
                    cur.execute("insert into Users (id, users_name) values (%s, %s);", (users_id, users_name))
        except:
            pass
    return redirect('/test_auth')
    
@app.route('/test_auth')
@require_auth
def test_auth():
    return render_template("main.html", profile=session['profile'])



@app.route('/add')
@require_auth
def page_add_animal():
    return render_template("addAnimal.html")


@app.route('/add', methods=['POST'])
def processAddAnimal():
    with db.get_db_cursor(commit=True) as cur:
        users_id = session['profile']['user_id'] 
        #users_id = 1 #TESTING TESTING TESTING - DON'T DEPLOY THIS
        species = request.form.get("species")
        endangerment_level = request.form.get("classification")
        
        animal_range = request.form.get("range")
        #latitude =
        #longitude =
        # Get image from the form
        #with open(request.form.get("image"), "rb") as image:
            # Encode image data into a string
         #   post_image = base64.b64encode(image.read())
          #  console.logger.info(post_image)
        imageURL = request.form.get("imageURL") #TODO: fix the image back-end
        animal_description = request.form.get("description")
        #post_time = str(datetime.now()) #Removed-this is not part of animal page right now
        cur.execute("insert into Animals (species, endangerment_level, animal_range, imageURL, animal_description) values (%s, %s, %s, %s, %s);", (species, endangerment_level, animal_range, imageURL, animal_description))
        
        ###THE NEXT LINE IS HOT GARBAGE FOR TESTING PURPOSES
        #cur.execute("insert into Posts (users_id, animal_id, post_text, imageURL, post_time, latitude, longitude) values (%s, %s, %s, %s, %s, %s, %s);", (users_id, 11, animal_description, imageURL, post_time, 1, 1))
        ###THE PREVIOUS LINE IS HOT GARBAGE FOR TESTING PURPOSES

        #cur.execute("insert into Locations (user_id, animal_id, lat, long) values (%s, %s, %s, %s);" (user_id, animal_id, lat, long))
        return redirect(url_for("page_feed"))

@app.route('/feed', methods=['GET'])
def page_feed():
    with db.get_db_cursor(False) as cur:
        return render_template("feed.html", dataList=getActivityFeed(cur))

@app.route('/animal/<int:animal_id>', methods=['GET'])
def page_lookup(animal_id):
    with db.get_db_cursor(False) as cur:
        # shared contents
        shared_data = getSharedContentsByAnimalId(cur, animal_id)
        
        if (len(shared_data) == 1):
            postList    = getAllPostsByAnimalId(cur, animal_id)
            commentList = getAllCommentsByAnimalId(cur, animal_id)
            users_id = session['profile']['user_id']
            locationList   = []
            for i in range(len(postList)):
                locationList.append([postList[i][0], float(postList[i][4]), float(postList[i][5])])
                
            return render_template("animalSpecific.html", shared_contents=shared_data[0], postList=postList, 
                                   commentList=commentList, animal_id=animal_id, locations=locationList, users_id=users_id)
        else:
            abort(404)

def is_allowed_image_extention(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', "jpeg"]
           
@app.route('/animal/<int:animal_id>', methods=['POST'])
def page_look_up_post(animal_id):
    with db.get_db_cursor(True) as cur:
        users_id = session['profile']['user_id']
        latitude    = request.form.get("latitude", None)
        longitude   = request.form.get("longitude", None)
        description = request.form.get("description", None)
        
        latitude    = None if latitude == "" else latitude
        longitude   = None if longitude == "" else longitude
        description = None if description == "" else description
        
        
        if (latitude == None or longitude == None or description == None):
            return "Latitude, longitude, and/or description cannot be empty!"
        
        file        = request.files.get("image", None)
        imageURL    = file.read()
        if file and is_allowed_image_extention(file.filename):
            cur.execute("INSERT INTO Posts (users_id, animal_id, post_text, imageURL, latitude, longitude) values (%s, %s, %s, %s, %s, %s)", (users_id, animal_id, description, imageURL, latitude, longitude))
        else:
            cur.execute("INSERT INTO Posts (users_id, animal_id, post_text, latitude, longitude) values (%s, %s, %s, %s, %s)", (users_id, animal_id, description, latitude, longitude))
        return redirect(url_for('page_lookup', animal_id=animal_id))
        
@app.route('/comment/<int:animal_id>', methods=['POST'])
def post_comment(animal_id):
    with db.get_db_cursor(True) as cur:
        users_id = session['profile']['user_id']
        description = request.form.get("description", None)

        cur.execute("INSERT INTO Comments (users_id, animal_id, comm_text) values (%s, %s, %s)", (users_id, animal_id, description))

    return redirect(url_for('page_lookup', animal_id=animal_id))

@app.route('/delete/<int:animal_id>/<int:comment_id>')
def delete_comment(animal_id, comment_id):
    with db.get_db_cursor(True) as cur:
        users_id = session['profile']['user_id']

        ##app.logger.info("users_id from session %s", users_id)
        ##app.logger.info("comment_id from session %s", comment_id)

        cur.execute("select users_id from Comments where id = '%s'", [comment_id]) 
        record = cur.fetchone()
        if record[0] == users_id:
            ##app.logger.info("record: %s", record[0])
            cur.execute("delete from comments where id = '%s'", [comment_id])
    return redirect(url_for('page_lookup', animal_id=animal_id))

@app.route('/edit/<int:animal_id>/<int:comment_id>', methods=['POST'])
def edit_comment(animal_id, comment_id):
    with db.get_db_cursor(True) as cur:
        users_id = session['profile']['user_id']
        description = request.form.get("description", None)

        cur.execute("select users_id from Comments where id = '%s'", [comment_id]) 
        record = cur.fetchone()
        if record[0] == users_id:
            
            ##FIX SQL
            cur.execute("UPDATE Comments set comm_text = %s where id = '%s'", (description, comment_id))

    return redirect(url_for('page_lookup', animal_id=animal_id))

@app.route('/report/<int:animal_id>/<int:comment_id>', methods=['POST'])
def report_comment(animal_id, comment_id):
    users_id = session['profile']['user_id']
    description = request.form.get("description", None)
    message_text = f'User {users_id} reported comment {comment_id} ------ '
    #app.logger.info('message_text: %s', message_text) 
    msg = Message(message_text, sender=app.config['MAIL_USERNAME'], recipients=[app.config['MAIL_USERNAME']] )
    msg.body=message_text + description
    mail.send(msg)

    return redirect(url_for('page_lookup', animal_id=animal_id))

@app.route('/reply/<int:animal_id>', methods=['POST'])
def reply_comment(animal_id):
    with db.get_db_cursor(True) as cur:
        users_id = session['profile']['user_id']
        description = request.form.get("description", None)

        cur.execute("INSERT INTO Comments (users_id, animal_id, comm_text) values (%s, %s, %s)", (users_id, animal_id, description))

    return redirect(url_for('page_lookup', animal_id=animal_id))

@app.route('/home')
def home():
    user_name = request.args.get("userName", "unknown")
    return render_template('main.html', user=user_name)

@app.route('/people', methods=['GET'])
def people():
    with db.get_db_cursor() as cur:
        cur.execute("SELECT * FROM person;")
        names = [record[1] for record in cur]

        return render_template("people.html", names=names)

@app.route('/people', methods=['POST'])
def new_person():
    with db.get_db_cursor(True) as cur:
        name = request.form.get("name", "unnamed friend")
        #app.logger.info("Adding person %s", name)
        cur.execute("INSERT INTO person (name) values (%s)", (name,))
        
        return redirect(url_for('people'))

@app.route('/api/foo')
def api_foo():
    data = {
        "message": "hello, world",
        "isAGoodExample": False,
        "aList": [1, 2, 3],
        "nested": {
            "key": "value"
        }
    }
    return jsonify(data)

def humanize_ts(timestamp=False):
    """ taken from https://shubhamjain.co/til/how-to-render-human-readable-time-in-jinja/ """
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    diff = now - timestamp
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(int(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago"

app.jinja_env.filters['humanize'] = humanize_ts