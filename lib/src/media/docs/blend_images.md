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