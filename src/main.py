# src/main.py
import sys
from src.exception.exception import WordSearchException
from src.logging import logger
from src.components.data_transformation import DataTransformation

if __name__ == "__main__":
    try:
        logger.logger.info("=== Data Transformation Pipeline Started ===")
        
        transformer = DataTransformation()
        artifact = transformer.initiate_data_transformation()

        logger.logger.info("=== Data Transformation Pipeline Completed ===")
        logger.logger.info(f"Extracted Images Folder: {artifact.image_file_path}")
        logger.logger.info(f"Converted Documents Folder: {artifact.converted_document_file_path}")

        print("\n--- Data Transformation Completed ---")
        print(f"Extracted Images Folder: {artifact.image_file_path}")
        print(f"Converted Documents Folder: {artifact.converted_document_file_path}")

    except Exception as e:
        raise WordSearchException(str(e), sys)
