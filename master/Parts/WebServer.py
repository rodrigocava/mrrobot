from CarCamera import CameraStream
import Utils

from tornado.ioloop import PeriodicCallback
import tornado.websocket
import tornado.web
import webbrowser
import threading
import hashlib
import base64
import time
import io
import os

class LocalServer(tornado.web.Application):
    def __init__(self,params,_car):
        Utils.print_log("Init. server",1)

        self.require_login = params['require_login']
        self.cookie = params['cookie']
        self.port = params['port']
        self.car = _car

        self.password = Utils.get_password()
        self.camera = self.car.camera.picam
        self.cookie_secret = self.password
        
        root = Utils.get_root()
        path = os.path.join(root, '../../master')

        self.handlers = [
            (r"/", IndexHandler),
            (r"/login", LoginHandler),
            (r"/websocket", WebSocket),
            (r"/static/config/password.txt", ErrorHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': path})
        ]

    def stream(self):
       settings = {'debug': True, 'cookie_secret':self.cookie_secret}
       super(LocalServer,self).__init__(self.handlers, **settings)

       #Start camera stream
       CameraStream(self.car)

       self.listen(self.port)
       tornado.ioloop.IOLoop.instance().start()


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        if self.application.require_login and not self.get_secure_cookie(self.application.cookie):
            self.redirect("/login")
        else:
            self.render("../server/index.html", port=self.application.port, mode=self.application.car.train_mode)

class ErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.send_error(status_code=403)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("../server/login.html")

    def post(self):
        password = self.get_argument("password", "")
        if hashlib.sha512(password).hexdigest() == self.application.password:
            self.set_secure_cookie(self.application.cookie, str(time.time()))
            self.redirect("/")
        else:
            time.sleep(1)
            self.redirect(u"/login?error")

class WebSocket(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        # Start an infinite loop when this is called
        if message == "read_camera":
            if not self.application.require_login or self.get_secure_cookie(self.application.cookie):
                self.camera_loop = PeriodicCallback(self.loop, 100) # 10 fps
                self.camera_loop.start()
            else:
                print("Unauthenticated websocket request")

        # Movement message
        elif (message in ["BACKWARDS","FORWARD","LEFT","RIGHT"]):
            direction = [message]
            if (message in ["LEFT","RIGHT"]):
                direction = [message,'FORWARD']

            if(self.application.car.train_mode):
                self.application.car.log_and_move(direction)
            else:
                self.application.car.move(direction)

        # Stop message
        elif (message[5:] in ["BACKWARDS","FORWARD","LEFT","RIGHT"]):
            self.application.car.stop()

        elif (message == 'self_drive'):
            Utils.print_log("\nDriiive, "+ self.application.car.name +"!!!!",1)
            self.application.car.drive = True
            self.application.car.self_drive()

        elif (message == 'manual'):
            Utils.print_log("Manual drive",1)
            self.application.car.drive = False

        elif (message == 'save_frames'):
            Utils.print_log("Saving frames",1)
            self.application.car.train_data.save()
            self.application.car.drive = False


        else:
            Utils.print_log("Unsupported function: " + message,1)

    def loop(self):
        """Sends camera images in an infinite loop."""
        try:
            self.write_message(base64.b64encode(self.application.car.camera.last_img_bytes))
        except tornado.websocket.WebSocketClosedError:
            self.camera_loop.stop()
