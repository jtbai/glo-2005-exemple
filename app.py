from flask import Flask
from json import loads
import requests

URL_API_PHOTO_CHIEN = "https://dog.ceo/api/breeds/image/random"
application = Flask('glo2005')


@application.route('/')
def index():
    return "<a href=/chien>photo de chien</a>"

@application.route('/chien')
def photo_de_chien():
    reponse_api_photo_chien = requests.get(URL_API_PHOTO_CHIEN)
    json_de_lapi = loads(reponse_api_photo_chien.text)
    json_de_lapi["message"]

    return "<img src=" + json_de_lapi["message"] +">"


application.run('0.0.0.0',8000)