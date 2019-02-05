import os,sys,pip
import time
from PIL import Image
#import numpy 
#import cv2
import platform
#from PIL import Image
from flask import Flask,render_template,send_from_directory,request,redirect,url_for,flash
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/home/ubuntu/files/'
STATIC_ROOT = '/home/ubuntu/flaskapp/static/'
ALLOWED_EXTENSIONS = set(['pdf'])
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['MAX_CONTENT_LENGTH'] = 2*1024*1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/first',methods=['GET', 'POST'])
def hello_world():
  return render_template('hello.html')
@app.route('/first/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')
@app.route('/first/upload/uploader', methods = ['GET', 'POST'])
def uploader():
   #filename = "/home/ubuntu/flaskapp/trial.py"
   if request.method == 'POST':
      if request.form['upload'] == 'upload':
       f = request.files['file']
       filename=secure_filename(f.filename)
       #if allowed_file(filename):
       f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      #return redirect(url_for('uploaded',filename=filename))
       flash('file uploaded succesfully')
       #session.pop('_flashes', None)
       #files=os.listdir(app.config['UPLOAD_FOLDER'])
       return render_template('upload.html', files=filename)
       #else:
       # flash('Please upload file in correct format')
      elif request.form['properties'] == 'prop':
       #return render_template('first.html')
       if filename != " ":
        return redirect(url_for('properties',filename=filename))
      elif request.form['delete'] == 'delete':
        return redirect(url_for('deletefile',filename=filename))
      elif request.form['view'] == 'view':
        return redirect(url_for('view'))
@app.route('/first/upload/uploader/uploaded/<filename>')
def uploaded(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
def flashmesg():
    flash('file uploaded succesfully')
@app.route('/first/upload/uploader/deletefile/<filename>', methods=['GET', 'POST'])
def deletefile(filename):
    file1 = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    os.remove(file1)
    flash('file deleted successfully')
    return render_template('upload.html')
@app.route('/first/upload/uploader/view',  methods=['GET', 'POST'])
def view():
    files=os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload.html',view=files)
@app.route('/first/upload/uploader/properties/<filename>', methods=['GET', 'POST'])
def properties(filename):
    file1 = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    if filename.lower().endswith(('.jpg' , '.png' , '.jpeg')):
     img = Image.open(file1)
     size = img.size
     #img1 = cv2.imread(file1)
     #avg_color_per_row = numpy.average(img, axis=0)
     #avg_color = numpy.average(avg_color_per_row, axis=0)
     pix=img.size[0]*img.size[1]
     columns = img.getcolors(pix)
     sumRGB = [(z[0]*z[1][0],z[0]*z[1][1],z[0]*z[1][2]) for z in columns]
     average = tuple([sum(z)/pix for z in zip(*sumRGB)])
     properties = { 'file_name': filename, 'creation_time' : time.ctime(os.path.getatime(file1)) , 'modified_time' : time.ctime(os.path.getmtime(file1)) , 'file size in Bytes' : os.stat(file1).st_size , 'Resolution' : size , 'average mean of RGB' : average }
    else:
     data = open(file1).readlines(  )
     lines = len(data)
     data1 = open(file1).read()
     words = len(data1.split())
     properties = { 'file_name' : filename , 'creation_time' : time.ctime(os.path.getatime(file1)) , 'modified_time' : time.ctime(os.path.getmtime(file1)) , 'file_size in Bytes' : os.stat(file1).st_size , 'Number of lines' : lines , 'Number of words' : words }
    return render_template('upload.html', prop=properties, files=filename)
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    #sess.init_app(app)
    while True:
     files=os.listdir(app.config['UPLOAD_FOLDER'])
     for f in files:
        file1 = os.path.join(app.config['UPLOAD_FOLDER'],f)
        ctime = os.stat(file1).st_mtime
        now = time.time()
        if  now - ctime > 300:
         os.remove(file1)
    app.run(debug = True)
