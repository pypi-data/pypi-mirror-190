from flask import Flask, request, Blueprint
from flask.views import MethodView
from pydantic import BaseModel

from importlib import import_module
from flask_siwadoc import CreateDoc, Docs


app = Flask(__name__)
models = {}
modules = import_module('tests.bps')

for name in dir(modules):
    instance = getattr(modules, name)
    if isinstance(instance, Blueprint):
        app.register_blueprint(instance)
    if isinstance(instance, Docs):
        models.update(instance.models)

CreateDoc(app, title="flask_docs", description="一个自动生成openapi文档的库", models=models)


if __name__ == '__main__':
    app.run()
