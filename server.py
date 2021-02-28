import os, db
from flask import Flask, render_template, request, g, redirect, url_for, jsonify, abort
from queryResults import *

app = Flask(__name__)

@app.route('/')
def page_landing():
    return render_template("main.html")

@app.route('/signup')
def page_signup():
    return render_template("signup.html")

@app.route('/login')
def page_login():
    return render_template("MemberLoginPage.html")

@app.route('/add')
def page_add_animal():
    return render_template("addAnimal.html")

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
            postList = getAllPostsFromAnimalId(cur, animal_id)
            
            return render_template("animalSpecific.html", shared_contents=shared_data[0], postList=postList, animal_id=animal_id)
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
            return "SUCCESS: IMAGE ALSO SAVED!"
        else:
            cur.execute("INSERT INTO Posts (users_id, animal_id, post_text, latitude, longitude) values (%s, %s, %s, %s, %s)", (1, animal_id, description, latitude, longitude))
            return "SUCCESS: HOWEVER, NO IMAGE SAVED!"
        
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
