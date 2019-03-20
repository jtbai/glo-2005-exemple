from flask import Flask, render_template, request
from mysql.connector import connect
from json import loads
import requests

URL_API_PHOTO_CHIEN = "https://dog.ceo/api/breeds/image/random"
application = Flask('glo2005')

MYSQL_URI = "localhost"
PORT = "1337"
USERNAME = "root"
PASSWORD = None
DATABASE_NAME = "what_is_it"

database_connector = connect(host=MYSQL_URI, port=PORT, user=USERNAME, password=PASSWORD, database=DATABASE_NAME)


@application.route('/')
def index():
    return "<a href=/chien>photo de chien</a>"

@application.route('/chien')
def photo_de_chien():
    reponse_api_photo_chien = requests.get(URL_API_PHOTO_CHIEN)
    json_de_lapi = loads(reponse_api_photo_chien.text)
    json_de_lapi["message"]

    return render_template('image_animal.html', url =json_de_lapi["message"], animal = "chien" )

@application.route("/vote", methods=["POST"])
def vote():
    add_vote = ("INSERT INTO vote "
                    "(image_url, value)"
                    "VALUES (%s, %s)")

    vote_values = (request.values['image_url'], request.values['vote_value'])
    cursor = database_connector.cursor()
    cursor.execute(add_vote, vote_values)
    database_connector.commit()

    return photo_de_chien()

@application.route("/vote/<animal>", methods=["GET"])
def get_vote(animal):
    select_animal = ("SELECT image_url FROM vote "
                    "WHERE value = %s")

    vote_values = (animal,)
    cursor = database_connector.cursor()
    cursor.execute(select_animal, vote_values)
    output = ""
    for vote in cursor:
        output += "<img src={}><br>".format(vote[0])

    return output

    return photo_de_chien()

application.run('0.0.0.0',8000)