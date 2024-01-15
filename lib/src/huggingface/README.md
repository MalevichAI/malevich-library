# Token Classification

## General Component Purpose

The Token Classification component is designed to perform entity recognition on text data. It utilizes models from the HuggingFace Transformers library to identify and classify entities within the text, such as person names, locations, and organizations. This component is useful for extracting structured information from unstructured text data.

## Input and Output Format

### Input Format

The input to this component should be a dataframe with the following column:

- `text`: The column containing the text to be classified.

### Output Format

The output from this component is a dataframe with the following columns:

- `sentence_index` (optional): The index of the sentence in the input dataframe.
- `entity`: The name of the entity identified in the text.
- `score`: The confidence score of the classification.
- `index`: The index of the token in the sentence.
- `word`: The text of the token.
- `start` (optional): The start index of the token in the sentence.
- `end` (optional): The end index of the token in the sentence.

## Configuration Parameters

| Parameter Name           | Expected Type       | Description |
|--------------------------|---------------------|-------------|
| `ignore_labels`          | List of Strings     | A list of labels to ignore during classification. |
| `keep_text`              | Boolean             | Whether to include the original input text in the output dataframe. |
| `keep_sentence_index`    | Boolean             | Whether to include the sentence index in the output dataframe. |
| `model`                  | String              | The name of the model to use for token classification. |
| `tokenizer`              | String              | The name of the tokenizer to use with the model. |
| `device`                 | String              | The device to run the model on (`cpu` or `gpu`). |
| `batch_size`             | Integer             | The batch size to use for inference. |
| `aggregation_strategy`   | String              | The aggregation strategy for handling multiple entities per token. |

## Detailed Configuration Parameters

- **ignore_labels**: Specify labels that should be ignored in the classification process. For example, to ignore the "Outside" label, you would set this to `["O"]`.

- **keep_text**: Set this to `True` if you want to keep the input text in the output dataframe. This can be useful for reference or further processing.

- **keep_sentence_index**: Set this to `True` if you want to maintain the sentence index in the output dataframe. This is helpful for tracking which sentence an entity belongs to.

- **model**: Provide the name of the pre-trained model you wish to use for token classification. For example, `dbmdz/bert-large-cased-finetuned-conll03-english`.

- **tokenizer**: Specify the tokenizer that corresponds to the chosen model. For example, `bert-base-cased`.

- **device**: Indicate whether the model should run on a CPU (`cpu`) or GPU (`gpu`). The availability of GPU will be automatically detected and used if possible.

- **batch_size**: The number of samples to process at once during inference. Larger batch sizes may lead to faster processing but can also consume more memory.

- **aggregation_strategy**: Define how to handle cases where multiple entities are found within a single token. Refer to the HuggingFace documentation for available strategies and their descriptions.

This component streamlines the process of token classification, making it accessible without the need for coding expertise. By configuring the above parameters, users can tailor the classification process to their specific needs and datasets.

