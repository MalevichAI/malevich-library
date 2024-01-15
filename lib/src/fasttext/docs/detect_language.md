# Detect Language

## General Purpose

The "Detect Language" component is designed to analyze a column of text data and identify the language in which each text entry is written. This component is useful for datasets containing multilingual text, where understanding or separating languages is necessary for further processing or analysis.

## Input and Output Format

### Input Format

The input for this component should be a dataframe with a single column:

- **Text**: A column containing text entries for language detection.

### Output Format

The output is a dataframe with the following columns:

- **Text**: The original text entries from the input.
- **Language**: The detected language for each text entry.

## Configuration Parameters

| Parameter Name | Expected Type | Description |
| -------------- | ------------- | ----------- |
| `model_path`   | String        | The file path to the pre-trained language detection model. |

## Configuration Parameters Details

- **model_path**: This is the path where the language detection model is stored. The model is used to predict the language of each text entry. It should be a string representing the file path to the `.ftz` model file.

Please ensure that the model file is accessible at the specified path for the component to function correctly.