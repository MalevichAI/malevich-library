import uuid

import pandas as pd
import pydantic
import torch
from malevich.square import DF, Context, processor, scheme
from transformers import Conversation, pipeline

from .models import ContinueConversation


@scheme()
class DialogMessageInput:
    content: str
    """The content of the message"""
    role: str
    """An identifier of the role of the message. It can be "user" or "assistant"."""
    # dialog_id: Optional[str] = None

@processor()
def continue_conversation(
    message: DF[DialogMessageInput], context: Context[ContinueConversation]
    ):
    """
    Starts or continues a conversation with the given messages using HuggingFace Transformers.

    ## Input:

        A dataframe with columns:

        - `content` (string): The content of the message
        - `role` (string):
            An identifier of the role of the message.
            It can be "user" or "assistant".
        - `dialog_id` (string, optional):
            An identifier of the dialog.
            If not provided, a new dialog will be created.

    ## Output:

        Output contains all the input messages and the responses from the model.
        It is a dataframe with columns:

        - `dialog_id` (string): An identifier of the dialog
        - `content` (string): The content of the message
        - `role` (string): An identifier of the role of the message

    ## Configuration:

        - `model`: str, default "facebook/blenderbot-400M-distill".
            Name of the model to use in the pipeline.
        - `min_length_for_response`: int, default 32.
            The minimum length (in number of tokens) for a response.
        - `minimum_tokens`: int, default 10.
            The minimum length of tokens to leave for a response.

    -----

    Args:
        message: input collection with messages
        context (dict): configuration (see above)

    Returns:
        Collection with messages and responses
    """

    p = pipeline(
        # https://huggingface.co/docs/transformers/v4.37.2/en/main_classes/pipelines#transformers.Conversation
        model=context.app_cfg.model,
        task='conversational',
        device='cuda' if torch.cuda.is_available() else 'cpu',
    )


    if 'dialog_id' not in message.columns:
        message.insert(0, 'dialog_id', [
            uuid.uuid4() for _ in range(len(message.index))
        ])

    message[message.dialog_id.isna()].dialog_id = [
        uuid.uuid4() for _ in range(len(message[message.dialog_id.isna()].index))
    ]

    conversations = []
    for dialog_id, group in message.groupby('dialog_id'):
        messages = group[['content', 'role']].to_dict(orient='records')
        conversations.append(Conversation(messages, dialog_id))

    context.logger.info(f"Got {len(conversations)} conversations")
    responses: list[Conversation] = p(conversations)

    if not isinstance(responses, list):
        # If the pipeline returns a single conversation,
        # we need to wrap it into a list
        responses = [responses]
    context.logger.info(f"Got {len(responses)} responses from model")

    output_records = []
    for conversation in responses:
        try:
            context.logger.info(
                f"Conversation: {conversation.uuid}, "
                f"n messages: {len(conversation.messages)}"
            )
            for message in conversation.messages:
                output_records.append({
                    'dialog_id': str(conversation.uuid),
                    'content': message['content'],
                    'role': message['role']
                })
        except Exception:
            context.logger.error(
                "Encountered an error while processing the response. "
                f"type(conversation): {type(conversation) if conversation else None}. "
                f"dir(conversation): {dir(conversation) if conversation else None}. "
            )
            raise

    return pd.DataFrame(output_records)
