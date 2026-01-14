from fastapi import FastAPI
from app.database import Database
from app.models import SubmitData

app = FastAPI(title="Pereval API")

db = Database()


@app.post("/submitData")
def submit_data(data: SubmitData):
    pereval_id = db.add_pereval(
        raw_data=data.raw_data,
        images=data.images
    )

    return {
        "status": 200,
        "message": "Отправлено успешно",
        "id": pereval_id
    }

@app.get("/submitData/{pereval_id}")
def get_submit_data(pereval_id: int):
    result = db.get_pereval_by_id(pereval_id)
    if result is None:
        return {"message": "Запись не найдена"}
    return result

@app.get("/submitData/")
def get_submit_data_by_email(user__email: str):
    return db.get_perevals_by_email(user__email)

@app.patch("/submitData/{pereval_id}")
def update_submit_data(pereval_id: int, data: SubmitData):
    state, message = db.update_pereval(
        pereval_id=pereval_id,
        new_raw_data=data.raw_data,
        new_images=data.images
    )

    return {
        "state": state,
        "message": message
    }