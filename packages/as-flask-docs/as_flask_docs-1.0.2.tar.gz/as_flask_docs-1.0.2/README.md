# flask_docs

在flask中支持**数据校验**和openapi(swagger)**文档自动生成**

**[flask_docs](https://github.com/Dorain-An/flask-docs)** fork自[flask-siwadoc](https://github.com/lzjun567/flask-siwadoc)，感谢原作者提供了主要功能的实现，原项目不支持flask中blueprint的使用因此魔改


## 特性

### 1、API接口自动生成文档

需要通过`CreateDoc(app)`,利用装饰器 `siwa.doc()`修饰flask视图函数，即可将该视图对应的路由加入openapi的paths中。

### 2、支持多种参数指定

可以将请求参数放置在 `query`、`path`、`header`、`cookie`、`body`5种不同的地方，完全支持openapi规范所定义的5种参数方式。

### 3、参数校验与自动转换

基于`pydantic`，请求参数可自动转换为对应的数据类型

### 4、ui切换

内置了`swagger`（默认）、`redoc`、`rapidoc`等多种UI界面，通过query参数"ui"控制

### 5、支持标签与分组

## 安装

```
pip install as-flask-docs
```

## 快速开始

```python
from flask import Flask
from flask_docs import CreateDoc

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

```

```
from flask import Blueprint
from flask_siwadoc import Docs
from pydantic import BaseModel

test1 = Blueprint("t1", __name__, url_prefix="/api/t1")
d = Docs(tags=["1"])

class A(BaseModel):
    a: int = 1

@test1.get('')
@d(body=A)
def fun(body: A):
    return 't1'
```

运行后，访问 [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs) 就可以看到openapi文档页面


### [更多用法介绍请移步原项目](https://github.com/lzjun567/flask-siwadoc)
