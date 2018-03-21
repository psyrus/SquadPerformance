from flask import Flask, render_template, request, session, g, flash, url_for, abort
from openid_gae.flask_openid import OpenID
from openid.extensions import pape
from forms import *
import logging, csv, io
from models import *
import settings

app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT',
    DEBUG = True,
    OPENID_FS_STORE_PATH = 'datastore'
)
oid = OpenID(app, './openid_db')

@app.route('/oid/')
def index():
    return '<a href="%s">Go here.</a>' % url_for('do_redirect')

@app.route('/oid/redirect/')
def do_redirect():
    session['hello'] = 'world!'
    return redirect(url_for('dump_session'))

@app.route('/oid/session/')
def dump_session():
    response = make_response(repr(session))
    response.content_type = 'text/plain'
    return response

@app.before_request
def lookup_current_user():

    g.user = None
    app.logger.debug("session in before request:" + str(session))
    if 'openid' in session:
        openid = session['openid']
        app.logger.debug("dir of User" + str(dir(User)))
        g.user = User.all().filter('openid =', openid).get()

@app.route('/oid/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():

    if g.user is not None:
        return redirect(oid.get_next_url())
    if request.method == "POST":
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email', 'fullname', 'nickname'])
    return render_template('oid_login.html', next=oid.get_next_url(), error=oid.fetch_error())

@oid.after_login
def create_or_login(resp):

    session['openid'] = resp.identity_url
    app.logger.debug("resp.identity_url:" + str(resp.identity_url))
    app.logger.debug("session in create profile:" + str(session))
    #user = User.all().filter('openid =', resp.identity_url).get()
    logging.info(resp.identity_url)
    user = None
    app.logger.debug("user in create_or_login:" + str(user))
    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    app.logger.debug("session in create profile at the end:" + str(session))
    return redirect(url_for('create_profile', next=oid.get_next_url(),name=resp.fullname or resp.nickname,email=resp.email))

@app.route('/oid/create-profile', methods=['GET', 'POST'])
def create_profile():

    app.logger.debug("create_profile -session:" + str(session.items()))
    app.logger.debug("g.user is not None:" + str(g.user is not None))
    app.logger.debug("'openid' not in session:" + str('openid' not in session))
    if g.user is not None or 'openid' not in session:
        app.logger.debug("g.user :" + str(g.user))
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

            u = User(full_name = name, email = email, nickname = name)
            return redirect(oid.get_next_url())
    return render_template('create_profile.html', next_url=oid.get_next_url())

@app.route('/oid/logout')
def logout():
    session.pop('openid', None)
    flash(u'You were signed out')
    return redirect(oid.get_next_url())