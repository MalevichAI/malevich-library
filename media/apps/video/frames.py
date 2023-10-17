import os

import cv2
import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class Videos(BaseModel):
    video: str


@processor()
def split_on_frames(videos: DF['Videos'], context: Context):
    """Splits videos on frames

    Input:
        An arbitrary dataframe with the following columns:
            - videos: the path to the input video in the shared storage

    Output:
        The same dataframe with the following columns:
            - videos: the path to the output video in the shared storage
            - frames: the path to the output frames in the shared storage

    Details:
        The video is split into frames using OpenCV. By default, produced frames
        are saved as PNG images in the folder with the same name as
        the video file with `.d `extension.

        For example, the frames of the video /videos/video.mp4 will be
        saved in the folder /videos/video.mp4.d

        All the columns of the input dataframe are copied to the output dataframe.
        The value in the that columns are copied as is and duplicated for each
        frame of the video.

    Configuration:
        - fps (int or float) [optional, default is 1]:
            Frames per second. If float is used then it is
            used as a percentage of the original fps.

    Args:
        videos: a DataFrame with the following columns:
            - videos: the path to the input video

    Returns:
        a DataFrame with the following columns:
            - videos: the path to the output video
            - frames: the path to the output frames
            - *: the same columns as in the input dataframe
    """
    # Convert the 'video' column of the input dataframe to a list
    try:
        video_list = videos.video.tolist()
    except AttributeError:
        return AttributeError('Input dataframe should have a column "video"')

    # Get the value of 'fps' from the application configuration dictionary
    config_fps = context.app_cfg.get('fps', 1)

    # Check if the value of 'fps' is either an integer or a float
    if not isinstance(config_fps, (int, float)):
        raise TypeError(f'fps should be int or float, but got {type(config_fps)}')

    # Initialize an empty list called 'outputs'
    outputs = []

    # Iterate over the 'videos' list
    for i, video in enumerate(video_list):
        # Get the real path of the video using the 'get_share_path'
        # method of the 'context' object
        real_path = context.get_share_path(video)
        # Create a 'cv2.VideoCapture' object for the video
        cap = cv2.VideoCapture(real_path)

        # Check if the value of 'fps' is a float
        if isinstance(config_fps, float):
            # Calculate the new fps value by multiplying the original fps value of the
            # video with the value of 'fps'
            fps = cap.get(cv2.CAP_PROP_FPS) * config_fps
        else:
            # Set the fps value to the value of 'fps'
            fps = cap.get(cv2.CAP_PROP_FPS)

        # Create a directory with the name of the video in the 'APP_DIR' directory
        frames_path = os.path.join(APP_DIR, video + '.d')
        os.makedirs(frames_path, exist_ok=True)

        j = 0
        # Read each frame of the video
        while cap.isOpened():
            # Get the current frame ID
            frame_id = cap.get(cv2.CAP_PROP_POS_FRAMES)
            # Read the next frame
            ret, frame = cap.read()
            # If there are no more frames, break out of the loop
            if not ret:
                break
            # Check if the current frame should be saved based on the fps value
            if frame_id % (fps // config_fps) == 0:
                # Save the frame as a PNG image in the directory created earlier
                frame_name = f'{int(j)}.png'
                frame_path = os.path.join(frames_path, frame_name)
                shared_path = os.path.join(video + '.d', frame_name)
                cv2.imwrite(frame_path, frame)

                # Share the path of the saved frame using the 'share' method of the
                # 'context' object
                context.share(shared_path)

                # Append a tuple containing the index of the video and the path of the
                # saved frame to the 'outputs' list
                outputs.append(
                    (i, shared_path)
                )

                j += 1
        # Release the 'cv2.VideoCapture' object
        cap.release()

    # Create a new dataframe called 'output_df' with columns 'video', 'frame',
    # and any other columns present in the 'videos' dataframe
    output_df = pd.DataFrame(columns=[*videos.columns, 'frame'])

    # Iterate over the 'outputs' list and create a new row in the 'output_df'
    # dataframe for each tuple in the list
    for i, frame in outputs:
        output_df = pd.concat([
            output_df,
            pd.Series(data={
                **videos.iloc[i].to_dict(),
                'frame': frame
            }).to_frame().T
        ], ignore_index=True)

    # Return the 'output_df' dataframe
    return output_df.reset_index()
