from flask import Flask, render_template, request, g, redirect, url_for, jsonify, abort, session
from urllib.parse import urlencode
import os
import db
from auth0 import auth0_setup, require_auth, auth0
from datetime import datetime

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
        cur.execute("""
                    
                SELECT * FROM (
                    SELECT
                        Posts.users_id,
                        Users.users_name,
                        Posts.post_text,
                        Posts.image_id,
                        array_to_string(array_agg(distinct "tag"),'; ') AS tag,
                        array_to_string(array_agg(distinct "tag_bootstrap_color"),'; ') AS tag_bootstrap_color,
                        Posts.post_time
                    FROM Posts, Users, Animals, HasTag, Tags, Images
                    WHERE
                        Posts.users_id = Users.id
                        AND Posts.animal_id = Animals.id
                        AND Animals.id = HasTag.animal_id
                        AND HasTag.tag_id = Tags.id
						AND Posts.image_id = Images.id
                    GROUP BY
                        Posts.post_time,
                        Posts.users_id,
                        Users.users_name,
                        Posts.post_text,
                        Posts.image_id,
                        Posts.post_time
                ) A
                ORDER BY A.post_time DESC;
                        
                    """)
        
        return render_template("feed.html", dataList=cur)
    
@app.route('/post/<int:id>', methods=['GET'])
def page_lookup(id):
    return render_template("post_lookup.html")

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