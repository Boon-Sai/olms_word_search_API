import sys
from src.exception.exception import WordSearchException
from src.logging import logger
from src.components.data_transformation import DataTransformation
from src.components.data_detection import DataDetection

class WordSearchPipeline:
    def __init__(self):
        logger.logger.info("Initializing Word Search Pipeline...")

    def run_pipeline(self):
        """
        Run the full Word Search pipeline:
        1. Data Transformation (convert docs/images to PDF & extract images)
        2. Data Detection (OCR and annotation)
        """
        try:
            logger.logger.info("=== Pipeline Started ===")

            # -------- Step 1: Data Transformation --------
            transformer = DataTransformation()
            transformation_artifact = transformer.initiate_data_transformation()
            logger.logger.info("Data Transformation Completed")
            logger.logger.info(f"Extracted Images Folder: {transformation_artifact.image_file_path}")
            logger.logger.info(f"Converted Documents Folder: {transformation_artifact.converted_document_file_path}")

            # -------- Step 2: Data Detection --------
            detector = DataDetection(
                image_folder_path=transformation_artifact.image_file_path
            )
            detection_artifact = detector.run_detection()
            logger.logger.info("Data Detection Completed")
            logger.logger.info(f"Annotated Images Folder: {detection_artifact.annotated_image_file_path}")
            logger.logger.info(f"Detection Results File: {detection_artifact.output_json_file_path}")

            logger.logger.info("=== Pipeline Completed Successfully ===")

            # Return artifacts for further use if needed
            return {
                "images_folder": transformation_artifact.image_file_path,
                "converted_docs_folder": transformation_artifact.converted_document_file_path,
                "annotated_images_folder": detection_artifact.annotated_image_file_path,
                "detection_results_file": detection_artifact.output_json_file_path
            }

        except Exception as e:
            raise WordSearchException(str(e), sys) from e
