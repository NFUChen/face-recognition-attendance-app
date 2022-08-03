from typing import Callable

import cv2

from webcam_video_stream import WebcamVideoStream


class VideoCapturer:
    def __init__(self, exit_key: str = "q", title: str = "Camera"):
        self.exit_key = exit_key
        self.title = title
        self.capture = None

    def capture_video(self, frame_callback: Callable = None, is_headless: bool = False) -> None:
        self.capture = cv2.VideoCapture(0)
        while True:
            # It contains a boolean indicating if it was sucessful (ret)
            # It also contains the images collected from the webcam (frame)
            ret, frame = self.capture.read()

            if frame_callback:
                frame = frame_callback(frame)

            if not is_headless:
                cv2.imshow(self.title, frame)

            if cv2.waitKey(1) == ord(self.exit_key):  # 13 is the Enter Key
                break
        # Release camera and close windows
        self.capture.release()
        cv2.destroyAllWindows()

    def capture_video_with_threading(self, frame_callback: Callable = None, is_headless: bool = False) -> None:
        stream = WebcamVideoStream().start()

        while True:
            # It contains a boolean indicating if it was sucessful (ret)
            # It also contains the images collected from the webcam (frame)
            frame = stream.read()

            if frame_callback:
                frame = frame_callback(frame)
            if not is_headless:
                cv2.imshow(self.title, frame)

            if cv2.waitKey(1) == ord(self.exit_key):
                break
        # Release camera and close windows
        stream.stop()
        cv2.destroyAllWindows()
