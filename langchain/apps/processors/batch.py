from typing import Any

from malevich.square import DF, Context, processor

from ..functions import df_prompt_format


@processor()
def send_messages_batch(input_variables: DF[Any], ctx: Context):
    """Send formatted messages to the AI Chatbot in a batch.

    Input:
        Two required inputs to this processor are:
            - input_variables: A dataframe with the variables to be used in the prompt template
            - prompt_template: A string with the prompt template

        While `input_variables` might came from the previous processor, `prompt_template` is
        a constant string defined in the app configuration.

    Configuration:
        `prompt_template` - a string with the prompt template. The template might contain
        variables in the following format: {variable_name}. The variables will be replaced
        with the values from the `input_variables` dataframe for each row.

    Details:
        Each row in the `input_variables` dataframe will be used to generate a single message
        to the AI Chatbot. The message will be generated by replacing the variables in the
        `prompt_template` with the values from the row. Messages will be sent to the AI Chatbot
        in a batch. The AI Chatbot will respond with a single message for each input message.
        The context is not shared between the messages: each message is processed independently.

    Output:
        A dataframe with the following columns:
            - result: AI Chatbot response to the input message

    Examples:
        Let's assume you want to come up with a name for your company services. You have
        a list of words that you want to use in the name. You want to generate a list of
        possible names by combining the words in different ways. You can use the following
        configuration:

        ```
        prompt_template: "Derive a name for our company services. The name should contain the word {word1} and the word {word2}."
        input_variables:
        | word1 | word2 |
        |-------|-------|
        | power | energy|
        | red   | panda |
        ```

        The processor will generate the following messages:

            First message:
            ```
            Derive a name for our company services. The name should contain the word power and the word energy.
            ```

            Second message:
            ```
            Derive a name for our company services. The name should contain the word red and the word panda.
            ```

        Each message will be sent to the AI Chatbot. The AI Chatbot will respond with a single
        message for each input message. The messages will be returned as a dataframe with a single
        column `result`:

        ```
        | result |
        |--------|
        | Power Energy Services |
        | Red Panda Services    |
        ```


    Args:
        input_variables (DF[Any]): A dataframe with the variables to be used in the prompt template

    Returns:
        DF[str]: A dataframe with the following columns:
            - result: AI Chatbot response to the input message
    """  # noqa: E501
    if 'prompt_template' not in ctx.app_cfg:
        raise ValueError(
            "The processor requires a `prompt_template` in the app configuration"
        )


    prompt_template = ctx.app_cfg.get("prompt_template")
    return df_prompt_format(input_variables, prompt_template, ctx.common.chat_model)