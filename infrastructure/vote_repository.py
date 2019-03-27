from mysql.connector import connect

class VoteRepository:
    MYSQL_URI = "localhost"
    PORT = "1337"
    USERNAME = "root"
    PASSWORD = None
    DATABASE_NAME = "what_is_it"

    def __init__(self):
        self.connector = connect(host=self.MYSQL_URI, port=self.PORT, user=self.USERNAME, password=self.PASSWORD, database=self.DATABASE_NAME)

    def insert_vote(self, vote_dto):
        add_vote_request = ("INSERT INTO vote "
                        "(image_url, value)"
                        "VALUES (%s, %s)")

        vote_values = (vote_dto['image_url'], vote_dto['vote_value'])
        cursor = self.connector.cursor()
        cursor.execute(add_vote_request, vote_values)
        self.connector.commit()

    def get_votes(self, animal):
        select_animal = ("SELECT image_url FROM vote "
                         "WHERE value = %s")
        vote_values = (animal,)
        cursor = self.connector.cursor()
        cursor.execute(select_animal, vote_values)

        return [vote for vote in cursor]


