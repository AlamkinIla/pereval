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

    def get_pereval_by_id(self, pereval_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, date_added, raw_data, images, status
                FROM pereval_added
                WHERE id = %s
                """,
                (pereval_id,)
            )
            result = cursor.fetchone()

        if result is None:
            return None

        return {
            "id": result[0],
            "date_added": result[1],
            "raw_data": result[2],
            "images": result[3],
            "status": result[4]
        }

    def get_perevals_by_email(self, email: str):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, date_added, raw_data, images, status
                FROM pereval_added
                WHERE raw_data - > 'user' ->>'email' = %s
                """,
                (email,)
            )
            rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "date_added": row[1],
                "raw_data": row[2],
                "images": row[3],
                "status": row[4]
            })

        return result

    def update_pereval(self, pereval_id: int, new_raw_data: dict, new_images: dict):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT raw_data, status FROM pereval_added WHERE id = %s",
                (pereval_id,)
            )
            row = cursor.fetchone()

            if row is None:
                return 0, "Запись не найдена"

            old_raw_data, status = row

            if status != "new":
                return 0, "Редактирование запрещено: статус не 'new'"

            # запрещённые поля
            user_fields = ["email", "fam", "name", "otc", "phone"]
            for field in user_fields:
                if (
                        new_raw_data.get("user", {}).get(field)
                        != old_raw_data.get("user", {}).get(field)
                ):
                    return 0, f"Поле user.{field} изменять нельзя"

            cursor.execute(
                """
                UPDATE pereval_added
                SET raw_data = %s,
                    images   = %s
                WHERE id = %s
                """,
                (Json(new_raw_data), Json(new_images), pereval_id)
            )

            self.conn.commit()

        return 1, "Запись успешно обновлена"