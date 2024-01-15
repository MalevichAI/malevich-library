# Send Messages with Dynamic Prompt

## General Component Purpose

This component is designed to interact with an AI Chatbot by sending it a series of dynamically generated messages. The messages are created by applying a set of input variables to a prompt template. This allows for batch processing of prompts to generate a variety of responses from the AI Chatbot. Each message is treated independently, without shared context, ensuring unique responses for each prompt variation.

## Input and Output Format

### Input Format

The component requires two inputs:

1. **Prompt Template**: A dataframe that contains a single cell with the string of the prompt template.
2. **Input Variables**: A dataframe where each row contains variables that will be substituted into the prompt template to create a message.

### Output Format

The output is a dataframe with one column:

- **result**: Contains the responses from the AI Chatbot for each dynamically generated message.

## Configuration Parameters

This component does not require any additional configuration.

## Detailed Parameter Descriptions

Since the component is not configurable, there are no additional parameters to describe. The functionality is solely based on the input prompt template and the variables provided.

## Examples

To illustrate how the component works, consider the scenario where you want to generate names for your company services using a combination of words. You would set up your inputs as follows:

- **Prompt Template**:

  | prompt |
  | --- |
  | Derive a name for our company services. The name should contain the word {word1} and the word {word2}. |

- **Input Variables**:

  | word1 | word2 |
  | --- | --- |
  | power | energy |
  | red | panda |

The component would then send messages to the AI Chatbot like:

- "Derive a name for our company services. The name should contain the word power and the word energy."
- "Derive a name for our company services. The name should contain the word red and the word panda."

The AI Chatbot's responses might be:

- "Power Energy Services"
- "Red Panda Services"

These responses would be returned in a dataframe with a single `result` column.

Please note that the actual responses from the AI Chatbot may vary and are dependent on the Chatbot's model and training.

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

