import sys
from typing import List
import numpy as np
import face_recognition
import cv2
import glob
import os

from video_capturer import VideoCapturer
from human_resource_system import HumanResourceSystem
from timer import Timer

UnknownName = "Unknown Name"

class FaceRecognizer:
    def __init__(self, images_folder_path:str, is_headless:bool = False) -> None:
        self.human_resources_system = HumanResourceSystem(images_folder_path)

        self.images_folder_path = images_folder_path
        self.is_headless = is_headless
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25
        
        self._load_encoding_images()
        
    def _get_all_images_files_path(self) -> List[str]:
        images_extensions = ["jpg","jpeg", "png", "webp"]
        images_path = []
        for extension in images_extensions:
            current_image_files = glob.glob(
                os.path.join(self.images_folder_path, f"*.{extension}")
            )
            images_path.extend(current_image_files)

        print(f"{len(images_path)} encoding images found.")
        
        return images_path

    
    

    def _load_encoding_images(self) -> None:
        
        all_images_file_path = self._get_all_images_files_path()
        
        for img_path in all_images_file_path:
            basename = os.path.basename(img_path)
            (filename, _ext) = os.path.splitext(basename)
            print(f"Loading {filename}...")
            array_file_path = f'./images_encoding/{filename}.npy'
            #如有現有的array文件可以用
            if os.path.exists(array_file_path):
                img_encoding = np.load(array_file_path)
                self.known_face_encodings.append(img_encoding)
                self.known_face_names.append(filename)
                print(f"Adding {filename} to system...")
                self.human_resources_system.add_employee(filename)
                continue

            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img).pop()
            np.save(f'./images_encoding/{filename}', img_encoding)

            
            print(f"Adding {filename} to system...")
            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
            self.human_resources_system.add_employee(filename)
        print("Encoding images loaded")
        
    def _detect_known_faces(self, frame:np.ndarray) -> np.ndarray:
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)


            # known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
    
            name = self.known_face_names[best_match_index] if matches[best_match_index] else UnknownName
            
        
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = (np.array(face_locations) / self.frame_resizing).astype(int)
        red_color_code = (0, 0, 255)
        green_color_code = (0,255, 0)

        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc
            if not self.human_resources_system.is_valid_employee(name):
                cv2.putText(frame, f"{UnknownName}", (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, red_color_code, 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), red_color_code, 8)
                continue

            cv2.putText(frame, f"Time Recorded: {Timer.get_current_time()}", (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, green_color_code, 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), green_color_code, 8)

            self.human_resources_system.record_time_for_employee(name)
        
        
        
        return frame
    
    def run(self):
        cap = VideoCapturer()
        cap.capture_video_with_threading(self._detect_known_faces, self.is_headless)