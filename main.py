from face_recognizer import FaceRecognizer

def main():
    recognizer = FaceRecognizer(images_folder_path= "./images",is_headless= False)
    recognizer.run()


if __name__ == "__main__":
    main()