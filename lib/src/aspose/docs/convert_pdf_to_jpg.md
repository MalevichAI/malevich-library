# Convert PDF to JPG

## General Component Purpose
The "Convert PDF to JPG" component is designed to transform PDF files into JPEG images. This component is useful when there is a need to convert documents into a more widely supported image format for easier viewing, sharing, or embedding in web pages and presentations.

## Input Format
The input for this component is a dataframe that must contain a column named `filename`. Each entry in this column should be the path to a PDF file that is to be converted.

## Output Format
The output is a dataframe that retains the original structure but with an additional column named `jpeg`. This column contains the paths to the converted JPEG files.

## Configuration Parameters

| Parameter Name  | Expected Type | Description                                      |
|-----------------|---------------|--------------------------------------------------|
| write_contents  | Boolean       | If true, outputs the contents of the JPEG files; otherwise, outputs the file paths. |

## Configuration Parameters Details

- **write_contents**: This parameter determines the nature of the output. When set to `true`, the component will include the actual contents of the JPEG files in the output dataframe. If `false`, the output will only contain the paths to the JPEG files. This allows for flexibility depending on whether the user needs to work with the file contents directly or just needs references to the files' locations.

## Usage Notes
This component is straightforward to use and requires minimal configuration. Users need to ensure that the input dataframe is correctly formatted with the necessary `filename` column. The component takes care of the conversion process and appends the results to the output dataframe, making it easy to integrate into product pipelines without the need for coding.