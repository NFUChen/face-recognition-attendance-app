import glob
import os
from typing import List

import cv2
import numpy as np
import pandas as pd
import face_recognition

from .human_resource_system import HumanResourceSystem
from .video_capturer import VideoCapturer

UnknownName = "Unknown Name"


class FaceRecognizer:
    
    def __init__(self,
                 images_folder_path: str,
                 is_headless: bool = False,
                 human_resources_system: HumanResourceSystem = HumanResourceSystem()) -> None:
        '''Create a FaceRecognizer object

        Args:
            images_folder_path (str): folder that are treated as known people folder
            is_headless (bool, optional): controls whether FaceRecognizer will run in the backgound or not. Defaults to False.
            human_resources_system (HumanResourceSystem, optional): system passing in to track its employee attendance. Defaults is to initialize a new HumanResourceSystem object.
        '''
        self.human_resources_system = human_resources_system

        self.images_folder_path = images_folder_path
        self.is_headless = is_headless
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.4

        self._load_encoding_images()

    def _get_all_images_files_path(self) -> List[str]:
    
        images_path = glob.glob(
            os.path.join(self.images_folder_path, f"*.*")
        )

        print(f"{len(images_path)} encoding images found.")

        return images_path

    def _load_encoding_images(self) -> None:
        ENCODING_IMAGES_DIR  = f"{self.images_folder_path}/images_encoding"
        if not os.path.exists(ENCODING_IMAGES_DIR):
            print(f"{ENCODING_IMAGES_DIR} not found, making folder...")
            os.makedirs(ENCODING_IMAGES_DIR)

        all_images_file_path = self._get_all_images_files_path()

        for img_path in all_images_file_path:
            basename = os.path.basename(img_path)
            (filename, _ext) = os.path.splitext(basename)
            print(f"Loading {filename}...")
            array_file_path = f"{ENCODING_IMAGES_DIR}/{filename}.npy"
            # if there exist a cached numpy array file
            if os.path.exists(array_file_path):
                img_encoding = np.load(array_file_path)
            else:
                img = cv2.imread(img_path)
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # Get encoding
                img_encoding = face_recognition.face_encodings(rgb_img).pop()
                np.save(array_file_path, img_encoding)

            print(f"Adding {filename} to system...")
            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
            self.human_resources_system.add_employee(filename)
        print("Encoding images loaded")

    def _detect_known_faces(self, frame: np.ndarray) -> np.ndarray:
        small_frame = cv2.resize(
            frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding)

            # known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            name = (
                self.known_face_names[best_match_index] 
                if (matches[best_match_index]) and (face_distances[best_match_index] < 0.4) 
                else UnknownName
            )

            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = (np.array(face_locations) /
                          self.frame_resizing).astype(int)

        red_color_code = (0, 0, 255)
        green_color_code = (0, 255, 0)

        if len(face_locations) == 0 or len(face_names) == 0:
            return frame

        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc
            if not self.human_resources_system.is_valid_employee(name):
                cv2.putText(frame, f"{UnknownName}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_DUPLEX, 1, red_color_code, 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), red_color_code, 8)
                continue

            cv2.putText(frame, f"Time Recorded: {name}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_DUPLEX, 1, green_color_code, 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), green_color_code, 8)

            self.human_resources_system.record_time_for_employee(name)

        return frame

    def run(self) -> pd.core.frame.DataFrame:
        '''Intialize a VideoCapturer and start to capture camera video stream 
        (i.e., using .capture_video method and passing self._detect_known_faces as callback).
        For breaking the stream, pressing "q" as exit key

        Returns:
            pd.core.frame.DataFrame: DataFrame containing timestamp collected by HumanResourceSystem
        '''
        cap = VideoCapturer()
        cap.capture_video(self._detect_known_faces, self.is_headless)
        self.human_resources_system.output_csv_file()

        return self.human_resources_system.output_current_seession_punchcard_info()
