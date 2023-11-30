from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel
from slack_sdk import WebClient


@scheme()
class SlackInput(BaseModel):
    channel_id: str
    message: str

@processor()
def send_message(df: DF[SlackInput], context: Context):
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
