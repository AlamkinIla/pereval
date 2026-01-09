from app.database import Database

db = Database()

test_id = db.add_pereval(
    raw_data={"test": "data"},
    images={"images": []}
)

print("Создана запись с id:", test_id)
