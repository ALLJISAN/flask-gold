import os
import process
import tensorflow as tf
from pred import predict
from flask import Flask, flash, request, redirect, url_for,jsonify,render_template,Response,g
from werkzeug.utils import secure_filename
# i think it is all fucking done
UPLOAD_FOLDER = '/static/'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif','JPG'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '123456'
basepath = os.path.dirname(__file__)
g = app.app_context()
g.ok=False
#g.model=tf.estimator.Estimator(model_dir='/tmp/mnist_convnet_model',model_fn=model_fn)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("Untitled-1.html")

@app.route('/pikachu', methods=['GET', 'POST'])
def pikachu():
    if request.method == 'POST':
        # 检查是否允许上传的文件类型
        if 'file' not in request.files:
            flash('No file part')
            print("NOT ALLOW")
            return redirect(request.url)
        file = request.files['file']
        # 如果用户没有上传图片，返回一个空的filename
        # 没有上传图片：
        if file.filename == '':
            flash('No selected file')
            print("NO FILE")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # 当前文件所在路径
            upload_path = os.path.join(basepath, 'static/photo',secure_filename(file.filename))
            # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            file.save(upload_path)
            g.ok=True
            return redirect(url_for("show_pkq",imgName=file.filename))
    return render_template("upload1.html")

@app.route('/gold', methods=['GET', 'POST'])
def gold():
    if request.method == 'POST':
        # 检查是否允许上传的文件类型
        if 'file' not in request.files:
            flash('No file part')
            print("NOT ALLOW")
            return redirect(request.url)
        file = request.files['file']
        # 如果用户没有上传图片，返回一个空的filename
        # 没有上传图片：
        if file.filename == '':
            flash('No selected file')
            print("NO FILE")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # 当前文件所在路径
            upload_path = os.path.join(basepath, 'static/photo',secure_filename(file.filename))
            # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            file.save(upload_path)
            g.ok=True
            return redirect(url_for("show_gold",imgName=file.filename))
    return render_template("upload2.html")
@app.route('/pikachu/<imgName>', methods=['GET', 'POST'])
def show_pkq(imgName):
    if g.ok==True:
        process.process(imgName)
        g.ok = False
        return render_template("Untitled-2.html",img=imgName)
    else:
        print("gok==false")
        return redirect(url_for('index'))
@app.route('/gold/<imgName>', methods=['GET', 'POST'])
def show_gold(imgName):
    if g.ok==True:
        #process.process(imgName)
        result=predict(imgName)
        g.ok = False
        #return render_template("Untitled-2.html",img=imgName)
        return render_template("Untitled-3.html",lines=result)
    else:
        return redirect(url_for('index'))
if __name__=="__main__":
    app.run(host="0.0.0.0")
