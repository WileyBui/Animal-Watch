from flask import Flask, render_template, request, g, redirect, url_for, jsonify, abort, session
from urllib.parse import urlencode
import os
import db
from auth0 import auth0_setup, require_auth, auth0
from datetime import datetime
from queryResults import *

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

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
        return redirect(url_for('test_auth'))
    else:
        return auth0().authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/logout')
def logout():
    session.clear()
    params = { 'returnTo': url_for('home', _external=True), 'client_id': os.environ['AUTH0_CLIENT_ID'] }
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
        cur.execute("insert into Users (id, users_name) values (%s. %s)", (users_id, users_name))
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
        animal_id = request.form.get("species")
        post_text = request.form.get("classification")
        post_location = request.form.get("range")
        #latitude =
        #longitude =
        # Get image from the form
        #with open(request.form.get("image"), "rb") as image:
            # Encode image data into a string
         #   post_image = base64.b64encode(image.read())
          #  console.logger.info(post_image)
        post_image = request.form.get("image")
        post_time = str(datetime.now())
        cur.execute("insert into Posts (users_id, animal_id, post_text, imageURL, post_time) values (%s, %s, %s, %s, %s);", (users_id, animal_id, post_text, post_image, post_time))
        #cur.execute("insert into Locations (user_id, animal_id, lat, long) values (%s, %s, %s, %s);" (user_id, animal_id, lat, long))
        return redirect(url_for("/feed"))

@app.route('/feed', methods=['GET'])
def page_feed():
    with db.get_db_cursor(False) as cur:
        return render_template("feed.html", dataList=getActivityFeed(cur))

@app.route('/animal/<int:animal_id>', methods=['GET'])
def page_lookup(animal_id):
    with db.get_db_cursor(False) as cur:
        # shared contents
        shared_data = getSharedContentsFromAnimalId(cur, animal_id)
        
        if (len(shared_data) == 1):
            postList    = getAllPostsFromAnimalId(cur, animal_id)
            locationList   = []
            for i in range(len(postList)):
                locationList.append([postList[i][0], float(postList[i][4]), float(postList[i][5])])
                
            return render_template("animalSpecific.html", shared_contents=shared_data[0], postList=postList, animal_id=animal_id, locations=locationList)
        else:
            abort(404)

def is_allowed_image_extention(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', "jpeg"]
           
@app.route('/animal/<int:animal_id>', methods=['POST'])
def page_look_up_post(animal_id):
    with db.get_db_cursor(True) as cur:
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
            cur.execute("INSERT INTO Posts (users_id, animal_id, post_text, imageURL, latitude, longitude) values (%s, %s, %s, %s, %s, %s)", (1, animal_id, description, imageURL, latitude, longitude))
        else:
            cur.execute("INSERT INTO Posts (users_id, animal_id, post_text, latitude, longitude) values (%s, %s, %s, %s, %s)", (1, animal_id, description, latitude, longitude))
        return redirect(url_for('page_lookup', animal_id=animal_id))
        
# have the DB submodule set itself up before we get started. groovy.
@app.before_first_request
def initialize():
    db.setup()

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
        app.logger.info("Adding person %s", name)
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