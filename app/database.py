import os
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.getenv("FSTR_DB_HOST"),
            port=os.getenv("FSTR_DB_PORT"),
            user=os.getenv("FSTR_DB_LOGIN"),
            password=os.getenv("FSTR_DB_PASS"),
            dbname=os.getenv("FSTR_DB_NAME"),
        )

    def add_pereval(self, raw_data: dict, images: dict | None = None) -> int:

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pereval_added (date_added, raw_data, images, status)
                VALUES (NOW(), %s, %s, 'new')
                RETURNING id;
                """,
                (Json(raw_data), Json(images)),
            )
            pereval_id = cursor.fetchone()[0]
            self.connection.commit()
            return pereval_id
