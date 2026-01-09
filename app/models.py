from pydantic import BaseModel
from typing import Optional, Dict, Any


class SubmitData(BaseModel):
    raw_data: Dict[str, Any]
    images: Optional[Dict[str, Any]] = None
