import os

import cv2
import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel
from ultralytics import YOLO

from .models import DetectVideo


@scheme()
class YOLOVideoInputs(BaseModel):
    video_path: str


class DeployedModel:
    def __init__(self, model_path, *args, **kwargs) -> None:
        self.__path = model_path
        self.__model = YOLO(self.__path, *args, **kwargs)

    @property
    def yolo(self):
        return self.__model

    def matches_path(self, path):
        return path == self.__path


@processor()
async def detect_with_asset(
    yolo: DF,
    inputs: DF,
    context: Context[DetectVideo]
):
    """Detects objects on a video

    ## Input:
        - `yolo`: a YOLO object
        - `inputs`: a YOLOVideoInputs object

    ## Output:
        A dataframe with the following columns:
            - `key` (str): the path to the input video in the shared storage
            - `xyxy` (str): the bounding boxes of the detected objects
            - `cls_ids` (str): the class ids of the detected objects
            - `cls_names` (str): the class names of the detected objects
            - `plot` (str): the path to the output video in the shared storage

    ## Details:
        Uses YOLOv8 Predict Operation to detect objects on a video.

    ## Configuration:
        - `conf`: float, default 0.25.
            Confidence threshold.
        - `iou`: float, default 0.45.
            IoU threshold.
        - `classes`: list[int], default None.
            A list of classes to detect. By default predicts all classes.
        - `gpus`: list[int], default None.
            List of GPU indices. If None, uses all available GPUs.
        - `save images`: bool, default True.
            Whether to save and share original images across apps.
        - `return_raw`: bool, default False.
            If True, returns JSON-serialized YOLO Results objects.
        - `fps`: int, default 1:
            Frame per second for video processing.

    -----

    Args:
        yolo (DF[obj]): An asset of the YOLO model
        inputs (YOLOVideoInputs): A collection of inputs
        config (DetectVideo): A configuration object

    Returns:
        A collection of YOLO results
    """
    def get_path(x):  # noqa: ANN202
        path = context.get_share_path(x, not_exist_ok=True)
        if path is not None and os.path.exists(path):  # noqa: E501
            return path
        else:
            return x

    yolo.path = yolo.path.apply(get_path)
    inputs.path = inputs.path.apply(get_path)

    asset_len = len(yolo.index)
    asset_pt = yolo[yolo.path.apply(lambda x: x.endswith('.pt'))]
    if asset_len != 1 and len(asset_pt.index) > 1:
        raise ValueError(
            'Invalid asset: should be a .pt file or a folder with a single .pt file'
        )

    path_ = asset_pt.path.iloc[0]
    if context.common is None or not context.common.matches_path(path_):
        context.common = DeployedModel(path_)

    outputs = []

    for _, video in inputs.iterrows():
        video_path = video.iloc[0]
        cap = cv2.VideoCapture(video_path)
        orig_fps = cap.get(cv2.CAP_PROP_FPS)
        vid_stride = max(1, round(orig_fps / (context.app_cfg.fps or orig_fps)))
        k = 0

        images = []
        results = []
        # tracemalloc.start()
        while True:
            success, frame = cap.read()
            if success:
                if k % vid_stride == 0:
                    r = context.common.yolo.predict(
                        frame,
                        conf=context.app_cfg.conf,
                        iou=context.app_cfg.iou,
                        classes=context.app_cfg.classes,
                        device=context.app_cfg.gpus,
                    )[0]
                    safe_path = video_path.replace('/', '_')
                    base_path = os.path.join(safe_path, 'images')
                    im_path = os.path.join(base_path, f'{k}.png')
                    os.makedirs(os.path.join(APP_DIR, base_path), exist_ok=True)
                    cv2.imwrite(os.path.join(APP_DIR, im_path), r.orig_img)
                    images.append(im_path)
                    del r.orig_img
                    try:
                        results.append(r.tojson() if context.app_cfg.return_raw else r)
                    except Exception: # !!!
                        results.append({})
                k += 1
            else:
                break
        cap.release()
        print(k, len(images), context.app_cfg.fps)
        # results_ = []
        for i in range(0, len(images), 25):
            # results_.append(context.share_many(images[i:i+25]))
            context.share_many(images[i:i+25])
        # await asyncio.gather(*results_)

        if context.app_cfg.return_raw:
            outputs.extend([
                {
                    'key': video_path,
                    'frame_id': frame,
                    'result': result,
                    'image': image,
                }
                for frame, (result, image) in enumerate(zip(results, images))
            ])
        else:
            for frame, (r, image) in enumerate(zip(results, images)):
                for box_id, box in enumerate(r.boxes):
                    x1, y1, x2, y2 = (
                        box.xyxy
                        .squeeze()
                        .cpu()
                        .numpy()
                        .tolist()
                    )
                    cls_ = int(box.cls.item())
                    conf_ = box.conf.item()
                    outputs.append({
                        'key': video_path,
                        'frame_id': frame,
                        'box_id': box_id,
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2,
                        'cls': cls_,
                        'conf': conf_,
                        'image': image
                    })

    df = pd.DataFrame(outputs)

    if not context.app_cfg.save_images:
        df.drop(columns=['image'], inplace=True)

    return df
