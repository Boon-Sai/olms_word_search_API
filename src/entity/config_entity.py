import os
from datetime import datetime
from src.constants import *

class ConfigEntity:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y__%H_%M_%S")

        # OCR settings
        self.data_detection_model = DETECTION_MODEL
        self.data_recognition_model = RECOGNITION_MODEL
        self.pretrained = PRETRAINED
        self.assume_straight_text = ASSUME_STRAIGHT_TEXT
        self.export_as_straingt_boxes = EXPORT_AS_STRAIGHT_BOXES

        # Supported file extensions
        self.supported_doc_extenctions = SUPPORTED_DOC_EXTENSIONS
        self.supported_img_extenctions = SUPPORTED_IMG_EXTENSIONS

        # Base folders
        self.data_folder_path = DATA_FOLDER_PATH
        self.artifact_folder_path = ARTIFACTS_FOLDER_PATH


class DataTransformationConfig:
    def __init__(self, config: ConfigEntity):
        # Base folders
        self.data_folder_path = config.data_folder_path
        self.artifact_folder_path = config.artifact_folder_path

        # Data transformation main folder
        self.data_transformation_folder_path = os.path.join(
            self.artifact_folder_path, "data_transformation"
        )
        os.makedirs(self.data_transformation_folder_path, exist_ok=True)

        # Subfolders for outputs
        self.documents_folder = os.path.join(
            self.data_transformation_folder_path, "documents"
        )
        os.makedirs(self.documents_folder, exist_ok=True)

        self.images_folder = os.path.join(
            self.data_transformation_folder_path, "images"
        )
        os.makedirs(self.images_folder, exist_ok=True)

        # Supported extensions
        self.supported_doc_extenctions = config.supported_doc_extenctions
        self.supported_img_extenctions = config.supported_img_extenctions
