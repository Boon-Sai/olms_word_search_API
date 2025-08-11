from src.exception.exception import WordSearchException
from src.logging.logger import logging

from src.constants import *

from datetime import datetime

class ConfigEntity:
    def __init__(self, timestamp = datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y__%H_%M_%S")

        self.data_detection_model = DETECTION_MODEL
        self.data_recognition_model = RECOGNITION_MODEL
        self.pretrained = PRETRAINED
        self.assume_straight_text = ASSUME_STRAIGHT_TEXT
        self.export_as_straingt_boxes = EXPORT_AS_STRAIGHT_BOXES

        self.supported_doc_extenctions = SUPPORTED_DOC_EXTENSIONS
        self.supported_img_extenctions = SUPPORTED_IMG_EXTENSIONS

        self.data_folder_path = DATA_FOLDER_PATH
        self.artifact_folder_path = ARTIFACTS_FOLDER_PATH


class DataTransformationConfig:
    def __init__(self, config: ConfigEntity):
        self.data_folder_path = config.data_folder_path
        self.artifact_folder_path = config.artifact_folder_path
        self.data_transformation_folder_path = os.path.join(self.artifact_folder_path, "data_transformation", exist_ok=True)
        self.data_transformation_images_path = os.path.join(self.artifact_folder_path, "extracted_images", exist_ok=True)
        self.supported_doc_extenctions = config.supported_doc_extenctions
        self.supported_img_extenctions = config.supported_img_extenctions
    

class DataDetectionConfig:
    def __init__(self, config: ConfigEntity):
        self.data_detection_model = config.data_detection_model
        self.data_recognition_model = config.data_recognition_model
        self.pretrained = config.pretrained
        self.assume_straight_text = config.assume_straight_text
        self.export_as_straingt_boxes = config.export_as_straingt_boxes

        self.artifact_folder_path = config.artifact_folder_path
        self.annotated_images_path = os.path.join(self.artifact_folder_path, "annotated_images", exist_ok = True)
        self.output_json_path = os.path.join(self.artifact_folder_path, "final_output.json", exist_ok = True)
