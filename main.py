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

    #Exit if the form is not valid
    if not request.method == "POST" or not form.validate():
        return render_template("submitted_form.html", error_string = "The form data was invalid")

    # Capture base data from the form
    cpu = form.cpu.data
    gpu = form.gpu.data
    ram = form.ram.data
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
    csv_data = list(csv_input)[1:]
    avg = 0

    #Initialize a simple min_val/max_val to use for comparisons in the loop
    min_val = int(csv_data[0][0])
    max_val = min_val

    invalid_lines = 0
    #Loop through to establish average, min and max fps
    for item in csv_data:
        if not item:
            invalid_lines += 1
            continue
        item = int(item[0])
        avg += item
        max_val = item if max_val < item else max_val
        min_val = item if min_val > item else min_val

    valid_data_count = len(csv_data) - invalid_lines
    avg = float(avg) / valid_data_count

    #Loop through a second time to establish the average standard deviation
    total_diff_from_avg = 0
    for item in csv_data:
        if not item:
            continue
        total_diff_from_avg += abs(int(avg) - int(item[0]))

    std_dev = total_diff_from_avg / valid_data_count

    #Should make a view model to clean up the render_template call
    return render_template("submitted_form.html", cpu=cpu, gpu=gpu, ram=ram, avg=avg, std_dev = std_dev, max_val = max_val, min_val = min_val, csv_data=csv_data)
