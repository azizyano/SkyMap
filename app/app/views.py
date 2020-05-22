
from flask import Flask, request, redirect, render_template, session, g, flash
from app import app
from werkzeug.utils import secure_filename
import tempfile, os
from siaskynet import Skynet
from flask.helpers import url_for
from flask.json import jsonify
from db_setup import init_db, db_session
from forms import SkyMapSearchForm
from models import Skylink

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skylink.db'
app.secret_key = "flask rocks!"

db = SQLAlchemy(app)


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

#########################################

app.config["IMAGE_UPLOADS"] = os.getcwd()
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 40024 * 40024



imagelink=None

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    
    if request.method == "POST":

        if request.files:

            if "filesize" in request.cookies:
                  
                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

                image = request.files["image"]
                
                if image == "":
                    print("No filename")
                    return redirect(request.url)


                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                    print("Image saved")
                    #print(os.path.join(os.environ["PATH"], filename))
                    skylink=Skynet.upload_file(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    #print("Upload successful, skylink: " + skylink)
                    #os.remove(filename)
                    global imagelink
                    imagelink='https://siasky.net/' + skylink[6:]
                    f= open('data.txt', 'w+')
                    f.write(imagelink + '\n')
                    f.close()
                    localisation= request.get_json()
                    print(imagelink)   
                    print(localisation)   
                    #skylink = Skynet.upload_file(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    #skylink = Skynet.upload_file(os.path.abspath(os.getcwd()))
                    return redirect(request.url)
                
                    #return redirect(url_for('upload_image', **locals()))
                    
                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)
             
    

    return render_template("public/upload_image.html", skylink=imagelink) 

#skylink='sia://AADWK37ZuFO7loPOfpiSLbcwfFTTepe9XykY0KjDry13VA'
#creation of the database for search 
init_db()
data=''

@app.route('/', methods=['GET', 'POST'])
def index():
    search = SkyMapSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)
@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        qry = db_session.query(location)
        results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)
