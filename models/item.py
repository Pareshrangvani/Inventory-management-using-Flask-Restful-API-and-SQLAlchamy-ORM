from db import db
from flask import request, render_template

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    category = db.Column(db.String(80))
    expiry_time = db.Column(db.DateTime)
    manufacturing_time = db.Column(db.DateTime)
    quantity = db.Column(db.Integer())
    file = db.Column(db.String(200))


    

    def __init__(self, name, category,expiry_time,manufacturing_time, quantity, file):
        self.name = name
        self.category = category
        self.expiry_time = expiry_time
        self.manufacturing_time = manufacturing_time
        self.quantity = quantity
        self.file = file

    def json(self):
        return {'name': self.name, 'category': self.category, 
                'expiry_time':self.expiry_time, 'manufacturing_time' : self.manufacturing_time,
                'quantity': self.quantity, 'file' : self.file }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit() 


def delete_many():
    ids = []
    ids = request.data['args']
    #ids = (30,)
    #ids = request.args.get('arg', type=int)
    
    db.session.query(ItemModel).filter(ItemModel.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    return {"message": "done."}, 200    
    

#pagination
def list_items(page):
    try:
        item_list = ItemModel.query.order_by(
            ItemModel.id.desc()
        ).paginate(page, per_page=5)
    except Exception:
        return(Exception)

    return render_template(
        'list.html',
        item_list=item_list,
        #form=form
    )

#code for image
class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text(100), nullable=False)
    name = db.Column(db.Text(100), nullable=False)
    mimetype = db.Column(db.Text(100), nullable=False)
#code for image end

