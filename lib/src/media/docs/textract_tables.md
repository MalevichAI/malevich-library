# Textract Tables

## General Component Purpose
The Textract Tables component is designed to extract tables from PDF files using AWS Textract service. It processes a list of PDF files and generates a structured representation of the tables found within those files. This component is ideal for users who need to convert tables from PDF format into a more usable form without writing any code.

## Input and Output Format

### Input Format
The input to this component is a dataframe with a single column:
- `filename`: The name of the PDF file to be processed.

### Output Format
The output is a dataframe with the following columns:
- `filename`: The name of the processed PDF file.
- `table`: Depending on the configuration, this can be either the name of the markdown file containing the table or the actual contents of the table.

## Configuration Parameters

| Parameter Name           | Expected Type | Description                                                  |
|--------------------------|---------------|--------------------------------------------------------------|
| aws_access_key_id        | String        | Your AWS access key ID (required).                           |
| aws_secret_access_key    | String        | Your AWS secret access key (required).                       |
| write_contents           | Boolean       | Whether to write the contents of the table to the output.    |

## Detailed Configuration Parameters

- **aws_access_key_id**: This is your AWS access key ID. It is required to authenticate and use the AWS Textract service.

- **aws_secret_access_key**: This is your AWS secret access key. It is required to authenticate and use the AWS Textract service.

- **write_contents**: A boolean parameter that defaults to `False`. If set to `True`, the component will include the actual contents of the extracted tables in the output dataframe. If `False`, the output will contain the names of the markdown files where the table contents are saved.