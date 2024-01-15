# Assert Regex Component

## General Purpose

The Assert Regex component is designed to validate the contents of a dataframe by checking whether its values match a specified regular expression (regex). This component is useful for ensuring that data conforms to expected patterns and can be used to identify and report errors in data.

## Input and Output Format

### Input Format

The input to this component is an arbitrary dataframe that you want to validate using regex rules.

### Output Format

The output is a dataframe with an additional column named `errors`. This column contains any errors found during the validation process.

## Configuration Parameters

| Name            | Type                | Description                                                                 |
|-----------------|---------------------|-----------------------------------------------------------------------------|
| rules           | List of Dictionaries| A list of dictionaries defining the regex rules to be applied to the data.   |
| raise_on_error  | Boolean             | Determines whether to raise an exception if an error is found.               |

## Configuration Parameters Detailed

### Rules

Each rule in the `rules` list is a dictionary with the following keys:

- `regex` (String): The regex pattern to match the values against.
- `column` (String or Index, optional): The specific column to apply the rule to. If not specified, the rule applies to all columns.
- `row` (String or Index, optional): The specific row to apply the rule to. If not specified, the rule applies to all rows.
- `invert` (Boolean, optional): If set to `True`, the rule will flag values that do not match the regex. The default is `False`.

An Index is a dictionary that may contain the following keys:

- `start` (Integer or Float, optional): The starting index or percentage of the dataframe length.
- `end` (Integer or Float, optional): The ending index or percentage of the dataframe length.
- `step` (Integer or Float, optional): The step of the index or percentage of the dataframe length.

If a float is provided for `start`, `end`, or `step`, it will be interpreted as a percentage of the length of the dataframe.

### raise_on_error

- `raise_on_error` (Boolean, default `False`): If set to `True`, the component will raise an exception when an error is found during validation. If `False`, the errors will be collected and returned in the output dataframe's `errors` column.

## Examples

Here is an example of a configuration for the Assert Regex component:

```json
{
    "rules": [
        {
            "regex": "^\\d{4}-\\d{2}-\\d{2}$",
            "column": "date_column",
            "invert": false
        },
        {
            "regex": "^[A-Z]{3}$",
            "column": "code_column",
            "row": {
                "start": 10,
                "end": 20
            }
        }
    ],
    "raise_on_error": true
}
```

In this example, the first rule checks that the `date_column` contains values in the format of a date (YYYY-MM-DD), and the second rule checks that the `code_column` contains values with three uppercase letters, but only for rows 10 to 20. If any value does not match the specified pattern, an exception will be raised due to `raise_on_error` being set to `true`.

