#working code
from flask import Flask, request, Response, render_template, redirect, flash
from flask_restful import Api
from flask_jwt import JWT
from werkzeug.utils import secure_filename
from flask_paginate import Pagination
#import os


from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from models.item import Img, ItemModel
from models.item import delete_many, list_items


app = Flask(__name__)   

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

#for img size
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.before_first_request
def create_tables():
    db.create_all()

#home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/deletemany', methods=['GET', 'DELETE'])
def deletemanyitem():
    delete_many()

#for pagination
class PageResult:
   def __init__(self, data, page = 1, number = 5):
     self.__dict__ = dict(zip(['data', 'page', 'number'], [data, page, number]))
     self.full_listing = [self.data[i:i+number] for i in range(0, len(self.data), number)]
   def __iter__(self):
       try:
          for i in self.full_listing[self.page-1]:
              yield i
       except Exception:
          print("end of lines")

   def __repr__(self): #used for page linking
     return "/displayitems/{}".format(self.page+1) #view the next page

#display items
@app.route('/displayitems/<int:pagenum>')
def displayitems(pagenum):
  item_list = ItemModel.query.all()
  return render_template('displayitems.html', listing = PageResult(item_list, pagenum))

#list all items without page in table
@app.route('/itemlist')  
def itemlist():  
   return render_template('items.html', 
                item_list = ItemModel.query.all())
                #item_list = ItemModel.query().limit(3).offset(1) )

# code for redirect.
@app.route('/upload_item', methods=['POST'])
def upload_item():
    return redirect("http://localhost:5000/item/{}".format(request.form['name']),code=307)


jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(Item, '/item/<string:name>' , methods=['GET' , 'POST', 'DELETE', 'PUT'])
#api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)


