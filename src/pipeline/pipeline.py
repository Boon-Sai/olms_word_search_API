import sys
from src.exception.exception import WordSearchException
from src.logging import logger
from src.components.data_transformation import DataTransformation
from src.components.data_detection import DataDetection


class TrainPipeline:
    def __init__(self):
        self.data_transformation = DataTransformation()
        self.data_detection = DataDetection()

    def run_pipeline(self, data_path):
        try:
            logger.logger.info("=== Data Pipeline Started ===")

            # ---------------- Data Transformation ----------------
            transformer = DataTransformation(data_folder_path=data_path)
            transformation_artifact = transformer.initiate_data_transformation()

            logger.logger.info("Data Transformation Completed")
            logger.logger.info(f"Extracted Images Folder: {transformation_artifact.image_file_path}")
            logger.logger.info(f"Converted Documents Folder: {transformation_artifact.converted_document_file_path}")

            # ---------------- Data Detection ----------------
            detector = DataDetection(
                image_folder_path=transformation_artifact.image_file_path
            )
            detection_artifact = detector.initiate_data_detection()

            logger.logger.info("Data Detection Completed")
            logger.logger.info(f"Detection Results File: {detection_artifact.output_json_file_path}")

            logger.logger.info("=== Data Pipeline Completed ===")

            return transformation_artifact, detection_artifact

        except Exception as e:
            raise WordSearchException(str(e), sys)
