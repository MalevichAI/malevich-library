# Object Detection Component

## General Purpose
The Object Detection Component is designed to detect objects in images using a pre-trained YOLO (You Only Look Once) model. It processes batches of images and identifies the location and class of objects within each image. This component is ideal for applications requiring image analysis such as surveillance, quality control, or retail product identification.

## Input Format
The input for this component is a dataframe with the following column:
- **source**: The path to the input image in the shared storage.

## Output Format
The output is a dataframe containing the following columns:
- **key**: The path to the input image in the shared storage.
- **xyxy**: The bounding boxes of the detected objects.
- **cls_ids**: The class IDs of the detected objects.
- **cls_names**: The class names of the detected objects.
- **plot**: The path to the output image in the shared storage (only if `save_plots` is set to `True`).

## Configuration Parameters

| Parameter Name | Expected Type | Description |
| -------------- | ------------- | ----------- |
| weights        | String        | (Optional) Path to the weights file in the shared storage. Default: 'yolo.pt'. |
| conf           | Float         | (Optional) Confidence threshold for detection. Default: 0.25. |
| iou            | Float         | (Optional) Intersection over Union (IoU) threshold for detection. Default: 0.45. |
| classes        | Dictionary    | (Optional) Maps class IDs to class names. Default: {}. |
| save_plots     | Boolean       | (Optional) Whether to save output images with detected objects highlighted. Default: False. |
| save_path      | Pattern       | (Optional) Pattern for the path to save output images. Variables: `RUN_ID`, `OP_ID`, `SRC_BASENAME`, `SRC_DIR`. Default: '{RUN_ID}/{SRC_BASENAME}'. |
| batch_size     | Integer       | (Optional) Number of images to process in a batch. Default: 1. |

## Detailed Configuration Parameters

- **weights**: The path to the model weights file. If not specified, the default 'yolo.pt' will be used. Ensure that the weights file is available in the shared storage before running the component.

- **conf**: This is the confidence threshold for the YOLO model to consider a detection valid. The default value is 0.25, but it can be adjusted depending on the desired precision.

- **iou**: The Intersection over Union (IoU) threshold is used to filter out overlapping bounding boxes. The default value is 0.45.

- **classes**: A dictionary that provides a mapping from numeric class IDs to human-readable class names. If not provided, class IDs will be used as names.

- **save_plots**: A boolean flag that determines whether the component should save images with detected objects highlighted. If set to `True`, the output images will be saved to the specified `save_path`.

- **save_path**: A pattern that defines the directory and filename structure for saving output images. It can include variables such as `RUN_ID`, `OP_ID`, `SRC_BASENAME`, and `SRC_DIR`. The default pattern is '{RUN_ID}/{SRC_BASENAME}' which organizes saved images by run ID and retains the original image basename.

- **batch_size**: Specifies the number of images to process in a single batch. A larger batch size can improve performance but requires more memory. The default batch size is 1.

## Remarks
- The 'plot' column in the output dataframe will only be present if `save_plots` is set to `True`.
- It is crucial to ensure that the weights file is present in the shared storage at the specified path before running the detection.
- The component uses YOLOv8 Predict Operation for object detection, which is a state-of-the-art method for real-time object recognition.