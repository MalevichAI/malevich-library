# Convert PDF to Markdown

## General Component Purpose

The "Convert PDF to Markdown" component is designed to transform PDF files into Markdown format. This conversion facilitates easier manipulation and display of the content originally locked within the PDF format, making it more accessible and editable. The component processes a batch of PDF files and generates corresponding Markdown files, which can then be used for various purposes such as documentation, web content, or version control.

## Input and Output Format

### Input Format

The input for this component is a dataframe that must contain a column named `filename`, which includes the paths to the PDF files intended for conversion.

### Output Format

The output is a dataframe identical to the input dataframe but with an additional column named `markdown`. This column contains either the paths to the converted Markdown files or the contents of those files, depending on the configuration.

## Configuration Parameters

| Parameter Name  | Expected Type | Description                                                  |
|-----------------|---------------|--------------------------------------------------------------|
| write_contents  | Boolean       | If true, the output will include the contents of the Markdown files instead of just their paths. |

## Configuration Parameters Description

- **write_contents**: This boolean parameter determines the nature of the output within the `markdown` column of the resulting dataframe. If set to `true`, the component will include the actual content of the converted Markdown files directly in the dataframe. If `false`, the dataframe will only contain the paths to the generated Markdown files, which can be accessed and read separately. This option allows users to choose between directly working with the data or referencing the files for later use.