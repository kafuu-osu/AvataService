from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer

import os
from flask import Flask, send_file, jsonify

app = Flask('avatar-server')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

avatarDir = "avatars"


def checkDir():
    if not os.path.exists(avatarDir):
        os.makedirs(avatarDir)


def avatar(uid=-1):
    return "{}/{}.png".format(avatarDir, uid)


@app.route("/status")
def serverStatus():
    return jsonify({"response": 200,"status": 1})


@app.route("/<int:uid>")
def serveAvatar(uid):
    if not os.path.isfile(avatar(uid)): uid = -1
    return send_file(avatar(uid))


@app.errorhandler(404)
def page_not_found(error):
    return send_file(avatar())


if __name__ == '__main__':
    print('\n\n\033[1;33mAVATAR SERVICE STARTED!\033[0m\n')
    checkDir()
    WSGIServer(("0.0.0.0", 5000), app).serve_forever()
