import pandas as pd
import pydantic
import torch
from malevich.square import DF, Context, processor, scheme
from transformers import Conversation, pipeline

from .models import AnswerQuestions


@scheme()
class QuestionInput:
    question: str
    """The content of the message"""
    context: str
    """A context for the question"""

class ConversationalPipelineConfig(pydantic.BaseModel):
    model: str = "deepset/roberta-base-squad2"
    """Name of the model to use in the pipeline"""


@processor()
def answer_questions(questions: DF[QuestionInput], context: Context[AnswerQuestions]):
    """
    Answers questions using HuggingFace Transformers.

    ## Input:

        A dataframe with columns:

        - `question` (string): The content of the question
        - `context` (string): A context for the question

    ## Output:

        It is a dataframe with columns:

            - score (float): The probability associated to the answer.
            - start (integer):
                The character start index of the answer
                (in the tokenized version of the input).
            - end (integer):
                The character end index of the answer
                (in the tokenized version of the input).
            - answer (string): The answer to the question.

    ## Configuration:

        - `model`: str, default "deepset/roberta-base-squad2".
            Name of the model to use in the pipeline.

    -----

    Args:

       questions: A collection of questions and contexts
       config: Configuration (see above)

    Returns:
        Collection with answers, scores and indices of the answers
    """
    try:
        config = ConversationalPipelineConfig(**context.app_cfg)
    except pydantic.ValidationError as err:
        context.logger.error(
            "Got an error while trying to get the config. "
            '. '.join([
                f"Field `{err['loc'][0]}` is not correct: {err['msg']}"
                for err in err.errors()
            ])
        )
        raise

    p = pipeline(
        model=config.model,
        task='question-answering',
        device='cuda' if torch.cuda.is_available() else 'cpu',
    )

    responses: list[Conversation] = p(questions.to_dict(orient='records'))
    if not isinstance(responses, list):
        # If the pipeline returns a single conversation,
        # we need to wrap it into a list
        responses = [responses]

    return pd.DataFrame(responses)
