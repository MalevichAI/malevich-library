# Convert PDF to JPEG

## General Component Purpose

The "Convert PDF to JPEG" component is designed to transform PDF files into JPEG images. It allows users to specify which pages of a PDF document they would like to convert, providing flexibility and control over the conversion process.

## Input and Output Format

### Input Format

The input for this component is a dataframe that must contain a single column:

- `filename`: The names of the PDF files to be converted. These files should be either downloaded or shared in apps beforehand.

### Output Format

The output is a dataframe with the following two columns:

- `filename`: The name of the original PDF file.
- `jpeg`: The name of the converted JPEG file. The converted file is shared in apps.

## Configuration Parameters

| Parameter   | Type | Description                                         |
|-------------|------|-----------------------------------------------------|
| start_page  | int  | The first page number to start converting from.     |
| page_num    | int  | The number of pages to convert from the start page. |

## Configuration Details

- **start_page**: This parameter defines the number of the first page to start the conversion from. If this parameter is not specified, the conversion will start from the first page of the PDF document.

- **page_num**: This parameter specifies the total number of pages to convert, counting from the `start_page`. If not specified, the component will convert all pages starting from the `start_page` to the end of the document.

By configuring these parameters, users can tailor the conversion process to their specific needs, whether they need to convert a single page, a range of pages, or the entire document.