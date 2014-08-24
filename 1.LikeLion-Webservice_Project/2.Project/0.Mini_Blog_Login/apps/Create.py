
__author__ = 'jeong-yonghan'

from models import Model
from flask.ext.sqlalchemy import db


model = Model(
    field1 = value1,
    field2 = value2
)

db.session.add(model)
db.session.commit()