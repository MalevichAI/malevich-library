import json
import os

import cv2
import pandas as pd
from malevich.square import APP_DIR, DF, Context, input_true, processor, scheme
from pydantic import BaseModel
from ultralytics import YOLO

from .models import Detect, DetectRaw


@scheme()
class YOLOInputs(BaseModel):
    source: str

@scheme()
class YOLOWeights(BaseModel):
    filename: str


@input_true(collection_from='yolo_inputs')
def from_yolo_inputs():
    pass


def eval_path(path: str, file: str, context: Context):
    return path.format(
        RUN_ID=context.run_id,
        OP_ID=context.operation_id,
        SRC_DIR=os.path.dirname(path),
        SRC_BASENAME=file
    )


@processor()
def detect(yolo_inputs: DF[YOLOInputs], context: Context[Detect]):
    """Detects objects on images

    ## Input:
        A dataframe with the following columns:
            - `source` (str): the path to the input image in the shared storage

    ## Output:
        A dataframe with the following columns:
            - `key` (str): the path to the input image in the shared storage
            - `xyxy` (str): the bounding boxes of the detected objects
            - `cls_ids` (str): the class ids of the detected objects
            - `cls_names` (str): the class names of the detected objects
            - `plot` (str): the path to the output image in the shared storage

    ## Details:
        Uses YOLOv8 Predict Operation to detect objects on images.


    ## Configuration:
        - `weights`: str, default 'yolo.pt'.
            A path to the weights file in the shared storage.
        - `conf`: float, default 0.25.
            Confidence threshold.
        - `iou`: float, default 0.45.
            IoU threshold.
        - `classes`: dict, default {}.
            A dictionary that maps class ids to class names.
        - `save_plots`: bool, default False.
            Whether to save the output images.
        - `save_path`: str.
            The pattern for the path to the output images.
        - `batch_size`: int, default 1.
            The batch size.

    ## Available variables:
        - RUN_ID: the id of the current run
        - OP_ID: the id of the current operation
        - SRC_BASENAME: the basename of the input image
        - SRC_DIR: the directory of the input image

    ## Default value:
        '{RUN_ID}/{SRC_BASENAME}'

    -----

    Args:
        yolo_inputs: a DataFrame with the following columns:
            - source: the path to the input image

    Returns:
        a DataFrame with the following columns:
            - key: the path to the input image
            - xyxy: the bounding boxes of the detected objects
            - cls_ids: the class ids of the detected objects
            - cls_names: the class names of the detected objects
            - plot**: the path to the output image, if save_plots True

    Remarks:
        **: the column is present only if save_plots is True
    """
    should_plot = context.app_cfg.get('save_plots', False)
    base_path = context.app_cfg.get('save_path', '{RUN_ID}/{SRC_BASENAME}')
    batch_size = context.app_cfg.get('batch_size', 1)
    mapping = context.app_cfg.get('classes', {})

    assert os.path.exists(os.path.join(APP_DIR, 'weights', 'yolo.pt')), \
        'Please download weights/yolo.pt'
    yolo = YOLO(model=os.path.abspath(
        os.path.join(APP_DIR, 'weights', 'yolo.pt'))
    )
    keys = []
    xyxy = []
    cls_ids = []
    cls_names = []
    plots_keys = []
    plots = []

    # for yolo_input in yolo_inputs.source.to_list():
    for i in range(0, len(yolo_inputs), batch_size):
        slice_ = yolo_inputs.iloc[i:i+batch_size].source.to_list()
        real_input = [context.get_share_path(x) for x in slice_]
        results = yolo(real_input)

        assert len(results) == len(slice_), \
            f'Expected {len(slice_)} results, got {len(results)}'

        # Open image to plot boxes on

        for j, r in enumerate(results):
            img = cv2.imread(real_input[j])
            __img = r.plot()

            # Plot boxes on image
            img = cv2.addWeighted(img, 0.5, __img, 0.5, 0)

            boxes = r.boxes
            xyxy.extend([json.dumps(x) for x in boxes.xyxy.tolist()])
            cls_ids.extend([json.dumps(x) for x in boxes.cls.long().tolist()])
            cls_names.extend(
                [mapping.get(str(i), str(i)) for i in boxes.cls.long().tolist()]
            )
            keys.extend([slice_[j]] * len(boxes))

            if should_plot:
                try:
                    basename = os.path.basename(slice_[j])
                    save_path = eval_path(base_path, file=basename, context=context)
                    os.makedirs(os.path.dirname(
                        os.path.join(APP_DIR, save_path)), exist_ok=True
                    )
                    with open(os.path.join(APP_DIR, save_path), 'wb+') as f:
                        f.write(cv2.imencode('.png', img)[1])
                        context.share(save_path)
                        plots.append(save_path)
                        plots_keys.append(slice_[j])
                except (Exception, BaseException) as e:
                    raise ValueError(f'Invalid save_path: {save_path}. Got error: {e}')


    __final = {
        'key': keys,
        'xyxy': xyxy,
        'cls_id': cls_ids,
        'cls_name': cls_names
    }

    if should_plot:
        return pd.DataFrame(__final)

    return pd.DataFrame(__final)


@processor()
def detect_raw(yolo_inputs: DF[YOLOInputs], context: Context[DetectRaw]):
    """Detects objects on images and returns raw YOLOv8 results

    ## Input:
        A dataframe with the following columns:
            - `source` (str): the path to the input image in the shared storage

    ## Output:
        A dataframe with the following columns:
            - `key` (str): the path to the input image in the shared storage
            - `result` (str): serialized YOLOv8 Result object

    ## Details:
        Uses YOLOv8 Predict Operation to detect objects on images.


    ## Configuration:
        - `weights`: str, default 'yolo.pt'.
            A path to the weights file in the shared storage.
        - `conf`: float, default 0.25.
            Confidence threshold.
        - `iou`: float, default 0.45.
            IoU threshold.
        - `classes`: dict, default {}.
            A dictionary that maps class ids to class names.
        - `save_plots`: bool, default False.
            Whether to save the output images.
        - `save_path`: pattern.
            The pattern for the path to the output images.
        - `batch_size`: int, default 1.
            The batch size.

    ## Available variables:
        - RUN_ID: the id of the current run
        - OP_ID: the id of the current operation
        - SRC_BASENAME: the basename of the input image
        - SRC_DIR: the directory of the input image

    ## Default value:
        '{RUN_ID}/{SRC_BASENAME}'

    -----

    Args:
        yolo_inputs: a DataFrame with the following columns:
            - source: the path to the input image

    Returns:
        a DataFrame with the following columns:
            - key: the path to the input image
            - xyxy: the bounding boxes of the detected objects
            - cls_ids: the class ids of the detected objects
            - cls_names: the class names of the detected objects
            - plot**: the path to the output image, if save_plots is True

    Remarks:
        **: the column is present only if save_plots is True
    """
    context.app_cfg.get('classes', {})
    should_plot = context.app_cfg.get('save_plots', False)
    base_path = context.app_cfg.get('save_path', '{RUN_ID}/{SRC_BASENAME}')
    batch_size = context.app_cfg.get('batch_size', 1)

    assert os.path.exists(os.path.join(APP_DIR, 'weights', 'yolo.pt')), \
        'Please download weights/yolo.pt'
    yolo = YOLO(model=os.path.abspath(
        os.path.join(APP_DIR, 'weights', 'yolo.pt'))
    )

    plots_keys = []
    plots = []
    yolo_results = []
    keys = []

    # for yolo_input in yolo_inputs.source.to_list():
    for i in range(0, len(yolo_inputs), batch_size):
        slice_ = yolo_inputs.iloc[i:i+batch_size].source.to_list()
        real_input = [context.get_share_path(x) for x in slice_]
        results = yolo(real_input)

        assert len(results) == len(slice_), \
            f'Expected {len(slice_)} results, got {len(results)}'

        # Open image to plot boxes on

        for j, r in enumerate(results):
            img = cv2.imread(real_input[j])
            __img = r.plot()

            # Plot boxes on image
            img = cv2.addWeighted(img, 0.5, __img, 0.5, 0)
            min_json = r.tojson()
            # Dumps and loads to minimize the size of the json
            yolo_results.append(json.dumps(json.loads(min_json)))
            keys.append(slice_[j])


            if should_plot:
                try:
                    basename = os.path.basename(slice_[j])
                    save_path = eval_path(base_path, file=basename, context=context)
                    os.makedirs(
                        os.path.dirname(os.path.join(APP_DIR, save_path)),
                        exist_ok=True
                    )
                    with open(os.path.join(APP_DIR, save_path), 'wb+') as f:
                        f.write(cv2.imencode('.png', img)[1])
                        context.share(save_path)
                        plots.append(save_path)
                        plots_keys.append(slice_[j])
                except (Exception, BaseException) as e:
                    raise ValueError(f'Invalid save_path: {save_path}. Got error: {e}')


    __final = {
        'key': keys,
        'result': yolo_results
    }

    if should_plot:
        return pd.DataFrame(__final), pd.DataFrame({'key': plots_keys, 'plot': plots})

    return pd.DataFrame(__final), pd.DataFrame({'plot': [], 'key': []})

