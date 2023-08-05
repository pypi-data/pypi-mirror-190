from flask import Blueprint
from flask_siwadoc import Docs
from pydantic import BaseModel

test1 = Blueprint("t1", __name__, url_prefix="/api/t1")
d = Docs(group='123')

class A(BaseModel):
    a: int = 1

@test1.get('')
@d(body=A, tags=['1'])
def fun(body: A):
    return {'2': 'h'}
