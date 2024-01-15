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