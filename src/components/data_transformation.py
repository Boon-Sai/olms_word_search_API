from src.exception.exception import WordSearchException
from src.logging.logger import logging

from src.entity.config_entity import DataTransformationConfig, ConfigEntity
from src.entity.artifact_entity import DataTransformationArtifact

import os
import sys
import glob
import subprocess
from PIL import Image


class DataTransformation:
    def __init__(self):
        try:
            logging.info("data transformation initialized...")
            self.data_transformation_config = DataTransformationConfig(config=ConfigEntity())
        
        except Exception as e:
            logging.error("Failed to start data transformation.")
            raise WordSearchException(e, sys) from e
    
    def preprocess_docx(self):
        """Convert DOCX files to PDFs using LibreOffice."""
        """Convert image file to PDFs using PIL."""
        try:
            logging.info("PDF conversion started...")
            os.makedirs(self.data_transformation_config.data_transformation_folder_path, exist_os=True)
            pdf_paths = []

            # scan all supported files
            for ext in self.supported_extensions:
                files = glob.glob(os.path.join(self.input_folder_path, f"*.{ext}"))
                for file_path in files:
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    pdf_path = os.path.join(self.output_folder_path, f"{base_name}.pdf")

                    try:
                        if ext in self.supported_doc_extensions:
                            # Use LibreOffice for Office docs
                            subprocess.run(
                                ["soffice", "--headless", "--convert-to", "pdf", file_path, "--outdir", self.data_transformation_config.output_folder_path],
                                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                            )
                        elif ext in self.supported_img_extensions:
                            # Use Pillow for images
                            img = Image.open(file_path)
                            rgb_img = img.convert("RGB")
                            rgb_img.save(pdf_path)
                        elif ext == "pdf":
                            # Just copy existing PDF
                            import shutil
                            shutil.copy(file_path, pdf_path)
                        else:
                            logging.warning(f"Unsupported format skipped: {file_path}")
                            continue

                        pdf_paths.append(pdf_path)
                        logging.info(f"Converted {file_path} to {pdf_path}")

                    except subprocess.CalledProcessError as e:
                        logging.error(f"LibreOffice conversion failed for {file_path}: {e.stderr.decode()}")
                    except Exception as e:
                        logging.error(f"Error converting {file_path}: {str(e)}")

            return pdf_paths

        except Exception as e:
            logging.error("Error during PDF conversion.")
            raise WordSearchException(e, sys) from e



