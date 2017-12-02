from flask import Flask, render_template, request
from forms import FpsForm
import logging, csv, io
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


@app.route('/how-to')
def how_to():
    return render_template("how_to.html")


@app.route('/fps-submitted', methods=['POST'])
def fps_submitted():
    form = FpsForm(request.form)
    if request.method == "POST" and form.validate():
        cpu = form.cpu.data
        gpu = form.gpu.data
        ram = form.gpu.data
        csv_data = []
        if request.files:
            print("Values in fps_values!")
            print(request.files)
            print(form.fps_values.name)
            fileobj = request.files[form.fps_values.name]
            print(fileobj)
            if not fileobj.mimetype  == "text/csv":
                print("This is not a csv!!!")
            else:
                print("It's a csv")
                stream = io.StringIO(fileobj.read().decode("UTF8"), newline=None)
                csv_input = csv.reader(stream)
                csv_data = list(csv_input)
        avg = 0
        return render_template("submitted_form.html", cpu=cpu, gpu=gpu, ram=ram, avg=avg, csv_data=csv_data)
    return "{}".format(form.cpu.data)
