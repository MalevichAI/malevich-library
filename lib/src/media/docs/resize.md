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