# src/main.py

import sys
from src.exception.exception import WordSearchException
from src.logging import logger
from src.components.data_transformation import DataTransformation
from src.components.data_detection import DataDetection

if __name__ == "__main__":
    try:
        logger.logger.info("=== Data Pipeline Started ===")

        # ---------------- Data Transformation ----------------
        transformer = DataTransformation()
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
        logger.logger.info(f"Detection Results File: {detection_artifact.detection_result_file_path}")

        print("\n--- Pipeline Completed ---")
        print(f"Extracted Images Folder: {transformation_artifact.image_file_path}")
        print(f"Converted Documents Folder: {transformation_artifact.converted_document_file_path}")
        print(f"Detection Results File: {detection_artifact.detection_result_file_path}")

        logger.logger.info("=== Data Pipeline Completed ===")

    except Exception as e:
        raise WordSearchException(str(e), sys)


#  python -m src.main  command to run
