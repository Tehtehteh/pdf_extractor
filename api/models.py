from typing import List

from pydantic import BaseModel


class ExtractedDateModel(BaseModel):
    id: int
    extracted_date: str
    pdf_id: int
    extracted_context: str

