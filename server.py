from flask import Flask, render_template, request, g, redirect, url_for, jsonify, abort, session, send_file, make_response, render_template_string
from werkzeug.utils import secure_filename
from urllib.parse import urlencode
import requests
from PIL import Image
from io import BytesIO
import os
import db, io
from auth0 import auth0_setup, require_auth, auth0
from datetime import datetime
from queryResults import *
from flask_mail import Mail, Message
from flask_moment import Moment

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'animalwatch2021@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ["MAIL_PASSWORD"] # must be added to .env file
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
moment = Moment(app)

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

@app.route('/profile')
def page_profile():
    with db.get_db_cursor(commit=False) as cur:
        users_id = session['profile']['user_id']
        # Animal Postings
        cur.execute(""" SELECT Animals.id, Animals.species, Animals.animal_description, Images.id
                        FROM Animals, Images
                        WHERE
                            Animals.users_id = %s
                            AND Animals.image_id = Images.id
                        ORDER BY Animals.id DESC;
                    """, [users_id])
        animal_postings = [record for record in cur]
        
        cur.execute(""" SELECT Animals.id, Animals.species, Posts.post_text
                        FROM Animals, Posts
                        WHERE
                            Posts.users_id = %s
                            AND Posts.animal_id = Animals.id
                        ORDER BY Posts.id DESC;
                    """, [users_id])
        postings_on_existing_animals = [record for record in cur]
        
        cur.execute(""" SELECT Animals.id, Animals.species, Comments.comm_text
                        FROM Animals, Comments
                        WHERE
                            Comments.users_id = %s
                            AND Animals.id = Comments.animal_id
                        ORDER BY Comments.id DESC;
                    """, [users_id])
        comments_on_existing_animals = [record for record in cur]
        
        return render_template("profile.html", animal_postings=animal_postings, postings_on_existing_animals=postings_on_existing_animals, comments_on_existing_animals=comments_on_existing_animals)

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
        users_avatar = session['profile']['picture']
        cur.execute("Select COUNT(*) FROM Users WHERE id = '%s';" % users_id)
        try:
            for record in cur:
                if record[0] == 0:
                    if (users_avatar):
                        #app.logger.info("users_avatar has a value %s", users_avatar)
                        #cur.execute("insert into Images (image_name, image_data) values (%s, %s) returning id;", (users_id, users_avatar))
                        #imageID = cur.fetchone()[0]
                        ##app.logger.info("imageID has a value %s", imageID)
                        cur.execute("insert into Users (id, users_name, profile_picture) values (%s, %s, %s);", (users_id, users_name, users_avatar))
                    else:
                        #app.logger.info("users_avatar has no value")
                        cur.execute("insert into Users (id, users_name) values (%s, %s);", (users_id, users_name))
        except:
            pass
    return redirect('/test_auth')

@app.route('/test_auth')
@require_auth
def test_auth():
    return render_template("main.html", profile=session['profile'])

### IMAGES
@app.route('/image/<int:img_id>')
def view_image(img_id):
    #app.logger.info(img_id)
    with db.get_db_cursor() as cur:
        cur.execute("SELECT * FROM Images where Images.id=%s", (img_id,))
        image_row = cur.fetchone() # just another way to interact with cursors

        # in memory pyhton IO stream
        stream = io.BytesIO(image_row["image_data"])

        # use special "send_file" function
        return send_file(stream, attachment_filename=image_row["image_name"])

@app.route('/avatar/<string:users_id>')
def view_avatar(users_id):
    #app.logger.info(users_id)
    with db.get_db_cursor() as cur:
        users_id.replace('%7C', '|')
        cur.execute("SELECT profile_picture FROM Users where id=%s", (users_id,))
        users_avatar = cur.fetchone()[0] # just another way to interact with cursors
        #app.logger.info("users_avatar has a value %s", users_avatar)

        return redirect(users_avatar)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', "gif"]


@app.route('/addAnimal')
@require_auth
def page_add_animal():
    status = request.args.get("status", "")
    if status:
        return render_template("addAnimal.html", stat=status)
    else:
        return render_template("addAnimal.html")


@app.route('/addAnimal', methods=['POST'])
def processAddAnimal():
    with db.get_db_cursor(commit=True) as cur:
        users_id = session['profile']['user_id']
        #users_id = 1 #TESTING TESTING TESTING - DON'T DEPLOY THIS
        species = request.form.get("species")
        endangerment_level = request.form.get("classification")
        animal_range = request.form.get("range")

        imageURL = request.form.get("imageURL") #TODO: fix the image back-end
        imageFile = request.files["imageFile"]
        if imageURL != '':
            resp = requests.get(imageURL)
            image = BytesIO(resp.content).read()
            #image = Image.frombytes(imagebytes,'raw',)
            #print(image)
            ##app.logger.info(image)
            cur.execute('insert into Images (image_name, image_data) values (%s, %s) RETURNING id;', (str(imageURL),image))
            imageID = cur.fetchone()[0]
        elif imageFile and allowed_file(imageFile.filename):
            filename = secure_filename(imageFile.filename)
            cur.execute("insert into Images (image_name, image_data) values (%s, %s) RETURNING id;", (filename, imageFile.read()))
            imageID = cur.fetchone()[0]
        else:
            return redirect(url_for("page_add_animal", status="Image Upload Failed"))
        animal_description = request.form.get("description")
        #post_time = str(datetime.now()) #Removed-this is not part of animal page right now
        cur.execute('insert into Animals (species, endangerment_level, animal_range, image_id, animal_description, users_id) values (%s, %s, %s, %s, %s, %s) RETURNING id;', (species, endangerment_level, animal_range, imageID, animal_description, users_id))
        tags = request.form.get("tags")
        tagList = tags.split(', ')
        #app.logger.info(tagList)
        addTags(cur, cur.fetchone()[0], tagList)

        return redirect(url_for("page_feed"))

@app.route('/feed', methods=['GET'])
def page_feed():
    with db.get_db_cursor(False) as cur:
        records = getActivityFeed(cur)
        #app.logger.info(records.fetchone())
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
            ##app.logger.info(len(postList))
            for i in range(len(postList)):
                locationList.append([postList[i][0], float(postList[i][4]), float(postList[i][5])])
            
            
            # RAY ADDED dispClassification TO FIX CLASSIFICATION SHOWING UP AS A NUMBER
            # Converts endangerment number from database to the level of endangerment that user specified when addingAnimal
            dispClassification = get_classification(shared_data[0][4])
            
            return render_template("animalSpecific.html", shared_contents=shared_data[0], postList=postList,
                                   commentList=commentList, animal_id=animal_id, locations=locationList, users_id=users_id, dClassification = dispClassification)
        else:
            abort(404)

# RAY ADDED get_classification TO FIX CLASSIFICATION SHOWING UP AS A NUMBER
def get_classification(classificationNum): #https://www.geeksforgeeks.org/switch-case-in-python-replacement/
    switcher = { 
        -1: "Unknown",
        0: "Not Evaluated (NE)",
        1: "Data deficient (DD)", 
        2: "Least concern (LC)", 
        3: "Conservation Dependent (CD)",
        4: "Near threatened (NT)",
        5: "Vulnerable (VU)",
        6: "Endangered (EN)",
        7: "Critically endangered (CR)",
        8: "Extinct in the wild (EW)",
        9: "Extinct (EX)"
    }
    return switcher.get(classificationNum, "Unspecified") 

@app.route('/animal/<int:animal_id>', methods=['POST'])
def page_look_up_post(animal_id):
    with db.get_db_cursor(True) as cur:
        users_id = session['profile']['user_id']
        users_avatar = session['profile']['picture']
        latitude    = request.form.get("latitude", None)
        longitude   = request.form.get("longitude", None)
        description = request.form.get("description", None)
        

        latitude    = None if latitude == "" else latitude
        longitude   = None if longitude == "" else longitude
        description = None if description == "" else description

        
        if (latitude == None or longitude == None or description == None):
            return "Latitude, longitude, and/or description cannot be empty!"

        imageFile        = request.files["image"]
        if imageFile and allowed_file(imageFile.filename):
            filename = secure_filename(imageFile.filename)
            cur.execute("insert into Images (image_name, image_data) values (%s, %s) RETURNING id;", (filename, imageFile.read()))
            imageID = cur.fetchone()[0]
            cur.execute("INSERT INTO Posts (users_id, animal_id, post_text, image_id, latitude, longitude) values (%s, %s, %s, %s, %s, %s)", (users_id, animal_id, description, imageID, latitude, longitude))
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

@app.route('/delete_comment/<int:animal_id>/<int:comment_id>')
def delete_comment(animal_id, comment_id):
    with db.get_db_cursor(True) as cur:
        users_id = session['profile']['user_id']

        ###app.logger.info("users_id from session %s", users_id)
        ###app.logger.info("comment_id from session %s", comment_id)

        cur.execute("select users_id from Comments where id = '%s'", [comment_id]) 
        record = cur.fetchone()
        if record[0] == users_id:
            ###app.logger.info("record: %s", record[0])
            cur.execute("delete from comments where id = '%s'", [comment_id])
    return redirect(url_for('page_lookup', animal_id=animal_id))

@app.route('/delete_post/<int:animal_id>/<int:post_id>')
def delete_post(animal_id, post_id):
    with db.get_db_cursor(True) as cur:
        users_id = session['profile']['user_id']

        ###app.logger.info("users_id from session %s", users_id)
        ###app.logger.info("post_id from session %s", post_id)

        cur.execute("select users_id from Posts where id = '%s'", [post_id]) 
        record = cur.fetchone()
        if record[0] == users_id:
            ###app.logger.info("record: %s", record[0])
            cur.execute("delete from Posts where id = '%s'", [post_id])
    return redirect(url_for('page_lookup', animal_id=animal_id))

@app.route('/edit_comment/<int:animal_id>/<int:comment_id>', methods=['POST'])
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

@app.route('/edit_post/<int:animal_id>/<int:post_id>', methods=['POST'])
def edit_post(animal_id, post_id):
    with db.get_db_cursor(True) as cur:
        users_id = session['profile']['user_id']
        description = request.form.get("description", None)

        cur.execute("select users_id from Posts where id = '%s'", [post_id]) 
        record = cur.fetchone()
        if record[0] == users_id:
            
            ##FIX SQL
            cur.execute("UPDATE Posts set post_text = %s where id = '%s'", (description, post_id))

    return redirect(url_for('page_lookup', animal_id=animal_id))

@app.route('/report_comment/<int:animal_id>/<int:comment_id>', methods=['POST'])
def report_comment(animal_id, comment_id):
    users_id = session['profile']['user_id']
    description = request.form.get("description", None)
    message_text = f'User {users_id} reported comment {comment_id} ------ '
    ##app.logger.info('message_text: %s', message_text) 
    msg = Message(message_text, sender=app.config['MAIL_USERNAME'], recipients=[app.config['MAIL_USERNAME']] )
    msg.body=message_text + description
    mail.send(msg)

    return redirect(url_for('page_lookup', animal_id=animal_id))

@app.route('/report_post/<int:animal_id>/<int:post_id>', methods=['POST'])
def report_post(animal_id, post_id):
    users_id = session['profile']['user_id']
    description = request.form.get("description", None)
    message_text = f'User {users_id} reported post {post_id} ------ '
    ##app.logger.info('message_text: %s', message_text) 
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
        ##app.logger.info("Adding person %s", name)
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