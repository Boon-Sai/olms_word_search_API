# src/pipeline/pipeline.py

import sys
from src.exception.exception import WordSearchException
from src.logging import logger
from src.components.data_transformation import DataTransformation
from src.components.data_detection import DataDetection

def run_pipeline(input_folder: str = None):
    """
    Runs the full data pipeline:
    1. Data Transformation (convert documents/images to PDFs & extract images)
    2. Data Detection (run OCR/detection on extracted images)

    Args:
        input_folder (str): Path to input data folder. If None, uses default from config.
    """
    try:
        logger.logger.info("=== Data Pipeline Started ===")

        # ---------------- Data Transformation ----------------
        transformer = DataTransformation(input_folder=input_folder)
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

        return {
            "extracted_images_folder": transformation_artifact.image_file_path,
            "converted_documents_folder": transformation_artifact.converted_document_file_path,
            "detection_results_file": detection_artifact.output_json_file_path
        }

    except Exception as e:
        raise WordSearchException(str(e), sys)
