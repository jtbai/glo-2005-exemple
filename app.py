from flask import Flask, render_template, request
from json import loads
from infrastructure import VoteRepository
import requests

URL_API_PHOTO_CHIEN = "https://dog.ceo/api/breeds/image/random"
application = Flask('glo2005')
vote_repository = VoteRepository()

@application.route('/')
def index():
    images = vote_repository.get_images()
    return render_template('index.html', images=images)

@application.route('/chien')
def photo_de_chien():
    reponse_api_photo_chien = requests.get(URL_API_PHOTO_CHIEN)
    json_de_lapi = loads(reponse_api_photo_chien.text)
    json_de_lapi["message"]

    return render_template('vote_page.html', url =json_de_lapi["message"], animal = "chien" )

@application.route("/vote", methods=["POST"])
def vote():
    vote_dto = {
        'image_url':request.values['image_url'],
        'vote_value':request.values['vote_value']
    }
    vote_repository.insert_vote(vote_dto)

    return photo_de_chien()

@application.route("/vote", methods=["GET"])
def get_vote():
    votes = vote_repository.get_votes(request.values['animal'])
    output = ""
    for vote in votes:
        output += "<img src={}><br>".format(vote[0])

    return output


@application.route("/image/<image_id>", methods=["GET"])
def get_photo(image_id):
    information = vote_repository.get_image_information(image_id)
    votes = vote_repository.get_votes_for_image(image_id)
    return render_template("image_animal.html", url =information['image_url'], votes = votes, animal=information['animal'])


application.run('0.0.0.0',8080)