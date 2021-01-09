from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import pickle

app=Flask(__name__)
app.secret_key="test"
app.permanent_session_lifetime=timedelta(minutes=5)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class User(db.Model):
        id=db.Column('id',db.Integer,primary_key=True)
        name=db.Column('name',db.String(100),nullable=False)
        email=db.Column('email',db.String(100),nullable=False,unique=True)
        password=db.Column('password',db.String(100),nullable=False)

        def __init__(self, name, email, password):
            self.name=name
            self.email=email
            self.password=password

@app.route('/')
@app.route('/home')
def home():
    if 'email' in session:
        email=session['email']
        #name=session['name']
        user=User.query.filter_by(email=email).first()
        return render_template('home.html',name=user.name,email=user.email)
    else:
        return redirect(url_for('login'))
    
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']

        session.permanent=True
        find_user=User.query.filter_by(email=email).first()
        if find_user:
            if password==find_user.password:
                session['name']=name
                session['email']=email
                return redirect(url_for('home'))
            else:
                flash('Invalid login')
                return render_template('login.html')
        else:
            session['name']=name
            session['email']=email
            user=User(name=name,email=email,password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    if 'admin' in session:
        if session['admin']:
            session.pop('admin',None)

    session.pop('email',None)
    session.pop('name',None)
    return redirect(url_for('login'))

@app.route('/adminlogin', methods=['POST','GET'])
def adminlog():
    if request.method=='POST':
        secretkey=request.form['secretkey']
        password=request.form['password']
        if password=='admin' and secretkey=='test':
            session['admin']=True
            return render_template('admin.html')
        else:
            return redirect(url_for('login'))
    else:
        return render_template('adminlogin.html')

@app.route('/admin')
def admin():
    if 'admin' in session:
        if session['admin']:
            return render_template('admin.html')
        else:
            return redirect(url_for('adminlog'))
    else :
        return redirect(url_for('adminlog'))

@app.route('/viewdb')
def viewdb():
    value=User.query.all()
    return render_template('view.html',value=value)

@app.route('/changePassword',methods=['POST','GET'])
def pwdchange():
    email=session['email']
    user=User.query.filter_by(email=email).first()
    if request.method=='GET':
        return render_template('pwdchange.html')
    else:
        current=request.form['current']
        new=request.form['new']
        if current==user.password:
            user.password=new
            db.session.commit()
            flash('Password changed successfully')
            return redirect(url_for('home'))
        else:
            flash('Invalid password')
            return render_template('pwdchange.html')

@app.route('/myModelReview',methods=['POST','GET'])
def model():
    m=None
    with open('model_pickle','rb') as f:
        m=pickle.load(f)
    if request.method=='GET':
        return render_template('model.html')
    else:
        x=int(request.form['x'])
        
        flash('output:'+str(m.predict([[x]])[0]))
        return render_template('model.html')
    



db.create_all()
app.run(debug=True,use_reloader=False,port="800")
