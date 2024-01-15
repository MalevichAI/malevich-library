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