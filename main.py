import os
import argparse
from datetime import timedelta

import cv2




class FramePicker():
    def __init__(self,video_path):
        os.path.isfile(video_path)
        self.video_path=video_path
        cap = cv2.VideoCapture(video_path)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"initialized with {video_path} ({self.fps}fps)")

    def _save_frame(self, frame_tuple):
        result_path = os.path.basename(self.video_path).split(".")[0] + f'_{frame_tuple[1]}.png'

        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            return

        # os.makedirs(os.path.dirname(result_path), exist_ok=True)

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_tuple[0])

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(result_path, frame)
            print(f'saved {frame_tuple[1]}')

    def _parse_to_frame(self,input_str:str):
        input_list = list(map(int,input_str.split(":")))
        if len(input_list) == 3:
            dt = timedelta(hours=input_list[0],minutes=input_list[1],seconds=input_list[2])
            return (dt.seconds*self.fps, dt.seconds)
        if len(input_list) == 2:
            dt = timedelta(minutes=input_list[0],seconds=input_list[1])
            return (dt.seconds*self.fps, dt.seconds)
        if len(input_list) == 1:
            dt = timedelta(seconds=input_list[0])
            return (dt.seconds*self.fps, dt.seconds)

    def save_frames(self,input_strs):
        for input_str in input_strs:
            self._save_frame(self._parse_to_frame(input_str))

parser = argparse.ArgumentParser()
parser.add_argument('input',help='input_video_path')
parser.add_argument('--times', nargs='*')

args = parser.parse_args()

print(args.input)
print(args.times)
picker = FramePicker(args.input)
picker.save_frames(args.times)
# print(parse_to_frame('01:02:30'))
# save_frame('data/temp/sample_video.mp4', 100, 'data/temp/result_single/sample_100.jpg')
