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