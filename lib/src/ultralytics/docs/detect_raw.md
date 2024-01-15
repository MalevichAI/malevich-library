# Detect Raw

The Detect Raw component is designed to process images and detect objects within them using the YOLOv8 algorithm. It takes a set of images as input and produces a set of detection results, which include the bounding boxes, class IDs, and class names of the detected objects. Optionally, it can also save the output images with the detections plotted on them.

## Input and Output Format

### Input Format

The input to this component should be a dataframe with the following column:

- `source`: The path to the input image in the shared storage.

### Output Format

The output from this component is a dataframe with the following columns:

- `key`: The path to the input image in the shared storage.
- `result`: Serialized YOLOv8 Result object.

If the `save_plots` configuration is set to `True`, an additional column will be present:

- `plot`: The path to the output image with the detections plotted.

## Configuration Parameters

| Parameter    | Type                | Description                                                                                   |
|--------------|---------------------|-----------------------------------------------------------------------------------------------|
| weights      | String              | Optional. The path to the weights file in the shared storage. Default is `'yolo.pt'`.         |
| conf         | Float               | Optional. Confidence threshold for detections. Default is `0.25`.                             |
| iou          | Float               | Optional. Intersection over Union (IoU) threshold for detections. Default is `0.45`.          |
| save_plots   | Boolean             | Optional. Whether to save output images with detections plotted. Default is `False`.          |
| save_path    | Pattern             | Optional. The pattern for the path to the output images.                                      |
| batch_size   | Integer             | Optional. The number of images to process in a batch. Default is `1`.                         |

## Detailed Configuration Parameters

- **weights**: A string specifying the location of the YOLOv8 weights file. If not provided, the default weights file named 'yolo.pt' will be used.

- **conf**: A floating-point number representing the confidence threshold for the object detection. The default value is `0.25`.

- **iou**: A floating-point number representing the Intersection over Union threshold used for object detection. The default value is `0.45`.

- **save_plots**: A boolean indicating whether the output images with detections plotted should be saved. By default, this is set to `False`.

- **save_path**: A pattern that defines the file naming scheme for saved plots. It supports variables like `RUN_ID`, `OP_ID`, `SRC_BASENAME`, and `SRC_DIR` to construct the file path dynamically. The default pattern is `'{RUN_ID}/{SRC_BASENAME}'`.

- **batch_size**: An integer that defines how many images should be processed together in one batch. The default batch size is `1`.

## Remarks

- The `plot` column in the output dataframe is only present if `save_plots` is set to `True`.
- The `weights` file must be present in the shared storage, specifically within the `weights` directory of the application directory.
- The `save_path` pattern is evaluated to determine the final path where the output images will be saved. If the path is invalid or the saving process encounters an error, an exception will be raised.

This component is essential for applications that require automated object detection in images, such as surveillance systems, image analysis tools, and more. It provides a no-code solution to integrate advanced AI capabilities into product pipelines.