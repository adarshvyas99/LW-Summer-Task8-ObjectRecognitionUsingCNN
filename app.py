from flask import Flask, render_template,request, flash, redirect, url_for
from  model_file import model
from rto_api_module import u_get_vehicle_info
from werkzeug.utils import secure_filename
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT,'static/uploads')

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')

'''
@app.route('/', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('index.html', msg='No file selected')
        file = request.files['file']
        #upfile = request.files['files']
        # if no file is selected
        if file.filename == '':
            return render_template('index.html', msg='No file selected')

        if file and allowed_file(file.filename):
            new_filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        
        elif request.method == 'GET':

            return render_template('index.html') 
'''
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash(message='No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash(message='No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash(message='Image successfully uploaded and owner details are displayed below')
        img_location = 'static/uploads/'+filename
        data=model(img_location)
        return render_template('index.html', result=data , filename= filename) 

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
'''
savedCarDetails=dict()
@app.route('/fetch',methods=["POST","GET"])
def fetch():
    file=request.files['file']
    fname='test.'+file.filename.split('.')[-1]
    file.save(fname)
    plateNo= noPlateRecognization(fname)
    if plateNo not in savedCarDetails.keys():
        dt=getVehicalInfo(plateNo,'kofil55747')
        savedCarDetails[plateNo]=dt
    return render_template('output.html',dt=savedCarDetails[plateNo])
'''

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)



@app.route('/', methods = ["POST"])
def upload_number():
    global output
    if request.method == "POST":
      u_number = request.form["u_number"]
      test_number= u_get_vehicle_info(u_number) 
    return ("#", test_number)



if __name__ == "__main__":
    app.run(debug=True, port=8080)


