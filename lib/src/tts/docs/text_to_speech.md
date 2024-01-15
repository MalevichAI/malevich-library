# Text to Speech

## General Component Purpose

The Text to Speech component is designed to convert text data into spoken words, effectively generating speech audio files from provided text. It is particularly useful in applications where audio representations of text data are needed, such as in accessibility features for visually impaired users, language learning tools, or automated voice messaging systems.

## Input Format

The input for this component is a DataFrame with the following column:

- `TextWithLanguageCode`: This column should contain the text to be converted to speech along with the language code in which the text is written.

## Output Format

The output of this component is a DataFrame with a single column:

- `speech`: This column contains the paths to the generated MP3 audio files corresponding to the input text.

## Configuration Parameters

| Parameter Name | Expected Type       | Description                                   |
| -------------- | ------------------- | --------------------------------------------- |
| `language`     | String (optional)   | The language code for the text-to-speech conversion. Defaults to English (`en`) if not provided. |

## Configuration Parameters Details

- **language**: This optional parameter allows the user to specify the language of the input text for conversion. The language should be provided as a standard language code (e.g., 'en' for English, 'es' for Spanish). If this parameter is not included in the input, the default language will be English.

The component utilizes the `gTTS` (Google Text-to-Speech) library to perform the text-to-speech conversion, ensuring high-quality audio output. Each piece of text is processed concurrently, resulting in efficient handling of large datasets. The generated audio files are saved with unique identifiers to avoid overwriting and are shared through the context for further use in the product pipeline.