# generated by datamodel-codegen:
#   filename:  answer_questions_model.json
#   timestamp: 2024-03-06T12:55:54+00:00

from __future__ import annotations
from malevich.square import scheme

from pydantic import BaseModel, Field


scheme()
class AnswerQuestions(BaseModel):
    model: str = Field(..., description='default "deepset/roberta-base-squad2"')