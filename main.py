from flask import Flask, render_template, request
from forms import FpsForm
import logging
app = Flask(__name__)

@app.before_request
def enable_local_error_handling():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
    

@app.route('/form')
def form():
    return render_template('form.html')


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


@app.route('/fps-submitted', methods=['POST'])
def fps_submitted():
    print(request.form)
    form = FpsForm(request.form)
    if request.method == "POST" and form.validate():
        return "Everything workedout!"
    return "{}".format(form.cpu.data)
