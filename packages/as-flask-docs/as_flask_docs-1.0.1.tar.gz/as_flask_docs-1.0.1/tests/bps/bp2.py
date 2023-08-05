from flask import Blueprint
from flask_siwadoc import Docs
from pydantic import BaseModel

class A(BaseModel):
    c: int = 3

class B(BaseModel):
    b: str = '2'

class D(BaseModel):
    d: str = 'd'

test2 = Blueprint("t2", __name__, url_prefix="/api/t2")
d = Docs(group='321')

@test2.get('')
@d(query=A, body=B, tags=['1', '2'], group='x')
def fun(query: A, body: B):
    return {'2': 'h'}


@test2.get('/d')
@d(query=D)
def fun2(query:D):
    return 'a'
