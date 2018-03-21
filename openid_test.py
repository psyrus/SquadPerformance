from flask import Flask, render_template, request, session, g, flash, url_for, abort
from openid_gae.flask_openid import OpenID
from openid.extensions import pape
from forms import *
import logging, csv, io
from models import *
app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT',
    DEBUG = True
)

# setup flask-openid
#oid = OpenID(app, safe_roots=[], extension_responses=[pape.Response])
oid = OpenID(app, './openid_db')

@app.before_request
def before_request():
    g.user = None
    if 'openid' in session:
        g.user = User.query.filter_by(openid=session['openid']).first()

@app.route("/oid/start", methods=['GET','POST'])
def start():
    return '<a href="/oid/login">Start OpenID Flow</a>'

@app.route('/oid/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """Does the login via OpenID.  Has to call into `oid.try_login`
    to start the OpenID machinery.
    """
    # if we are already logged in, go back to were we came from
    logging.info(g.user)
    logging.info("This is working")
    if g.user is not None:
        logging.warning("Going to redirect")
        return redirect(oid.get_next_url())

    if request.method == 'POST':
        logging.warning("Post?")
        openid = request.form.get('openid')
        if openid:
            pape_req = pape.Request([])
            return oid.try_login(openid, ask_for=['email', 'nickname', 'fullname'])
    logging.warning("Supposed to render template now")

    return render_template('oid_login.html', next=oid.get_next_url(),
                           error=oid.fetch_error())


@oid.after_login
def create_or_login(resp):
    """This is called when login with OpenID succeeded and it's not
    necessary to figure out if this is the users's first login or not.
    This function has to redirect otherwise the user will be presented
    with a terrible URL which we certainly don't want.
    """
    session['openid'] = resp.identity_url
    if 'pape' in resp.extensions:
        pape_resp = resp.extensions['pape']
        session['auth_time'] = pape_resp.auth_time
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    return redirect(url_for('create_profile', next=oid.get_next_url(),
                            name=resp.fullname or resp.nickname,
                            email=resp.email))


@app.route('/oid/create-profile', methods=['GET', 'POST'])
def create_profile():
    """If this is the user's first login, the create_or_login function
    will redirect here so that the user can set up his profile.
    """
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name:
            flash(u'Error: you have to provide a name')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            db_session.add(User(name, email, session['openid']))
            db_session.commit()
            return redirect(oid.get_next_url())
    return render_template('create_profile.html', next_url=oid.get_next_url())