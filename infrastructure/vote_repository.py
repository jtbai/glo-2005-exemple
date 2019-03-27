from mysql.connector import connect
import hashlib



class VoteRepository:
    # MYSQL_URI = "localhost"
    # PORT = "1337"
    MYSQL_URI = "ma_bd"
    PORT = "3306"
    USERNAME = "root"
    PASSWORD = None
    DATABASE_NAME = "what_is_it"

    def __init__(self):
        self.connector = connect(host=self.MYSQL_URI, port=self.PORT, user=self.USERNAME, password=self.PASSWORD, database=self.DATABASE_NAME)

    def insert_vote(self, vote_dto):
        add_vote_request = ("INSERT INTO vote "
                        "(image_url, value, image_id)"
                        "VALUES (%s, %s, %s)")
        md5_converter = hashlib.md5()
        md5_converter.update(vote_dto['image_url'].encode("UTF-8"))
        vote_values = (vote_dto['image_url'], vote_dto['vote_value'], md5_converter.hexdigest())
        cursor = self.connector.cursor()
        cursor.execute(add_vote_request, vote_values)
        self.connector.commit()

    def get_votes(self, animal):
        select_animal = ("SELECT image_url FROM vote "
                         "WHERE value = %s")
        vote_values = (animal,)
        cursor = self.connector.cursor()
        cursor.execute(select_animal, vote_values)

        return [{'image_url':vote[0]} for vote in cursor]

    def get_images(self):
        select_query = "SELECT DISTINCT image_id, image_url FROM vote "
        cursor = self.connector.cursor()
        cursor.execute(select_query)

        return [{'image_id': vote[0], 'image_url': vote[1]} for vote in cursor]

    def get_image_information(self, image_id):
        select_image = ("SELECT image_url, value FROM vote "
                         "WHERE image_id = %s LIMIT 0,1")

        select_values = (image_id,)
        cursor = self.connector.cursor()
        cursor.execute(select_image, select_values)
        reponse = cursor.fetchall()[0]

        return {'image_url': reponse[0], 'animal': reponse[1]}


    def get_votes_for_image(self, image_id):
        vote_query = ("SELECT value, count(value) FROM vote "
                         "WHERE image_id = %s GROUP BY value")
        select_values = (image_id,)
        cursor = self.connector.cursor()
        cursor.execute(vote_query, select_values)

        return [{'animal': reponse[0], 'nb_votes':reponse[1]} for reponse in cursor ]





