from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel
from slack_sdk import WebClient

from .models import SendMessage


@scheme()
class SlackInput(BaseModel):
    channel_id: str
    message: str

@processor()
def send_message(df: DF[SlackInput], context: Context[SendMessage]):
    """Sends message to specified Slack channel

    ## Input:

        A dataframe with a column:
        - `channel_id` (str): contains ids of the channels.
        - `message` (str): that contains messages to send. Each row is a separate message.

    ## Output:

        A dataframe with a column:
        - `channel_id` (str): contains ids of the channels.
        - `message` (str): that contains messages that was sent. Each row is a separate message.

    ## Configuration:

        - `token`: str.
            Slack token.

    -----

    Args:

        df (DF[SlackInput]): a dataframe with a column `channel_id`
            that contains ids of the channels and a column `message`
            that contains messages to send. Each row is a separate message
        context (Context): a context object that contains
            the configuration and the methods to work with files

    Returns:
        DF[SlackInput]: a dataframe with two columns: `channel_id` and `message`.
            The `channel_id` column contains the id of the channel
            and the `message` column contains the message that was sent.
    """  # noqa: E501
    token = context.app_cfg.get('token')
    client = WebClient(token=token)
    for _, row in df.iterrows():
        channel_id = row['channel_id']
        message = row['message']
        client.chat_postMessage(
            channel=channel_id,
            text=message,
        )
    return df
