# Match Pattern

## General Purpose

The "Match Pattern" component is designed to process tabular data by identifying and extracting fragments within each cell that match a specified pattern. Once these fragments are found, they are concatenated together using a specified character and placed back into their respective cells, effectively transforming the data based on the pattern recognition.

## Input and Output Format

The input for this component is a dataframe with any number of columns and rows. Each cell in the dataframe should contain text data for the pattern matching to be performed.

The output is a new dataframe of the same dimensions and column names as the input. Each cell in the output dataframe contains the concatenated fragments that matched the specified pattern.

## Configuration Parameters

| Parameter Name | Expected Type       | Description                                           |
|----------------|---------------------|-------------------------------------------------------|
| pattern        | String              | The pattern to match within each cell of the dataframe.|
| join_char      | String (optional)   | The character used to join matched fragments.         |

## Configuration Parameters Details

- **pattern**: This is the specific sequence of characters that the component will search for within each cell of the dataframe. The pattern should be provided as a string and can include regular expression syntax to match a variety of text fragments.

- **join_char**: This optional parameter defines the character that will be used to concatenate the matched fragments found in each cell. If not specified, a default character will be used. The join character should be provided as a single string character.

## Usage Notes

- The component operates on string-type columns within the dataframe. Non-string columns will be ignored during the pattern matching process.
- The pattern matching is case-sensitive, and the pattern must be specified accurately to ensure correct matches.
- The resulting dataframe maintains the original structure, with the transformation applied only to the content of the cells.

Remember, no coding knowledge is required to configure and use this component. By specifying the desired pattern and join character, you can easily manipulate and transform your tabular data to better suit your analysis or reporting needs.