#!/usr/bin/python

import os
import web
import json
import time

urls = (
        '/','index',
        '/cpu','get_cpu_status',
        '/mem','get_mem_status'
)
app = web.application(urls, globals())

class index:
    def GET(self):
        return 'Hello, World!'

class get_cpu_status:
    def GET(self):
        while True:
            result = os.popen("mpstat -u -P ALL").read()
            return result
           # return json.dumps(result.split())

class get_mem_status:
    def GET(self):
        while True:
            data  = os.popen("free").read()
            jsonp  = json.dumps(data.split())
            return "showData("+jsonp+")"

if __name__ == "__main__":
    app.run()
