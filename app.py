from flask import Flask, request, redirect , session, g
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'dhaneesh'

#database framework python
db = SQLAlchemy(app)

#database
#User_acc->stores user data
class User_acc(db.Model):
    __tablename__ = 'user_acc'
    id = db.Column(db.Integer,primary_key=True)
    Password = db.Column(db.String(50),nullable=False)
    Email_id = db.Column(db.String(200),nullable=False)
    Date_created=db.Column(db.DateTime,default=datetime.utcnow)
    Secret = db.Column(db.String(200))

    def __repr__(self) -> str:
        return str(self.id)

#Comments->store comment data
class Comments(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,nullable=False)
    Comment = db.Column(db.String(500))

def connect_db():
    return sqlite3.connect('database.db')

@app.before_request
def before_request():
    if 'username' in session:
        g.user = session['username']

@app.route('/',methods=['POST','GET'])
@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('mail')
        pwd = request.form.get('pwd')
        #checking if user present
        selectapplicant = User_acc.query.filter_by(Email_id=email).first()
        if selectapplicant and selectapplicant.Password == pwd:
            session["username"]=selectapplicant.id
            return redirect('/comment_page')
        else:
            message = "User with Given Credentials not found"
            return render_template('login.html',message=message)
    else:
        return render_template('login.html',message="")

@app.route('/register',methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        secret = request.form['secret']
        password= request.form['password']
        email= request.form['email']
        query =User_acc.query.filter_by(Email_id=email).first()
        if(query!=None):
            #checking if user already present
            message = "Email-id already available.Please Login!"
            return render_template('login.html',message=message)
        data = User_acc(Password=password,Email_id=email,Secret=secret)
        try:
            #adding new user
            db.session.add(data)
            db.session.commit() 
            user = User_acc.query.filter_by(Email_id=email).first()
            session["username"]=user.id
            return render_template('login.html',message="")
        except:
            return "error adding values to database"
    else:
        return render_template('register.html')
    
@app.route('/forget_password',methods=['POST', 'GET'])
def forget_password():
    if request.method == 'POST':
        secret = request.form['secret']
        email= request.form['mail']
        query =User_acc.query.filter_by(Email_id=email,Secret=secret).first()
        if(query!=None):
            message = "Your password for "+email+" is "+query.Password
            return render_template('login.html',message=message)
        else:
            message="No such email-id"
            return render_template('login.html',message=message)
    else:
        return render_template('forget_password.html')
    
@app.route('/comment_page',methods=['POST', 'GET'])
def comment_page():
    if request.method == 'POST':
        comment = request.form['data']
        print(comment)
        if comment:
            data = Comments(Comment=comment,user_id=int(g.user))
            try:
                db.session.add(data)
                db.session.commit() 
                d=[]
                cur=0
                for c, u in db.session.query(Comments, User_acc).filter(Comments.user_id == User_acc.id).all():
                    d.append(dict())
                    d[cur]['comment']=c.Comment
                    d[cur]['email']=u.Email_id
                    cur+=1
                return render_template('comment_page.html',d=d)
            except:
                return "error adding values to database"
        else:
            return redirect('/comment_page')
    else:
        d=[]
        cur=0
        for c, u in db.session.query(Comments, User_acc).filter(Comments.user_id == User_acc.id).all():
            d.append(dict())
            d[cur]['comment']=c.Comment
            d[cur]['email']=u.Email_id
            cur+=1
        return render_template('comment_page.html',d=d)

@app.route('/comment_page_user',methods=['POST', 'GET'])
def comment_page_user():
    if request.method=='GET':
        d=[]
        cur=0
        for c, u in db.session.query(Comments, User_acc).filter(Comments.user_id == User_acc.id).all():
            if(u.id==int(g.user)):
                d.append(dict())
                d[cur]['comment']=c.Comment
                d[cur]['email']=u.Email_id
                cur+=1
        return render_template('comment_page.html',d=d)

@app.route('/logout')
def logout():
   session.pop('username', None)
   return render_template('login.html',message="")

if __name__ == "__main__":
    app.run(debug=True)