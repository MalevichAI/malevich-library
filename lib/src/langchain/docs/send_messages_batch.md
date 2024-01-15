# Send Messages Batch

## General Component Purpose

The "Send Messages Batch" component is designed to automate the process of sending formatted messages to an AI Chatbot in batches. It is particularly useful for generating and sending multiple messages based on a set of input variables and a predefined prompt template. This component is ideal for users who need to interact with an AI Chatbot for tasks such as generating ideas, names, or any other creative content where batch processing is beneficial.

## Input and Output Format

### Input Format

The component requires the following inputs:

1. **input_variables**: A dataframe containing the variables to be used in the prompt template.
2. **prompt_template**: A string defined in the app configuration that serves as the template for message generation.

### Output Format

The output of this component is a dataframe with a single column:

- **result**: Contains the AI Chatbot's response to each input message.

## Configuration Parameters

| Parameter Name   | Expected Type | Description                                              |
|------------------|---------------|----------------------------------------------------------|
| prompt_template  | String        | The template for generating messages to send to the AI Chatbot. |

## Detailed Parameter Descriptions

- **prompt_template**: This is a string that contains the template used to generate messages. It can include placeholders for variables in the format `{variable_name}`, which will be replaced with actual values from the `input_variables` dataframe for each row. The template is a constant string defined in the application configuration and is crucial for the message generation process.

## Examples

Imagine you want to generate names for your company's services using a list of words. You can set up the component with the following configuration:

- **prompt_template**: `"Derive a name for our company services. The name should contain the word {word1} and the word {word2}."`
- **input_variables**:

  | word1  | word2  |
  |--------|--------|
  | power  | energy |
  | red    | panda  |

The processor will generate messages like:

- For the first row: "Derive a name for our company services. The name should contain the word power and the word energy."
- For the second row: "Derive a name for our company services. The name should contain the word red and the word panda."

Each message will be sent to the AI Chatbot, which will respond with a single message for each input. The responses will be compiled into a dataframe with the `result` column:

  | result                 |
  |------------------------|
  | Power Energy Services  |
  | Red Panda Services     |

This component streamlines the process of sending multiple, variable-based messages to an AI Chatbot and collecting the responses efficiently.