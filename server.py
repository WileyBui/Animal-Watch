from flask import Flask, render_template, request, g, redirect, url_for, jsonify

import db

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
        cur.execute("""
                    
                SELECT * FROM (
                    SELECT
                        Posts.users_id,
                        Users.users_name,
                        Posts.post_text,
                        Posts.imageURL,
                        array_to_string(array_agg(distinct "tag"),'; ') AS tag,
                        array_to_string(array_agg(distinct "tag_bootstrap_color"),'; ') AS tag_bootstrap_color,
                        Posts.post_time
                    FROM Posts, Users, Animals, HasTag, Tags
                    WHERE
                        Posts.users_id = Users.id
                        AND Posts.animal_id = Animals.id
                        AND Animals.id = HasTag.animal_id
                        AND HasTag.tag_id = Tags.id
                    GROUP BY
                        Posts.post_time,
                        Posts.users_id,
                        Users.users_name,
                        Posts.post_text,
                        Posts.imageURL,
                        Posts.post_time
                ) A
                ORDER BY A.post_time DESC;
                        
                    """)
        
        return render_template("feed.html", dataList=cur)
    
@app.route('/post/<int:id>', methods=['GET'])
def page_lookup(id):
    return render_template("post_lookup.html")


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
