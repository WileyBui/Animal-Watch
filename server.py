from flask import Flask, render_template, request, g, redirect, url_for, jsonify, abort

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
                            Animals.id,
                            Animals.species,
                            Animals.imageURL,
                            array_to_string(array_agg(distinct "tag"),'; ') AS tag,
                            array_to_string(array_agg(distinct "tag_bootstrap_color"),'; ') AS tag_bootstrap_color
                        FROM Animals, HasTag, Tags
                        WHERE
                            Animals.id = HasTag.animal_id
                            AND HasTag.tag_id = Tags.id
                        GROUP BY
                            Animals.id,
                            Animals.species,
                            Animals.imageURL
                    ) A
                    ORDER BY A.id DESC;
                    """)
        
        return render_template("feed.html", dataList=cur)
    
@app.route('/animal/<int:animal_id>', methods=['GET'])
def page_lookup(animal_id):
    with db.get_db_cursor(False) as cur:
        cur.execute("""
                    SELECT
                        Animals.species,
                        array_to_string(array_agg(distinct "tag"),'; ') AS tag,
                        array_to_string(array_agg(distinct "tag_bootstrap_color"),'; ') AS tag_bootstrap_color,
                        Animals.imageURL
                    FROM Animals, HasTag, Tags
                    WHERE
                        Animals.id = %s
                        AND Animals.id = HasTag.animal_id
                        AND HasTag.tag_id = Tags.id
                    GROUP BY
                        Animals.species,
                        Animals.imageURL;
                    """, [animal_id])
        
        shared_data = [record for record in cur]
        
        if (len(shared_data) == 1):
            return render_template("animalSpecific.html", shared_contents=shared_data[0])
        else:
            abort(404)


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
