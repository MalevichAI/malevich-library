# generated by datamodel-codegen:
#   filename:  answer_questions_model.json
#   timestamp: 2024-03-05T17:40:30+00:00

from __future__ import annotations

from pydantic import BaseModel, Field


class AnswerQuestions(BaseModel):
    model: str = Field(..., description='default "deepset/roberta-base-squad2"')
