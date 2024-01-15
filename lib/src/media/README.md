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

# Resize Images Component

## General Purpose

The Resize Images Component is designed to adjust the size of images in a dataset and optionally change their format. It is useful for standardizing image dimensions or reducing file size for more efficient storage and processing.

## Input and Output Format

### Input Format

The input to this component is a dataframe that must contain a column named `filename`, which includes the paths to the images that need to be resized.

### Output Format

The output is a dataframe with a column named `filename`. This column will contain the paths to the resized (and potentially reformatted) images.

## Configuration Parameters

| Parameter Name   | Expected Type | Description                                           |
|------------------|---------------|-------------------------------------------------------|
| width            | Integer       | The desired width of the resized image (optional).    |
| height           | Integer       | The desired height of the resized image (optional).   |
| preserve_ratio   | Boolean       | Preserve the aspect ratio of the image (default True).|
| image_type       | String        | The desired image format (e.g., "jpg", "png").        |

## Detailed Configuration Parameters

- **width**: (Optional) Specify the width to which the image should be resized. If only the width is provided and `preserve_ratio` is set to True, the height will be adjusted to maintain the image's aspect ratio.

- **height**: (Optional) Specify the height to which the image should be resized. If only the height is provided and `preserve_ratio` is set to True, the width will be adjusted to maintain the image's aspect ratio.

- **preserve_ratio**: By default, this is set to True, which means the component will maintain the original aspect ratio of the image when resizing. If set to False, the image will be resized to the provided width and height without regard to the original aspect ratio.

- **image_type**: This parameter allows you to specify the desired image format for the output files. The default format is "jpg". Please note that some image formats may not support transparency.

This component is part of a no-code platform designed to simplify the process of working with AI-driven product development. It provides a user-friendly interface that allows users to easily configure and apply transformations to their data without the need for programming knowledge.

# Blend Images

## General Purpose

The "Blend Images" component is designed to combine two images by overlaying one image on top of the other. This process is often referred to as blending and can be used to create composite images, watermarks, or visual effects. The component takes a pair of image paths for each set of images to be blended and produces a new image that represents the combined visual data of both inputs.

## Input and Output Format

### Input Format

The input for this component is a dataframe with two columns:

- `background_image_path`: The file path to the background image.
- `patch_image_path`: The file path to the patch (overlay) image.

Each row in the dataframe represents a pair of images that will be blended together.

### Output Format

The output is a dataframe with a single column:

- `blended`: The file paths to the resulting blended images.

## Configuration Parameters

This component does not require any configuration.

## Detailed Configuration Parameters

Since there is no configuration required for this processor, you can use it directly without any additional setup.

## Usage

To use the "Blend Images" component, simply provide it with the input dataframe as described above. The component will process each pair of images and output a dataframe containing the paths to the blended images. These images will be a composition of the background and patch images, with the patch image overlaid on top of the background image.

# Remove Background

## General Component Purpose

The "Remove Background" component is designed to process images by removing their background. This component is ideal for users who need to isolate the subject of an image from its surroundings, which can be useful for various applications such as product photography, graphic design, and content creation.

## Input and Output Format

### Input Format

The input for this component is a dataframe that must contain a column named `path_to_image`. Each entry in this column should be a string representing the file path to an image from which the background will be removed.

### Output Format

The output is a dataframe with a single column named `no_background_image`. This column contains the file paths to the processed images with the backgrounds removed.

## Configuration Parameters

This component does not require any configuration.

## Detailed Configuration Parameters

Since there is no configuration needed for this component, users can simply provide the input dataframe and execute the component to receive the output.

---

This component is part of a no-code platform designed to streamline AI-driven product development. It allows users to assemble sophisticated product pipelines without writing any code, making the process more accessible and efficient.

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

# Split on Frames

## General Purpose
The "Split on Frames" component is designed to process video files by splitting them into individual frames. This operation is essential for tasks that require frame-by-frame analysis, such as video editing, motion analysis, or machine learning applications where individual frames serve as input data.

## Input and Output Format

### Input Format
The input to this component is a DataFrame that must contain the following column:
- `videos`: A column with paths to the input video files stored in shared storage.

### Output Format
The output is a DataFrame that includes the original columns plus the following additional columns:
- `videos`: Paths to the original video files in shared storage.
- `frames`: Paths to the output frames stored in shared storage.

## Configuration Parameters

| Parameter | Expected Type | Description |
| --------- | ------------- | ----------- |
| fps       | Int or Float  | The number of frames per second to extract. If a float is provided, it represents a percentage of the original video's fps. Default is 1. |

## Configuration Parameters Details

- **fps**: This parameter controls the frame extraction rate. When set to an integer, it specifies the exact number of frames to be extracted per second. If set as a float, it acts as a multiplier to the video's original frame rate. For example, a value of `0.5` would extract frames at half the original frame rate. The default value is `1`, which means that by default, one frame per second will be extracted.

## Example Usage

To use the "Split on Frames" component, you would pass it a DataFrame with a column named `videos` containing the paths to the video files. The component will then process each video, splitting it into frames according to the specified `fps` configuration. The output will be a DataFrame with the same columns as the input, plus a `frames` column containing the paths to the extracted frames.

Please note that all other columns from the input DataFrame will be preserved and duplicated for each frame of the video, allowing for easy traceability and association between the original video data and the extracted frames.

