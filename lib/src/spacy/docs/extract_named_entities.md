# Extract Named Entities

## General Purpose

The "Extract Named Entities" component is designed to process tabular data to identify and extract named entities from text. Named entities are real-world objects, such as persons, locations, organizations, and so on, that can be denoted with a proper name. This component can be configured to output the extracted entities in various formats suitable for different use cases.

## Input and Output Format

### Input Format

The input for this component is a dataframe with a column named `text` that contains the textual data from which named entities will be extracted.

### Output Format

The output format of the dataframe depends on the configuration provided:

- **List**: A dataframe with a column named `entities` containing a list of named entities as plain text.
- **Struct**: A dataframe with a column named `entities` containing JSON objects with details of the named entities, including the text, start character, end character, and label.
- **Table**: A dataframe with multiple columns (`text`, `start_char`, `end_char`, `label`) detailing each named entity extracted from the text.

## Configuration Parameters

| Parameter Name | Expected Type | Description |
| -------------- | ------------- | ----------- |
| output_format  | String        | The format of the output. Valid values are "list", "struct", and "table". Default is "list". |
| model_name     | String        | The name of the model to use for entity extraction. Default is "en_core_web_sm". |
| filter_labels  | List of Strings | A list of entity labels to filter the named entities by. If not provided, all named entities will be returned. |

## Detailed Parameter Descriptions

- **output_format**: This parameter determines the structure of the output dataframe. The default format is "list", which provides a simple list of entity names. The "struct" format includes additional information about each entity in a JSON structure, and the "table" format provides a tabular representation with each entity detail in separate columns.

- **model_name**: Specifies the model to be used for named entity recognition. The default model is "en_core_web_sm", which is a small English model provided by spaCy. Users can choose from other available models that spaCy supports, which can be found at their official model repository.

- **filter_labels**: If you are only interested in specific types of named entities, you can use this parameter to provide a list of entity labels that you want to extract. For example, if you only want to extract "PERSON" and "ORG" entities, you would provide `["PERSON", "ORG"]`. If this parameter is not set, the component will extract all types of entities found in the text.

By configuring these parameters, users can tailor the component to meet the needs of their specific product pipeline and ensure that the output is in the most useful format for subsequent processing or analysis.