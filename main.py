from flask import Flask, render_template, request, session
from flask_openid import OpenID
import flask_login
from forms import *
import logging, csv, io
from models import *
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@app.before_request
def enable_local_error_handling():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        logging.info(form.username.data)
        user = User(id=form.username.data.lower())
        user.username = form.username.data
        user.email = form.email.data
        user.activated = False
        user.password = User.hash_password(form.password.data)
        user.put()

    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    logging.info("Got the form")
    logging.info(form.username.data)
    if request.method == 'POST' and form.validate():
        #user = User.getByUsername(form.username)
        user = load_user(form.username.data)
        logging.info(user.username)
        if not flask_login.login_user(user, remember=True):
            logging.info("login failed")
            return "Failed to login"
        logging.info("Successfully logged in user. session id is now: %s" % session['_id'])
        logging.info("session user is now: %s" % session['user_id'])
    else:
        logging.info("This failed")

    return render_template("login.html", form=form)

@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    return render_template(
      'submitted_form.html',
      name=name,
      email=email,
      site=site,
      comments=comments)


@app.route('/')
def index():
    form = FpsForm()
    return render_template("index.html", form=form)

@app.route('/open')
def open():
    #Challenge here is to get the OpenID to write to the datastore
    # The stuff below doesn't work because it tries to write to disk which isn't allowed on GAE
    #oid = OpenID(app, '/oauth', safe_roots=[])
    #oid.try_login('https://steamcommunity.com/openid/')
    return "Hi there"

@app.route('/how-to')
def how_to():
    return render_template("how_to.html")


@app.route('/fps-submitted', methods=['POST'])
def fps_submitted():
    form = FpsForm(request.form)

    #Exit if the form is not valid
    if not request.method == "POST" or not form.validate():
        return render_template("submitted_form.html", error_string = "The form data was invalid")

    # Capture base data from the form
    cpu = form.cpu.data
    gpu = form.gpu.data
    ram = form.ram.data
    res = form.resolution.data
    csv_data = []

    #Exit if no files were uploaded
    if not request.files:
        return render_template("submitted_form.html", error_string = "No file was uploaded")

    fileobj = request.files[form.fps_values.name]

    #Exit if the uploaded file was not a CSV
    if not fileobj.mimetype  == "text/csv":
        return render_template("submitted_form.html", error_string = "The uploaded file was not a CSV file")

    #Convert uploaded file to a list of strings for processing
    stream = io.StringIO(fileobj.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    csv_data = [int(i[0]) for i in list(csv_input)[1:] if len(i) > 0]
    avg = 0

    if len(csv_data) < 250:
        return render_template("submitted_form.html", error_string = "There were not enough FPS entries in the file, please ensure you benchmark 5 minutes of FPS")
    #Initialize a simple min_val/max_val to use for comparisons in the loop
    min_val = csv_data[0]
    max_val = min_val

    invalid_lines = 0
    #Loop through to establish average, min and max fps
    for item in csv_data:
        if not item:
            invalid_lines += 1
            continue
        avg += item
        max_val = item if max_val < item else max_val
        min_val = item if min_val > item else min_val

    valid_data_count = len(csv_data) - invalid_lines
    avg = int(round(float(avg) / valid_data_count))

    #Loop through a second time to establish the average standard deviation
    total_diff_from_avg = 0
    for item in csv_data:
        if not item:
            continue
        total_diff_from_avg += abs(int(avg) - item)

    std_dev = total_diff_from_avg / valid_data_count

    testModel = PC_Config.create(cpu, gpu, ram, res)

    print(testModel.CPU)
    #Should make a view model to clean up the render_template call
    return render_template("submitted_form.html", cpu=cpu, gpu=gpu, ram=ram, avg=avg, std_dev = std_dev, max_val = max_val, min_val = min_val, csv_data=csv_data)
@app.route('/Test')
def Test():
    from social_flask.routes import social_auth
    from social_core.backends.steam import SteamOpenId
    app.register_blueprint(social_auth)
    SOCIAL_AUTH_STEAM_API_KEY = "9F9094B71C4D5F8DEAFD471687AEADAE"

    auth_thing = SteamOpenId()
    return openid_url()

@login_manager.user_loader
def load_user(user_id):
    logging.info("id: %s" % user_id)
    this_user = User.get_by_id(user_id)
    logging.info(this_user)
    return this_user