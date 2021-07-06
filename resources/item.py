from flask import request, flash, render_template
from flask.helpers import url_for
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import Img, ItemModel
from datetime import datetime
import os
from werkzeug.utils import secure_filename


class Item(Resource):
    parser = reqparse.RequestParser()                   
    #for display item
    
    #@jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            #calculation of expiry
            exp_obj = item.expiry_time
            current_time = datetime.now()


            diff = exp_obj - current_time
            diff_minutes = diff.total_seconds() / 60
            if int(diff_minutes) >0 :
                is_expired = False
            else:
                is_expired = True
            #image_insertion
            img_url = str(item.file)
            tempv = r'F:\Maruti Techlab Files\rest-api-sections-master\section6\static\uploads'
            imgurl = url_for('static', filename = ('uploads/' + img_url))
            final_url = tempv + img_url
            item_dict = {'name' : item.name, 'category' : item.category,
                        'is_expired' :is_expired , 'quantity' : item.quantity,
                        'img_url' : imgurl}

            return item_dict

            #return item.json()
        return {'message': 'Item not found'}, 404

    #for storing the item
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400


        #img_store
        file = request.files['file']
        filename = file.filename
        if 'file' not in request.files:
            print('No file part')
		
        if file.filename == '':
            print('No image selected for uploading')

# img_url = "F:\Maruti Techlab Files\rest-api-sections-master\section6\static\uploads" + filename
        file.save(os.path.join('static/uploads/', filename))
        item = ItemModel(name, request.form['category'],request.form['expiry_time'],
                        request.form['manufacturing_time'],request.form['quantity'], filename)


        try:
            item.save_to_db()

        except:
            return {"message": "An error occurred inserting the item."}, 500

        return {'message': 'Item successfully added'}, 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.quantity = data['quantity']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()

#for displaying all items
class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

class DeleteMany(Resource):
    def delete(self):
        pass