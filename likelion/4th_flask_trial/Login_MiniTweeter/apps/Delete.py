from flask.ext.sqlalchemy import db
__author__ = 'jeong-yonghan'

from models import Model


model = Model.query.get(id)
db.session.delete(model)
db.session.commit()