from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def page_landing():
    return render_template("main.html")

    # user_name = request.args.get("userName", "unknown")
    # return render_template('main.html', user=user_name)
    
@app.route('/feed')
def page_feed():
    return render_template("feed.html")

@app.route('/lookup')
def page_lookup():
    return render_template("animal_look_up.html")

# @app.route('/thanks')
# def survey_thanks():
#     return render_template("thanks.html")