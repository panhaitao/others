
## 参考

* 使用ajax完成python flask前端与后台数据的交互 <https://blog.csdn.net/just_so_so_fnc/article/details/77984315>
* 在Flask开发RESTful后端时，前端请求会遇到跨域的问题。下面是解决方法。Python版本：2.7.12
* https://flask-cors.corydolphin.com/en/latest/api.html#using-cors-with-cookies
* 前端常见跨域请求方案 https://segmentfault.com/a/1190000011145364

下载flask_cors

pip install flask-cors

使用flask_cors的CORS，代码示例

```
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

```
