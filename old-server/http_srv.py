#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from scrapy import scrapy_key
from shutil import copyfile
from threading import Thread
from time import sleep
import cgi

PORT_NUMBER = 8080

def watch_thread(kw, watch_price, email):
    while True:
        print("Thread is watching ... ")
        print(watch_price)
        scrapy_key(kw, watch_price, email)
        sleep(5)


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

    def _response(self, resp_data):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(resp_data)

    #Handler for the GET requests
    def do_GET(self):
        if self.path=="/":

            try:
                f = open("scrapy.html") 
                data = f.read()
                f.close()
                self._response(data)
                return

            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD':'POST',
                'CONTENT_TYPE':self.headers['Content-Type']
            }
        )

        if self.path=="/search":
            fp = open("scrapy.html")
            file_content = fp.read()
            fp.close()

            result = scrapy_key(form["keyword"].value)
            result = file_content.replace("NONE", result)
            self._response(result)
            return          
        elif self.path == "/watch":
            watch_price = {}
            kw = form["searched_kw"].value
            for key in form.keys():
                if key != "email" and key != "searched_kw":
                    watch_price[key] = form[key].value
                else:
                    email = form[key].value

            
            thd = Thread(
                target=watch_thread,
                args=(kw, watch_price, email, )
            )
            thd.start()

            self._response("Start to watch items and will notify %s." % email)
            return

if __name__ == "__main__":
    try:
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print('Started httpserver on port ' , PORT_NUMBER)
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
