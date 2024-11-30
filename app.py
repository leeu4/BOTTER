from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime,jwt
from creation import SECRET,PORT,DB_URL
import requests as rq
import bs4
import time
import json

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class User(db.Model):
    id  =      db.Column(db.Integer,primary_key=True)
    username=  db.Column(db.String(100),unique=True,nullable=False)
    email=     db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),unique=False,nullable=False)

    def __repr__(self):
        username = self.username
        email = self.email
        id = self.id
        return f"{id , username , email}"
class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    isInstock=db.Column(db.Boolean,default=True)
    
    def __repr__(self):
        name = self.name
        isinstock = self.isInstock
        data = {
            "name":name,
            "isinstock":isinstock
        }
        return f"{json.dumps(data,indent=2)}"
        
        

@app.route("/register",methods=["POST"])
def Register():
    data = request.get_json()
    
    userBy_username = User.query.filter(User.username == data["username"]).first()
    userBy_email = User.query.filter(User.email == data["email"]).first()

    if userBy_email == None and userBy_username == None:
        user = User(username=data["username"],email=data["email"],password=data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"User Created Successfully"}),200
    
    else:    
        return jsonify({"message":"Username or Email is already used"}),400
    

@app.route("/login",methods=["POST"])
def Login():
    time.sleep(2)
    data = request.get_json()
    user_search = User.query.filter(User.username == data["username"]).first()
    if user_search == None:
        return jsonify({"message":"Username or password is wrong"}),400
    elif data["password"] == user_search.password and data["username"] == user_search.username:
        payload = {
            "id":user_search.id,
            "username":user_search.username,
            "exp":int((datetime.datetime.utcnow() + datetime.timedelta(hours=1)).timestamp())
        }
        token = jwt.encode(payload,SECRET,algorithm="HS256")
        return jsonify({"token":token,"name":user_search.username,"message":f"Welcome back {user_search.username}"}),200
    else:
        return jsonify({"message":"Username or password is wrong"}),400

@app.route("/search",methods=["GET"])
def search():
    db.session.query(Product).delete()
    db.session.commit()
    req = rq.get("https://www.dzrt.com/en-sa/category/nicotine-pouches",headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36'
    })

    if req.status_code != 200:
        raise RuntimeError(f"dzrt status code is {req.status_code}")
    html = req.text

    
    all_names = []

    parser = bs4.BeautifulSoup(html,"html.parser")
    cards = parser.find_all("div",attrs={"class":"relative bg-white px-2.5 pb-3 pt-6"})

    for card in cards:
        names = card.find_next("span",attrs={"class":"text-3.5 font-bold leading-5 text-custom-black-900"})
        all_names.append(names.text)

# To filter the in stock or out of stock products
    out_of_stock = [
        card for card in cards if card.find("button",attrs={"disabled":True})
    ]
    out_of_stock_names = []

    # To have out of stock products names
    for card in out_of_stock:
        names = card.find_next("span",attrs={"class":"text-3.5 font-bold leading-5 text-custom-black-900"})
        out_of_stock_names.append(names.text)
    for name in all_names:
        if name in out_of_stock_names:
            product_to_db = Product(name=name,isInstock=False)
            db.session.add(product_to_db)
            db.session.commit()
            
        else:
            product_to_db = Product(name=name,isInstock=True)
            db.session.add(product_to_db)
            db.session.commit()

    return f"{Product.query.all()}"
    
if __name__ == "__main__":

    app.run(port=PORT)