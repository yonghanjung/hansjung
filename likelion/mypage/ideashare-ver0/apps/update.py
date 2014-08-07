from flask.ext.sqlalchemy import db
from models import Model

__author__ = 'jeong-yonghan'

# UPDATE

model = Model.query.get(id)
model.field1 = value1_modified

db.session.commit()