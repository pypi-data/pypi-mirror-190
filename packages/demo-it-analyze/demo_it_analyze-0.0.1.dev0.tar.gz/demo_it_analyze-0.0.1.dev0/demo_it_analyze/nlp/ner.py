import spacy
from typing import List
from pydantic import BaseModel


nlp = spacy.load("it_core_news_sm")


class Entity(BaseModel):
    text: str
    start: int
    end: int
    label: str


def compute_ner(text: str) -> List[Entity]:
    doc = nlp(text)
    return [
        Entity(text=ent.text, start=ent.start, end=ent.end, label=ent.label_)
        for ent in doc.ents
    ]
