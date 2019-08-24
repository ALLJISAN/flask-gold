import os
import process
import tensorflow as tf
from pred import predict
from photoTocartoon import turn2cartoon
from flask import Flask, flash, request, redirect, url_for,render_template,Response,g,jsonify
from werkzeug.utils import secure_filename
# i think it is all fucking done
UPLOAD_FOLDER = '/static/'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif','JPG'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '123456'
basepath = os.path.dirname(__file__)
g = app.app_context()
#g.ok=False
#g.model=tf.estimator.Estimator(model_dir='/tmp/mnist_convnet_model',model_fn=model_fn)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template("template.html")
@app.route('/result/<imgName>', methods=['GET', 'POST'])
def resultgold(imgName):
    if imgName!="None":
        result=predict(imgName)
        return render_template("template-gold.html",result=result)
    else:
        return render_template("template.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    #return render_template("Untitled-1.html")
    return redirect(url_for("pikachu"))

@app.route('/pikachu', methods=['GET', 'POST'])
def pikachu(imgName=""):
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
            #g.ok=True
            process.process(file.filename)
            return render_template("page.html",imgName=file.filename)
            #render_template("template.html",imgName=file.filename)
            #return redirect(url_for("show_pkq",imgName=file.filename))
    return render_template("page.html")

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
            return render_template("page-gold.html",imgName=file.filename)
            #return redirect(url_for("show_gold",imgName=file.filename))
    return render_template("page-gold.html",imgName="None")

@app.route('/phptotocartoon', methods=['GET', 'POST'])
def phptotocartoon():
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
            turn2cartoon(file.filename,"./static/photo/")
            return render_template("page-cartoon.html",imgName=file.filename)
    return render_template("page-cartoon.html")

@app.route('/pikachu/<imgName>', methods=['GET', 'POST'])
def show_pkq(imgName):
    if True:
        process.process(imgName)
        #g.ok = False
        return render_template("Untitled-2.html",img=imgName)
    else:
        print("gok==false")
        return redirect(url_for('index'))
"""
@app.route('/gold/<imgName>', methods=['GET', 'POST'])
def show_gold(imgName):
    if True:
        #process.process(imgName)
        result=predict(imgName)
        #g.ok = False
        #return render_template("Untitled-2.html",img=imgName)
        return jsonify({"result":result})
    else:
        return redirect(url_for('index'))
"""

if __name__=="__main__":
    app.run(host="0.0.0.0")