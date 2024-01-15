# Translate Texts

## General Purpose

The **Translate Texts** component is designed to facilitate the translation of text from one language to another. It leverages the capabilities of the Google Translate API to provide accurate and swift translations for a variety of language pairs. This component is particularly useful in scenarios where multilingual support is needed, such as in international applications, content localization, or global communication platforms.

## Input Format

The input for this component is a dataframe with the following columns:

- `text`: The text to be translated.
- `from_language`: The language code of the original text to translate from.
- `to_language`: The language code of the target language to translate to.

## Output Format

The output is a dataframe that includes the original columns from the input and an additional column:

- `translation`: The translated text in the target language.

The original `text`, `from_language`, and `to_language` columns are retained without any modifications.

## Configuration Parameters

This component is not configurable and does not require any configuration parameters.

## Detailed Parameter Descriptions

Since this component does not have any configuration parameters, there are no additional details to describe. The component uses the input data as is and performs the translation process based on the provided language codes.

## Usage Notes

The **Translate Texts** component is straightforward to use and does not require any programming knowledge. Users simply need to provide the input data in the specified format, and the component will handle the rest. It is important to ensure that the language codes used in the `from_language` and `to_language` columns are valid and supported by the Google Translate API for successful translation.